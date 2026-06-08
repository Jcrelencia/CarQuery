import vehicle
import customer
import salesperson
import sales
import reports
from db import close_connection


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
            close_connection()
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
            vehicle.add_vehicle_client()
        elif choice == "2":
            vehicle.update_vehicle_price_client()
        elif choice == "3":
            vehicle.initiate_vehicle_transfer_client()
        elif choice == "4":
            vehicle.confirm_vehicle_arrival_client()
        elif choice == "5":
            vehicle.get_vehicle_by_vin_client()
        elif choice == "6":
            vehicle.search_vehicles_by_vin_client()
        elif choice == "7":
            vehicle.get_price_history_client()
        elif choice == "8":
            vehicle.search_vehicles_client()
        elif choice == "9":
            vehicle.get_slow_moving_vehicles_client()
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
            customer.add_customer_client()
        elif choice == "2":
            customer.update_customer_client()
        elif choice == "3":
            customer.get_customer_history_client()
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
            salesperson.add_salesperson_client()
        elif choice == "2":
            salesperson.update_salesperson_client()
        elif choice == "3":
            salesperson.list_all_salespersons_client()
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
            sales.sell_vehicle_no_trade_in_client()
        elif choice == "2":
            sales.sell_vehicle_with_trade_in_client()
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
            reports.get_inventory_report_by_lot_client()
        elif choice == "2":
            reports.get_sales_report_client()
        elif choice == "3":
            reports.list_all_lots_client()
        elif choice == "4":
            reports.list_all_conditions_client()
        elif choice == "5":
            salesperson.list_all_salespersons_client()
        elif choice == "0":
            break
        else:
            print("Invalid option, try again.")


if __name__ == "__main__":
    main()