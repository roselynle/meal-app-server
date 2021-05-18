from bson.objectid import ObjectId #type: ignore
from flask import request, session, flash # type: ignore
from pymongo import MongoClient  # type: ignore
import bcrypt # type: ignore

def connect_to_users():
    client = MongoClient(username='user', password='password')
    db = client.foodApp
    return db.User

def create_user(request):
    users = connect_to_users()
    existing_user = users.find_one({'username': request.form['username']})
    print(existing_user)
    if existing_user is None:
        print("there is no user with that username")
        hashpass = bcrypt.hashpw(request.form['password'].encode('utf-8'), bcrypt.gensalt(14))
        users.insert_one({
            'email': request.form['email'],
            'username': request.form['username'],
            'password': hashpass, "favourites": []})
        session['username'] =  request.form['username']
    else:
        print("user already exists")
        flash(request.form['username'] + ' username already exists')

def log_in(request):
    users = connect_to_users()
    login_user = users.find_one({'username' : request.form['username']})
    print(login_user)
    if login_user:
        if bcrypt.checkpw(request.form['password'].encode('utf-8'), login_user['password']):
            print("password matches")
            session['username'] = request.form['username']
        else:
            flash("Password is incorrect, please try again")  
    else:
        flash("Username does not exist")

def get_favourites(user_id):
    users = connect_to_users()
    return users.find_one({'_id': ObjectId(user_id)})["favourites"]

def new_favourite(user_id, recipe_id):
    users = connect_to_users()
    users.update_one({'_id': ObjectId(user_id)}, {"$push": {"favourites": recipe_id}})