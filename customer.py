from db import get_connection


# ─────────────────────────────────────────
# SERVER FUNCTIONS
# ─────────────────────────────────────────

def add_customer(first_name, last_name, email, phone, address):
    try:
        conn = get_connection()
        cur = conn.cursor()
        cur.execute("""
            INSERT INTO Customer (first_name, last_name, email, phone, address)
            VALUES (%s, %s, %s, %s, %s)
        """, (first_name, last_name, email, phone, address))
        conn.commit()
        return "Customer added successfully."
    except Exception as e:
        conn.rollback()
        return f"Error: {e}"


def update_customer(email, first_name=None, last_name=None, phone=None, address=None):
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
        return "No fields provided to update."
    values.append(email)
    try:
        conn = get_connection()
        cur = conn.cursor()
        cur.execute(f"UPDATE Customer SET {', '.join(fields)} WHERE email = %s", values)
        if cur.rowcount == 0:
            conn.rollback()
            return "No customer found with that email."
        conn.commit()
        return "Customer updated successfully."
    except Exception as e:
        conn.rollback()
        return f"Error: {e}"


def get_customer_history(email):
    try:
        conn = get_connection()
        cur = conn.cursor()
        cur.execute("""
            SELECT first_name, last_name, email, phone, address
            FROM Customer WHERE email = %s
        """, (email,))
        customer = cur.fetchone()
        if not customer:
            return None, []
        cur.execute("""
            SELECT v.vin, v.make, v.model, v.year, s.sale_price, s.sale_date
            FROM Sale s
            JOIN Vehicle v ON s.vehicle_id = v.vehicle_id
            WHERE s.customer_email = %s
            ORDER BY s.sale_date DESC
        """, (email,))
        return customer, cur.fetchall()
    except Exception as e:
        return f"Error: {e}", []


# ─────────────────────────────────────────
# CLIENT FUNCTIONS
# ─────────────────────────────────────────

def add_customer_client():
    first_name = input("Enter first name: ").strip()
    last_name = input("Enter last name: ").strip()
    email = input("Enter email: ").strip()
    phone = input("Enter phone: ").strip()
    address = input("Enter address: ").strip()
    print(add_customer(first_name, last_name, email, phone, address))


def update_customer_client():
    email = input("Enter customer email: ").strip()
    print("Leave blank to keep unchanged.")
    first_name = input("New first name: ").strip() or None
    last_name = input("New last name: ").strip() or None
    phone = input("New phone: ").strip() or None
    address = input("New address: ").strip() or None
    print(update_customer(email, first_name, last_name, phone, address))


def get_customer_history_client():
    email = input("Enter customer email: ").strip()
    customer, purchases = get_customer_history(email)
    if isinstance(customer, str):
        print(customer)
        return
    if customer is None:
        print("No customer found with that email.")
        return
    print(f"\nCustomer Profile")
    print("----------------")
    print(f"Name:    {customer[0]} {customer[1]}")
    print(f"Email:   {customer[2]}")
    print(f"Phone:   {customer[3]}")
    print(f"Address: {customer[4]}")
    print(f"\nPurchase History")
    print("----------------")
    if not purchases:
        print("No purchase history.")
    else:
        for r in purchases:
            print(f"VIN: {r[0]}  |  {r[1]} {r[2]} ({r[3]})  |  ${r[4]}  |  {r[5]}")