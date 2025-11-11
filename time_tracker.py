import time
from datetime import datetime
from data_manager import add_entry

start_time = None
current_task = None

def start_timer(task_name, category):
    global start_time, current_task
    start_time = time.time()
    current_task = {"task": task_name, "category": category, "start": datetime.now().strftime("%Y-%m-%d %H:%M:%S")}
    print(f"⏱ Timer started for task: {task_name}")

def stop_timer():
    global start_time, current_task
    if start_time is None:
        print("⚠️ Timer not started!")
        return
    end_time = time.time()
    duration = round((end_time - start_time) / 60, 2)  # minutes
    current_task["end"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    current_task["duration_mins"] = duration
    add_entry(current_task)
    print(f"✅ Task '{current_task['task']}' logged ({duration} mins).")
    start_time = None
    current_task = None
