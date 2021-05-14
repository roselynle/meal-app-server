from pymongo import MongoClient # type: ignore
import pprint

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
    return [recipe for recipe in all_recipes]
