import sqlite3

class TodoItem:
    def __init__(self, title, description, category, completed=False):
        self.title = title
        self.description = description
        self.category = category
        self.completed = completed

def create_connection():
    conn = sqlite3.connect('todo.db')
    return conn

def create_table(conn):
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS todo_items
                 (title TEXT NOT NULL,
                  description TEXT,
                  category TEXT,
                  completed INTEGER)''')
    conn.commit()

def add_todo_item(conn, title, description, category):
    if title:
        c = conn.cursor()
        c.execute("INSERT INTO todo_items (title, description, category, completed) VALUES (?, ?, ?, ?)",
                  (title, description, category, 0))
        conn.commit()
        print("To-do item added successfully.")
    else:
        print("Title cannot be empty.")

def get_user_input():
    title = input("Enter the title: ")
    description = input("Enter the description: ")
    category = input("Enter the category (urgent, schedule, delegate, automate, eliminate, uncategorized): ")
    return title, description, category

def add_todo_item_from_user_input(conn):
    title, description, category = get_user_input()
    add_todo_item(conn, title, description, category)

def main():
    conn = create_connection()
    create_table(conn)

    while True:
        print("\n1. Add To-Do Item")
        print("2. Quit")
        choice = input("Enter your choice: ")

        if choice == "1":
            add_todo_item_from_user_input(conn)
        elif choice == "2":
            conn.close()
            break
        else:
            print("Invalid choice. Please try again.")

if __name__ == "__main__":
    main()
