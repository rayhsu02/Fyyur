import os
from flask import Flask, request, jsonify, abort
from sqlalchemy import exc
import json
from flask_cors import CORS
from werkzeug.wrappers import BaseResponse

from .database.models import db_drop_and_create_all, setup_db, Drink
from .auth.auth import AuthError, requires_auth

app = Flask(__name__)
setup_db(app)
CORS(app)

'''
@TODO uncomment the following line to initialize the datbase
!! NOTE THIS WILL DROP ALL RECORDS AND START YOUR DB FROM SCRATCH
!! NOTE THIS MUST BE UNCOMMENTED ON FIRST RUN
'''
# db_drop_and_create_all()

# ROUTES


@app.route('/drinks')
def get_drinks():
    try:
        drinks = Drink.query.all()
        formated_drinks = [drink.short() for drink in drinks]

        return jsonify({
            'success': True,
            'drinks': formated_drinks
        })
    except BaseException as e:
        print(e)
        abort(422)


@app.route('/drinks-detail')
@requires_auth('get:drinks-detail')
def get_drinks_detail(jwt):
    try:
        drinks = Drink.query.all()
        formated_drinks = [drink.long() for drink in drinks]

        return jsonify({
            'success': True,
            'drinks': formated_drinks
        })
    except BaseException as e:
        print(e)
        abort(422)


@app.route('/drinks', methods=['POST'])
@requires_auth('post:drinks')
def create_drink(jwt):
    try:
        body = request.get_json()
        title = body.get('title', None)
        recipe = body.get('recipe', None)

        if title is NotImplemented or recipe is None:
            abort(400)

        new_drink = Drink(title=title, recipe=json.dumps(recipe))
        Drink.insert(new_drink)
        drinks = Drink.query.all()
        formated_drink = [drink.long() for drink in drinks]
        return jsonify({
            'success': True,
            'drinks': formated_drink
        })
    except BaseException as e:
        print(e)
        abort(422)


@app.route('/drinks/<int:id>', methods=['PATCH'])
@requires_auth('patch:drinks')
def update_drink(jwt, id):
    try:
        drink = Drink.query.filter(Drink.id == id).one_or_none()

        if drink is None:
            abort(404, 'Resource can not be found.')

        body = request.get_json()
        title = body.get('title', None)
        recipe = body.get('recipe', None)

        if title:
            drink.title = title
        if recipe:
            drink.recipe = json.dumps(recipe)

        drink.update()

        drinks = Drink.query.all()
        formated_drinks = [drink.long() for drink in drinks]
        return jsonify({
            'success': True,
            'drinks': formated_drinks
        })

    except BaseException as e:
        print(e)
        abort(400)


@app.route('/drinks/<int:id>', methods=["DELETE"])
@requires_auth('delete:drinks')
def delete_drink(jwt, id):
    try:
        drink = Drink.query.filter(Drink.id == id).one_or_none()
        if drink is None:
            abort(404, 'Resource can not be found')
        drink.delete()
        return jsonify({
            'success': True,
            'delete': id
        })

    except BaseException as e:
        print(e)
        abort(422)


# Error Handling
'''
Example error handling for unprocessable entity
'''


@app.errorhandler(422)
def unprocessable(error):
    return jsonify({
        "success": False,
        "error": 422,
        "message": "unprocessable"
    }), 422


@app.errorhandler(400)
def handle_400(error):
    return jsonify({
        'success': False,
        'error': 400,
        'message': 'Error in patching'
    }), 400


@app.errorhandler(404)
def handle_notfound(error):
    return jsonify({
        'success': False,
        'error': 404,
        'message': 'Resource not found'
    }), 404


@app.errorhandler(500)
def handle_500(error):
    return jsonify({
        'success': False,
        'error': 500,
        'message': 'Server error'
    }), 500


@app.errorhandler(AuthError)
def handle_auth_error(exception):
    print(exception)
    response = jsonify(exception.error)
    response.status_code = exception.status_code

    return response, exception.status_code
