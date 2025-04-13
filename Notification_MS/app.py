from flask import Flask, request, jsonify

app = Flask(__name__)

notifications = []

@app.route('/notify', methods=['POST'])
def send_notification():
    data = request.json
    agent_code = data.get("agent_code")
    message = f"Sales target achieved by Agent {agent_code}"
    notifications.append(message)
    print(message)  # Simulate sending email/SMS
    return jsonify({"message": "Notification sent"}), 200

@app.route('/notifications', methods=['GET'])
def get_notifications():
    return jsonify(notifications)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5002)
