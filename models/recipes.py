from bson.objectid import ObjectId #type: ignore
from pymongo import MongoClient # type: ignore
import json, pdb

# mongoDB_username = 'user'

def connect_to_meals():
    client = MongoClient("mongodb+srv://user:foodpassword@cluster0.xxngz.mongodb.net/foodApp?retryWrites=true&w=majority")
    db = client.foodApp
    return db.Meal

def add_recipe(recipe):
    # pdb.set_trace()
    recipes = connect_to_meals()
    recipe = json.loads(recipe)

    # print(recipe)
    diet_reqs = []
    for diet_req in recipe["dietary-req"]:
        print(diet_req)
        for key, value in diet_req.items():
            if value:
                diet_reqs.append(key.lower())
    db_recipe = {"title": recipe["recipeName"], "description": recipe["recipeDescription"], "ingredients": recipe["ingredients"], "instructions": recipe["instructions"], "diet_req": diet_reqs, "image_url": recipe["image_url"]}

    recipes.insert_one(db_recipe)

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
