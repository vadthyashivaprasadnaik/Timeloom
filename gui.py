import tkinter as tk
from tkinter import ttk, messagebox, simpledialog
from time_tracker import start_timer, stop_timer
from data_manager import delete_entry, load_data
from datetime import datetime
import matplotlib.pyplot as plt
import pandas as pd
import csv
import os
import threading
import time

class TimeLoomApp:
    def __init__(self, root):
        self.root = root
        self.root.title("TimeLoom – Productivity Visualizer")
        self.root.geometry("850x650")

        self.theme = "light"
        self.colors = {
            "light": {"bg": "#F7F9FC", "fg": "#000000", "accent": "#3A6EA5", "textbox": "#FFFFFF"},
            "dark": {"bg": "#1E1E1E", "fg": "#FFFFFF", "accent": "#4EA8DE", "textbox": "#2C2C2C"},
        }

        self.timer_running = False
        self.timer_start_time = None
        self.timer_thread = None

        self.apply_theme()

        
        self.header = tk.Label(
            root, text="⏰ TimeLoom – Productivity Visualizer",
            font=("Arial", 18, "bold"), bg=self.colors[self.theme]["bg"], fg=self.colors[self.theme]["accent"]
        )
        self.header.pack(pady=10)

        
        frame = tk.Frame(root, bg=self.colors[self.theme]["bg"])
        frame.pack(pady=10)

        tk.Label(frame, text="Task Name:", bg=self.colors[self.theme]["bg"], fg=self.colors[self.theme]["fg"]).grid(row=0, column=0, padx=5, pady=5)
        self.task_entry = tk.Entry(frame, width=30, bg=self.colors[self.theme]["textbox"], fg=self.colors[self.theme]["fg"])
        self.task_entry.grid(row=0, column=1, padx=5, pady=5)

        tk.Label(frame, text="Category:", bg=self.colors[self.theme]["bg"], fg=self.colors[self.theme]["fg"]).grid(row=1, column=0, padx=5, pady=5)
        self.category_entry = tk.Entry(frame, width=30, bg=self.colors[self.theme]["textbox"], fg=self.colors[self.theme]["fg"])
        self.category_entry.grid(row=1, column=1, padx=5, pady=5)

        
        self.timer_label = tk.Label(root, text="Timer: 00:00:00", font=("Consolas", 14, "bold"),
                                    bg=self.colors[self.theme]["bg"], fg=self.colors[self.theme]["accent"])
        self.timer_label.pack(pady=5)

        
        btn_frame = tk.Frame(root, bg=self.colors[self.theme]["bg"])
        btn_frame.pack(pady=10)

        ttk.Button(btn_frame, text="Start Timer", command=self.start_timer_ui).grid(row=0, column=0, padx=10)
        ttk.Button(btn_frame, text="Stop Timer", command=self.stop_timer_ui).grid(row=0, column=1, padx=10)
        ttk.Button(btn_frame, text="View Entries", command=self.view_entries_ui).grid(row=0, column=2, padx=10)
        ttk.Button(btn_frame, text="Category Summary", command=self.summary_ui).grid(row=0, column=3, padx=10)
        ttk.Button(btn_frame, text="View Weekly Chart", command=self.show_chart_ui).grid(row=0, column=4, padx=10)
        ttk.Button(btn_frame, text="Weekly Heatmap", command=self.show_heatmap_ui).grid(row=0, column=5, padx=10)
        ttk.Button(btn_frame, text="Delete Entry", command=self.delete_entry_ui).grid(row=0, column=6, padx=10)

        ttk.Button(btn_frame, text="🌗 Toggle Dark/Light", command=self.toggle_theme).grid(row=1, column=2, padx=10, pady=10)
        ttk.Button(btn_frame, text="💾 Export Data (CSV)", command=self.export_csv).grid(row=1, column=3, padx=10, pady=10)

        
        self.text_area = tk.Text(root, height=15, width=100,
                                 bg=self.colors[self.theme]["textbox"], fg=self.colors[self.theme]["fg"])
        self.text_area.pack(pady=10)
        self.text_area.insert(tk.END, "Welcome to TimeLoom! 👋\nUse the buttons above to get started.\n")

    
    def start_timer_ui(self):
        task = self.task_entry.get().strip()
        cat = self.category_entry.get().strip()
        if not task or not cat:
            messagebox.showwarning("Input Error", "Please enter both task and category.")
            return
        start_timer(task, cat)
        self.timer_running = True
        self.timer_start_time = time.time()
        threading.Thread(target=self.update_timer_display, daemon=True).start()
        self.text_area.insert(tk.END, f"⏱ Timer started for task '{task}' ({cat}) at {datetime.now()}\n")

    def stop_timer_ui(self):
        if not self.timer_running:
            messagebox.showinfo("Info", "Timer not running.")
            return
        self.timer_running = False
        stop_timer()
        self.timer_label.config(text="Timer: 00:00:00")
        self.text_area.insert(tk.END, f"✅ Timer stopped and logged at {datetime.now()}\n")

    def update_timer_display(self):
        while self.timer_running:
            elapsed = time.time() - self.timer_start_time
            h, m, s = int(elapsed // 3600), int((elapsed % 3600) // 60), int(elapsed % 60)
            self.timer_label.config(text=f"Timer: {h:02d}:{m:02d}:{s:02d}")
            time.sleep(1)

    
    def view_entries_ui(self):
        data = load_data()
        self.text_area.delete(1.0, tk.END)
        if not data:
            self.text_area.insert(tk.END, "No records found.\n")
            return
        self.text_area.insert(tk.END, "📋 All Logged Entries:\n\n")
        for i, d in enumerate(data):
            self.text_area.insert(tk.END, f"{i}. {d.get('task','')} ({d.get('category','')}) - {round(d.get('duration_mins', 0), 2)} mins\n")

    def summary_ui(self):
        data = load_data()
        if not data:
            messagebox.showinfo("Summary", "No records to summarize.")
            return
        cat_time = {}
        for d in data:
            cat_time[d["category"]] = cat_time.get(d["category"], 0) + d.get("duration_mins", 0)
        msg = "\n".join([f"{k}: {round(v,2)} mins" for k, v in cat_time.items()])
        messagebox.showinfo("Category Summary", msg)

    
    def delete_entry_ui(self):
        idx = simpledialog.askinteger("Delete Entry", "Enter entry number to delete:")
        if idx is None:
            return
        if idx < 0:
            messagebox.showerror("Error", "Please enter a non-negative integer.")
            return
        success = delete_entry(idx)
        if success:
            messagebox.showinfo("Deleted", "Entry deleted successfully!")
            self.view_entries_ui()
        else:
            messagebox.showerror("Error", "Invalid entry number.")

    
    def show_chart_ui(self):
        data = load_data()
        if not data:
            messagebox.showinfo("Chart", "No data available to display chart.")
            return

        cat_time = {}
        for d in data:
            cat_time[d["category"]] = cat_time.get(d["category"], 0) + d.get("duration_mins", 0)

        if not cat_time:
            messagebox.showinfo("Chart", "No valid duration data to plot.")
            return

        categories = list(cat_time.keys())
        durations = [round(v, 2) for v in cat_time.values()]

        plt.close('all')
        fig, ax = plt.subplots(figsize=(7, 4))
        ax.bar(categories, durations, color="#4EA8DE" if self.theme == "light" else "#FFDD57")
        ax.set_title("Weekly Productivity Summary", fontsize=13, fontweight='bold')
        ax.set_xlabel("Category")
        ax.set_ylabel("Total Time (Minutes)")
        ax.grid(axis="y", linestyle="--", alpha=0.7)
        plt.tight_layout()
        plt.show(block=False)

    def show_heatmap_ui(self):
        data = load_data()
        if not data:
            messagebox.showinfo("Heatmap", "No data to display heatmap.")
            return

        df = pd.DataFrame(data)
        if "start" not in df or df.empty:
            messagebox.showinfo("Heatmap", "No valid timestamps available.")
            return

        df["date"] = pd.to_datetime(df["start"]).dt.date
        df_grouped = df.groupby("date")["duration_mins"].sum().reset_index()

        
        all_days = pd.date_range(datetime.now().date() - pd.Timedelta(days=6), datetime.now().date())
        df_full = pd.DataFrame({"date": all_days})
        df_full["duration_mins"] = df_full["date"].map(
            df_grouped.set_index("date")["duration_mins"]
        ).fillna(0)

        plt.close("all")
        fig, ax = plt.subplots(figsize=(8, 2))
        ax.imshow([df_full["duration_mins"]], cmap="Blues" if self.theme == "light" else "plasma", aspect="auto")
        ax.set_xticks(range(7))
        ax.set_xticklabels([d.strftime("%a") for d in df_full["date"]])
        ax.set_yticks([])
        ax.set_title("Weekly Heatmap (Total Minutes per Day)")
        plt.tight_layout()
        plt.show(block=False)

    
    def toggle_theme(self):
        self.theme = "dark" if self.theme == "light" else "light"
        self.apply_theme()
        self.text_area.insert(tk.END, f"🌗 Switched to {self.theme.capitalize()} Mode.\n")

    def apply_theme(self):
        c = self.colors[self.theme]
        self.root.config(bg=c["bg"])
        if hasattr(self, "header"):
            self.header.config(bg=c["bg"], fg=c["accent"])
        if hasattr(self, "timer_label"):
            self.timer_label.config(bg=c["bg"], fg=c["accent"])
        for widget in self.root.winfo_children():
            if isinstance(widget, tk.Frame):
                widget.config(bg=c["bg"])
            elif isinstance(widget, tk.Text):
                widget.config(bg=c["textbox"], fg=c["fg"])

    def export_csv(self):
        data = load_data()
        if not data:
            messagebox.showinfo("Export", "No data to export.")
            return

        filename = "timeloom_export.csv"
        with open(filename, "w", newline="", encoding="utf-8") as f:
            writer = csv.writer(f)
            writer.writerow(["Task", "Category", "Start", "End", "Duration (mins)"])
            for d in data:
                writer.writerow([
                    d.get("task", ""),
                    d.get("category", ""),
                    d.get("start", ""),
                    d.get("end", ""),
                    round(d.get("duration_mins", 0), 2)
                ])
        messagebox.showinfo("Export Successful", f"Data exported to '{os.path.abspath(filename)}'")


if __name__ == "__main__":
    root = tk.Tk()
    app = TimeLoomApp(root)
    root.mainloop()
