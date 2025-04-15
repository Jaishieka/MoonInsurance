from flask import Flask, request, jsonify

app = Flask(__name__)

agents = {}  # Simulated in-memory database

@app.route('/health', methods=['GET'])
def health():
    return jsonify({"status": "healthy"}), 200  # Health check route

@app.route('/agents', methods=['GET'])
def get_agents():
    return jsonify(agents)

@app.route('/agents', methods=['POST'])
def add_agent():
    data = request.json
    agent_code = data.get("agent_code")
    agents[agent_code] = data
    return jsonify({"message": "Agent added"}), 201


@app.route('/agents/<agent_code>', methods=['GET'])
def get_agent(agent_code):
    agent = agents.get(agent_code)
    if agent:
        return jsonify(agent)
    return jsonify({"error": "Agent not found"}), 404

@app.route('/agents/<agent_code>', methods=['PUT'])
def update_agent(agent_code):
    data = request.json
    agents[agent_code] = data
    return jsonify({"message": "Agent updated"})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
