# reports.py
# Reporting API for CarQuery

from db import get_connection


def GetInventoryReportByLot(lot_id=None):
    """
    Returns a summary of current unsold inventory grouped by lot.
    Parameters: lot_id (optional — if omitted, returns all lots)
    Returns: List of (lot_name, vehicle_count, avg_price, avg_days_in_inventory).
    """
    conn = None
    try:
        conn = get_connection()
        cur = conn.cursor()

        if lot_id is not None:
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
                  AND v.current_lot_id = %s
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
        return rows
    except Exception as e:
        return f"Failure: {e}"
    finally:
        if 'cur' in locals() and cur:
            cur.close()
        if conn:
            conn.close()


def GetSalesReport(date_start, date_end, employee_id=None):
    """
    Returns sales performance for the specified period.
    Parameters: date_start, date_end, employee_id (optional)
    Returns: List of (employee_id, name, vehicles_sold, total_revenue).
    """
    conn = None
    try:
        conn = get_connection()
        cur = conn.cursor()

        if employee_id is not None:
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
        return rows
    except Exception as e:
        return f"Failure: {e}"
    finally:
        if 'cur' in locals() and cur:
            cur.close()
        if conn:
            conn.close()


def ListAllLots():
    """
    Returns all lots in the system.
    Parameters: none
    Returns: List of (lot_id, name, address, city, state).
    """
    conn = None
    try:
        conn = get_connection()
        cur = conn.cursor()
        cur.execute(
            """
            SELECT lot_id, name, address, city, state
            FROM Lot
            ORDER BY name
            """
        )
        rows = cur.fetchall()
        return rows
    except Exception as e:
        return f"Failure: {e}"
    finally:
        if 'cur' in locals() and cur:
            cur.close()
        if conn:
            conn.close()


def ListAllConditions():
    """
    Returns all valid vehicle condition codes and their descriptions.
    Parameters: none
    Returns: List of (condition_code, description).
    """
    conn = None
    try:
        conn = get_connection()
        cur = conn.cursor()
        cur.execute(
            """
            SELECT condition_code, description
            FROM Condition
            ORDER BY condition_code
            """
        )
        rows = cur.fetchall()
        return rows
    except Exception as e:
        return f"Failure: {e}"
    finally:
        if 'cur' in locals() and cur:
            cur.close()
        if conn:
            conn.close()
