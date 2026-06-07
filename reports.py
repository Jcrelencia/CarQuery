# reports.py
# Reporting API for CarQuery

from db import get_connection


def get_inventory_report_by_lot():
    lot_id = input("Enter lot ID (or blank for all lots): ").strip() or None

    conn = None
    try:
        conn = get_connection()
        cur  = conn.cursor()

        if lot_id:
            cur.execute(
                """
                SELECT
                    l.name AS lot_name,
                    COUNT(v.vehicle_id) AS vehicle_count,
                    ROUND(AVG(v.current_asking_price), 2) AS avg_price,
                    ROUND(AVG(CURRENT_DATE - v.date_acquired), 2) AS avg_days_in_inventory
                FROM Vehicle v
                JOIN Lot l ON v.current_lot_id = l.lot_id
                WHERE v.sold = FALSE AND v.current_lot_id = %s
                GROUP BY l.lot_id, l.name
                ORDER BY l.name
                """,
                (lot_id,)
            )
        else:
            cur.execute(
                """
                SELECT
                    l.name AS lot_name,
                    COUNT(v.vehicle_id) AS vehicle_count,
                    ROUND(AVG(v.current_asking_price), 2) AS avg_price,
                    ROUND(AVG(CURRENT_DATE - v.date_acquired), 2) AS avg_days_in_inventory
                FROM Vehicle v
                JOIN Lot l ON v.current_lot_id = l.lot_id
                WHERE v.sold = FALSE
                GROUP BY l.lot_id, l.name
                ORDER BY l.name
                """
            )

        rows = cur.fetchall()
        if not rows:
            print("No inventory data found.")
        else:
            print(f"\n{'Lot':<20} {'Vehicles':<10} {'Avg Price':<15} {'Avg Days'}")
            print("-" * 60)
            for row in rows:
                print(f"{row[0]:<20} {row[1]:<10} ${row[2]:<14} {row[3]}")
    except Exception as e:
        print(f"Error: {e}")
    finally:
        if 'cur' in locals() and cur:
            cur.close()
        if conn:
            conn.close()


def get_sales_report():
    date_start  = input("Enter start date (YYYY-MM-DD): ").strip()
    date_end    = input("Enter end date (YYYY-MM-DD): ").strip()
    employee_id = input("Enter employee ID (or blank for all): ").strip() or None

    conn = None
    try:
        conn = get_connection()
        cur  = conn.cursor()

        if employee_id:
            cur.execute(
                """
                SELECT
                    s.employee_id,
                    s.first_name || ' ' || s.last_name AS name,
                    COUNT(sa.sale_id) AS vehicles_sold,
                    COALESCE(SUM(sa.sale_price), 0) AS total_revenue
                FROM Salesperson s
                LEFT JOIN Sale sa ON s.employee_id = sa.employee_id
                    AND sa.sale_date BETWEEN %s AND %s
                WHERE s.employee_id = %s
                GROUP BY s.employee_id, s.first_name, s.last_name
                ORDER BY total_revenue DESC
                """,
                (date_start, date_end, employee_id)
            )
        else:
            cur.execute(
                """
                SELECT
                    s.employee_id,
                    s.first_name || ' ' || s.last_name AS name,
                    COUNT(sa.sale_id) AS vehicles_sold,
                    COALESCE(SUM(sa.sale_price), 0) AS total_revenue
                FROM Salesperson s
                LEFT JOIN Sale sa ON s.employee_id = sa.employee_id
                    AND sa.sale_date BETWEEN %s AND %s
                GROUP BY s.employee_id, s.first_name, s.last_name
                ORDER BY total_revenue DESC
                """,
                (date_start, date_end)
            )

        rows = cur.fetchall()
        if not rows:
            print("No sales data found for that period.")
        else:
            print(f"\n{'Employee ID':<15} {'Name':<25} {'Sold':<8} {'Revenue'}")
            print("-" * 65)
            for row in rows:
                print(f"{row[0]:<15} {row[1]:<25} {row[2]:<8} ${row[3]}")
    except Exception as e:
        print(f"Error: {e}")
    finally:
        if 'cur' in locals() and cur:
            cur.close()
        if conn:
            conn.close()


def list_all_lots():
    conn = None
    try:
        conn = get_connection()
        cur  = conn.cursor()
        cur.execute(
            """
            SELECT lot_id, name, address, city, state
            FROM Lot
            ORDER BY name
            """
        )
        rows = cur.fetchall()
        if not rows:
            print("No lots found.")
        else:
            print(f"\n{'ID':<6} {'Name':<20} {'Address':<25} {'City':<15} {'State'}")
            print("-" * 75)
            for row in rows:
                print(f"{row[0]:<6} {row[1]:<20} {str(row[2]):<25} {str(row[3]):<15} {row[4]}")
    except Exception as e:
        print(f"Error: {e}")
    finally:
        if 'cur' in locals() and cur:
            cur.close()
        if conn:
            conn.close()


def list_all_conditions():
    conn = None
    try:
        conn = get_connection()
        cur  = conn.cursor()
        cur.execute(
            """
            SELECT condition_code, description
            FROM Condition
            ORDER BY condition_code
            """
        )
        rows = cur.fetchall()
        if not rows:
            print("No conditions found.")
        else:
            print(f"\n{'Code':<15} {'Description'}")
            print("-" * 50)
            for row in rows:
                print(f"{row[0]:<15} {row[1]}")
    except Exception as e:
        print(f"Error: {e}")
    finally:
        if 'cur' in locals() and cur:
            cur.close()
        if conn:
            conn.close()
