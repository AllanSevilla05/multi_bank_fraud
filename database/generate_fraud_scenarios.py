import random
from faker import Faker
import mysql.connector

fake = Faker()

DBS = ["bank_a_db", "bank_b_db", "bank_c_db"]

def connect(db):
    return mysql.connector.connect(
        host="localhost",
        user="root",
        password="temp_password",
        database=db
    )

def add_fraud(cursor, account_id):
    fraud_type = random.choice([
        "ATO", "MULE", "SMURFING", "SYNTHETIC", "RAPID", "RING"
    ])

    # fraud patterns
    if fraud_type == "ATO":
        amount = -random.uniform(400, 1500)
        tx_type = "withdrawal"

    elif fraud_type == "MULE":
        amount = random.uniform(3000, 6000)
        tx_type = "deposit"

    elif fraud_type == "SMURFING":
        amount = random.choice([9800, 9900, 9950])
        tx_type = "deposit"

    elif fraud_type == "SYNTHETIC":
        amount = random.uniform(5000, 10000)
        tx_type = "deposit"

    elif fraud_type == "RAPID":
        amount = -random.uniform(20, 100)
        tx_type = "withdrawal"

    elif fraud_type == "RING":
        amount = random.uniform(900, 1500)
        tx_type = "deposit"

    cursor.execute("""
        INSERT INTO transactions (account_id, amount, transaction_type, is_fraud)
        VALUES (%s, %s, %s, 1)
    """, (account_id, amount, tx_type))

def add_normal(cursor, account_id):
    amount = random.uniform(5, 800)
    tx_type = random.choice(["deposit", "withdrawal"])
    if tx_type == "withdrawal":
        amount = -amount

    cursor.execute("""
        INSERT INTO transactions (account_id, amount, transaction_type, is_fraud)
        VALUES (%s, %s, %s, 0)
    """, (account_id, amount, tx_type))

def populate_transactions(db, fraud_ratio=0.05):
    conn = connect(db)
    cursor = conn.cursor()

    cursor.execute("SELECT account_id FROM accounts")
    accounts = [a[0] for a in cursor.fetchall()]

    for acc in accounts:
        for _ in range(50):
            if random.random() < fraud_ratio:
                add_fraud(cursor, acc)
            else:
                add_normal(cursor, acc)

    conn.commit()
    cursor.close()
    conn.close()
    print(f"Fraud + normal data added to {db}")

for db in DBS:
    populate_transactions(db)