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

def create_notifications_table():
    connection = get_db_connection()
    if connection:
        cursor = connection.cursor()
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS notifications (
                id INT AUTO_INCREMENT PRIMARY KEY,
                agent_code VARCHAR(50),
                message TEXT,
                notification_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)
        connection.commit()
        cursor.close()
        connection.close()
        print("'notifications' table checked/created.")

create_notifications_table()

# ---------------------------
# Routes
# ---------------------------

@app.route('/health', methods=['GET'])
def health():
    return jsonify({"status": "healthy"}), 200

@app.route('/notify', methods=['POST'])
def send_notification():
    data = request.json
    agent_code = data.get("agent_code")
    message = f"Sales target achieved by Agent {agent_code}"

    connection = get_db_connection()
    cursor = connection.cursor()
    try:
        cursor.execute("""
            INSERT INTO notifications (agent_code, message)
            VALUES (%s, %s)
        """, (agent_code, message))
        connection.commit()
        print(message)  # Simulate sending email/SMS
        return jsonify({"message": "Notification sent"}), 200
    except Error as e:
        return jsonify({"error": str(e)}), 500
    finally:
        cursor.close()
        connection.close()

@app.route('/notifications', methods=['GET'])
def get_notifications():
    connection = get_db_connection()
    cursor = connection.cursor(dictionary=True)
    cursor.execute("SELECT * FROM notifications")
    notifications = cursor.fetchall()
    cursor.close()
    connection.close()
    return jsonify(notifications), 200

# ---------------------------
# Start App
# ---------------------------
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5002)
