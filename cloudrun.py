import subprocess, json, datetime
from assets.animations import spinner
from rich.console import Console

console = Console()

class CloudRun:
    def __init__(self):
        self.active_services = {}

    def deploy_service(self, service_name, source_type="github", repo=None, docker_image=None,
                       region="us-central1", cpu="1", memory="512Mi", concurrency=80):
        spinner("Deploying Cloud Run service...")
        cmd = ["gcloud", "run", "deploy", service_name, "--region", region, "--platform", "managed"]
        if source_type.lower() == "github":
            cmd += ["--source", repo]
        elif source_type.lower() == "docker":
            cmd += ["--image", docker_image]
        cmd += ["--cpu", cpu, "--memory", memory, "--concurrency", str(concurrency), "--quiet"]
        subprocess.run(cmd)
        console.print(f"[green]Service {service_name} deployed![/green]")

    def check_status(self, service_name, region="us-central1"):
        spinner(f"Checking status for {service_name}...")
        cmd = ["gcloud", "run", "services", "describe", service_name, "--region", region, "--format", "json"]
        result = subprocess.run(cmd, capture_output=True, text=True)
        if result.returncode != 0:
            console.print("[red]Service not found[/red]")
            return None
        info = json.loads(result.stdout)
        status = info.get("status", {}).get("conditions", [{}])[0].get("state", "UNKNOWN")
        url = info.get("status", {}).get("url", "N/A")
        creation_ts = info.get("metadata", {}).get("creationTimestamp")
        expiration = "N/A"
        if creation_ts:
            creation_time = datetime.datetime.fromisoformat(creation_ts.replace("Z", "+00:00"))
            expiration = creation_time + datetime.timedelta(days=90)
        console.print(f"[green]Status:[/green] {status}")
        console.print(f"[green]URL:[/green] {url}")
        console.print(f"[cyan]Expiration:[/cyan] {expiration}")
        return {"status": status, "url": url, "expiration": str(expiration)}