from db import get_connection


# ─────────────────────────────────────────
# SERVER FUNCTIONS
# ─────────────────────────────────────────

def get_inventory_report_by_lot(lot_id=None):
    try:
        conn = get_connection()
        cur = conn.cursor()
        if lot_id:
            cur.execute("""
                SELECT l.name, COUNT(v.vehicle_id),
                       ROUND(AVG(v.current_asking_price), 2),
                       ROUND(AVG(CURRENT_DATE - v.date_acquired), 2)
                FROM Vehicle v JOIN Lot l ON v.current_lot_id = l.lot_id
                WHERE v.sold = FALSE AND v.current_lot_id = %s
                GROUP BY l.lot_id, l.name ORDER BY l.name
            """, (lot_id,))
        else:
            cur.execute("""
                SELECT l.name, COUNT(v.vehicle_id),
                       ROUND(AVG(v.current_asking_price), 2),
                       ROUND(AVG(CURRENT_DATE - v.date_acquired), 2)
                FROM Vehicle v JOIN Lot l ON v.current_lot_id = l.lot_id
                WHERE v.sold = FALSE
                GROUP BY l.lot_id, l.name ORDER BY l.name
            """)
        return cur.fetchall()
    except Exception as e:
        return f"Error: {e}"


def get_sales_report(date_start, date_end, employee_id=None):
    try:
        conn = get_connection()
        cur = conn.cursor()
        if employee_id:
            cur.execute("""
                SELECT s.employee_id, s.first_name || ' ' || s.last_name,
                       COUNT(sa.sale_id), COALESCE(SUM(sa.sale_price), 0)
                FROM Salesperson s
                LEFT JOIN Sale sa ON s.employee_id = sa.employee_id
                    AND sa.sale_date BETWEEN %s AND %s
                WHERE s.employee_id = %s
                GROUP BY s.employee_id, s.first_name, s.last_name
                ORDER BY 4 DESC
            """, (date_start, date_end, employee_id))
        else:
            cur.execute("""
                SELECT s.employee_id, s.first_name || ' ' || s.last_name,
                       COUNT(sa.sale_id), COALESCE(SUM(sa.sale_price), 0)
                FROM Salesperson s
                LEFT JOIN Sale sa ON s.employee_id = sa.employee_id
                    AND sa.sale_date BETWEEN %s AND %s
                GROUP BY s.employee_id, s.first_name, s.last_name
                ORDER BY 4 DESC
            """, (date_start, date_end))
        return cur.fetchall()
    except Exception as e:
        return f"Error: {e}"


def list_all_lots():
    try:
        conn = get_connection()
        cur = conn.cursor()
        cur.execute("SELECT lot_id, name, address, city, state FROM Lot ORDER BY name")
        return cur.fetchall()
    except Exception as e:
        return f"Error: {e}"


def list_all_conditions():
    try:
        conn = get_connection()
        cur = conn.cursor()
        cur.execute("SELECT condition_code, description FROM Condition ORDER BY condition_code")
        return cur.fetchall()
    except Exception as e:
        return f"Error: {e}"


# ─────────────────────────────────────────
# CLIENT FUNCTIONS
# ─────────────────────────────────────────

def get_inventory_report_by_lot_client():
    lot_id = input("Enter lot ID (or blank for all lots): ").strip() or None
    rows = get_inventory_report_by_lot(lot_id)
    if isinstance(rows, str):
        print(rows)
    elif not rows:
        print("No inventory data found.")
    else:
        print(f"\n{'Lot':<20} {'Vehicles':<10} {'Avg Price':<15} {'Avg Days'}")
        print("-" * 55)
        for r in rows:
            print(f"{r[0]:<20} {r[1]:<10} ${r[2]:<14} {r[3]}")


def get_sales_report_client():
    date_start = input("Enter start date (YYYY-MM-DD): ").strip()
    date_end = input("Enter end date (YYYY-MM-DD): ").strip()
    employee_id = input("Enter employee ID (or blank for all): ").strip() or None
    rows = get_sales_report(date_start, date_end, employee_id)
    if isinstance(rows, str):
        print(rows)
    elif not rows:
        print("No sales data found.")
    else:
        print(f"\n{'Employee ID':<15} {'Name':<25} {'Sold':<8} {'Revenue'}")
        print("-" * 60)
        for r in rows:
            print(f"{r[0]:<15} {r[1]:<25} {r[2]:<8} ${r[3]}")


def list_all_lots_client():
    rows = list_all_lots()
    if isinstance(rows, str):
        print(rows)
    elif not rows:
        print("No lots found.")
    else:
        print(f"\n{'ID':<6} {'Name':<20} {'Address':<25} {'City':<15} {'State'}")
        print("-" * 70)
        for r in rows:
            print(f"{r[0]:<6} {r[1]:<20} {str(r[2]):<25} {str(r[3]):<15} {r[4]}")


def list_all_conditions_client():
    rows = list_all_conditions()
    if isinstance(rows, str):
        print(rows)
    elif not rows:
        print("No conditions found.")
    else:
        print(f"\n{'Code':<15} {'Description'}")
        print("-" * 45)
        for r in rows:
            print(f"{r[0]:<15} {r[1]}")