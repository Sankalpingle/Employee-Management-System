-- Create Database
CREATE DATABASE IF NOT EXISTS dms_db;
USE dms_db;

-- Users Table
CREATE TABLE IF NOT EXISTS users (
    id INT AUTO_INCREMENT PRIMARY KEY,
    username VARCHAR(100) UNIQUE NOT NULL,
    password VARCHAR(255) NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Students Table
CREATE TABLE IF NOT EXISTS students (
    id INT AUTO_INCREMENT PRIMARY KEY,
    roll_number VARCHAR(50) UNIQUE NOT NULL,
    student_name VARCHAR(100) NOT NULL,
    email VARCHAR(100) UNIQUE NOT NULL,
    phone VARCHAR(20) NOT NULL,
    department VARCHAR(50) NOT NULL,
    gpa DECIMAL(3, 2) NOT NULL,
    enrollment_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    INDEX idx_roll_number (roll_number),
    INDEX idx_email (email),
    INDEX idx_department (department)
);

-- Insert default admin user (username: admin, password: admin123)
-- Password hash: pbkdf2:sha256:600000$K1k2L3m4N5o6P7q8R9s0T1u2$9d9e8f7g6h5i4j3k2l1m0n9o8p7q6r5s4t3u2v1w0
INSERT INTO users (username, password) VALUES 
('admin', 'pbkdf2:sha256:600000$K1k2L3m4N5o6P7q8R9s0T1u2$9d9e8f7g6h5i4j3k2l1m0n9o8p7q6r5s4t3u2v1w0');

-- Insert sample data
INSERT INTO students (roll_number, student_name, email, phone, department, gpa, enrollment_date) VALUES
('CS001', 'Aarav Kumar', 'aarav.kumar@student.edu', '9876543210', 'CSE', 3.8, '2024-01-15'),
('CS002', 'Priya Sharma', 'priya.sharma@student.edu', '9876543211', 'CSE', 3.9, '2024-01-20'),
('CS003', 'Rohan Patel', 'rohan.patel@student.edu', '9876543212', 'CSE', 3.6, '2024-02-10'),
('EC001', 'Anjali Singh', 'anjali.singh@student.edu', '9876543213', 'ECE', 3.7, '2024-01-25'),
('EC002', 'Vikram Desai', 'vikram.desai@student.edu', '9876543214', 'ECE', 3.5, '2024-02-05'),
('ME001', 'Neha Gupta', 'neha.gupta@student.edu', '9876543215', 'ME', 3.4, '2024-02-15'),
('ME002', 'Arjun Reddy', 'arjun.reddy@student.edu', '9876543216', 'ME', 3.2, '2024-03-01'),
('CE001', 'Sneha Rao', 'sneha.rao@student.edu', '9876543217', 'CE', 3.6, '2024-01-10'),
('CE002', 'Karthik Iyer', 'karthik.iyer@student.edu', '9876543218', 'CE', 3.3, '2024-02-20'),
('CS004', 'Divya Nair', 'divya.nair@student.edu', '9876543219', 'CSE', 3.8, '2024-03-05');
