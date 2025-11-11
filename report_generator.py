from data_manager import load_data
from prettytable import PrettyTable
from collections import defaultdict

def view_all_entries():
    data = load_data()
    if not data:
        print("No records found.")
        return
    table = PrettyTable(["#", "Task", "Category", "Start", "End", "Duration (min)"])
    for i, d in enumerate(data):
        table.add_row([i, d["task"], d["category"], d.get("start", ""), d.get("end", ""), d.get("duration_mins", "")])
    print(table)

def category_summary():
    data = load_data()
    if not data:
        print("No records found.")
        return
    summary = defaultdict(float)
    for d in data:
        summary[d["category"]] += d.get("duration_mins", 0)
    print("\nCategory Summary (Total Time in Minutes):")
    for cat, total in summary.items():
        print(f"  • {cat}: {total} mins")
