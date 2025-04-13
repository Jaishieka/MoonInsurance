from flask import Flask, request, jsonify

app = Flask(__name__)

sales_data = []

# Health check route
@app.route('/health', methods=['GET'])
def health():
    return jsonify({"status": "healthy"}), 200

# Route to receive sales data
@app.route('/sales', methods=['POST'])
def receive_sales():
    data = request.json
    sales_data.append(data)
    return jsonify({"message": "Sales data received"}), 200

# Route to get sales data
@app.route('/sales', methods=['GET'])
def get_sales():
    return jsonify(sales_data)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5001)
