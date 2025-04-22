from flask import Flask, request, jsonify
import mysql.connector
from mysql.connector import Error
import os

app = Flask(__name__)

# ---------------------------
# DB Connection Setup
# ---------------------------
def get_db_connection():
    try:
        connection = mysql.connector.connect(
            host=os.environ['DB_HOST'],
            user=os.environ['DB_USER'],
            password=os.environ['DB_PASSWORD'],
            database=os.environ['DB_NAME']
        )
        return connection
    except Error as e:
        print("Error connecting to database:", e)
        return None

def create_sales_table():
    connection = get_db_connection()
    if connection:
        cursor = connection.cursor()
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS sales (
                id INT AUTO_INCREMENT PRIMARY KEY,
                policy_id VARCHAR(50),
                customer_name VARCHAR(100),
                amount DECIMAL(10,2),
                sale_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                agent_code VARCHAR(50),
                INDEX(agent_code),
                FOREIGN KEY (agent_code) REFERENCES agents(agent_code)  -- Foreign key to agents
            )
        """)
        connection.commit()
        cursor.close()
        connection.close()
        print("✅ 'sales' table checked/created.")

create_sales_table()

# ---------------------------
# Routes
# ---------------------------

@app.route('/health', methods=['GET'])
def health():
    return jsonify({"status": "healthy"}), 200

@app.route('/sales', methods=['POST'])
def receive_sales():
    data = request.json
    policy_id = data.get("policy_id")
    customer_name = data.get("customer_name")
    amount = data.get("amount")
    agent_code = data.get("agent_code")  # Added agent_code to link to Agent

    connection = get_db_connection()
    cursor = connection.cursor()
    try:
        cursor.execute("""
            INSERT INTO sales (policy_id, customer_name, amount, agent_code)
            VALUES (%s, %s, %s, %s)
        """, (policy_id, customer_name, amount, agent_code))
        connection.commit()
        return jsonify({"message": "Sales data received"}), 200
    except Error as e:
        return jsonify({"error": str(e)}), 500
    finally:
        cursor.close()
        connection.close()

@app.route('/sales', methods=['GET'])
def get_sales():
    connection = get_db_connection()
    cursor = connection.cursor(dictionary=True)
    cursor.execute("SELECT * FROM sales")
    sales = cursor.fetchall()
    cursor.close()
    connection.close()
    return jsonify(sales), 200

# ---------------------------
# Start App
# ---------------------------
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5001)
