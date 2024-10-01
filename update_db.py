def update_db(conn):
    c = conn.cursor()
    c.execute(
        """ALTER TABLE todo_items
                 ADD COLUMN start_date TEXT;"""
    )
    c.execute(
        """ALTER TABLE todo_items
                 ADD COLUMN start_time TEXT;"""
    )
    c.execute(
        """ALTER TABLE todo_items
                 ADD COLUMN end_date TEXT;"""
    )
    c.execute(
        """ALTER TABLE todo_items
                 ADD COLUMN end_time TEXT;"""
    )
    conn.commit()

    print("\nDB UPDATED.")


if __name__ == "__main__":
    update_db()
