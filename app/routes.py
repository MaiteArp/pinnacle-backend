from flask import Blueprint, request, jsonify, make_response, session
from app import db
from app.models.user import User
from app.models.session import Session
from app.models.preference import Preference
from app.models.challenge import Challenge
from sqlalchemy import desc


users_bp = Blueprint('users', __name__, url_prefix="/app/users")
sessions_bp = Blueprint('sessions', __name__, url_prefix="/app/sessions")
preferences_bp = Blueprint('preferences', __name__, url_prefix="/app/preferences")
challenges_bp = Blueprint('challenges', __name__, url_prefix="/app/challenges")
root_bp = Blueprint('root', __name__, url_prefix="/app")

############################################################################## HEALTH CHECK
@root_bp.route("/check", methods=["GET"])
def get_health_check():
    response = {
        "healthy": True,
    }
    return make_response(jsonify(response), 200)

############################################################################## USER CRUD

@users_bp.route("", methods=["POST"])
def create_single_user():
    request_body = request.get_json()
    try:
        new_user = User(name=request_body['name'],
                        password=request_body['password'])
    except KeyError:
        return make_response({
            "detials": "invalid data"
        }, 400)
    db.session.add(new_user)
    db.session.commit()
    response = {
        "user": new_user.to_json()
    }
    return make_response(jsonify(response), 201)
'''
Request Body: a JSON dict with 'name and 'password' 
Action: Creates new user with said name and password. Throws 400 error if missing details
Response: 200 Created. resturns JSON dict with key user, 
which value is in another dict detailing info (user id, name, password)
'''
#############################################################################

@users_bp.route("/login", methods=["POST"])
def login_user():
    request_body = request.get_json()
    try:
        user = User.query.filter(User.name==request_body['name'],
                                User.password==request_body['password']).first()
    except KeyError:
        return make_response({
            "details": "invalid data"
            }, 400)
    
    if user is None:
        return make_response("no user", 404)
    response = make_response({
                        "user": user.to_json()
                    }, 200)
    session['user_id'] = str(user.id) #session is dict we are setting key to id 
    response.set_cookie('user_id', str(user.id)) #for react purposes
    return response
'''
Request Body: a JSON dict with name and password
Action: Matches user to the body passed in, 
Response: if no match returns no user, if match returns user dict and cookie
'''
##################################################################################

@users_bp.route("/<id>", methods=["PATCH"])
def update_user_best_time(id):
    auth_user = -1
    try:
        auth_user = int(session['user_id'])
    except KeyError:
        return make_response("", 403)
    if auth_user != int(id):
        return make_response("", 403)
    
    request_body = request.get_json()
    
    user = User.query.get(id)
    
    if user is None:
        return make_response("", 404)
    user.best_time = request_body['best_time']
    
    db.session.commit()

    return make_response(
        {
            "user": user.to_json()
        })
'''
Request Body: a JSON dict with user and best time
Action: Matches user and updates their best time
Response: if not authorixed user returns 403, 
if no match returns no user, if match returns updated user dict and cookie
'''
##################################################################################

@users_bp.route("/<id>/deposit", methods=["POST"])
def deposit_user_coins(id):
    auth_user = -1
    try:
        auth_user = int(session['user_id'])
    except KeyError:
        return make_response("", 403)
    
    if auth_user != int(id):
        return make_response("", 403)
    
    request_body = request.get_json()

    user = User.query.with_for_update().get(id) #'with_for_update()' locks the db row so noone can use the data until done updating

    user.coins += request_body['amount']

    db.session.commit()

    return make_response(
        {
            "user": user.to_json()
        })
'''
Request Body: a JSON dict with user and coin amount
Action: Matches user and updates their coins
Response: if not authorixed user returns 403, 
if no match returns no user, if match returns updated user dict and cookie
'''
###################################################################################






