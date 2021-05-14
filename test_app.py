import json

def test_api_get_home(api):
    res = api.get('/')
    assert res.json == {'message': 'Hello from Community Cook API!'}
    assert res.status == '200 OK'

def test_api_404(api):
    res = api.get('/incorrect_route')
    assert 'Error occurred' in res.json['message']
    assert res.status == '404 NOT FOUND'