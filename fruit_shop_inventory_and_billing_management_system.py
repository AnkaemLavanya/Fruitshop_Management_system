import mysql.connector as db
from datetime import datetime

# -------- DATABASE CONNECTION --------
con = db.connect(
    host="localhost",
    user="root",
    password="Lavanya@7",
    database="fruit_shop"
)

cursor = con.cursor(buffered=True)

# -------- CREATE USER --------
def create_customer():

    username=input("Enter username: ")

    cursor.execute("SELECT * FROM users WHERE username=%s",(username,))
    if cursor.fetchone():
        print("User already exists")
        return

    password=input("Enter password: ")

    cursor.execute(
        "INSERT INTO users(username,password,role) VALUES(%s,%s,'customer')",
        (username,password)
    )

    con.commit()

    print("Customer account created successfully")


# -------- LOGIN --------
def login():

    username=input("Enter username: ")
    password=input("Enter password: ")

    cursor.execute(
        "SELECT * FROM users WHERE username=%s AND password=%s",
        (username,password)
    )

    user=cursor.fetchone()

    if user:
        print("Login successful")
        return user
    else:
        print("Invalid login")
        return None  
# -------- CUSTOMER ACCESS MENU --------
def customer_access():

    while True:

        print("\n--- Customer Access ---")
        print("1 Create Account")
        print("2 Login")
        print("3 Back")

        ch=input("Enter choice: ")

        if ch=="1":
            create_customer()

        elif ch=="2":

            user=login()

            if user and user[3]=="customer":
                customer_menu(user[0])
            else:
                print("Customer login only")

        elif ch=="3":
            break

        else:
            print("Invalid choice")

# -------- VIEW INVENTORY --------
def view_inventory(shopkeeper=False):

    cursor.execute("SELECT item_id,name,quantity,price FROM inventory")
    fruits=cursor.fetchall()

    print("\n--- Fruits Available ---")

    for f in fruits:
        if shopkeeper and f[2]<5:
            print("ID:",f[0],"Name:",f[1],"Qty:",f[2],"Price:",f[3],"LOW STOCK")
        else:
            print("ID:",f[0],"Name:",f[1],"Qty:",f[2],"Price:",f[3])


# -------- ADD FRUIT --------
def add_item():

    name=input("Fruit name: ")

    cursor.execute("SELECT * FROM inventory WHERE name=%s",(name,))
    if cursor.fetchone():
        print("Fruit already exists")
        return

    qty=int(input("Quantity: "))
    price=float(input("Selling price: "))
    cost=float(input("Cost price: "))

    cursor.execute(
        "INSERT INTO inventory(name,quantity,price,cost_price) VALUES(%s,%s,%s,%s)",
        (name,qty,price,cost)
    )

    con.commit()

    print("Fruit added successfully")


# -------- MODIFY FRUIT --------
def modify_item():
    view_inventory()

    name = input("Enter fruit name to modify: ")

    cursor.execute("SELECT quantity FROM inventory WHERE name=%s", (name,))
    result = cursor.fetchone()

    if not result:
        print("Fruit not found")
        return

    add_qty = int(input("Enter quantity to add: "))
    price = float(input("Enter new selling price: "))
    cost = float(input("Enter new cost price: "))

    cursor.execute(
        """UPDATE inventory 
           SET quantity = quantity + %s,
               price = %s,
               cost_price = %s
           WHERE name = %s""",
        (add_qty, price, cost, name)
    )

    con.commit()

    print("Fruit updated successfully")


# -------- REMOVE FRUIT --------
def remove_item():

    name=input("Enter fruit name to remove: ")

    cursor.execute("SELECT * FROM inventory WHERE name=%s",(name,))
    if not cursor.fetchone():
        print("Fruit not found")
        return

    cursor.execute("DELETE FROM inventory WHERE name=%s",(name,))
    con.commit()

    print("Fruit removed successfully")


# -------- ADD TO CART --------
def add_to_cart(user_id):
    view_inventory()

    item_id=int(input("Enter fruit ID: "))
    qty=int(input("Enter quantity: "))

    cursor.execute(
        "SELECT price,cost_price,quantity FROM inventory WHERE item_id=%s",
        (item_id,)
    )

    fruit=cursor.fetchone()

    if not fruit:
        print("Fruit not found")
        return

    if fruit[2] < qty:
        print("Not enough stock")
        return

    total=fruit[0]*qty

    cursor.execute(
        "INSERT INTO cart(user_id,item_id,quantity,total_price) VALUES(%s,%s,%s,%s)",
        (user_id,item_id,qty,total)
    )

    con.commit()

    print("Item added to cart")


# -------- VIEW CART --------
def view_cart(user_id):

    cursor.execute(
        """SELECT cart.cart_id,inventory.name,cart.quantity,cart.total_price
        FROM cart
        JOIN inventory ON cart.item_id=inventory.item_id
        WHERE cart.user_id=%s""",
        (user_id,)
    )

    items=cursor.fetchall()

    if not items:
        print("Cart empty")
        return

    print("\n--- Cart ---")

    for i in items:
        print("CartID:",i[0],"Fruit:",i[1],"Qty:",i[2],"Total:",i[3])


# -------- REMOVE FROM CART --------
def remove_from_cart(user_id):
    view_cart()
    cart_id=int(input("Enter cart ID to remove: "))

    cursor.execute(
        "SELECT item_id,quantity FROM cart WHERE cart_id=%s AND user_id=%s",
        (cart_id,user_id)
    )

    item=cursor.fetchone()

    if not item:
        print("Cart item not found")
        return

    cursor.execute(
        "DELETE FROM cart WHERE cart_id=%s AND user_id=%s",
        (cart_id,user_id)
    )

    cursor.execute(
        "UPDATE inventory SET quantity=quantity+%s WHERE item_id=%s",
        (item[1],item[0])
    )

    con.commit()

    print("Item removed from cart")


# -------- GENERATE BILL --------
def generate_bill(user_id):

    cursor.execute(
        """SELECT cart.item_id,cart.quantity,inventory.name,
        inventory.price,inventory.cost_price
        FROM cart
        JOIN inventory ON cart.item_id=inventory.item_id
        WHERE cart.user_id=%s""",
        (user_id,)
    )

    items=cursor.fetchall()

    if not items:
        print("Cart empty")
        return

    total=0
    now=datetime.now()
    timestamp=now.strftime("%Y-%m-%d %H:%M:%S")

    item_count=0

    bill_number=generate_bill_no()

    print("="*35)
    print("        FRUIT SHOP")
    print("   Hyderabad   ph.no:xxxxxxxxxx")
    print("="*35)
    print("Bill No:",bill_number)
    print("Date:",timestamp)
    print("-"*35)
    print("{:<10} {:<5} {:<8}".format("Fruit","Qty","Amount"))
    print("-"*35)

    for i in items:

        item_id=i[0]
        qty=i[1]
        name=i[2]
        price=i[3]
        cost=i[4]

        amount=price*qty
        profit=(price-cost)*qty

        total+=amount
        item_count+=qty

        print(f"{name:<10} {qty:<5} {amount:<8}")

        # reduce inventory after purchase
        cursor.execute(
            "UPDATE inventory SET quantity=quantity-%s WHERE item_id=%s",
            (qty,item_id)
        )

        cursor.execute(
            "INSERT INTO sales(item_id,quantity,profit,sale_date) VALUES(%s,%s,%s,%s)",
            (item_id,qty,profit,timestamp)
        )

    print("-"*35)
    print("Items Purchased:",item_count)
    print("{:<10} {:<5} {:<8}".format("Total","",total))
    print("="*35)
    print("       Purchase Successful")
    print("     Thank You! Visit Again ")
    print("="*35)

    cursor.execute("DELETE FROM cart WHERE user_id=%s",(user_id,))
    con.commit()


# -------- GENERATE BILL NUMBER --------

def generate_bill_no():

    cursor.execute("SELECT bill_no FROM bill_counter WHERE id=1")
    result = cursor.fetchone()

    bill = result[0] + 1

    cursor.execute("UPDATE bill_counter SET bill_no=%s WHERE id=1",(bill,))
    con.commit()

    return "BILL-" + str(bill)

# -------- PURCHASE REPORT --------
def purchase_report():

    cursor.execute(
        """SELECT inventory.name,sales.quantity,sales.profit,sales.sale_date
        FROM sales
        JOIN inventory ON sales.item_id=inventory.item_id""" )

    report=cursor.fetchall()

    print("\n--- Purchase Report ---")

    for r in report:
        print("Fruit:",r[0],"Qty:",r[1],"Profit:",r[2],"Date:",r[3])


# -------- DAILY PROFIT --------
def daily_profit():

    date=input("Enter date (YYYY-MM-DD): ")

    cursor.execute(
        "SELECT SUM(profit) FROM sales WHERE DATE(sale_date)=%s",
        (date,))

    profit=cursor.fetchone()[0]

    if profit is None:
        profit=0

    print("Total Profit on",date,"=",profit)


# -------- MONTHLY PROFIT --------
def monthly_profit():

    month=input("Enter month (YYYY-MM): ")

    cursor.execute(
        "SELECT SUM(profit) FROM sales WHERE DATE_FORMAT(sale_date,'%Y-%m')=%s",
        (month,))

    profit=cursor.fetchone()[0]

    if profit is None:
        profit=0

    print("Total Profit in",month,"=",profit)


# -------- PROFIT MENU --------
def profit_menu():

    print("\n1 Daily Profit")
    print("2 Monthly Profit")

    ch=input("Enter choice: ")

    if ch=="1":
        daily_profit()

    elif ch=="2":
        monthly_profit()


# -------- VIEW CUSTOMERS --------
def view_users():

    cursor.execute("SELECT user_id,username FROM users WHERE role='customer'")
    users=cursor.fetchall()

    print("\n--- Customers ---")

    for u in users:
        print("ID:",u[0],"Username:",u[1])

# -------- TOTAL SALES --------
def total_sales():

    cursor.execute("""
    SELECT SUM(inventory.price * sales.quantity)
    FROM sales
    JOIN inventory ON sales.item_id = inventory.item_id
    """)

    result = cursor.fetchone()

    if result[0] is None:
        print("Total Sales = 0")
    else:
        print("Total Sales Amount =", result[0])

# -------- TOP SELLING FRUIT --------
def top_selling_fruit():

    cursor.execute("""
    SELECT inventory.name, SUM(sales.quantity) AS total_sold
    FROM sales
    JOIN inventory ON sales.item_id = inventory.item_id
    GROUP BY inventory.name
    ORDER BY total_sold DESC
    LIMIT 1
    """)

    result = cursor.fetchone()

    if result:
        print("Top Selling Fruit:", result[0], "| Quantity Sold:", result[1])
    else:
        print("No sales data available")        


# -------- SHOPKEEPER MENU --------
def shopkeeper_menu():

    while True:

        print("\n--- Shopkeeper Menu ---")
        print("1 View Inventory")
        print("2 Add Fruit")
        print("3 Modify Fruit")
        print("4 Remove Fruit")
        print("5 Purchase Report")
        print("6 Profit Report")
        print("7 View Customers")
        print("8 Total Sales")
        print("9 Top Selling Fruit")
        print("10 Logout")

        choice=input("Enter choice: ")

        if choice=="1":
            view_inventory(True)

        elif choice=="2":
            add_item()

        elif choice=="3":
            modify_item()

        elif choice=="4":
            remove_item()

        elif choice=="5":
            purchase_report()

        elif choice=="6":
            profit_menu()

        elif choice=="7":
            view_users()
            
        elif choice=="8":
            total_sales()

        elif choice=="9":
            top_selling_fruit()
            
        elif choice=="10":
            break
        else:
            print("Invalid choice. Please enter a number from 1 to 10.")


# -------- CUSTOMER MENU --------
def customer_menu(user_id):

    while True:

        print("\n--- Customer Menu ---")
        print("1 View Fruits")
        print("2 Add to Cart")
        print("3 View Cart")
        print("4 Remove from Cart")
        print("5 Generate Bill")
        print("6 Logout")

        choice=input("Enter choice: ")

        if choice=="1":
            view_inventory()

        elif choice=="2":
            add_to_cart(user_id)

        elif choice=="3":
            view_cart(user_id)

        elif choice=="4":
            remove_from_cart(user_id)

        elif choice=="5":
            generate_bill(user_id)

        elif choice=="6":
            break
        else:
            print("Invalid choice. Please enter a number from 1 to 6.")


# -------- MAIN MENU --------
while True:

    print("\n===== FRUIT SHOP SYSTEM =====")
    print("1 Shopkeeper")
    print("2 Customer")
    print("3 Exit")

    choice=input("Enter choice: ")

    if choice=="1":

        print("\n--- Shopkeeper Login ---")

        user=login()

        if user and user[3]=="shopkeeper":
            shopkeeper_menu()
        else:
            print("Invalid shopkeeper login")


    elif choice=="2":

        customer_access()


    elif choice=="3":

        print('-'*35)
        print("     Thank You for Shopping")
        print("          Visit Again!!")
        break


    else:
        print("Invalid choice. Please enter 1, 2, or 3.")
