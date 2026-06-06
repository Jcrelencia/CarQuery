import psycopg2
from db import get_connection

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
        if choice == "0":
            break
        else:
            print("(Not implemented yet)")

def customer_menu():
    while True:
        print("\n--- Customer Management ---")
        print("1. Add Customer")
        print("2. Update Customer")
        print("3. Get Customer History")
        print("0. Back")
        choice = input("Select an option: ").strip()
        if choice == "0":
            break
        else:
            print("(Not implemented yet)")

def salesperson_menu():
    while True:
        print("\n--- Salesperson Management ---")
        print("1. Add Salesperson")
        print("2. Update Salesperson")
        print("3. List All Salespersons")
        print("0. Back")
        choice = input("Select an option: ").strip()
        if choice == "0":
            break
        else:
            print("(Not implemented yet)")

def sales_menu():
    while True:
        print("\n--- Sales Transactions ---")
        print("1. Sell Vehicle (No Trade-In)")
        print("2. Sell Vehicle (With Trade-In)")
        print("0. Back")
        choice = input("Select an option: ").strip()
        if choice == "0":
            break
        else:
            print("(Not implemented yet)")

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
        if choice == "0":
            break
        else:
            print("(Not implemented yet)")

if __name__ == "__main__":
    main()