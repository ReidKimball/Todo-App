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


#
class TodoItem:
    def __init__(
        self,
        title,
        description,
        category,
        completed=False,
        start_date=None,
        start_time=None,
        end_date=None,
        end_time=None,
    ):
        self.title = title
        self.description = description
        self.category = category
        self.completed = completed
        self.start_date = start_date
        self.start_time = start_time
        self.end_date = end_date
        self.end_time = end_time


def create_connection():
    conn = sqlite3.connect("data/todo.db")
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


def add_todo_item(conn, todo_item):
    if todo_item.title:
        c = conn.cursor()
        c.execute(
            "INSERT INTO todo_items (title, description, category, completed) VALUES (?, ?, ?, ?)",
            (
                todo_item.title,
                todo_item.description,
                todo_item.category,
                int(todo_item.completed),
            ),
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
    todo_item = TodoItem(title, description, category)
    add_todo_item(conn, todo_item)


def view_and_manage_todo_items(conn):
    while True:
        print("\n1. View all to-do items")
        print("2. View uncategorized to-do items")
        print("3. View to-do items by category")
        print("4. Remove a to-do item")
        print("5. Edit a to-do item")
        print("6. Schedule a to-do item")
        print("7. Focus on Urgent to-do item")
        print("8. Back to main menu")
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
            edit_todo_item(conn)
        elif choice == "6":
            view_schedule_todo_item(conn)
        elif choice == "7":
            focus_todo_item(conn)
        elif choice == "8":
            break
        else:
            print("Invalid choice. Please try again.")


def view_all_todo_items(conn):
    c = conn.cursor()
    c.execute("SELECT * FROM todo_items")
    todo_items = [TodoItem(*item) for item in c.fetchall()]

    if todo_items:
        print("\nAll to-do items:")
        for i, item in enumerate(todo_items):
            print(f"{i+1}. {item.title} - {item.description} ({item.category})")
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

    if category.lower() == "schedule":
        c.execute(
            "SELECT title, description, start_date, start_time, end_date, end_time FROM todo_items WHERE category = ?",
            (category,),
        )
        todo_items = c.fetchall()

        if todo_items:
            print(f"\nTo-do items in category '{category}':")
            for i, item in enumerate(todo_items):
                print(f"{i+1}. {item[0]} - {item[1]}")
                print(f"   Start: {item[2]} at {item[3]}")
                print(f"   End: {item[4]} at {item[5]}")
                print()
        else:
            print(f"No to-do items found in category '{category}'.")
    else:
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


def edit_todo_item(conn):
    print("\nEdit.")


def view_schedule_todo_item(conn):
    while True:
        print("\nWhich to-do item would you like to schedule?")

        # List scheduled items
        c = conn.cursor()
        c.execute("SELECT title FROM todo_items WHERE category='schedule'")
        scheduled_items = c.fetchall()

        if not scheduled_items:
            print("No items categorized as 'schedule' found.")
        else:
            for idx, item in enumerate(scheduled_items, 1):
                print(f"{idx}. {item[0]}")

        print("3. Go back to main menu")

        choice = input("\nEnter your choice: ")

        if choice == "3":
            return

        # Check if the entered choice matches any scheduled item
        matching_item = next(
            (item[0] for item in scheduled_items if item[0].lower() == choice.lower()),
            None,
        )

        if matching_item:
            schedule_todo_item(conn, matching_item)
            break
        else:
            print(
                "Sorry, that item doesn't match any scheduled to-do. Please try again by typing the name exactly, not the number."
            )


def schedule_todo_item(conn, item_title):
    print(f"\nScheduling item: {item_title}")

    start_date = input(
        f"What day would you like to start on {item_title}? (YYMMDD format): "
    )
    start_time = input(
        f"What time would you like to start on {item_title}? (hh:mm AM/PM format): "
    )
    end_date = input(
        f"What day would you like to complete {item_title}? (YYMMDD format): "
    )
    end_time = input(
        f"What time would you like to complete {item_title}? (hh:mm AM/PM format): "
    )

    c = conn.cursor()
    c.execute("SELECT * FROM todo_items WHERE title = ?", (item_title,))
    item_data = c.fetchone()

    if item_data:
        todo_item = TodoItem(*item_data)
        todo_item.start_date = start_date
        todo_item.start_time = start_time
        todo_item.end_date = end_date
        todo_item.end_time = end_time

        c.execute(
            """UPDATE todo_items
                     SET start_date = ?, start_time = ?, end_date = ?, end_time = ?
                     WHERE title = ?""",
            (
                todo_item.start_date,
                todo_item.start_time,
                todo_item.end_date,
                todo_item.end_time,
                todo_item.title,
            ),
        )
        conn.commit()

        print("Schedule information updated successfully.")
    else:
        print(f"No to-do item found with title '{item_title}'.")


def focus_todo_item(conn):
    print("\nFocus.")


def how_to_app(conn):
    print("\nUse the command line.")


def about_app(conn):
    print("\nThis app is by Reid Kimball.")


def main():
    conn = create_connection()
    create_table(conn)

    while True:
        print("\n1. Add To-Do Item")
        print("2. View and Manage To-Do Items")
        print("3. How to Use CLI To-Do")
        print("4. About CLI To-Do app")
        print("5. Quit")
        choice = input("Enter your choice: ")

        if choice == "1":
            add_todo_item_from_user_input(conn)
        elif choice == "2":
            view_and_manage_todo_items(conn)
        elif choice == "3":
            # add function for How to Use CLI To-Do
            how_to_app(conn)
        elif choice == "4":
            # add function for About CLI To-Do
            about_app(conn)
        elif choice == "5":
            conn.close()
            break
        else:
            print("Invalid choice. Please try again.")


if __name__ == "__main__":
    main()
