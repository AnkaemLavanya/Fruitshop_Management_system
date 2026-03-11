CREATE DATABASE fruit_shop;
USE fruit_shop;

CREATE TABLE users(
user_id INT AUTO_INCREMENT PRIMARY KEY,
username VARCHAR(50) UNIQUE,
password VARCHAR(50),
role VARCHAR(20)
);
alter table users modify role ENUM('shopkeeper','customer');
desc users;
INSERT INTO users(username,password,role)
VALUES('lavanya','lvny7','shopkeeper');
truncate table users;
set foreign_key_checks=0;
set foreign_key_checks=1;

select * from users;

CREATE TABLE inventory(
item_id INT AUTO_INCREMENT PRIMARY KEY,
name VARCHAR(50) UNIQUE,
quantity INT,
price FLOAT,
cost_price FLOAT
);
select * from inventory;
truncate table inventory;
CREATE TABLE cart(
cart_id INT AUTO_INCREMENT PRIMARY KEY,
user_id INT,
item_id INT,
quantity INT,
total_price FLOAT,
FOREIGN KEY (user_id) REFERENCES users(user_id),
FOREIGN KEY (item_id) REFERENCES inventory(item_id)
);
select * from cart;
truncate table cart;
CREATE TABLE sales(
sale_id INT AUTO_INCREMENT PRIMARY KEY,
item_id INT,
quantity INT,
profit FLOAT,
sale_date DATETIME,
FOREIGN KEY (item_id) REFERENCES inventory(item_id)
);
select * from sales;
truncate table sales;
CREATE TABLE bill_counter(
id INT PRIMARY KEY,
bill_no INT
);
select * from bill_counter;
INSERT INTO bill_counter VALUES (1,1000);
truncate table bill_counter;
commit;