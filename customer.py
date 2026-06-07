from db import get_connection


# ─────────────────────────────────────────
# Customer Management
# Functions:
# AddCustomer
# UpdateCustomer
# GetCustomerHistory
# ─────────────────────────────────────────


def AddCustomer():
    first_name = input("Enter first name: ").strip()
    last_name = input("Enter last name: ").strip()
    email = input("Enter email: ").strip()
    phone = input("Enter phone: ").strip()
    address = input("Enter address: ").strip()

    conn = None
    cur = None

    try:
        conn = get_connection()
        cur = conn.cursor()

        cur.execute("""
            INSERT INTO Customer
                (first_name, last_name, email, phone, address)
            VALUES (%s, %s, %s, %s, %s)
        """, (first_name, last_name, email, phone, address))

        conn.commit()
        print("Customer added successfully.")

    except Exception as e:
        if conn:
            conn.rollback()
        print(f"Error: {e}")

    finally:
        if cur:
            cur.close()
        if conn:
            conn.close()


def UpdateCustomer():
    email = input("Enter the customer's email: ").strip()

    print("Leave a field blank if you do not want to update it.")
    first_name = input("New first name: ").strip()
    last_name = input("New last name: ").strip()
    phone = input("New phone: ").strip()
    address = input("New address: ").strip()

    fields = []
    values = []

    if first_name:
        fields.append("first_name = %s")
        values.append(first_name)

    if last_name:
        fields.append("last_name = %s")
        values.append(last_name)

    if phone:
        fields.append("phone = %s")
        values.append(phone)

    if address:
        fields.append("address = %s")
        values.append(address)

    if not fields:
        print("No updates entered.")
        return

    values.append(email)

    conn = None
    cur = None

    try:
        conn = get_connection()
        cur = conn.cursor()

        query = f"""
            UPDATE Customer
            SET {', '.join(fields)}
            WHERE email = %s
        """

        cur.execute(query, tuple(values))

        if cur.rowcount == 0:
            conn.rollback()
            print("No customer found with that email.")
        else:
            conn.commit()
            print("Customer updated successfully.")

    except Exception as e:
        if conn:
            conn.rollback()
        print(f"Error: {e}")

    finally:
        if cur:
            cur.close()
        if conn:
            conn.close()


def GetCustomerHistory():
    email = input("Enter customer email: ").strip()

    conn = None
    cur = None

    try:
        conn = get_connection()
        cur = conn.cursor()

        cur.execute("""
            SELECT first_name, last_name, email, phone, address
            FROM Customer
            WHERE email = %s
        """, (email,))

        customer = cur.fetchone()

        if not customer:
            print("No customer found with that email.")
            return

        print("\nCustomer Profile")
        print("----------------")
        print(f"Name:    {customer[0]} {customer[1]}")
        print(f"Email:   {customer[2]}")
        print(f"Phone:   {customer[3]}")
        print(f"Address: {customer[4]}")

        cur.execute("""
            SELECT 
                s.vin,
                v.make,
                v.model,
                v.year,
                s.sale_price,
                s.sale_date
            FROM Sale s
            LEFT JOIN Vehicle v ON s.vin = v.vin
            WHERE s.customer_email = %s
            ORDER BY s.sale_date DESC
        """, (email,))

        rows = cur.fetchall()

        print("\nPurchase History")
        print("----------------")

        if not rows:
            print("This customer has no purchase history.")
        else:
            for row in rows:
                print(f"""
VIN:        {row[0]}
Vehicle:    {row[1]} {row[2]} ({row[3]})
Sale Price: ${row[4]}
Sale Date:  {row[5]}
""")

    except Exception as e:
        print(f"Error: {e}")

    finally:
        if cur:
            cur.close()
        if conn:
            conn.close()


# Lowercase aliases in case the menu file uses snake_case names.
def add_customer():
    AddCustomer()


def update_customer():
    UpdateCustomer()


def get_customer_history():
    GetCustomerHistory()