from flask import Blueprint, request, jsonify, make_response
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

############################################################################## CRUD

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

@users_bp.route("/<id>", methods=["GET"])
def get_single_user(id):
    user = User.query.get(id)
    if user is None:
        return make_response("", 404)
    return {
        "user": user.to_json()
    }

'''
Request body: None, requested user specified in path.
Action: Gets user of ID, returns 404 if no user found
Response: 200 ok, returns JSON dict with key user and 
value detailing info (user id, name, password)
'''

@users_bp.route("/<id>", methods=["PUT"])
def update_user(id):
    pass
    
# @users_bp.route("/<id>", methods=["DELETE"])
# def delete_single_user(id):
#     pass 
#not sure I want to delete users





