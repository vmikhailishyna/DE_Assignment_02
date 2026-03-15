Create database if not exists support_call_centre_database;
 USE support_call_centre_database;


CREATE TABLE IF NOT EXISTS employees (
    employee_id int primary key,
    full_name varchar(50),
    team varchar(50),
    hire_date DATE
);

CREATE TABLE IF NOT EXISTS calls(
    call_id int primary key AUTO_INCREMENT,
    employee_id int,
    call_time DATETIME,
    phone varchar(20),
    direction ENUM('inbound', 'outbound'),
    status ENUM('completed', 'missed', 'failed'),
    FOREIGN KEY (employee_id) REFERENCES employees(employee_id)
);
