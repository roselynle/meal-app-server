from pymongo import MongoClient # type: ignore
import json

def connect_to_meals():
    client = MongoClient(username="user", password='password')
    db = client.foodApp
    return db.Meal

def connect_to_users():
    client = MongoClient(username="user", password='password')
    db = client.foodApp
    return db.User

test_meal_id = str(connect_to_meals().find_one()["_id"])
test_user_id = str(connect_to_users().find_one()["_id"])

def test_api_get_home(api):
    res = api.get('/')
    assert res.json == {'message': 'Hello from Community Cook API!'}
    assert res.status == '200 OK'

def test_api_new_recipe(api):
    mock_data = json.dumps({"instructions": "", "dietary-req": [{"Vegan": True}, {"Vegetarian": True}, {"Pescatarian": False}, {"Gluten-free": False}, {"Dairy-free": False}, {"Nut-free": True}], "ingredients": [], "recipeDescription": "test", "recipeName": "test pasta", "image_url": ""})
    mock_headers = {'Content-Type': 'application/json'}
    res = api.post('/recipes/new/', data=mock_data, headers=mock_headers)
    assert res.status == '201 CREATED'
    assert 'New recipe added' in res.json['message']

def test_api_get_recipes(api):
    res = api.get('/recipes/')
    assert res.json[0]["title"] == "test pasta"
    assert res.status == '200 OK'

def test_api_get_recipes_query(api):
    query = "gluten"
    res = api.get('/recipes/?' + query)
    assert len(res.json) == 1
    assert res.json[0]["title"] == "Pasta"
    assert res.status == '200 OK'

def test_api_get_recipes_id(api):
    res = api.get('/recipes/' + test_meal_id)
    assert res.json["title"] == "Pasta"
    assert res.status == '200 OK'

def test_api_new_favourite(api):
    mock_data = json.dumps({"recipe_id": test_meal_id})
    mock_headers = {'Content-Type': 'application/json'}
    res = api.patch('/user/' + test_user_id + '/favourites/new', data=mock_data, headers=mock_headers)
    assert "favourites updated" in res.json["message"]
    assert res.status == '201 CREATED'

def test_api_get_favourites(api):
    res = api.get('/user/' + test_user_id + '/favourites')
    assert res.json[-1]["title"] == "Pasta"
    assert res.status == '200 OK'

def test_api_new_meal_plan(api):
    mock_data = json.dumps({"body": json.dumps([test_meal_id] * 7)})
    mock_headers = {'Content-Type': 'application/json'}
    res = api.patch('/user/' + test_user_id + '/mealplan/new', data=mock_data, headers=mock_headers)
    assert "meal plan updated" in res.json["message"]
    assert res.status == '201 CREATED'

def test_api_get_meal_plan(api):
    res = api.get('/user/' + test_user_id + '/mealplan')
    assert res.json[0]["_id"] == test_meal_id
    assert res.status == '200 OK'

def test_api_404(api):
    res = api.get('/incorrect_route')
    assert 'Error occurred' in res.json['message']
    assert res.status == '404 NOT FOUND'

def test_api_500(api):
    res = api.get('/recipes/60')
    assert 'Error occurred' in res.json['message']
    assert res.status == '500 INTERNAL SERVER ERROR'