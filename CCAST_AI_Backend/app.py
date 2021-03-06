from re import S
import jwt
import os
from dotenv import load_dotenv
from flask import Flask, request, jsonify

from validate import validate_email_and_password, validate_user
from AIController import *

from models import User
from auth_middleware import token_required
load_dotenv()


# Cors

config = {
    'ORIGINS': ['*']
}


app = Flask(__name__)
#SECRET_KEY = os.environ.get('SECRET_KEY')
SECRET_KEY = "saZfoJSQGAXeixoIt3MJFz4Tu5FaLi24"
#print("URL = ", os.environ.get('REACT_APP_API_URL'))
app.config['SECRET_KEY'] = SECRET_KEY
controller = AiController()


@app.after_request
def after_request(response):
    response.headers.add('Access-Control-Allow-Origin', '*')
    response.headers.add('Access-Control-Allow-Headers',
                         'Content-Type,Authorization')
    response.headers.add('Access-Control-Allow-Methods',
                         'GET,PUT,POST,DELETE,OPTIONS')
    response.headers.add('Access-Control-Allow-Credentials', 'true')
    return response


@app.route("/")
def hello():
    return "Hello World!"

# -------------------------------------------------------------------------------------------------------
# Authentication


@app.route("/users/", methods=["POST"])
def add_user():
    try:
        details = request.json
        if not details:
            return {
                "message": "Please provide user details",
                "data": None,
                "error": "Bad request"
            }, 400
        is_validated = validate_user(**details)
        if is_validated is not True:
            return dict(message='Invalid data', data=None, error=is_validated), 400
        user = User().create(**details)
        if not user:
            return {
                "message": "User already exists",
                "error": "Conflict",
                "data": None
            }, 409
        return {
            "message": "Successfully created new user",
            "data": user.email
        }, 201
    except Exception as e:
        return {
            "message": "Something went wrong",
            "error": str(e),
            "data": None
        }, 500


@app.route("/users/login", methods=["POST"])
def login():
    try:
        data = request.json
        if not data:
            return {
                "message": "Please provide user details",
                "data": None,
                "error": "Bad request"
            }, 400
        # validate input
        is_validated = validate_email_and_password(
            data.get('email'), data.get('password'))
        if is_validated is not True:
            return dict(message='Invalid username or password', data=None, error=is_validated), 400
        user = User().login(
            data["email"],
            data["password"]
        )
        if user:
            try:
                # token should expire after 24 hrs
                user.token = jwt.encode(
                    {"user_id": user.id},
                    app.config["SECRET_KEY"],
                    algorithm="HS256"
                )
                return {
                    "message": "Successfully fetched auth token",
                    "data": {
                        "id": user.id,
                        "name": user.name,
                        "email": user.email,
                        "marketToken": user.marketToken,
                        "marketSecret": user.marketSecret,
                        "accessToken": user.token
                    }
                }
            except Exception as e:
                return {
                    "error": "Something went wrong",
                    "message": str(e)
                }, 500
        return {
            "message": "Invalid email or password, Authentication failed.",
            "data": None,
            "error": "Unauthorized"
        }, 404
    except Exception as e:
        return {
            "message": "Something went wrong!",
            "error": str(e),
            "data": None
        }, 500


@app.route("/users/", methods=["GET"])
def get_current_user(current_user):
    return jsonify({
        "message": "successfully retrieved user profile",
        "data": current_user
    })


@app.route("/users/", methods=["PUT"])
def update_user(current_user):
    try:
        user = request.json
        if user.get("name"):
            user = User().update(current_user["_id"], user["name"])
            return jsonify({
                "message": "successfully updated account",
                "data": user
            }), 201
        return {
            "message": "Invalid data, you can only update your account name!",
            "data": None,
            "error": "Bad Request"
        }, 400
    except Exception as e:
        return jsonify({
            "message": "failed to update account",
            "error": str(e),
            "data": None
        }), 400


@app.route("/users/", methods=["DELETE"])
def disable_user(current_user):
    try:
        User().disable_account(current_user["_id"])
        return jsonify({
            "message": "successfully disabled acount",
            "data": None
        }), 204
    except Exception as e:
        return jsonify({
            "message": "failed to disable account",
            "error": str(e),
            "data": None
        }), 400


@app.errorhandler(403)
def forbidden(e):
    return jsonify({
        "message": "Forbidden",
        "error": str(e),
        "data": None
    }), 403


@app.errorhandler(404)
def forbidden(e):
    return jsonify({
        "message": "Endpoint Not Found",
        "error": str(e),
        "data": None
    }), 404


@app.route("/users/token", methods=["POST"])
def setMarketToken():
    try:
        data = request.json
        if not data:
            return {
                "message": "Please provide market details",
                "data": None,
                "error": "Bad request"
            }, 400
        print(data)

        success = User().setMarketDetails(
            data["email"],
            data["token"],
            data["secret"]
        )
        if not success:
            return {
                "message": "Something went wrong",
                "error": "Error",
                "data": None
            }, 500
        return {
            "message": "Successfully stored market details"
        }, 201
    except Exception as e:
        return {
            "message": "Something went wrong",
            "error": str(e),
            "data": None
        }, 500

# -------------------------------------------------------------------------------------------------------
# AI controls


@app.route("/ai/startReal", methods=["POST"])
def startAIReal():
    data = request.json
    if not data:
        return {
            "message": "Please provide user details",
            "data": None,
            "error": "Bad request"
        }, 400
    # controller.add_Pair(data.get('id'), 0, data.get(
    #    'token'), data.get('secret'), "ETH/BTC")
    controller.add_Pair_Read(data.get('id'), 0, data.get('token'), data.get('secret'))

    return "Started Real Successfully"


@app.route("/ai/startFake", methods=["POST"])
def startAIFake():
    data = request.json
    if not data:
        return {
            "message": "Please provide user details",
            "data": None,
            "error": "Bad request"
        }, 400
    controller.add_Pair_Read(
        data.get('id'), 
        1, 
        data.get('marketToken'), 
        data.get('marketSecret'))
    return "Started Dummy Successfully"


@app.route("/ai/stop", methods=["POST"])
def stopAI():
    data = request.json
    if not data:
        return {
            "message": "Please provide user details",
            "data": None,
            "error": "Bad request"
        }, 400
    controller.remove_Pair(data.get('id'))
    return "Stopped Successfully"


@app.route("/ai/status", methods=["POST"])
def getStatus():
    try:
        data = request.json
        if not data:
            return {
                "message": "Please provide user details",
                "data": None,
                "error": "Bad request"
            }, 400
    # return controller.status(data.get('id'))

        status = controller.status(data.get('id'))

        if status == 'Live' or status == 'Dummy' or status == 'Idle':

            return {
                "message": "Successfully retrieved information",
                "data": status
            }, 201

        return {
            "message": "An Internal Error has occured",            
            "data": status
        }, 400
    except Exception as e:
        return {
            "message": "An Internal Error has occured",
            "error": str(e),
            "data": None
        }, 500


@app.route("/ai/info", methods=["POST"])
def getInfo():

    try:
        data = request.json      
        info = controller.info(data.get('id'))

        if info != "No Data Retrieved":
            return {
                "message": "Successfully retrieved information",
                "data": info
            }, 201

        else:
            return {
                "message": "An error occured while retrieving information.",
                "data": info
            }, 400

    except Exception as e:
        return {
            "message": "An Internal Error has occured",
            "error": str(e),
            "data": None
        }, 500


if __name__ == "__main__":
    app.run(debug=True)
