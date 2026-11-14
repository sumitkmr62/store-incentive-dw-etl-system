/*
 Synthetic OLTP source database for portfolio project.
 SQL Server 2022. All records are fictional.
 Run in SSMS using an account permitted to create databases.
*/
USE master;
GO
IF DB_ID(N'StoreIncentiveOLTP') IS NULL
    CREATE DATABASE StoreIncentiveOLTP;
GO
USE StoreIncentiveOLTP;
GO

IF SCHEMA_ID(N'retail') IS NULL EXEC(N'CREATE SCHEMA retail');
IF SCHEMA_ID(N'hr') IS NULL EXEC(N'CREATE SCHEMA hr');
IF SCHEMA_ID(N'clinical') IS NULL EXEC(N'CREATE SCHEMA clinical');
IF SCHEMA_ID(N'ops') IS NULL EXEC(N'CREATE SCHEMA ops');
GO

CREATE TABLE retail.Store (
    store_id INT NOT NULL CONSTRAINT PK_Store PRIMARY KEY,
    store_code VARCHAR(20) NOT NULL CONSTRAINT UQ_Store_Code UNIQUE,
    store_name NVARCHAR(120) NOT NULL,
    city NVARCHAR(60) NOT NULL,
    state NVARCHAR(60) NOT NULL,
    region NVARCHAR(40) NOT NULL,
    opening_date DATE NOT NULL,
    store_status VARCHAR(20) NOT NULL
);
CREATE TABLE hr.Employee (
    employee_id INT NOT NULL CONSTRAINT PK_Employee PRIMARY KEY,
    employee_code VARCHAR(20) NOT NULL CONSTRAINT UQ_Employee_Code UNIQUE,
    first_name NVARCHAR(60) NOT NULL,
    last_name NVARCHAR(60) NOT NULL,
    store_id INT NOT NULL,
    manager_employee_id INT NULL,
    job_role NVARCHAR(60) NOT NULL,
    employment_type VARCHAR(30) NOT NULL,
    hire_date DATE NOT NULL,
    employment_status VARCHAR(20) NOT NULL,
    CONSTRAINT FK_Employee_Store FOREIGN KEY (store_id) REFERENCES retail.Store(store_id),
    CONSTRAINT FK_Employee_Manager FOREIGN KEY (manager_employee_id) REFERENCES hr.Employee(employee_id)
);
CREATE TABLE retail.Customer (
    customer_id INT NOT NULL CONSTRAINT PK_Customer PRIMARY KEY,
    customer_code VARCHAR(20) NOT NULL CONSTRAINT UQ_Customer_Code UNIQUE,
    first_name NVARCHAR(60) NOT NULL,
    last_name NVARCHAR(60) NOT NULL,
    city NVARCHAR(60) NOT NULL,
    state NVARCHAR(60) NOT NULL,
    created_at DATETIME2(0) NOT NULL,
    customer_segment VARCHAR(20) NOT NULL
);
CREATE TABLE retail.Product (
    product_id INT NOT NULL CONSTRAINT PK_Product PRIMARY KEY,
    sku VARCHAR(20) NOT NULL CONSTRAINT UQ_Product_SKU UNIQUE,
    product_name NVARCHAR(120) NOT NULL,
    category NVARCHAR(60) NOT NULL,
    brand NVARCHAR(60) NOT NULL,
    list_price DECIMAL(12,2) NOT NULL,
    is_active BIT NOT NULL
);
CREATE TABLE retail.SalesOrder (
    order_id INT NOT NULL CONSTRAINT PK_SalesOrder PRIMARY KEY,
    order_number VARCHAR(30) NOT NULL CONSTRAINT UQ_SalesOrder_Number UNIQUE,
    order_datetime DATETIME2(0) NOT NULL,
    store_id INT NOT NULL,
    customer_id INT NOT NULL,
    sales_employee_id INT NOT NULL,
    order_status VARCHAR(20) NOT NULL,
    channel VARCHAR(20) NOT NULL,
    CONSTRAINT FK_SalesOrder_Store FOREIGN KEY (store_id) REFERENCES retail.Store(store_id),
    CONSTRAINT FK_SalesOrder_Customer FOREIGN KEY (customer_id) REFERENCES retail.Customer(customer_id),
    CONSTRAINT FK_SalesOrder_Employee FOREIGN KEY (sales_employee_id) REFERENCES hr.Employee(employee_id)
);
CREATE TABLE retail.SalesOrderItem (
    order_line_id BIGINT NOT NULL CONSTRAINT PK_SalesOrderItem PRIMARY KEY,
    order_id INT NOT NULL,
    product_id INT NOT NULL,
    quantity SMALLINT NOT NULL,
    unit_price DECIMAL(12,2) NOT NULL,
    discount_amount DECIMAL(12,2) NOT NULL,
    net_line_amount DECIMAL(12,2) NOT NULL,
    CONSTRAINT FK_OrderItem_Order FOREIGN KEY (order_id) REFERENCES retail.SalesOrder(order_id),
    CONSTRAINT FK_OrderItem_Product FOREIGN KEY (product_id) REFERENCES retail.Product(product_id)
);
CREATE TABLE retail.Payment (
    payment_id INT NOT NULL CONSTRAINT PK_Payment PRIMARY KEY,
    order_id INT NOT NULL,
    payment_datetime DATETIME2(0) NOT NULL,
    payment_method VARCHAR(20) NOT NULL,
    payment_amount DECIMAL(14,2) NOT NULL,
    payment_status VARCHAR(20) NOT NULL,
    CONSTRAINT FK_Payment_Order FOREIGN KEY (order_id) REFERENCES retail.SalesOrder(order_id)
);
CREATE TABLE retail.ReturnTxn (
    return_id INT NOT NULL CONSTRAINT PK_ReturnTxn PRIMARY KEY,
    order_line_id BIGINT NOT NULL,
    return_datetime DATETIME2(0) NOT NULL,
    return_quantity SMALLINT NOT NULL,
    return_amount DECIMAL(12,2) NOT NULL,
    return_status VARCHAR(20) NOT NULL,
    CONSTRAINT FK_Return_OrderItem FOREIGN KEY (order_line_id) REFERENCES retail.SalesOrderItem(order_line_id)
);
CREATE TABLE hr.Attendance (
    attendance_id BIGINT NOT NULL CONSTRAINT PK_Attendance PRIMARY KEY,
    employee_id INT NOT NULL,
    attendance_date DATE NOT NULL,
    attendance_status VARCHAR(20) NOT NULL,
    scheduled_minutes SMALLINT NOT NULL,
    worked_minutes SMALLINT NOT NULL,
    source_system VARCHAR(40) NOT NULL,
    CONSTRAINT FK_Attendance_Employee FOREIGN KEY (employee_id) REFERENCES hr.Employee(employee_id)
);
CREATE TABLE clinical.EyeTest (
    eye_test_id INT NOT NULL CONSTRAINT PK_EyeTest PRIMARY KEY,
    customer_id INT NOT NULL,
    store_id INT NOT NULL,
    optometrist_employee_id INT NOT NULL,
    completed_at DATETIME2(0) NOT NULL,
    eye_test_status VARCHAR(20) NOT NULL,
    quality_score DECIMAL(5,2) NOT NULL,
    sop_compliant BIT NOT NULL,
    CONSTRAINT FK_EyeTest_Customer FOREIGN KEY (customer_id) REFERENCES retail.Customer(customer_id),
    CONSTRAINT FK_EyeTest_Store FOREIGN KEY (store_id) REFERENCES retail.Store(store_id),
    CONSTRAINT FK_EyeTest_Optometrist FOREIGN KEY (optometrist_employee_id) REFERENCES hr.Employee(employee_id)
);
CREATE TABLE ops.EmployeeMonthlyTarget (
    target_id INT NOT NULL CONSTRAINT PK_EmployeeMonthlyTarget PRIMARY KEY,
    employee_id INT NOT NULL,
    target_month DATE NOT NULL,
    sales_target DECIMAL(14,2) NOT NULL,
    eye_test_target INT NOT NULL,
    target_version SMALLINT NOT NULL,
    approval_status VARCHAR(20) NOT NULL,
    CONSTRAINT FK_Target_Employee FOREIGN KEY (employee_id) REFERENCES hr.Employee(employee_id),
    CONSTRAINT UQ_Target_EmployeeMonthVersion UNIQUE (employee_id,target_month,target_version)
);
CREATE TABLE ops.QualityAudit (
    audit_id INT NOT NULL CONSTRAINT PK_QualityAudit PRIMARY KEY,
    employee_id INT NOT NULL,
    store_id INT NOT NULL,
    audit_datetime DATETIME2(0) NOT NULL,
    audit_type VARCHAR(40) NOT NULL,
    score DECIMAL(5,2) NOT NULL,
    audit_status VARCHAR(20) NOT NULL,
    CONSTRAINT FK_Audit_Employee FOREIGN KEY (employee_id) REFERENCES hr.Employee(employee_id),
    CONSTRAINT FK_Audit_Store FOREIGN KEY (store_id) REFERENCES retail.Store(store_id)
);
GO

CREATE INDEX IX_SalesOrder_OrderDate ON retail.SalesOrder(order_datetime);
CREATE INDEX IX_SalesOrder_StoreDate ON retail.SalesOrder(store_id, order_datetime);
CREATE INDEX IX_OrderItem_OrderID ON retail.SalesOrderItem(order_id);
CREATE INDEX IX_Attendance_EmployeeDate ON hr.Attendance(employee_id, attendance_date);
CREATE INDEX IX_EyeTest_CompletedAt ON clinical.EyeTest(completed_at);
GO
