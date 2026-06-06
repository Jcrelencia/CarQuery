-- Condition codes
INSERT INTO Condition (condition_code, description) VALUES
    ('Excellent', 'Like new, no visible wear'),
    ('Good',      'Minor wear, fully functional'),
    ('Fair',      'Noticeable wear, mechanically sound'),
    ('Poor',      'Significant wear or mechanical issues');

-- Lots
INSERT INTO Lot (name, address, city, state) VALUES
    ('North Lot',  '100 Main St',   'Albany',   'NY'),
    ('South Lot',  '200 Elm St',    'Buffalo',  'NY'),
    ('East Lot',   '300 Oak Ave',   'Syracuse', 'NY');

-- Salespersons
INSERT INTO Salesperson (employee_id, first_name, last_name, lot_id, hire_date) VALUES
    ('EMP001', 'Jack',   'Smith',   1, '2023-01-15'),
    ('EMP002', 'Joshua', 'Lee',     2, '2023-03-20'),
    ('EMP003', 'Omar',   'Hassan',  1, '2022-11-01'),
    ('EMP004', 'Aqdas',  'Khan',    3, '2023-06-10');

-- Vehicles
INSERT INTO Vehicle (vin, make, model, year, mileage, color, condition_code, current_lot_id, current_asking_price, date_acquired) VALUES
    ('1HGBH41JXMN109186', 'Honda',  'Civic',   2019, 45000, 'Blue',  'Good',      1, 14999.00, '2024-01-10'),
    ('2T1BURHE0JC043821', 'Toyota', 'Corolla', 2020, 30000, 'White', 'Excellent', 2, 18500.00, '2024-02-05'),
    ('3VWFE21C04M000001', 'VW',     'Jetta',   2018, 62000, 'Black', 'Fair',      1, 11200.00, '2024-03-01');

-- Customers
INSERT INTO Customer (first_name, last_name, email, phone) VALUES
    ('Alice', 'Johnson', 'alice@email.com', '555-1001'),
    ('Bob',   'Martinez','bob@email.com',   '555-1002');