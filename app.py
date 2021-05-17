from flask import Flask, jsonify, request # type: ignore
from flask_cors import CORS, cross_origin # type: ignore
from flask_mail import Message, Mail # type: ignore
from werkzeug import exceptions # type: ignore
from models import recipes #type: ignore

app = Flask(__name__)
CORS(app)

app.config['CORS_HEADERS'] = 'Content-Type'

mail_settings = {
    "MAIL_SERVER": 'smtp.gmail.com',
    "MAIL_PORT": 465,
    "MAIL_USE_SSL": True,
    "MAIL_USERNAME": 'communitycookalerts@gmail.com',
    "MAIL_PASSWORD": 'FutureProof'
}

app.config.update(mail_settings)
mail = Mail(app)

@app.route('/', methods=['GET'])
@cross_origin()
def home():
    message = f"Hey there, come check out Lenny\'s new album!"
    subject = 'New Release 🔥'
    msg = Message(recipients=["james.wheadon@yahoo.com"], body=message, sender='CommunityCook', subject=subject)
    print(msg)
    mail.send(msg)
    return jsonify({'message': 'Hello from Community Cook API!'}), 200

@app.route('/recipes/new/', methods=['POST'])
@cross_origin()
def new_recipe():
    new_meal = request.data
    recipes.add_recipe(new_meal)
    return {'message': "New recipe added"}, 201

@app.route('/recipes/', methods=['GET'])
@cross_origin()
def get_recipes():
    query = request.query_string.decode()
    if query:
        dietary_reqs = query.split('&')
        diet_filter = {"diet_req": [req for req in dietary_reqs]}
        print(diet_filter)
        meals = recipes.get_recipes(diet_filter)
    else:
        meals = recipes.get_recipes()
    return jsonify(meals), 200

@app.route('/recipes/<recipe_id>', methods=['GET'])
@cross_origin()
def get_recipe(recipe_id):
    recipe = recipes.get_recipe(recipe_id)
    return jsonify(recipe), 200

@app.errorhandler(exceptions.NotFound)
def handle_404(err):
    return {'message': f'Error occurred: {err}'}, 404

@app.errorhandler(exceptions.InternalServerError)
def handle_500(err):
    return {'message': f'Error occurred: {err}'}, 500

print('test')
"""
msg = Message(subject="Hello",
        sender=app.config.get("MAIL_USERNAME"),
        recipients=["james.wheadon@yahoo.com"], # replace with your email for testing
        body="This is a test email I sent with Gmail and Python!")
mail.send(msg)"""

if __name__ == "__main__":
    app.run(debug=True)