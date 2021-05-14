from flask import Flask, jsonify, request # type: ignore
from flask_cors import CORS # type: ignore
from werkzeug import exceptions # type: ignore

app = Flask(__name__)
CORS(app)

@app.route('/', methods=['GET'])
def home():
    return jsonify({'message': 'Hello from Community Cook API!'}), 200

@app.errorhandler(exceptions.NotFound)
def handle_404(err):
    return {'message': f'Error occurred: {err}'}, 404


if __name__ == "__main__":
    app.run(debug=True)