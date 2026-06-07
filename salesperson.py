# salesperson.py
# Salesperson Management API for CarQuery

from db import get_connection


def AddSalesperson(employee_id, first_name, last_name, lot_id, hire_date):
    """
    Adds a new salesperson to the system, assigned to a home lot.
    Parameters: employee_id, first_name, last_name, lot_id, hire_date
    Returns: Success or failure message.
    """
    conn = None
    try:
        conn = get_connection()
        cur = conn.cursor()
        cur.execute(
            """
            INSERT INTO Salesperson (employee_id, first_name, last_name, lot_id, hire_date)
            VALUES (%s, %s, %s, %s, %s)
            """,
            (employee_id, first_name, last_name, lot_id, hire_date)
        )
        conn.commit()
        return f"Success: Salesperson '{employee_id}' added."
    except Exception as e:
        return f"Failure: {e}"
    finally:
        if 'cur' in locals() and cur:
            cur.close()
        if conn:
            conn.close()


def UpdateSalesperson(employee_id, first_name=None, last_name=None, lot_id=None):
    """
    Updates a salesperson's name and/or lot assignment.
    Parameters: employee_id (required), first_name (opt), last_name (opt), lot_id (opt)
    Returns: Success or failure message.
    """
    conn = None
    try:
        if not any([first_name, last_name, lot_id]):
            return "Failure: No fields provided to update."

        fields = []
        values = []

        if first_name is not None:
            fields.append("first_name = %s")
            values.append(first_name)
        if last_name is not None:
            fields.append("last_name = %s")
            values.append(last_name)
        if lot_id is not None:
            fields.append("lot_id = %s")
            values.append(lot_id)

        values.append(employee_id)

        conn = get_connection()
        cur = conn.cursor()
        cur.execute(
            f"UPDATE Salesperson SET {', '.join(fields)} WHERE employee_id = %s",
            values
        )

        if cur.rowcount == 0:
            return f"Failure: No salesperson found with employee_id '{employee_id}'."

        conn.commit()
        return f"Success: Salesperson '{employee_id}' updated."
    except Exception as e:
        return f"Failure: {e}"
    finally:
        if 'cur' in locals() and cur:
            cur.close()
        if conn:
            conn.close()


def ListAllSalespersons():
    """
    Returns all salespersons in the system with their lot name.
    Parameters: none
    Returns: List of (employee_id, first_name, last_name, lot_name).
    """
    conn = None
    try:
        conn = get_connection()
        cur = conn.cursor()
        cur.execute(
            """
            SELECT s.employee_id, s.first_name, s.last_name, l.name AS lot_name
            FROM Salesperson s
            JOIN Lot l ON s.lot_id = l.lot_id
            ORDER BY s.last_name, s.first_name
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
