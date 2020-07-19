from flask import Flask, request,  abort

from database.db import GraphDB
from models.user import User
from models.meal import Meal

app = Flask(__name__)

GraphDB.init_app(app)


@app.route('/meal-recommendation/user/<int:user_id>/get-meal', methods=['POST'])
def get_meal(user_id):
    req_data = request.json
    if not req_data:
        abort(400)
    return Meal.get_recommended_meals(user_id, req_data.get('cuisines'),
                                      req_data.get('medical_conditions'), req_data.get('allergies'))


@app.route('/meal-recommendation/user', methods=['POST'])
def add_user():
    req_data = request.json
    if not req_data:
        abort(400)
    assert 'name' in req_data
    assert 'age' in req_data
    return User.register_user(req_data.get('name'), req_data.get('age'))


if __name__ == '__main__':
    app.run(debug=True)
