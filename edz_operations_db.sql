DROP DATABASE IF EXISTS edz_operations_db;

-- 1. Create the Schema
CREATE DATABASE IF NOT EXISTS edz_operations_db;
USE edz_operations_db;

-- 2. Create Dimensions (The "1" side of relationships)
CREATE TABLE dim_staff (
    staff_id INT PRIMARY KEY,
    staff_name VARCHAR(255) NOT NULL,
    role VARCHAR(50), -- Reader, Collector, Technician
    phone_number VARCHAR(20),
    active_status BOOLEAN DEFAULT TRUE
);

CREATE TABLE dim_geography (
    neighborhood_id INT PRIMARY KEY,
    neighborhood_name VARCHAR(255) NOT NULL,
    center_lat DECIMAL(9,6),
    center_long DECIMAL(9,6),
    assigned_collector_id INT,
    FOREIGN KEY (assigned_collector_id) REFERENCES dim_staff(staff_id)
);

CREATE TABLE dim_customer (
    customer_id INT PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    phone VARCHAR(20),
    max_amperage INT,
    fixed_fee_usd DECIMAL(10,2),
    phase_type INT, -- 1 or 3
    connection_type VARCHAR(50),
    neighborhood_id INT,
    customer_lat DECIMAL(9,6),
    customer_long DECIMAL(9,6),
    contract_date DATETIME,
    is_active BOOLEAN DEFAULT TRUE,
    FOREIGN KEY (neighborhood_id) REFERENCES dim_geography(neighborhood_id)
);

CREATE TABLE dim_expenses (
    expense_id INT PRIMARY KEY,
    category VARCHAR(100), -- Diesel, Maintenance, Salary
    amount_usd DECIMAL(15,2),
    date DATETIME,
    staff_id INT, -- To see ROI of staff
    neighborhood_id INT, -- To see cost per zone
    FOREIGN KEY (staff_id) REFERENCES dim_staff(staff_id),
    FOREIGN KEY (neighborhood_id) REFERENCES dim_geography(neighborhood_id)
);

-- 3. Create Fact Tables (The "Many" side)
CREATE TABLE fact_readings (
    reading_id INT PRIMARY KEY,
    meter_id INT,
    customer_id INT,
    reader_id INT,
    kwh_value DECIMAL(10,2),
    captured_lat DECIMAL(9,6),
    captured_long DECIMAL(9,6),
    is_estimated BOOLEAN,
    timestamp DATETIME,
    FOREIGN KEY (customer_id) REFERENCES dim_customer(customer_id),
    FOREIGN KEY (reader_id) REFERENCES dim_staff(staff_id)
);

CREATE TABLE fact_billing (
    bill_id INT PRIMARY KEY,
    reading_id INT,
    customer_id INT, -- Your "Senior" choice for faster Power BI filtering
    fixed_charge_amount DECIMAL(15,2),
    consumption_charge_amount DECIMAL(15,2),
    amount_lbp DECIMAL(15,2),
    amount_usd DECIMAL(15,2),
    issue_date DATETIME,
    due_date DATETIME,
    status VARCHAR(20), -- Paid, Unpaid, Partial
    FOREIGN KEY (reading_id) REFERENCES fact_readings(reading_id),
    FOREIGN KEY (customer_id) REFERENCES dim_customer(customer_id)
);

CREATE TABLE fact_collection (
    collection_id INT PRIMARY KEY,
    bill_id INT,
    collector_id INT,
    amount_paid DECIMAL(15,2),
    collection_date DATETIME,
    payment_method VARCHAR(50), -- Cash, OMT, Bank
    FOREIGN KEY (bill_id) REFERENCES fact_billing(bill_id),
    FOREIGN KEY (collector_id) REFERENCES dim_staff(staff_id)
);