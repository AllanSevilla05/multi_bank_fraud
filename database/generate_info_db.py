import random
from faker import Faker
import mysql.connector

fake = Faker()

#SQL Databases
DBS = ["bank_a_db", "bank_b_db", "bank_c_db"]

#Connecting to mysql
def connect(db):
    try:
        return mysql.connector.connect(host="localhost", user="root", database=db, port= "3306", password="temp_password")
    except mysql.connector.Error as err:
        print(f"Error: {err}")

#Creating customer name, email, and phone number
def create_customer(cursor):
    name = fake.name() #initializing fake name
    email = fake.email() #initializing fake email
    phone = fake.numerify(text="###-###-####")
    #initializing fake phone number; did not use fake.phone_number due to \
    # phone number being too long
    cursor.execute("""
                   INSERT INTO customers (full_name, email, phone) 
                   VALUES (%s, %s, %s)
                   """, (name, email, phone)) # .execute executes SQL query written
    return cursor.lastrowid

#creating account type and balance
def create_account(cursor, customer_id): #connecting new info to customer_id
    account_type = random.choice(["savings", "checking"]) #randomizing savings or checking account
    balance = round(random.uniform(100, 2000), 2) #random amount between 100 and 2000 with 2 decimal places for balance
    cursor.execute("""
                   INSERT INTO accounts (customer_id, account_type, balance)
                   VALUES (%s, %s, %s)
                   """, (customer_id, account_type, balance)) #inserting account_type and balance
    return cursor.lastrowid

def create_transaction(cursor, account_id):
    amount = round(random.uniform(5, 2000), 2) #random amount for transaction amount
    if random.random() < 0.5: #randomizing 0 to 1 for withdrawal or deposit
        amount = -amount
        tx_type = "withdrawal"
    else:
        tx_type = "deposit"

    cursor.execute("""
        INSERT INTO transactions (account_id, amount, transaction_type)
        VALUES (%s, %s, %s)
    """, (account_id, amount, tx_type)) #SQL Query

def populate(db, num_customers = 10000):
    conn = connect(db) #assigning conn to connect method mentioned above
    cursor = conn.cursor()
    for _ in range(num_customers):
        cust_id = create_customer(cursor)
        for _ in range(random.randint(1,5)):
            acc_id = create_account(cursor, cust_id)
            for _ in range(random.randint(1,10)):
                create_transaction(cursor, acc_id)
    conn.commit()
    cursor.close()
    conn.close()
    print(f"Inserted data into {db} successfully.")

for db in DBS:
    populate(db)

