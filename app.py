from flask import Flask, jsonify, request, render_template # type: ignore
from flask_cors import CORS, cross_origin # type: ignore
from flask_mail import Message, Mail # type: ignore
from werkzeug import exceptions # type: ignore
from models import recipes, users #type: ignore
import json
# import pymongo
# from pymongo import MongoClient

# DATABASE_URL='mongodb+srv://user:foodpassword@cluster0.xxngz.mongodb.net/foodDatabase?retryWrites=true&w=majority' # get connection url from environment

# client=pymongo.MongoClient(DATABASE_URL)  # establish connection with database
# mongo_db=client.test # assign database to mongo_db

app = Flask(__name__)
cors = CORS(app)

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
    return jsonify({'message': 'Hello from Community Cook API!'}), 200

@app.route('/recipes/new/', methods=['POST'])
@cross_origin()
def new_recipe():
    new_meal = request.data.decode()
    recipes.add_recipe(new_meal)
    return {'message': "New recipe added"}, 201

@app.route('/recipes/', methods=['GET'])
@cross_origin()
def get_recipes():
    query = request.query_string.decode()
    if query:
        dietary_reqs = query.split('&')
        diet_filter = {"diet_req": [req for req in dietary_reqs]}
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
    user = json.loads(new_user.decode())
    success = users.create_user(user)
    if (success == True):
        return {'message': "Registration successful"}, 200
    else:
        return {'err': "Registration unsuccessful"}, 500

@app.route('/login', methods=['POST'])
@cross_origin()
def login_user():
    registered_user = request.data
    user = json.loads(registered_user.decode())
    success = users.log_in(user)
    if success:
        return jsonify(success), 200
    else:
        return {'err': "Login unsuccessful"}, 500

@app.route('/user/<user_id>/favourites', methods=['GET'])
@cross_origin()
def get_favourites(user_id):
    favourites = users.get_favourites(user_id)
    meals = []
    for favourite in favourites:
        meal = recipes.get_recipe(favourite)
        meals.append({"_id": meal["_id"], "title": meal["title"], "description": meal["description"], "image_url": meal["image_url"]})
    return jsonify(meals), 200

@app.route('/user/<user_id>/favourites/new', methods=['PATCH'])
@cross_origin()
def new_favourite(user_id):
    recipe_id = json.loads(request.data.decode())["recipe_id"]
    users.new_favourite(user_id, recipe_id)
    return {'message': "favourites updated"}, 201

@app.route('/user/<user_id>/favourites/delete', methods=['DELETE'])
@cross_origin()
def delete_favourite(user_id):
    recipe_id = json.loads(request.data.decode())["recipe_id"]
    users.delete_favourite(user_id, recipe_id)
    return {'message': "favourites updated"}, 200

@app.route('/user/<user_id>/mealplan', methods=['GET'])
@cross_origin()
def get_meal_plan(user_id):
    plan = users.get_meal_plan(user_id)
    print(plan)
    return jsonify(plan), 200

@app.route('/user/<user_id>/mealplan/new', methods=['PATCH'])
@cross_origin()
def new_meal_plan(user_id):
    plan_data = json.loads(json.loads(request.data.decode())["body"])
    users.new_meal_plan(user_id, plan_data)
    return {'message': "meal plan updated"}, 201

@app.route('/user/<user_id>/mealplan/ingredients', methods=['GET'])
@cross_origin()
def get_ingredients(user_id):
    plan = users.get_meal_plan(user_id)
    user = users.get_user(user_id)
    ingredients = {}
    for day, meal in plan.items():
        meal = recipes.get_recipe(meal["_id"])
        meal_ingredients = {}
        for ingredient in meal["ingredients"]:
            try:
                if ingredient["measure"] and ingredient["measure"] != "null":
                    meal_ingredients[ingredient["ingredient"] + ':' + ingredient["measure"]] = float(ingredient["amount"])
                else:
                    meal_ingredients[ingredient["ingredient"]] = float(ingredient["amount"])
            except:
                meal_ingredients[ingredient["ingredient"]] = 0
        ingredients = {ingredient: ingredients.get(ingredient, 0) + meal_ingredients.get(ingredient, 0) for ingredient in set(ingredients) | set(meal_ingredients)}
    sorted_ingredients = sorted(ingredients.keys(), key=lambda x:x.lower())
    ingredient_list = []
    for i in sorted_ingredients:
        amount = ingredients[i]
        if amount:
            if amount % 1 == 0:
                amount = int(amount)
        else:
            amount = ""
        if ':' in i:
            ingredient_list.append(f"{i.split(':')[0]}: {amount}{i.split(':')[1]}")
        else:
            if amount:
                ingredient_list.append(f"{i}: {amount}")
            else:
                ingredient_list.append(f"{i}")
    msg = Message("Your Shopping List", sender='PlanEat', recipients = [user["email"]])
    msg.html = render_template('ingredients.html', user_name=user["username"], ingredients=ingredient_list)
    mail.send(msg)
    return {'message': "ingredients sent"}, 200

@app.errorhandler(exceptions.NotFound)
def handle_404(err):
    return {'err': f'Error occurred: {err}'}, 404

@app.errorhandler(exceptions.InternalServerError)
def handle_500(err):
    return {'err': f'Error occurred: {err}'}, 500

if __name__ == "__main__":
    app.run(debug=True)