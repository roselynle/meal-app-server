from flask import Flask, jsonify, request # type: ignore
from flask_cors import CORS # type: ignore
from werkzeug import exceptions # type: ignore
from models import recipes #type: ignore
import json

app = Flask(__name__)
CORS(app)

@app.route('/', methods=['GET'])
def home():
    return jsonify({'message': 'Hello from Community Cook API!'}), 200

@app.route('/recipes/new/', methods=['POST'])
def new_recipe():
    new_meal = request.data
    recipes.add_recipe(new_meal)
    return {'message': "New recipe added"}, 201

@app.route('/recipes/', methods=['GET'])
def get_recipes():
    query = request.query_string.decode()
    dietary_reqs = query.split('&')
    diet_filter = [{req.split('=')[0]: req.split('=')[1]} for req in dietary_reqs]
    print(diet_filter)
    meals = recipes.get_recipes()
    return jsonify(meals), 200

@app.errorhandler(exceptions.NotFound)
def handle_404(err):
    return {'message': f'Error occurred: {err}'}, 404

@app.errorhandler(exceptions.InternalServerError)
def handle_500(err):
    return {'message': f'Error occurred: {err}'}, 500


if __name__ == "__main__":
    app.run(debug=True)