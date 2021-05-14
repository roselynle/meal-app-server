from flask import Flask, jsonify, request # type: ignore
from flask_cors import CORS # type: ignore

app = Flask(__name__)
CORS(app)

@app.route('/', methods=['GET'])
def home():
    return jsonify({'message': 'Hello from Community Cook API!'}), 200

if __name__ == "__main__":
    app.run(debug=True)