from db import get_connection


# ─────────────────────────────────────────
# Sales Transactions
# Functions:
# SellVehicleNoTradeIn
# SellVehicleWithTradeIn
# ─────────────────────────────────────────


def SellVehicleNoTradeIn():
    vin = input("Enter VIN of vehicle being sold: ").strip()
    customer_email = input("Enter customer email: ").strip()
    employee_id = input("Enter salesperson employee ID: ").strip()
    sale_price = input("Enter sale price: ").strip()

    conn = None
    cur = None

    try:
        conn = get_connection()
        cur = conn.cursor()

        # Make sure the vehicle exists and is not already sold
        cur.execute("""
            SELECT sold
            FROM Vehicle
            WHERE vin = %s
        """, (vin,))

        vehicle = cur.fetchone()

        if not vehicle:
            print("No vehicle found with that VIN.")
            return

        if vehicle[0] is True:
            print("This vehicle is already sold.")
            return

        # Make sure customer exists
        cur.execute("""
            SELECT email
            FROM Customer
            WHERE email = %s
        """, (customer_email,))

        if not cur.fetchone():
            print("No customer found with that email.")
            return

        # Make sure salesperson exists
        cur.execute("""
            SELECT employee_id
            FROM Salesperson
            WHERE employee_id = %s
        """, (employee_id,))

        if not cur.fetchone():
            print("No salesperson found with that employee ID.")
            return

        # Mark vehicle as sold
        cur.execute("""
            UPDATE Vehicle
            SET sold = TRUE
            WHERE vin = %s
        """, (vin,))

        # Insert sale record
        cur.execute("""
            INSERT INTO Sale
                (vin, customer_email, employee_id, sale_price,
                 trade_in_vin, trade_in_value, sale_date)
            VALUES (%s, %s, %s, %s, NULL, NULL, CURRENT_DATE)
        """, (vin, customer_email, employee_id, sale_price))

        conn.commit()
        print("Vehicle sale recorded successfully.")

    except Exception as e:
        if conn:
            conn.rollback()
        print(f"Error: {e}")

    finally:
        if cur:
            cur.close()
        if conn:
            conn.close()


def SellVehicleWithTradeIn():
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
    trade_in_asking_price = input("Enter asking price for trade-in vehicle: ").strip()

    conn = None
    cur = None

    try:
        conn = get_connection()
        cur = conn.cursor()

        # Get sold vehicle info and make sure it is available
        cur.execute("""
            SELECT sold, current_lot_id
            FROM Vehicle
            WHERE vin = %s
        """, (vin,))

        vehicle = cur.fetchone()

        if not vehicle:
            print("No vehicle found with that VIN.")
            return

        if vehicle[0] is True:
            print("This vehicle is already sold.")
            return

        lot_id = vehicle[1]

        # Make sure customer exists
        cur.execute("""
            SELECT email
            FROM Customer
            WHERE email = %s
        """, (customer_email,))

        if not cur.fetchone():
            print("No customer found with that email.")
            return

        # Make sure salesperson exists
        cur.execute("""
            SELECT employee_id
            FROM Salesperson
            WHERE employee_id = %s
        """, (employee_id,))

        if not cur.fetchone():
            print("No salesperson found with that employee ID.")
            return

        # Mark original vehicle as sold
        cur.execute("""
            UPDATE Vehicle
            SET sold = TRUE
            WHERE vin = %s
        """, (vin,))

        # Record the sale with trade-in information
        cur.execute("""
            INSERT INTO Sale
                (vin, customer_email, employee_id, sale_price,
                 trade_in_vin, trade_in_value, sale_date)
            VALUES (%s, %s, %s, %s, %s, %s, CURRENT_DATE)
        """, (vin, customer_email, employee_id, sale_price,
              trade_in_vin, trade_in_value))

        # Add the trade-in vehicle to inventory at the same lot
        cur.execute("""
            INSERT INTO Vehicle
                (vin, make, model, year, mileage, color,
                 condition_code, current_lot_id, location_status,
                 current_asking_price, date_acquired, sold)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s,
                    'Available', %s, CURRENT_DATE, FALSE)
        """, (trade_in_vin, trade_in_make, trade_in_model,
              trade_in_year, trade_in_mileage, trade_in_color,
              trade_in_condition_code, lot_id, trade_in_asking_price))

        conn.commit()
        print("Vehicle sale with trade-in recorded successfully.")

    except Exception as e:
        if conn:
            conn.rollback()
        print(f"Error: {e}")

    finally:
        if cur:
            cur.close()
        if conn:
            conn.close()


# Lowercase aliases in case the menu file uses snake_case names.
def sell_vehicle_no_trade_in():
    SellVehicleNoTradeIn()


def sell_vehicle_with_trade_in():
    SellVehicleWithTradeIn()