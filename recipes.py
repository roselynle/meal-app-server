from pymongo import MongoClient # type: ignore
import pprint

client = MongoClient(username='user', password='password')

db = client.foodApp

recipes = db.Meal

pprint.pprint(recipes.find_one())