# Fruitshop_Management_system
The Fruit Shop Inventory and Billing Management System is an application developed using Python and MySQL to manage fruit inventory, customer purchases, and billing. It provides separate functionalities for shopkeepers and customers, including inventory management, cart operations, sales tracking, profit reports, and automated bill generation.

🍎 Fruit Shop Inventory and Billing Management System
📌 Overview

This project is a console-based Fruit Shop Management System developed using Python and MySQL. The system allows a shopkeeper to manage fruit inventory, track sales, and view profit reports, while customers can view available fruits, add items to a cart, and generate bills.

The application demonstrates the use of database operations, role-based login systems, and modular Python programming.

🎯 Features
👨‍💼 Shopkeeper Features

View fruit inventory

Add new fruits to inventory

Modify fruit quantity and price

Remove fruits from inventory

View purchase reports

View daily and monthly profit reports

View registered customers

View total sales

View top-selling fruit

👤 Customer Features

Create a new account

Login to the system

View available fruits

Add fruits to cart

View cart items

Remove items from cart

Generate purchase bill

🧾 Billing System

The system generates a bill containing:

Shop name

Bill number

Date and time of purchase

Fruit name

Quantity purchased

Total amount

Total number of items purchased

🗄 Database Tables

The project uses the following tables:

Table	Purpose
users	Stores shopkeeper and customer login details
inventory	Stores fruit details and stock quantity
cart	Temporarily stores customer purchase items
sales	Stores completed purchase records
bill_counter	Generates automatic bill numbers
🛠 Technologies Used

Python

MySQL

mysql-connector-python

Datetime module

▶️ How to Run the Project
1️⃣ Install MySQL Connector
pip install mysql-connector-python
2️⃣ Create Database
CREATE DATABASE fruit_shop;
3️⃣ Create Required Tables

Create the following tables in the database:

users

inventory

cart

sales

bill_counter

4️⃣ Insert Shopkeeper Account
INSERT INTO users(username,password,role)
VALUES('admin','admin123','shopkeeper');
5️⃣ Initialize Bill Counter
INSERT INTO bill_counter(id,bill_no)
VALUES(1,1000);
6️⃣ Run the Program
python fruit_shop.py
📊 Reports Available

Purchase Report

Daily Profit Report

Monthly Profit Report

Total Sales Report

Top Selling Fruit

🔐 Security Features

Unique username validation

Role-based login system

Input validation for stock availability

👩‍💻 Author

Lavanya
