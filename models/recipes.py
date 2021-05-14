from bson.objectid import ObjectId #type: ignore
from pymongo import MongoClient # type: ignore

def connect_to_meals():
    client = MongoClient(username='user', password='password')
    db = client.foodApp
    return db.Meal

def add_recipe(recipe):
    recipes = connect_to_meals()
    recipes.insert_one(recipe)

def get_recipes(query=None):
    recipes = connect_to_meals()
    if query:
        all_recipes = recipes.find(query).sort("_id", -1).limit(10)
    else:
        all_recipes = recipes.find().sort("_id", -1).limit(10)
    return [convert_id(recipe) for recipe in all_recipes]

def get_recipe(recipe_id):
    recipes = connect_to_meals()
    return convert_id(recipes.find_one({'_id': ObjectId(recipe_id)}))

def convert_id(recipe):
    recipe["_id"] = str(recipe["_id"])
    return recipe
