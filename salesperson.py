# salesperson.py
# Salesperson Management API for CarQuery

from db import get_connection


def add_salesperson():
    employee_id = input("Enter employee ID: ").strip()
    first_name  = input("Enter first name: ").strip()
    last_name   = input("Enter last name: ").strip()
    lot_id      = input("Enter lot ID: ").strip()
    hire_date   = input("Enter hire date (YYYY-MM-DD): ").strip()

    conn = None
    try:
        conn = get_connection()
        cur  = conn.cursor()
        cur.execute(
            """
            INSERT INTO Salesperson (employee_id, first_name, last_name, lot_id, hire_date)
            VALUES (%s, %s, %s, %s, %s)
            """,
            (employee_id, first_name, last_name, lot_id, hire_date)
        )
        conn.commit()
        print(f"Salesperson '{employee_id}' added successfully.")
    except Exception as e:
        print(f"Error: {e}")
    finally:
        if 'cur' in locals() and cur:
            cur.close()
        if conn:
            conn.close()


def update_salesperson():
    employee_id = input("Enter employee ID to update: ").strip()
    print("Leave a field blank to keep it unchanged.")
    first_name = input("New first name (or blank): ").strip() or None
    last_name  = input("New last name (or blank): ").strip() or None
    lot_id     = input("New lot ID (or blank): ").strip() or None

    if not any([first_name, last_name, lot_id]):
        print("No fields provided. Nothing updated.")
        return

    fields = []
    values = []

    if first_name:
        fields.append("first_name = %s")
        values.append(first_name)
    if last_name:
        fields.append("last_name = %s")
        values.append(last_name)
    if lot_id:
        fields.append("lot_id = %s")
        values.append(lot_id)

    values.append(employee_id)

    conn = None
    try:
        conn = get_connection()
        cur  = conn.cursor()
        cur.execute(
            f"UPDATE Salesperson SET {', '.join(fields)} WHERE employee_id = %s",
            values
        )
        if cur.rowcount == 0:
            print(f"No salesperson found with employee ID '{employee_id}'.")
        else:
            conn.commit()
            print(f"Salesperson '{employee_id}' updated successfully.")
    except Exception as e:
        print(f"Error: {e}")
    finally:
        if 'cur' in locals() and cur:
            cur.close()
        if conn:
            conn.close()


def list_all_salespersons():
    conn = None
    try:
        conn = get_connection()
        cur  = conn.cursor()
        cur.execute(
            """
            SELECT s.employee_id, s.first_name, s.last_name, l.name AS lot_name
            FROM Salesperson s
            JOIN Lot l ON s.lot_id = l.lot_id
            ORDER BY s.last_name, s.first_name
            """
        )
        rows = cur.fetchall()
        if not rows:
            print("No salespersons found.")
        else:
            print(f"\n{'Employee ID':<15} {'First Name':<15} {'Last Name':<15} {'Lot'}")
            print("-" * 60)
            for row in rows:
                print(f"{row[0]:<15} {row[1]:<15} {row[2]:<15} {row[3]}")
    except Exception as e:
        print(f"Error: {e}")
    finally:
        if 'cur' in locals() and cur:
            cur.close()
        if conn:
            conn.close()
