from flask import Flask, jsonify, request # type: ignore
from flask_cors import CORS, cross_origin # type: ignore
from flask_mail import Message, Mail # type: ignore
from werkzeug import exceptions # type: ignore
from models import recipes, users #type: ignore

app = Flask(__name__)
CORS(app)

app.config['CORS_HEADERS'] = 'Content-Type'

mail_settings = {
    "MAIL_SERVER": 'smtp.gmail.com',
    "MAIL_PORT": 465,
    "MAIL_USE_SSL": True,
    "MAIL_USERNAME": 'communitycookalerts@gmail.com',
    "MAIL_PASSWORD": 'FutureProof'
}

app.config.update(mail_settings)
mail = Mail(app)

@app.route('/', methods=['GET'])
@cross_origin()
def home():
    message = f"Hey there, come check out Lenny\'s new album!"
    subject = 'New Release 🔥'
    msg = Message(recipients=["james.wheadon@yahoo.com"], body=message, sender='CommunityCook', subject=subject)
    print(msg)
    mail.send(msg)
    return jsonify({'message': 'Hello from Community Cook API!'}), 200

@app.route('/recipes/new/', methods=['POST'])
@cross_origin()
def new_recipe():
    new_meal = request.data
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

@app.route('/register', methods=['POST'])
@cross_origin()
def register_user():
    new_user = request.data
    users.create_user(new_user)
    return {'message': "Registration successful"}, 201

@app.route('/login', methods=['POST'])
@cross_origin()
def login_user():
    registered_user = request.data
    users.log_in(registered_user)
    return {'message': "Login successful"}, 201

@app.route('/user/<user_id>/favourites', methods=['GET'])
@cross_origin()
def get_favourites(user_id):
    favourites = users.get_favourites(user_id)
    recipes = []
    for favourite in favourites:
        recipe = recipes.get_recipe(favourite)
        recipes.append({"_id": recipe["_id"], "title": recipe["title"], "description": recipe["description"]})
    return jsonify(recipes), 201

@app.route('/user/<user_id>/favourites/new', methods=['PATCH'])
@cross_origin()
def new_favourite(user_id):
    recipe_id = request.data
    users.new_favourite(user_id, recipe_id)
    return {'message': "favourites updated"}, 204


@app.errorhandler(exceptions.NotFound)
def handle_404(err):
    return {'message': f'Error occurred: {err}'}, 404

@app.errorhandler(exceptions.InternalServerError)
def handle_500(err):
    return {'message': f'Error occurred: {err}'}, 500

if __name__ == "__main__":
    app.run(debug=True)