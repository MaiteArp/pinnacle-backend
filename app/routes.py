from flask import Blueprint, request, jsonify, make_response, session
from flask_bcrypt import Bcrypt
from app import db
from app.models.user import User
from app.models.session import Session
from app.models.preference import Preference
from app.models.challenge import Challenge
from sqlalchemy import desc

bcrypt = Bcrypt()
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
        password = bcrypt.generate_password_hash(request_body['password']).decode('utf-8')
        new_user = User(name=request_body['name'],
                        password=password)
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
        user = User.query.filter(User.name==request_body['name']).first()
        request_password = request_body['password']

    except KeyError:
        return make_response({
            "details": "invalid data"
            }, 400)
    
    if user is None:
        return make_response("no user", 404)
    actual_password = user.password

    if bcrypt.check_password_hash(actual_password, request_password):
        response = make_response({
                            "user": user.to_json()
                        }, 200)
        session['user_id'] = str(user.id) #session is dict we are setting key to id 
        response.set_cookie('user_id', str(user.id)) #for react purposes
        return response
    else:
        return make_response("no user", 404)

'''
Request Body: a JSON dict with name and password
Action: Matches user to the body passed in, 
Response: if no match returns no user, if match returns user dict and cookie
'''
##################################################################################

@users_bp.route("/<id>", methods=["PATCH"])
def update_user_best_time(id):
    auth_user = -1  # creates auth user so it can be referenced, sets it to neg 1 so it wont ever be valid in the db 
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
        
    if 'best_time' in request_body.keys():
        user.best_time = request_body['best_time']
    if 'theme' in request_body.keys():
        user.theme = request_body['theme']

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
#############################################################################

@users_bp.route("<id>", methods=["GET"])
def get_username_from_id(id):
    auth_user = -1
    try:
        auth_user = int(session['user_id'])
    except KeyError:
        return make_response("", 403)
    
    user = User.query.get(id)

    if user:
        return ({"name": user.name}, 200)
    return ({"errors":[f"User {id} not Found"]}, 404)
'''
Request Body: 
Action: 
Response: 
'''
########################################################################### CHALLENGE CRUD

@challenges_bp.route("", methods=["POST"])
def issue_new_challenge():
    auth_user = -1
    try:
        auth_user = int(session['user_id'])
    except KeyError:
        return make_response("", 403)

    request_body = request.get_json()

    try:
        destination = User.query.filter(User.name==request_body['challenged']).first()
        #                         User.password==request_body['password']).first()
    except KeyError:
        return make_response({
            "details": "invalid data"
            }, 400)
    
    if destination is None:
        return make_response("no user to challenge found", 404)
    
    challenge = Challenge( #here
        challenger_id=auth_user,
        destination_id=destination.id, 
        sent_time=request_body["best_time"],
        winner=None,
    )
    db.session.add(challenge) #here
    db.session.commit()
    return make_response(
        {
            "challenge": challenge.to_json() #made changes to this response
        }, 201) #might need this to answer the challenge
'''
Request Body: Json dict with 'challenged' and 'best_time'
Action: finds the id of the user and makes a new challenge, sets winner to none
Response: if not authorixed user returns 403, 
if no match returns no user, the id of the new challenge, the dict and cookie
'''
###################################################################################

@challenges_bp.route("/check/<id>", methods=["GET"])
def get_user_challenges(id):
    auth_user = -1
    try:
        auth_user = int(session['user_id'])
    except KeyError:
        return make_response("", 403)

    if auth_user != int(id):
        return make_response("", 403)

    request_body = request.get_json() # I dont think this is needed

    try:
        challenges = Challenge.query.filter(Challenge.destination_id==auth_user, 
                                            Challenge.winner==None).all() #? 
    except KeyError:
        return make_response({
            "details": "invalid data"
            }, 400)

    return make_response({"challenges": [challenge.to_json() for challenge in challenges]}, 200) 
'''
Request Body: no body
Action: finds the id of the user and winner that is none in challenge table
Response: if not authorixed user returns 403, 
and a dict with key challenges and a list value with the challenges, the dict and cookie
'''
###################################################################################

@challenges_bp.route("/<id>", methods=["PATCH"])
def update_challenge_winner(id):
    auth_user = -1  # creates auth user so it can be referenced, sets it to neg 1 so it wont ever be valid in the db 
    try:
        auth_user = int(session['user_id'])
    except KeyError:
        return make_response("", 403)
    
    request_body = request.get_json()
    
    challenge = Challenge.query.get(id)
    
    if challenge is None:
        return make_response("", 400)
    challenge.winner = request_body['winner']
    
    db.session.commit()

    return make_response(
        {
            "challenge": challenge.to_json()
        })
'''
Request Body: a JSON dict with everything and the 'winner'
Action: Matches user and updates the winner
Response: if not authorixed user returns 403, 
if no match returns, if match returns updated user dict and cookie
'''
################################################################################ 
