from rich.live import Live
from rich.table import Table
import threading, time

class Dashboard:
    def __init__(self):
        self.services = {}  # service_name -> {status,url,uptime,expiration}
        self.lock = threading.Lock()

    def add_service(self, name, url, status="DEPLOYING", expiration="N/A"):
        with self.lock:
            self.services[name] = {"status": status, "url": url, "uptime": 0, "expiration": expiration}
            threading.Thread(target=self.track_uptime, args=(name,), daemon=True).start()

    def track_uptime(self, name):
        while True:
            with self.lock:
                self.services[name]["uptime"] += 1
            time.sleep(1)

    def update_service(self, name, uptime):
        with self.lock:
            if name in self.services:
                self.services[name]["uptime"] = uptime

    def show(self):
        with Live(refresh_per_second=1) as live:
            while True:
                table = Table(title="OmniCloudRun Pro Dashboard")
                table.add_column("Service Name")
                table.add_column("Status")
                table.add_column("URL")
                table.add_column("Uptime (s)")
                table.add_column("Expiration")
                with self.lock:
                    for s, data in self.services.items():
                        table.add_row(s, data["status"], data["url"], str(data["uptime"]), data["expiration"])
                live.update(table)
                time.sleep(1)