from flask import Flask, jsonify, request

app = Flask(__name__)

orientation_data = {"orientation": 0}  # Initialize orientation data

@app.route('/update_orientation', methods=['POST'])
def update_orientation():
    global orientation_data
    data = request.json
    if 'orientation' in data:
        orientation_data['orientation'] = data['orientation']
        return jsonify({"message": "Orientation updated successfully"})
    else:
        return jsonify({"error": "Invalid data format"}), 400

@app.route('/get_orientation', methods=['GET'])
def get_orientation():
    global orientation_data
    return jsonify(orientation_data)

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
