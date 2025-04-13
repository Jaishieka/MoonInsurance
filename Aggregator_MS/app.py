# aggregator-service/app.py
from flask import Flask, jsonify
import requests

app = Flask(__name__)

@app.route('/aggregate')
def aggregate_data():
    try:
        agent_data = requests.get("http://agent-service/agent").json()
        integration_data = requests.get("http://integration-service/integration").json()
        notification_data = requests.get("http://notification-service/notifications").json()

        combined = {
            "agent": agent_data,
            "integration": integration_data,
            "notifications": notification_data
        }
        return jsonify(combined)

    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
