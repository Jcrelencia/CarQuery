-- Lot (domain table)
CREATE TABLE Lot (
    lot_id   SERIAL PRIMARY KEY,
    name     VARCHAR(100) NOT NULL,
    address  VARCHAR(200),
    city     VARCHAR(100),
    state    CHAR(2)
);

-- Condition (domain table)
CREATE TABLE Condition (
    condition_code  VARCHAR(10) PRIMARY KEY,
    description     VARCHAR(200)
);

-- Customer
CREATE TABLE Customer (
    customer_id  SERIAL PRIMARY KEY,
    first_name   VARCHAR(50),
    last_name    VARCHAR(50),
    email        VARCHAR(100) UNIQUE NOT NULL,
    phone        VARCHAR(20),
    address      VARCHAR(200)
);

-- Salesperson  
CREATE TABLE Salesperson (
    salesperson_id  SERIAL PRIMARY KEY,
    employee_id     VARCHAR(20)  NOT NULL UNIQUE,
    first_name      VARCHAR(50),
    last_name       VARCHAR(50),
    lot_id          INT          REFERENCES Lot(lot_id),
    hire_date       DATE
);

-- Vehicle
CREATE TABLE Vehicle (
    vehicle_id           SERIAL PRIMARY KEY,
    vin                  CHAR(17)       NOT NULL,
    make                 VARCHAR(50)    NOT NULL,
    model                VARCHAR(50)    NOT NULL,
    year                 SMALLINT       NOT NULL,
    mileage              INT,
    color                VARCHAR(30),
    condition_code       VARCHAR(10)    REFERENCES Condition(condition_code),
    current_lot_id       INT            REFERENCES Lot(lot_id),
    location_status      VARCHAR(20)    DEFAULT 'Available',
    current_asking_price DECIMAL(10,2),
    date_acquired        DATE,
    sold                 BOOLEAN        DEFAULT FALSE
);

-- PriceHistory
CREATE TABLE PriceHistory (
    price_history_id  SERIAL PRIMARY KEY,
    vehicle_id        INT            NOT NULL REFERENCES Vehicle(vehicle_id),
    old_price         DECIMAL(10,2),
    new_price         DECIMAL(10,2),
    changed_by        INT            REFERENCES Salesperson(salesperson_id),
    changed_at        TIMESTAMP      DEFAULT NOW()
);

-- VehicleLocationLog
CREATE TABLE VehicleLocationLog (
    log_id        SERIAL PRIMARY KEY,
    vehicle_id    INT         NOT NULL REFERENCES Vehicle(vehicle_id),
    from_lot_id   INT         REFERENCES Lot(lot_id),
    to_lot_id     INT         REFERENCES Lot(lot_id),
    status        VARCHAR(20),
    initiated_at  TIMESTAMP   DEFAULT NOW(),
    arrived_at    TIMESTAMP
);

-- Sale
CREATE TABLE Sale (
    sale_id             SERIAL PRIMARY KEY,
    vehicle_id          INT            NOT NULL REFERENCES Vehicle(vehicle_id),
    customer_email      VARCHAR(100)   REFERENCES Customer(email),
    employee_id         VARCHAR(20)    REFERENCES Salesperson(employee_id),
    sale_price          DECIMAL(10,2),
    trade_in_vehicle_id INT            REFERENCES Vehicle(vehicle_id),
    trade_in_value      DECIMAL(10,2),
    sale_date           DATE
);