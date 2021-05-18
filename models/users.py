from flask import request, session, flash
from pymongo import MongoClient  # type: ignore
# import bcrypt
import json

def connect_to_users():
    client = MongoClient(username='user', password='password')
    db = client.foodApp
    return db.User

def create_user(request):
    users = connect_to_users()
    existing_user = users.find_one({'username': request['username']})
    print(existing_user)
    if existing_user is None:
        print("there is no user with that username")
        # hashpass = bcrypt.hashpw(request.form['password'].encode('utf-8'), bcrypt.gensalt(14))
        users.insert_one({
            'email': request['email'],
            'username': request['username'],
            'password': request['password']})
        # session['username'] =  request['username']
        return True
    else:
        print("user already exists")
        return False

def log_in(request):
    print(request)
    users = connect_to_users()
    # print(users)
    login_user = users.find_one({'username': request['username']})
    print(login_user)
    if login_user:
        if (request['password'] == login_user['password']):
            print("password matches")
            # session['username'] = request.form['username']
            username = login_user['username']
            return username
        else:
            print("password does not match")
    else:
        print("Username does not exist")  
    return False