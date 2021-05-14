from pymongo import MongoClient # type: ignore

def connect_to_meals():
    client = MongoClient(username='user', password='password')
    db = client.foodApp
    return db.Meal

def add_recipe(recipe):
    recipes = connect_to_meals()
    recipes.insert_one(recipe)