import json
import os

DATA_FILE = "data.json"

def load_data():
    if not os.path.exists(DATA_FILE):
        return []
    with open(DATA_FILE, "r") as f:
        try:
            return json.load(f)
        except json.JSONDecodeError:
            return []

def save_data(data):
    with open(DATA_FILE, "w") as f:
        json.dump(data, f, indent=4)

def add_entry(entry):
    data = load_data()
    data.append(entry)
    save_data(data)

def delete_entry(index):
    data = load_data()
    if 0 <= index < len(data):
        data.pop(index)
        save_data(data)
        return True
    return False

def update_entry(index, new_entry):
    data = load_data()
    if 0 <= index < len(data):
        data[index] = new_entry
        save_data(data)
        return True
    return False
