from db import get_connection


# ─────────────────────────────────────────
# SERVER FUNCTIONS
# ─────────────────────────────────────────

def add_salesperson(employee_id, first_name, last_name, lot_id, hire_date):
    try:
        conn = get_connection()
        cur = conn.cursor()
        cur.execute("""
            INSERT INTO Salesperson (employee_id, first_name, last_name, lot_id, hire_date)
            VALUES (%s, %s, %s, %s, %s)
        """, (employee_id, first_name, last_name, lot_id, hire_date))
        conn.commit()
        return f"Salesperson '{employee_id}' added successfully."
    except Exception as e:
        conn.rollback()
        return f"Error: {e}"


def update_salesperson(employee_id, first_name=None, last_name=None, lot_id=None):
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
    if not fields:
        return "No fields provided to update."
    values.append(employee_id)
    try:
        conn = get_connection()
        cur = conn.cursor()
        cur.execute(f"UPDATE Salesperson SET {', '.join(fields)} WHERE employee_id = %s", values)
        if cur.rowcount == 0:
            conn.rollback()
            return f"No salesperson found with employee ID '{employee_id}'."
        conn.commit()
        return f"Salesperson '{employee_id}' updated successfully."
    except Exception as e:
        conn.rollback()
        return f"Error: {e}"


def list_all_salespersons():
    try:
        conn = get_connection()
        cur = conn.cursor()
        cur.execute("""
            SELECT s.employee_id, s.first_name, s.last_name, l.name
            FROM Salesperson s
            JOIN Lot l ON s.lot_id = l.lot_id
            ORDER BY s.last_name, s.first_name
        """)
        return cur.fetchall()
    except Exception as e:
        return f"Error: {e}"


# ─────────────────────────────────────────
# CLIENT FUNCTIONS
# ─────────────────────────────────────────

def add_salesperson_client():
    employee_id = input("Enter employee ID: ").strip()
    first_name = input("Enter first name: ").strip()
    last_name = input("Enter last name: ").strip()
    lot_id = input("Enter lot ID: ").strip()
    hire_date = input("Enter hire date (YYYY-MM-DD): ").strip()
    print(add_salesperson(employee_id, first_name, last_name, lot_id, hire_date))


def update_salesperson_client():
    employee_id = input("Enter employee ID to update: ").strip()
    print("Leave blank to keep unchanged.")
    first_name = input("New first name: ").strip() or None
    last_name = input("New last name: ").strip() or None
    lot_id = input("New lot ID: ").strip() or None
    print(update_salesperson(employee_id, first_name, last_name, lot_id))


def list_all_salespersons_client():
    rows = list_all_salespersons()
    if isinstance(rows, str):
        print(rows)
    elif not rows:
        print("No salespersons found.")
    else:
        print(f"\n{'Employee ID':<15} {'First Name':<15} {'Last Name':<15} {'Lot'}")
        print("-" * 60)
        for r in rows:
            print(f"{r[0]:<15} {r[1]:<15} {r[2]:<15} {r[3]}")