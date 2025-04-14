from flask import Flask, jsonify
import requests

app = Flask(__name__)

@app.route('/health', methods=['GET'])
def health():
    return jsonify({"status": "healthy"}), 200

@app.route('/aggregate')
def aggregate_data():
    try:
        agent_data = requests.get("http://agent-service/agents", timeout=5).json()
        integration_data = requests.get("http://integration-service/sales", timeout=5).json()
        notification_data = requests.get("http://notification-service/notifications", timeout=5).json()

        combined = {
            "agents": agent_data,
            "sales": integration_data,
            "notifications": notification_data
        }
        return jsonify(combined)

    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
