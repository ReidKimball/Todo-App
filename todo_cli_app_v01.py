class TodoItem:
    def __init__(self, title, description):
        self.title = title
        self.description = description
        self.completed = False

todo_list = []

def add_todo_item(title, description):
    if title:
        new_item = TodoItem(title, description)
        todo_list.append(new_item)
        print("To-do item added successfully.")
    else:
        print("Title cannot be empty.")

def get_user_input():
    title = input("Enter the title: ")
    description = input("Enter the description: ")
    return title, description

def add_todo_item_from_user_input():
    title, description = get_user_input()
    add_todo_item(title, description)

def main():
    while True:
        print("\n1. Add To-Do Item")
        print("2. Quit")
        choice = input("Enter your choice: ")

        if choice == "1":
            add_todo_item_from_user_input()
        elif choice == "2":
            break
        else:
            print("Invalid choice. Please try again.")

if __name__ == "__main__":
    main()

