from flask import Flask, jsonify, request # type: ignore
from flask_cors import CORS, cross_origin # type: ignore
from werkzeug import exceptions # type: ignore
from models import recipes #type: ignore
# from pymongo import MongoClient

app = Flask(__name__)
cors = CORS(app)

app.config['CORS_HEADERS'] = 'Content-Type'

# connect_string = 'mongodb+srv://user:foodpassword@cluster0.q17xw.mongodb.net/foodApp?retryWrites=true&w=majority'
# client = MongoClient(connect_string)
# db = client.get_default_database()

# def get_mongo_connect_string():
#     return os.environ.get("MONGO_CONNECT_STRING", "")

@app.route('/', methods=['GET'])
@cross_origin()
def home():
    return jsonify({'message': 'Hello from Community Cook API!'}), 200

@app.route('/recipes/new/', methods=['POST'])
@cross_origin()
def new_recipe():
    new_meal = request.data.decode()
    print(new_meal)
    recipes.add_recipe(new_meal)
    return {'message': "New recipe added"}, 201

@app.route('/recipes/', methods=['GET'])
@cross_origin()
def get_recipes():
    query = request.query_string.decode()
    if query:
        dietary_reqs = query.split('&')
        diet_filter = {"diet_req": [req for req in dietary_reqs]}
        print(diet_filter)
        meals = recipes.get_recipes(diet_filter)
    else:
        meals = recipes.get_recipes()
    return jsonify(meals), 200

@app.route('/recipes/<recipe_id>', methods=['GET'])
@cross_origin()
def get_recipe(recipe_id):
    recipe = recipes.get_recipe(recipe_id)
    return jsonify(recipe), 200

@app.errorhandler(exceptions.NotFound)
def handle_404(err):
    return {'message': f'Error occurred: {err}'}, 404

@app.errorhandler(exceptions.InternalServerError)
def handle_500(err):
    return {'message': f'Error occurred: {err}'}, 500


if __name__ == "__main__":
    app.run(debug=True)