import json

def test_api_get_home(api):
    res = api.get('/')
    assert res.json == {'message': 'Hello from Community Cook API!'}
    assert res.status == '200 OK'