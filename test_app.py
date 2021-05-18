import json

def test_api_get_home(api):
    res = api.get('/')
    assert res.json == {'message': 'Hello from Community Cook API!'}
    assert res.status == '200 OK'

def test_api_new_recipe(api):
    mock_data = json.dumps({"Instructions": "", "dietary-req": [{"Vegan": True}, {"Vegetarian": True}, {"Pescatarian": False}, {"Gluten-free": False}, {"Dairy-free": False}, {"Nut-free": True}], "ingredients": [], "recipeDescription": "test", "recipeName": "test pasta"})
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
    res = api.get('/recipes/60a3a76b2cbcf9c375520654')
    assert res.json["title"] == "Pasta"
    assert res.status == '200 OK'

def test_api_new_favourite(api):
    mock_data = json.dumps({"recipe_id": "60a3a76b2cbcf9c375520654"})
    mock_headers = {'Content-Type': 'application/json'}
    res = api.patch('/user/60a3a76a2cbcf9c375520653/favourites/new', data=mock_data, headers=mock_headers)
    assert "favourites updated" in res.json["message"]
    assert res.status == '201 CREATED'

def test_api_get_favourites(api):
    res = api.get('/user/60a3a76a2cbcf9c375520653/favourites')
    assert res.json[-1]["title"] == "Pasta"
    assert res.status == '200 OK'

def test_api_404(api):
    res = api.get('/incorrect_route')
    assert 'Error occurred' in res.json['message']
    assert res.status == '404 NOT FOUND'

def test_api_500(api):
    res = api.get('/recipes/60')
    assert 'Error occurred' in res.json['message']
    assert res.status == '500 INTERNAL SERVER ERROR'