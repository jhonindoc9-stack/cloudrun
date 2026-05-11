import json
from rich.console import Console
from assets.animations import spinner, loading_bar
from cloudrun import CloudRun
from dashboard import Dashboard

console = Console()

def load_config():
    with open("config/config.json") as f:
        return json.load(f)

def main_menu():
    console.clear()
    console.print(open("assets/banner.txt").read(), style="bold cyan")
    console.print("\n[1] Deploy Cloud Run\n[2] Check Status & Uptime\n[3] Open Dashboard\n[4] Quit\n", style="bold green")
    return console.input("Select an option: ")

def run():
    config = load_config()
    cr = CloudRun()
    dashboard = Dashboard()
    while True:
        choice = main_menu()
        if choice == "1":
            service_name = console.input("Service Name: ") or config["default_service_name"]
            source_type = console.input("Source Type (github/docker): ").lower()
            repo_or_image = console.input("GitHub Repo or Docker Image URL: ")
            cpu = console.input(f"CPU [{config['default_cpu']}]: ") or config["default_cpu"]
            memory = console.input(f"Memory [{config['default_memory']}]: ") or config["default_memory"]
            concurrency = console.input(f"Concurrency [{config['default_concurrency']}]: ") or config["default_concurrency"]

            cr.deploy_service(service_name, source_type, repo_or_image, repo_or_image,
                              cpu=cpu, memory=memory, concurrency=int(concurrency))
            
            status_info = cr.check_status(service_name)
            dashboard.add_service(service_name, status_info["url"], status=status_info["status"], expiration=status_info["expiration"])
        elif choice == "2":
            service_name = console.input("Service Name: ")
            cr.check_status(service_name)
            console.input("Press Enter to continue...")
        elif choice == "3":
            dashboard.show()
        elif choice == "4":
            console.print("Quitting...", style="bold red")
            break

if __name__ == "__main__":
    run()