from database import get_user, init_user
# from serverTypes import ResSendObject (Python doesn't typically use type imports like this, but you can use Python type hints)
from flask import jsonify
import bcrypt

def handle_login(login_data):
    try:
        user = get_user(login_data["username"])
        if user:
            if bcrypt.checkpw(login_data["password"].encode('utf-8'), user["password"].encode('utf-8')):
                info = {
                    "message": "Login successful",
                    "status": 200,
                    "data": {
                        "username": user["username"],
                        "internal_id": user["internal_id"],
                        "socket": user["socket"],
                        "latest_connect": user["latest_connect"],
                        "first_connection": user["first_connection"]
                    }
                }
                return jsonify(info), 200
            else:
                info = {
                    "message": "Wrong password or username",
                    "status": 401
                }
                return jsonify(info), 401
        else:
            info = {
                "message": "Wrong password or username",
                "status": 401
            }
            return jsonify(info), 401
    except Exception as e:
        info = {
            "message": "Wrong password or username",
            "status": 401
        }
        return jsonify(info), 401
    
def handle_new_user(user_data):
    try:
        user = get_user(user_data["username"])
        if user:
            info = {
                "message": "User already exists",
                "status": 409
            }
            return jsonify(info), 409
        else:
            new_user = init_user(user_data)
            info = {
                "message": "User created",
                "status": 200,
                "data": {
                    "username": new_user["username"],
                    "internal_id": new_user["internal_id"],
                    "socket": new_user["socket"],
                    "latest_connect": new_user["latest_connection"],
                    "first_connection": new_user["first_connection"]
                }
            }
            return jsonify(info), 200
    except Exception as e:
        print(e)
        info = {
            "message": "Error creating user",
            "status": 500
        }
        return jsonify(info), 500