from time_tracker import start_timer, stop_timer
from report_generator import view_all_entries, category_summary
from data_manager import delete_entry
from utils import menu

def main():
    while True:
        choice = menu()
        if choice == "1":
            task = input("Enter task name: ")
            category = input("Enter category: ")
            start_timer(task, category)
        elif choice == "2":
            stop_timer()
        elif choice == "3":
            view_all_entries()
        elif choice == "4":
            category_summary()
        elif choice == "5":
            idx = int(input("Enter entry number to delete: "))
            if delete_entry(idx):
                print("✅ Entry deleted.")
            else:
                print("⚠️ Invalid entry number.")
        elif choice == "6":
            print("👋 Exiting TimeLoom. Have a productive day!")
            break
        else:
            print("Invalid option. Try again.")

if __name__ == "__main__":
    main()
