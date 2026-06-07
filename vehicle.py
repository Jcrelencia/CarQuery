# vehicle.py

from db import get_connection

# ─────────────────────────────────────────
# TEMPLATE — copy this pattern for every function
# ─────────────────────────────────────────

def AddVehicle():
    # 1. Collect inputs from the user
    vin   = input("Enter VIN: ").strip()
    make  = input("Enter make: ").strip()
    model = input("Enter model: ").strip()
    year  = input("Enter year: ").strip()
    mileage = input("Enter mileage: ").strip()
    color   = input("Enter color: ").strip()
    condition_code = input("Enter condition code (Excellent/Good/Fair/Poor): ").strip()
    lot_id  = input("Enter lot ID: ").strip()
    asking_price = input("Enter asking price: ").strip()

    # 2. Connect and run the query
    try:
        conn = get_connection()
        cur  = conn.cursor()

        cur.execute("""
            INSERT INTO Vehicle
                (vin, make, model, year, mileage, color,
                 condition_code, current_lot_id, current_asking_price, date_acquired)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, CURRENT_DATE)
        """, (vin, make, model, year, mileage, color,
              condition_code, lot_id, asking_price))

        conn.commit()
        print("Vehicle added successfully.")

    # 3. Handle errors
    except Exception as e:
        print(f"Error: {e}")

    # 4. Always close the connection
    finally:
        cur.close()
        conn.close()


def GetVehicleByVIN():
    vin = input("Enter VIN: ").strip()

    try:
        conn = get_connection()
        cur  = conn.cursor()

        cur.execute("""
            SELECT v.vin, v.make, v.model, v.year, v.mileage,
                   v.color, v.condition_code, l.name AS lot,
                   v.location_status, v.current_asking_price,
                   v.date_acquired, v.sold
            FROM Vehicle v
            JOIN Lot l ON v.current_lot_id = l.lot_id
            WHERE v.vin = %s
        """, (vin,))

        rows = cur.fetchall()

        if not rows:
            print("No vehicle found with that VIN.")
        else:
            for row in rows:
                print(f"""
VIN:        {row[0]}
Make/Model: {row[1]} {row[2]} ({row[3]})
Mileage:    {row[4]}
Color:      {row[5]}
Condition:  {row[6]}
Lot:        {row[7]}
Status:     {row[8]}
Price:      ${row[9]}
Acquired:   {row[10]}
Sold:       {row[11]}
                """)

    except Exception as e:
        print(f"Error: {e}")

    finally:
        if cur:
            cur.close()
        if conn:
            conn.close()


def UpdateVehiclePrice():
    vin = input("Enter VIN: ").strip()
    new_price = input("Enter new asking price: ").strip()
    employee_id = input("Enter salesperson employee ID: ").strip()

    conn = None
    cur = None
    try:
        conn = get_connection()
        cur = conn.cursor()

        cur.execute("""
            SELECT vehicle_id, current_asking_price
            FROM Vehicle
            WHERE vin = %s AND sold = FALSE
            ORDER BY date_acquired DESC
            LIMIT 1
        """, (vin,))
        vehicle = cur.fetchone()

        if not vehicle:
            print("No active vehicle found with that VIN.")
            return

        vehicle_id, old_price = vehicle

        cur.execute("""
            SELECT salesperson_id
            FROM Salesperson
            WHERE employee_id = %s
        """, (employee_id,))
        salesperson = cur.fetchone()

        if not salesperson:
            print("No salesperson found with that employee ID.")
            return

        salesperson_id = salesperson[0]

        cur.execute("""
            UPDATE Vehicle
            SET current_asking_price = %s
            WHERE vehicle_id = %s
        """, (new_price, vehicle_id))

        cur.execute("""
            INSERT INTO PriceHistory
                (vehicle_id, old_price, new_price, changed_by, changed_at)
            VALUES (%s, %s, %s, %s, NOW())
        """, (vehicle_id, old_price, new_price, salesperson_id))

        conn.commit()
        print("Vehicle price updated and price history recorded.")

    except Exception as e:
        print(f"Error: {e}")

    finally:
        if cur:
            cur.close()
        if conn:
            conn.close()


def InitiateVehicleTransfer():
    vin = input("Enter VIN: ").strip()
    to_lot_id = input("Enter destination lot ID: ").strip()
    employee_id = input("Enter salesperson employee ID: ").strip()

    conn = None
    cur = None
    try:
        conn = get_connection()
        cur = conn.cursor()

        cur.execute("""
            SELECT vehicle_id, current_lot_id, location_status, sold
            FROM Vehicle
            WHERE vin = %s AND sold = FALSE
            ORDER BY date_acquired DESC
            LIMIT 1
        """, (vin,))
        vehicle = cur.fetchone()

        if not vehicle:
            print("No active vehicle found with that VIN.")
            return

        vehicle_id, from_lot_id, location_status, sold = vehicle
        if location_status == 'InTransit':
            print("This vehicle is already in transit.")
            return

        cur.execute("""
            SELECT salesperson_id
            FROM Salesperson
            WHERE employee_id = %s
        """, (employee_id,))
        salesperson = cur.fetchone()

        if not salesperson:
            print("No salesperson found with that employee ID.")
            return

        cur.execute("""
            UPDATE Vehicle
            SET location_status = 'InTransit'
            WHERE vehicle_id = %s
        """, (vehicle_id,))

        cur.execute("""
            INSERT INTO VehicleLocationLog
                (vehicle_id, from_lot_id, to_lot_id, status, initiated_at)
            VALUES (%s, %s, %s, 'InTransit', NOW())
        """, (vehicle_id, from_lot_id, to_lot_id))

        conn.commit()
        print("Vehicle transfer initiated.")

    except Exception as e:
        print(f"Error: {e}")

    finally:
        if cur:
            cur.close()
        if conn:
            conn.close()


def ConfirmVehicleArrival():
    vin = input("Enter VIN: ").strip()
    employee_id = input("Enter salesperson employee ID: ").strip()

    conn = None
    cur = None
    try:
        conn = get_connection()
        cur = conn.cursor()

        cur.execute("""
            SELECT vehicle_id, location_status
            FROM Vehicle
            WHERE vin = %s AND sold = FALSE
            ORDER BY date_acquired DESC
            LIMIT 1
        """, (vin,))
        vehicle = cur.fetchone()

        if not vehicle:
            print("No active vehicle found with that VIN.")
            return

        vehicle_id, location_status = vehicle
        if location_status != 'InTransit':
            print("This vehicle is not currently in transit.")
            return

        cur.execute("""
            SELECT log_id, to_lot_id
            FROM VehicleLocationLog
            WHERE vehicle_id = %s AND arrived_at IS NULL AND status = 'InTransit'
            ORDER BY initiated_at DESC
            LIMIT 1
        """, (vehicle_id,))
        log_entry = cur.fetchone()

        if not log_entry:
            print("No open transfer log found for this vehicle.")
            return

        log_id, to_lot_id = log_entry

        cur.execute("""
            UPDATE VehicleLocationLog
            SET arrived_at = NOW(), status = 'Arrived'
            WHERE log_id = %s
        """, (log_id,))

        cur.execute("""
            UPDATE Vehicle
            SET current_lot_id = %s,
                location_status = 'Available'
            WHERE vehicle_id = %s
        """, (to_lot_id, vehicle_id))

        conn.commit()
        print("Vehicle arrival confirmed and inventory updated.")

    except Exception as e:
        print(f"Error: {e}")

    finally:
        if cur:
            cur.close()
        if conn:
            conn.close()


def SearchVehiclesByVIN():
    vin = input("Enter VIN: ").strip()

    conn = None
    cur = None
    try:
        conn = get_connection()
        cur = conn.cursor()

        cur.execute("""
            SELECT v.vehicle_id, v.vin, v.make, v.model, v.year, v.mileage,
                   l.name AS lot, v.location_status, v.current_asking_price,
                   CURRENT_DATE - v.date_acquired AS days_in_inventory
            FROM Vehicle v
                LEFT JOIN Lot l ON v.current_lot_id = l.lot_id
            WHERE v.vin = %s
            ORDER BY v.date_acquired DESC
        """, (vin,))

        rows = cur.fetchall()
        if not rows:
            print("No vehicles found with that VIN.")
            return

        for row in rows:
            print(f"\nVehicle ID: {row[0]}")
            print(f"VIN: {row[1]}")
            print(f"Make/Model: {row[2]} {row[3]} ({row[4]})")
            print(f"Mileage: {row[5]}")
            print(f"Lot: {row[6]}")
            print(f"Status: {row[7]}")
            print(f"Asking Price: ${row[8]}")
            print(f"Days in Inventory: {row[9]}")

    except Exception as e:
        print(f"Error: {e}")

    finally:
        if cur:
            cur.close()
        if conn:
            conn.close()


def GetPriceHistory():
    vin = input("Enter VIN: ").strip()

    conn = None
    cur = None
    try:
        conn = get_connection()
        cur = conn.cursor()

        # First, verify the vehicle exists
        cur.execute("""
            SELECT vehicle_id FROM Vehicle WHERE vin = %s
        """, (vin,))
        vehicle = cur.fetchone()
        
        if not vehicle:
            print(f"No vehicle found with VIN: {vin}")
            return

        # Now fetch price history
        cur.execute("""
            SELECT ph.old_price, ph.new_price,
                   s.employee_id, s.first_name, s.last_name,
                   ph.changed_at
            FROM PriceHistory ph
                JOIN Vehicle v ON ph.vehicle_id = v.vehicle_id
                LEFT JOIN Salesperson s ON ph.changed_by = s.salesperson_id
            WHERE v.vin = %s
            ORDER BY ph.changed_at DESC
        """, (vin,))

        rows = cur.fetchall()
        if not rows:
            print(f"Vehicle found but has no price history yet. (No price updates have been recorded)")
            return

        for row in rows:
            changed_by = row[2] if row[2] else 'Unknown'
            if row[3] and row[4]:
                changed_by = f"{row[2]} ({row[3]} {row[4]})"
            print(f"\nOld Price: ${row[0]}")
            print(f"New Price: ${row[1]}")
            print(f"Changed By: {changed_by}")
            print(f"Changed At: {row[5]}")

    except Exception as e:
        print(f"Error: {e}")

    finally:
        if cur:
            cur.close()
        if conn:
            conn.close()


def SearchVehicles():
    make = input("Enter make (optional): ").strip()
    model = input("Enter model (optional): ").strip()
    year_min = input("Enter minimum year (optional): ").strip()
    year_max = input("Enter maximum year (optional): ").strip()
    price_min = input("Enter minimum price (optional): ").strip()
    price_max = input("Enter maximum price (optional): ").strip()
    mileage_max = input("Enter maximum mileage (optional): ").strip()
    lot_id = input("Enter lot ID (optional): ").strip()

    filters = ["v.sold = FALSE"]
    params = []

    if make:
        filters.append("v.make ILIKE %s")
        params.append(f"%{make}%")
    if model:
        filters.append("v.model ILIKE %s")
        params.append(f"%{model}%")
    if year_min:
        filters.append("v.year >= %s")
        params.append(year_min)
    if year_max:
        filters.append("v.year <= %s")
        params.append(year_max)
    if price_min:
        filters.append("v.current_asking_price >= %s")
        params.append(price_min)
    if price_max:
        filters.append("v.current_asking_price <= %s")
        params.append(price_max)
    if mileage_max:
        filters.append("v.mileage <= %s")
        params.append(mileage_max)
    if lot_id:
        filters.append("v.current_lot_id = %s")
        params.append(lot_id)

    if len(filters) == 1:
        print("At least one search filter must be provided.")
        return

    query = f"""
        SELECT v.vin, v.make, v.model, v.year, v.mileage,
               l.name AS lot, v.location_status, v.current_asking_price,
               CURRENT_DATE - v.date_acquired AS days_in_inventory
        FROM Vehicle v
            LEFT JOIN Lot l ON v.current_lot_id = l.lot_id
        WHERE {' AND '.join(filters)}
        ORDER BY v.date_acquired DESC
    """

    conn = None
    cur = None
    try:
        conn = get_connection()
        cur = conn.cursor()
        cur.execute(query, tuple(params))

        rows = cur.fetchall()
        if not rows:
            print("No vehicles matched the search criteria.")
            return

        for row in rows:
            print(f"\nVIN: {row[0]}")
            print(f"Make/Model: {row[1]} {row[2]} ({row[3]})")
            print(f"Mileage: {row[4]}")
            print(f"Lot: {row[5]}")
            print(f"Status: {row[6]}")
            print(f"Asking Price: ${row[7]}")
            print(f"Days in Inventory: {row[8]}")

    except Exception as e:
        print(f"Error: {e}")

    finally:
        if cur:
            cur.close()
        if conn:
            conn.close()


def GetSlowMovingVehicles():
    days_threshold = input("Enter days threshold: ").strip()

    conn = None
    cur = None
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

        rows = cur.fetchall()
        if not rows:
            print("No slow-moving vehicles found for that threshold.")
            return

        for row in rows:
            print(f"\nVIN: {row[0]}")
            print(f"Make/Model: {row[1]} {row[2]} ({row[3]})")
            print(f"Asking Price: ${row[4]}")
            print(f"Days in Inventory: {row[5]}")

    except Exception as e:
        print(f"Error: {e}")

    finally:
        if cur:
            cur.close()
        if conn:
            conn.close()

# Backwards-compatible snake_case aliases (point to PascalCase implementations)
add_vehicle = AddVehicle
get_vehicle_by_vin = GetVehicleByVIN
update_vehicle_price = UpdateVehiclePrice
initiate_vehicle_transfer = InitiateVehicleTransfer
confirm_vehicle_arrival = ConfirmVehicleArrival
search_vehicles_by_vin = SearchVehiclesByVIN
get_price_history = GetPriceHistory
search_vehicles = SearchVehicles
get_slow_moving_vehicles = GetSlowMovingVehicles


#The four rules every function must follow:

#Always use %s for query parameters — never put variables directly in the SQL string. So WHERE vin = %s with (vin,) at the end — not WHERE vin = '{vin}'. This prevents SQL injection and crashes.
#Always conn.commit() after INSERT/UPDATE/DELETE — without this the change won't actually save to the database.
#Always wrap in try/except/finally — so if something goes wrong it prints a clean error instead of crashing the whole program.
#Always close cur and conn in the finally block — so database connections don't pile up.
