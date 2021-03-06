from bson.objectid import ObjectId #type: ignore
from flask import request, session, flash # type: ignore
from pymongo import MongoClient  # type: ignore
import bcrypt # type: ignore

# mongoDB_username = 'user'

def connect_to_users():
    client = MongoClient("mongodb+srv://user:foodpassword@cluster0.xxngz.mongodb.net/foodApp?retryWrites=true&w=majority")
    db = client.foodApp
    return db.User

def create_user(request):
    users = connect_to_users()
    existing_user = users.find_one({'username': request['username']})
    print(existing_user)
    if existing_user is None:
        print("there is no user with that username")
        hashpass = bcrypt.hashpw(request['password'].encode('utf-8'), bcrypt.gensalt(14))
        users.insert_one({
            'email': request['email'],
            'username': request['username'],
            'password': hashpass,
            "favourites": [],
            "meal_plan": []})
        return True
    else:
        print("user already exists")
        return False

def log_in(request):
    print(request)
    users = connect_to_users()
    login_user = users.find_one({'username': request['username']})
    print(login_user)
    if login_user:
        if bcrypt.checkpw(request['password'].encode('utf-8'), login_user['password']):
            print("password matches")
            username = login_user['username']
            user_id = login_user['_id']
            return (username, str(user_id))
        else:
            print("password does not match")
    else:
        flash("Username does not exist")
        print("Username does not exist")  
    return False

def get_user(user_id):
    users = connect_to_users()
    return users.find_one({'_id': ObjectId(user_id)})

def get_favourites(user_id):
    users = connect_to_users()
    print(user_id)
    print(users.find_one({'_id': ObjectId(user_id)}))
    return users.find_one({'_id': ObjectId(user_id)})["favourites"]

def new_favourite(user_id, recipe_id):
    users = connect_to_users()
    users.update_one({'_id': ObjectId(user_id)}, {"$push": {"favourites": recipe_id}})

def delete_favourite(user_id, recipe_id):
    users = connect_to_users()
    users.update_one({'_id': ObjectId(user_id)}, {"$pull": {"favourites": recipe_id}})

def get_meal_plan(user_id):
    users = connect_to_users()
    return users.find_one({'_id': ObjectId(user_id)})["meal_plan"]

def new_meal_plan(user_id, new_plan):
    users = connect_to_users()
    users.update_one({'_id': ObjectId(user_id)}, {"$set": {"meal_plan": new_plan}})
