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

def create_agents_table():
    connection = get_db_connection()
    if connection:
        cursor = connection.cursor()
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS agents (
                agent_code VARCHAR(50) PRIMARY KEY,
                name VARCHAR(100),
                email VARCHAR(100),
                phone VARCHAR(20),
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)
        connection.commit()
        cursor.close()
        connection.close()
        print("'agents' table checked/created.")

create_agents_table()

# ---------------------------
# Routes
# ---------------------------

@app.route('/health', methods=['GET'])
def health():
    return jsonify({"status": "healthy"}), 200

@app.route('/agents', methods=['GET'])
def get_agents():
    connection = get_db_connection()
    cursor = connection.cursor(dictionary=True)
    cursor.execute("SELECT * FROM agents")
    agents = cursor.fetchall()
    cursor.close()
    connection.close()
    return jsonify(agents), 200

@app.route('/agents', methods=['POST'])
def add_agent():
    data = request.json
    agent_code = data.get("agent_code")
    name = data.get("name")
    email = data.get("email")
    phone = data.get("phone")

    connection = get_db_connection()
    cursor = connection.cursor()
    try:
        cursor.execute("""
            INSERT INTO agents (agent_code, name, email, phone)
            VALUES (%s, %s, %s, %s)
        """, (agent_code, name, email, phone))
        connection.commit()
        return jsonify({"message": "Agent added"}), 201
    except Error as e:
        return jsonify({"error": str(e)}), 500
    finally:
        cursor.close()
        connection.close()

@app.route('/agents/<agent_code>', methods=['GET'])
def get_agent(agent_code):
    connection = get_db_connection()
    cursor = connection.cursor(dictionary=True)
    cursor.execute("SELECT * FROM agents WHERE agent_code = %s", (agent_code,))
    agent = cursor.fetchone()
    cursor.close()
    connection.close()
    if agent:
        return jsonify(agent), 200
    return jsonify({"error": "Agent not found"}), 404

@app.route('/agents/<agent_code>', methods=['PUT'])
def update_agent(agent_code):
    data = request.json
    name = data.get("name")
    email = data.get("email")
    phone = data.get("phone")

    connection = get_db_connection()
    cursor = connection.cursor()
    cursor.execute("""
        UPDATE agents SET name=%s, email=%s, phone=%s WHERE agent_code=%s
    """, (name, email, phone, agent_code))
    connection.commit()
    cursor.close()
    connection.close()
    return jsonify({"message": "Agent updated"}), 200

# ---------------------------
# Start App
# ---------------------------
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
