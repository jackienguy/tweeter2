from flask import Flask, request, Response
import json

app = Flask(__name__)

@app.route('/user', methods=['GET','POST','PATCH','DELETE'])
def login():
    if (request.method == 'POST'):
        user_data = request.json 
        user_username = user_data.get("username")
        user_password = user_data.get("password")
        user_bio = user_data.get("bio")
        user_email = user_data.get("email")
        user_birthdate = user_data.get("birthdate")
        print(user_data)
        return Response(json.dumps(user_data, user_username, user_password, user_bio, user_email, user_birthdate),
                    mimetype="application/json",
                    status=200)
    elif (request.method == 'GET'):
        user_params = request.args 
        print(user_params)
        return Response(json.dumps(user_params),
                        mimetype="application/json",
                        status=200)
        print("got your into")