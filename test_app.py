import json

def test_api_get_home(api):
    res = api.get('/')
    assert res.json == {'message': 'Hello from Community Cook API!'}
    assert res.status == '200 OK'

def test_api_new_recipe(api):
    mock_data = json.dumps({"Instructions": "", "dietary-req": [{"Vegan": True}, {"Vegetarian": True}, {"Pescatarian": False}, {"Gluten-free": False}, {"Dairy-free": False}, {"Nut-free": True}], "ingredients": [], "recipeDescription": "test", "recipeName": "test pasta"})
    mock_headers = {'Content-Type': 'application/json'}
    res = api.post('/recipes/new', data=mock_data, headers=mock_headers)
    assert 'New recipe added' in res.json['message']
    assert res.status == '201 CREATED'
    

def test_api_404(api):
    res = api.get('/incorrect_route')
    assert 'Error occurred' in res.json['message']
    assert res.status == '404 NOT FOUND'