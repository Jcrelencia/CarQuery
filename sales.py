from db import get_connection


# ─────────────────────────────────────────
# SERVER FUNCTIONS
# ─────────────────────────────────────────

def sell_vehicle_no_trade_in(vin, customer_email, employee_id, sale_price):
    try:
        conn = get_connection()
        cur = conn.cursor()
        cur.execute("""
            SELECT vehicle_id FROM Vehicle
            WHERE vin = %s AND sold = FALSE LIMIT 1
        """, (vin,))
        row = cur.fetchone()
        if not row:
            return "No available vehicle found with that VIN."
        vehicle_id = row[0]
        cur.execute("SELECT email FROM Customer WHERE email = %s", (customer_email,))
        if not cur.fetchone():
            return "No customer found with that email."
        cur.execute("SELECT employee_id FROM Salesperson WHERE employee_id = %s", (employee_id,))
        if not cur.fetchone():
            return "No salesperson found with that employee ID."
        cur.execute("UPDATE Vehicle SET sold = TRUE WHERE vehicle_id = %s", (vehicle_id,))
        cur.execute("""
            INSERT INTO Sale
                (vehicle_id, customer_email, employee_id, sale_price,
                 trade_in_vehicle_id, trade_in_value, sale_date)
            VALUES (%s, %s, %s, %s, NULL, NULL, CURRENT_DATE)
        """, (vehicle_id, customer_email, employee_id, sale_price))
        conn.commit()
        return "Vehicle sale recorded successfully."
    except Exception as e:
        conn.rollback()
        return f"Error: {e}"


def sell_vehicle_with_trade_in(vin, customer_email, employee_id, sale_price,
                                trade_in_vin, trade_in_make, trade_in_model,
                                trade_in_year, trade_in_mileage, trade_in_color,
                                trade_in_condition_code, trade_in_value, trade_in_asking_price):
    try:
        conn = get_connection()
        cur = conn.cursor()
        cur.execute("""
            SELECT vehicle_id, current_lot_id FROM Vehicle
            WHERE vin = %s AND sold = FALSE LIMIT 1
        """, (vin,))
        row = cur.fetchone()
        if not row:
            return "No available vehicle found with that VIN."
        vehicle_id, lot_id = row
        cur.execute("SELECT email FROM Customer WHERE email = %s", (customer_email,))
        if not cur.fetchone():
            return "No customer found with that email."
        cur.execute("SELECT employee_id FROM Salesperson WHERE employee_id = %s", (employee_id,))
        if not cur.fetchone():
            return "No salesperson found with that employee ID."
        cur.execute("UPDATE Vehicle SET sold = TRUE WHERE vehicle_id = %s", (vehicle_id,))
        cur.execute("""
            INSERT INTO Vehicle
                (vin, make, model, year, mileage, color, condition_code,
                 current_lot_id, location_status, current_asking_price,
                 date_acquired, sold)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, 'Available', %s, CURRENT_DATE, FALSE)
            RETURNING vehicle_id
        """, (trade_in_vin, trade_in_make, trade_in_model, trade_in_year,
              trade_in_mileage, trade_in_color, trade_in_condition_code,
              lot_id, trade_in_asking_price))
        trade_in_vehicle_id = cur.fetchone()[0]
        cur.execute("""
            INSERT INTO Sale
                (vehicle_id, customer_email, employee_id, sale_price,
                 trade_in_vehicle_id, trade_in_value, sale_date)
            VALUES (%s, %s, %s, %s, %s, %s, CURRENT_DATE)
        """, (vehicle_id, customer_email, employee_id, sale_price,
              trade_in_vehicle_id, trade_in_value))
        conn.commit()
        return "Vehicle sale with trade-in recorded successfully."
    except Exception as e:
        conn.rollback()
        return f"Error: {e}"


# ─────────────────────────────────────────
# CLIENT FUNCTIONS
# ─────────────────────────────────────────

def sell_vehicle_no_trade_in_client():
    vin = input("Enter VIN of vehicle being sold: ").strip()
    customer_email = input("Enter customer email: ").strip()
    employee_id = input("Enter salesperson employee ID: ").strip()
    sale_price = input("Enter sale price: ").strip()
    print(sell_vehicle_no_trade_in(vin, customer_email, employee_id, sale_price))


def sell_vehicle_with_trade_in_client():
    vin = input("Enter VIN of vehicle being sold: ").strip()
    customer_email = input("Enter customer email: ").strip()
    employee_id = input("Enter salesperson employee ID: ").strip()
    sale_price = input("Enter sale price: ").strip()
    print("\nTrade-In Vehicle Information")
    trade_in_vin = input("Enter trade-in VIN: ").strip()
    trade_in_make = input("Enter trade-in make: ").strip()
    trade_in_model = input("Enter trade-in model: ").strip()
    trade_in_year = input("Enter trade-in year: ").strip()
    trade_in_mileage = input("Enter trade-in mileage: ").strip()
    trade_in_color = input("Enter trade-in color: ").strip()
    trade_in_condition_code = input("Enter trade-in condition code: ").strip()
    trade_in_value = input("Enter trade-in value: ").strip()
    trade_in_asking_price = input("Enter asking price for trade-in: ").strip()
    print(sell_vehicle_with_trade_in(
        vin, customer_email, employee_id, sale_price,
        trade_in_vin, trade_in_make, trade_in_model,
        trade_in_year, trade_in_mileage, trade_in_color,
        trade_in_condition_code, trade_in_value, trade_in_asking_price
    ))