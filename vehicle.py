from db import get_connection


# ─────────────────────────────────────────
# SERVER FUNCTIONS
# Take parameters, talk to DB, return result
# ─────────────────────────────────────────

def add_vehicle(vin, make, model, year, mileage, color, condition_code, lot_id, asking_price):
    conn = None
    try:
        conn = get_connection()
        cur = conn.cursor()
        cur.execute("""
            INSERT INTO Vehicle
                (vin, make, model, year, mileage, color,
                 condition_code, current_lot_id, current_asking_price,
                 location_status, sold, date_acquired)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, 'Available', FALSE, CURRENT_DATE)
        """, (vin, make, model, year, mileage, color, condition_code, lot_id, asking_price))
        conn.commit()
        return "Vehicle added successfully."
    except Exception as e:
        if conn:
            conn.rollback()
        return f"Error: {e}"


def update_vehicle_price(vin, new_price, employee_id):
    conn = None
    try:
        conn = get_connection()
        cur = conn.cursor()
        cur.execute("""
            SELECT vehicle_id, current_asking_price FROM Vehicle
            WHERE vin = %s AND sold = FALSE LIMIT 1
        """, (vin,))
        row = cur.fetchone()
        if not row:
            return "No available vehicle found with that VIN."
        vehicle_id, old_price = row
        cur.execute("""
            SELECT salesperson_id FROM Salesperson WHERE employee_id = %s
        """, (employee_id,))
        sp = cur.fetchone()
        if not sp:
            return "No salesperson found with that employee ID."
        cur.execute("""
            UPDATE Vehicle SET current_asking_price = %s WHERE vehicle_id = %s
        """, (new_price, vehicle_id))
        cur.execute("""
            INSERT INTO PriceHistory (vehicle_id, old_price, new_price, changed_by)
            VALUES (%s, %s, %s, %s)
        """, (vehicle_id, old_price, new_price, sp[0]))
        conn.commit()
        return "Vehicle price updated and price history recorded."
    except Exception as e:
        if conn:
            conn.rollback()
        return f"Error: {e}"


def initiate_vehicle_transfer(vin, to_lot_id):
    conn = None
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
        vehicle_id, from_lot_id = row
        cur.execute("""
            UPDATE Vehicle SET location_status = 'InTransit' WHERE vehicle_id = %s
        """, (vehicle_id,))
        cur.execute("""
            INSERT INTO VehicleLocationLog (vehicle_id, from_lot_id, to_lot_id, status)
            VALUES (%s, %s, %s, 'InTransit')
        """, (vehicle_id, from_lot_id, to_lot_id))
        conn.commit()
        return "Vehicle transfer initiated."
    except Exception as e:
        if conn:
            conn.rollback()
        return f"Error: {e}"


def confirm_vehicle_arrival(vin):
    conn = None
    try:
        conn = get_connection()
        cur = conn.cursor()
        cur.execute("""
            SELECT vehicle_id FROM Vehicle
            WHERE vin = %s AND location_status = 'InTransit' AND sold = FALSE LIMIT 1
        """, (vin,))
        row = cur.fetchone()
        if not row:
            return "No in-transit vehicle found with that VIN."
        vehicle_id = row[0]
        cur.execute("""
            SELECT log_id, to_lot_id FROM VehicleLocationLog
            WHERE vehicle_id = %s AND status = 'InTransit'
            ORDER BY initiated_at DESC LIMIT 1
        """, (vehicle_id,))
        log = cur.fetchone()
        if not log:
            return "No open transfer log found for this vehicle."
        log_id, to_lot_id = log
        cur.execute("""
            UPDATE Vehicle SET current_lot_id = %s, location_status = 'Available'
            WHERE vehicle_id = %s
        """, (to_lot_id, vehicle_id))
        cur.execute("""
            UPDATE VehicleLocationLog SET status = 'Arrived', arrived_at = NOW()
            WHERE log_id = %s
        """, (log_id,))
        conn.commit()
        return "Vehicle arrival confirmed."
    except Exception as e:
        if conn:
            conn.rollback()
        return f"Error: {e}"


def get_vehicle_by_vin(vin):
    try:
        conn = get_connection()
        cur = conn.cursor()
        cur.execute("""
            SELECT v.vin, v.make, v.model, v.year, v.mileage, v.color,
                   v.condition_code, l.name, v.location_status,
                   v.current_asking_price, v.date_acquired, v.sold,
                   CURRENT_DATE - v.date_acquired AS days_in_inventory
            FROM Vehicle v
            JOIN Lot l ON v.current_lot_id = l.lot_id
            WHERE v.vin = %s
        """, (vin,))
        return cur.fetchall()
    except Exception as e:
        return f"Error: {e}"


def search_vehicles_by_vin(vin):
    try:
        conn = get_connection()
        cur = conn.cursor()
        cur.execute("""
    SELECT v.vehicle_id, v.vin, v.make, v.model, v.year,
           l.name, v.location_status, v.current_asking_price,
           CURRENT_DATE - v.date_acquired AS days_in_inventory,
           v.sold
    FROM Vehicle v
    JOIN Lot l ON v.current_lot_id = l.lot_id
    WHERE v.vin = %s
""", (vin,))
        return cur.fetchall()
    except Exception as e:
        return f"Error: {e}"


def get_price_history(vin):
    try:
        conn = get_connection()
        cur = conn.cursor()
        cur.execute("""
            SELECT ph.old_price, ph.new_price,
                   s.employee_id, ph.changed_at
            FROM PriceHistory ph
            JOIN Vehicle v ON ph.vehicle_id = v.vehicle_id
            JOIN Salesperson s ON ph.changed_by = s.salesperson_id
            WHERE v.vin = %s
            ORDER BY ph.changed_at DESC
        """, (vin,))
        return cur.fetchall()
    except Exception as e:
        return f"Error: {e}"


def search_vehicles(make=None, model=None, year_min=None, year_max=None,
                    price_min=None, price_max=None, mileage_max=None, lot_id=None):
    try:
        conn = get_connection()
        cur = conn.cursor()
        filters = ["v.sold = FALSE"]
        values = []
        if make:
            filters.append("v.make ILIKE %s")
            values.append(f"%{make}%")
        if model:
            filters.append("v.model ILIKE %s")
            values.append(f"%{model}%")
        if year_min is not None:
            filters.append("v.year >= %s")
            values.append(year_min)
        if year_max is not None:
            filters.append("v.year <= %s")
            values.append(year_max)
        if price_min is not None:
            filters.append("v.current_asking_price >= %s")
            values.append(price_min)
        if price_max is not None:
            filters.append("v.current_asking_price <= %s")
            values.append(price_max)
        if mileage_max is not None:
            filters.append("v.mileage <= %s")
            values.append(mileage_max)
        if lot_id is not None:
            filters.append("v.current_lot_id = %s")
            values.append(lot_id)
        cur.execute(f"""
            SELECT v.vin, v.make, v.model, v.year, v.mileage,
                   v.current_asking_price, l.name,
                   CURRENT_DATE - v.date_acquired AS days_in_inventory
            FROM Vehicle v
            JOIN Lot l ON v.current_lot_id = l.lot_id
            WHERE {' AND '.join(filters)}
            ORDER BY v.make, v.model
        """, values)
        return cur.fetchall()
    except Exception as e:
        return f"Error: {e}"


def get_slow_moving_vehicles(days_threshold):
    try:
        conn = get_connection()
        cur = conn.cursor()
        cur.execute("""
            SELECT v.vin, v.make, v.model, v.year,
                   v.current_asking_price,
                   CURRENT_DATE - v.date_acquired AS days_in_inventory
            FROM Vehicle v
            WHERE v.sold = FALSE
              AND CURRENT_DATE - v.date_acquired > %s
            ORDER BY days_in_inventory DESC
        """, (days_threshold,))
        return cur.fetchall()
    except Exception as e:
        return f"Error: {e}"


# ─────────────────────────────────────────
# CLIENT FUNCTIONS
# Handle user input/output, call server functions
# ─────────────────────────────────────────

def add_vehicle_client():
    vin = input("Enter VIN: ").strip()
    make = input("Enter make: ").strip()
    model = input("Enter model: ").strip()
    year = input("Enter year: ").strip()
    mileage = input("Enter mileage: ").strip()
    color = input("Enter color: ").strip()
    condition_code = input("Enter condition code (Excellent/Good/Fair/Poor): ").strip()
    lot_id = input("Enter lot ID: ").strip()
    asking_price = input("Enter asking price: ").strip()
    print(add_vehicle(vin, make, model, year, mileage, color, condition_code, lot_id, asking_price))


def update_vehicle_price_client():
    vin = input("Enter VIN: ").strip()
    new_price = input("Enter new price: ").strip()
    employee_id = input("Enter salesperson employee ID: ").strip()
    print(update_vehicle_price(vin, new_price, employee_id))


def initiate_vehicle_transfer_client():
    vin = input("Enter VIN: ").strip()
    to_lot_id = input("Enter destination lot ID: ").strip()
    print(initiate_vehicle_transfer(vin, to_lot_id))


def confirm_vehicle_arrival_client():
    vin = input("Enter VIN: ").strip()
    print(confirm_vehicle_arrival(vin))


def get_vehicle_by_vin_client():
    vin = input("Enter VIN: ").strip()
    rows = get_vehicle_by_vin(vin)
    if isinstance(rows, str):
        print(rows)
    elif not rows:
        print("No vehicle found with that VIN.")
    else:
        for r in rows:
            print(f"""
VIN:          {r[0]}
Make/Model:   {r[1]} {r[2]} ({r[3]})
Mileage:      {r[4]}
Color:        {r[5]}
Condition:    {r[6]}
Lot:          {r[7]}
Status:       {r[8]}
Price:        ${r[9]}
Acquired:     {r[10]}
Sold:         {r[11]}
Days in inv:  {r[12]}
""")


def search_vehicles_by_vin_client():
    vin = input("Enter VIN: ").strip()
    rows = search_vehicles_by_vin(vin)
    if isinstance(rows, str):
        print(rows)
    elif not rows:
        print("No records found for that VIN.")
    else:
        print(f"\n{'ID':<6} {'VIN':<18} {'Make':<12} {'Model':<12} {'Year':<6} {'Lot':<15} {'Status':<12} {'Price':<12} {'Days'}")
        print("-" * 100)
        for r in rows:
            status = ("Sold+Transit" if r[6] == "InTransit" else "Sold") if r[9] else r[6]
            print(f"{r[0]:<6} {r[1]:<18} {r[2]:<12} {r[3]:<12} {r[4]:<6} {r[5]:<15} {status:<12} ${r[7]:<11} {r[8]}")


def get_price_history_client():
    vin = input("Enter VIN: ").strip()
    rows = get_price_history(vin)
    if isinstance(rows, str):
        print(rows)
    elif not rows:
        print("No price history found for that VIN.")
    else:
        print(f"\n{'Old Price':<14} {'New Price':<14} {'Changed By':<15} {'Changed At'}")
        print("-" * 60)
        for r in rows:
            print(f"${r[0]:<13} ${r[1]:<13} {r[2]:<15} {r[3]}")


def search_vehicles_client():
    print("Leave any field blank to skip that filter.")
    make = input("Make: ").strip() or None
    model = input("Model: ").strip() or None
    year_min = input("Year min: ").strip() or None
    year_max = input("Year max: ").strip() or None
    price_min = input("Price min: ").strip() or None
    price_max = input("Price max: ").strip() or None
    mileage_max = input("Mileage max: ").strip() or None
    lot_id = input("Lot ID: ").strip() or None
    rows = search_vehicles(make, model, year_min, year_max, price_min, price_max, mileage_max, lot_id)
    if isinstance(rows, str):
        print(rows)
    elif not rows:
        print("No vehicles found matching those filters.")
    else:
        print(f"\n{'VIN':<18} {'Make':<12} {'Model':<12} {'Year':<6} {'Miles':<10} {'Price':<12} {'Lot':<15} {'Days'}")
        print("-" * 100)
        for r in rows:
            print(f"{r[0]:<18} {r[1]:<12} {r[2]:<12} {r[3]:<6} {r[4]:<10} ${r[5]:<11} {r[6]:<15} {r[7]}")


def get_slow_moving_vehicles_client():
    days = input("Enter days threshold (e.g. 90): ").strip()
    try:
        days = int(days)
    except ValueError:
        print("Invalid input: please enter a whole number.")
        return
    rows = get_slow_moving_vehicles(days)
    if isinstance(rows, str):
        print(rows)
    elif not rows:
        print("No slow-moving vehicles found.")
    else:
        print(f"\n{'VIN':<18} {'Make':<12} {'Model':<12} {'Year':<6} {'Price':<12} {'Days in Inventory'}")
        print("-" * 80)
        for r in rows:
            print(f"{r[0]:<18} {r[1]:<12} {r[2]:<12} {r[3]:<6} ${r[4]:<11} {r[5]}")