from rich.progress import Progress, SpinnerColumn, BarColumn, TextColumn
import time, threading

def spinner(text="Processing..."):
    from rich.console import Console
    console = Console()
    with Progress(SpinnerColumn(), TextColumn("[progress.description]{task.description}"), transient=True) as progress:
        task = progress.add_task(text, total=None)
        time.sleep(2)
        progress.remove_task(task)

def loading_bar(total=100, text="Loading..."):
    from rich.progress import Progress, BarColumn, SpinnerColumn, TextColumn
    import time
    with Progress(SpinnerColumn(), BarColumn(), TextColumn("[progress.description]{task.description}")) as progress:
        task = progress.add_task(text, total=total)
        for i in range(total):
            time.sleep(0.02)
            progress.update(task, advance=1)

def uptime_counter(service_name, stop_event, update_callback):
    import time
    start_time = time.time()
    while not stop_event.is_set():
        uptime = int(time.time() - start_time)
        update_callback(service_name, uptime)
        time.sleep(1)