from db import get_connection

# Uncomment these as teammates finish their files
# import vehicle
# import customer
# import salesperson
# import sales
# import reports

def main():
    while True:
        print("\n========== CarQuery ==========")
        print("1. Vehicle Management")
        print("2. Customer Management")
        print("3. Salesperson Management")
        print("4. Sales Transactions")
        print("5. Reports")
        print("0. Exit")
        choice = input("Select an option: ").strip()

        if choice == "1":
            vehicle_menu()
        elif choice == "2":
            customer_menu()
        elif choice == "3":
            salesperson_menu()
        elif choice == "4":
            sales_menu()
        elif choice == "5":
            reports_menu()
        elif choice == "0":
            print("Goodbye!")
            break
        else:
            print("Invalid option, try again.")


def vehicle_menu():
    while True:
        print("\n--- Vehicle Management ---")
        print("1.  Add Vehicle")
        print("2.  Update Vehicle Price")
        print("3.  Initiate Vehicle Transfer")
        print("4.  Confirm Vehicle Arrival")
        print("5.  Get Vehicle by VIN")
        print("6.  Search Vehicles by VIN")
        print("7.  Get Price History")
        print("8.  Search Vehicles")
        print("9.  Get Slow Moving Vehicles")
        print("0.  Back")
        choice = input("Select an option: ").strip()

        if choice == "1":
            pass  # replace with: vehicle.add_vehicle()
        elif choice == "2":
            pass  # replace with: vehicle.update_vehicle_price()
        elif choice == "3":
            pass  # replace with: vehicle.initiate_vehicle_transfer()
        elif choice == "4":
            pass  # replace with: vehicle.confirm_vehicle_arrival()
        elif choice == "5":
            pass  # replace with: vehicle.get_vehicle_by_vin()
        elif choice == "6":
            pass  # replace with: vehicle.search_vehicles_by_vin()
        elif choice == "7":
            pass  # replace with: vehicle.get_price_history()
        elif choice == "8":
            pass  # replace with: vehicle.search_vehicles()
        elif choice == "9":
            pass  # replace with: vehicle.get_slow_moving_vehicles()
        elif choice == "0":
            break
        else:
            print("Invalid option, try again.")


def customer_menu():
    while True:
        print("\n--- Customer Management ---")
        print("1. Add Customer")
        print("2. Update Customer")
        print("3. Get Customer History")
        print("0. Back")
        choice = input("Select an option: ").strip()

        if choice == "1":
            pass  # replace with: customer.add_customer()
        elif choice == "2":
            pass  # replace with: customer.update_customer()
        elif choice == "3":
            pass  # replace with: customer.get_customer_history()
        elif choice == "0":
            break
        else:
            print("Invalid option, try again.")


def salesperson_menu():
    while True:
        print("\n--- Salesperson Management ---")
        print("1. Add Salesperson")
        print("2. Update Salesperson")
        print("3. List All Salespersons")
        print("0. Back")
        choice = input("Select an option: ").strip()

        if choice == "1":
            pass  # replace with: salesperson.add_salesperson()
        elif choice == "2":
            pass  # replace with: salesperson.update_salesperson()
        elif choice == "3":
            pass  # replace with: salesperson.list_all_salespersons()
        elif choice == "0":
            break
        else:
            print("Invalid option, try again.")


def sales_menu():
    while True:
        print("\n--- Sales Transactions ---")
        print("1. Sell Vehicle (No Trade-In)")
        print("2. Sell Vehicle (With Trade-In)")
        print("0. Back")
        choice = input("Select an option: ").strip()

        if choice == "1":
            pass  # replace with: sales.sell_vehicle_no_trade_in()
        elif choice == "2":
            pass  # replace with: sales.sell_vehicle_with_trade_in()
        elif choice == "0":
            break
        else:
            print("Invalid option, try again.")


def reports_menu():
    while True:
        print("\n--- Reports ---")
        print("1. Inventory Report by Lot")
        print("2. Sales Report")
        print("3. List All Lots")
        print("4. List All Conditions")
        print("5. List All Salespersons")
        print("0. Back")
        choice = input("Select an option: ").strip()

        if choice == "1":
            pass  # replace with: reports.get_inventory_report_by_lot()
        elif choice == "2":
            pass  # replace with: reports.get_sales_report()
        elif choice == "3":
            pass  # replace with: reports.list_all_lots()
        elif choice == "4":
            pass  # replace with: reports.list_all_conditions()
        elif choice == "5":
            pass  # replace with: reports.list_all_salespersons()
        elif choice == "0":
            break
        else:
            print("Invalid option, try again.")


if __name__ == "__main__":
    main()
