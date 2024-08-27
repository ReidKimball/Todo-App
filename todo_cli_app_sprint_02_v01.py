"""
The `TodoItem` class represents a to-do item with a title, description, category, and completion status.

The `create_connection()` function creates a connection to a SQLite database named "todo.db".

The `create_table(conn)` function creates a table named "todo_items" in the database if it doesn't already exist. The table has columns for the title, description, category, and completion status of each to-do item.

The `add_todo_item(conn, title, description, category)` function adds a new to-do item to the database. If the title is empty, it prints an error message.

The `get_user_input()` function prompts the user to enter the title, description, and category of a new to-do item.

The `add_todo_item_from_user_input(conn)` function calls `get_user_input()` and then adds the new to-do item to the database using `add_todo_item()`.

The `view_todo_items(conn)` function provides a menu-driven interface for viewing and managing to-do items, including options to view all items, view uncategorized items, view items by category, and remove items.

The `view_all_todo_items(conn)`, `view_uncategorized_todo_items(conn)`, and `view_todo_items_by_category(conn)` functions retrieve and display to-do items from the database based on the selected options.

The `remove_todo_item(conn)` function prompts the user to enter the title of a to-do item to remove, and then deletes the item from the database if it exists.

The `main()` function creates a database connection, creates the "todo_items" table if it doesn't exist, and then enters a loop that allows the user to add new to-do items, view and manage existing to-do items, or quit the application.
"""

import sqlite3


class TodoItem:
    def __init__(self, title, description, category, completed=False):
        self.title = title
        self.description = description
        self.category = category
        self.completed = completed


def create_connection():
    conn = sqlite3.connect("todo.db")
    return conn


def create_table(conn):
    c = conn.cursor()
    c.execute(
        """CREATE TABLE IF NOT EXISTS todo_items
                 (title TEXT NOT NULL,
                  description TEXT,
                  category TEXT,
                  completed INTEGER)"""
    )
    conn.commit()


def add_todo_item(conn, title, description, category):
    if title:
        c = conn.cursor()
        c.execute(
            "INSERT INTO todo_items (title, description, category, completed) VALUES (?, ?, ?, ?)",
            (title, description, category, 0),
        )
        conn.commit()
        print("To-do item added successfully.")
    else:
        print("Title cannot be empty.")


def get_user_input():
    title = input("Enter the title: ")
    description = input("Enter the description: ")
    category = input(
        "Enter the category (urgent, schedule, delegate, automate, eliminate, uncategorized): "
    )
    return title, description, category


def add_todo_item_from_user_input(conn):
    title, description, category = get_user_input()
    add_todo_item(conn, title, description, category)


def view_todo_items(conn):
    while True:
        print("\n1. View all to-do items")
        print("2. View uncategorized to-do items")
        print("3. View to-do items by category")
        print("4. Remove a to-do item")
        print("5. Back to main menu")
        choice = input("Enter your choice: ")

        if choice == "1":
            view_all_todo_items(conn)
        elif choice == "2":
            view_uncategorized_todo_items(conn)
        elif choice == "3":
            view_todo_items_by_category(conn)
        elif choice == "4":
            remove_todo_item(conn)
        elif choice == "5":
            break
        else:
            print("Invalid choice. Please try again.")


def view_all_todo_items(conn):
    c = conn.cursor()
    c.execute("SELECT * FROM todo_items")
    todo_items = c.fetchall()

    if todo_items:
        print("\nAll to-do items:")
        for i, item in enumerate(todo_items):
            print(f"{i+1}. {item[0]} - {item[1]} ({item[2]})")
    else:
        print("No to-do items found.")


def view_uncategorized_todo_items(conn):
    c = conn.cursor()
    c.execute("SELECT * FROM todo_items WHERE category = 'uncategorized'")
    todo_items = c.fetchall()

    if todo_items:
        print("\nUncategorized to-do items:")
        for i, item in enumerate(todo_items):
            print(f"{i+1}. {item[0]} - {item[1]}")
    else:
        print("No uncategorized to-do items found.")


def view_todo_items_by_category(conn):
    category = input(
        "Enter the category (urgent, schedule, delegate, automate, eliminate): "
    )
    c = conn.cursor()
    c.execute("SELECT * FROM todo_items WHERE category = ?", (category,))
    todo_items = c.fetchall()

    if todo_items:
        print(f"\nTo-do items in category '{category}':")
        for i, item in enumerate(todo_items):
            print(f"{i+1}. {item[0]} - {item[1]}")
    else:
        print(f"No to-do items found in category '{category}'.")


def remove_todo_item(conn):
    title = input("Enter the title of the to-do item to remove: ")
    c = conn.cursor()
    c.execute("SELECT * FROM todo_items WHERE title = ?", (title,))
    todo_item = c.fetchone()

    if todo_item:
        confirm = input(
            f"Are you sure you want to remove the to-do item '{title}'? (y/n): "
        )
        if confirm.lower() == "y":
            c.execute("DELETE FROM todo_items WHERE title = ?", (title,))
            conn.commit()
            print("To-do item removed successfully.")
    else:
        print(f"No to-do item found with title '{title}'.")


def main():
    conn = create_connection()
    create_table(conn)

    while True:
        print("\n1. Add To-Do Item")
        print("2. View To-Do Items")
        print("3. Quit")
        choice = input("Enter your choice: ")

        if choice == "1":
            add_todo_item_from_user_input(conn)
        elif choice == "2":
            view_todo_items(conn)
        elif choice == "3":
            conn.close()
            break
        else:
            print("Invalid choice. Please try again.")


if __name__ == "__main__":
    main()
