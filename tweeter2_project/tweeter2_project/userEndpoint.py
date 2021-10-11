import mariadb
import dbcreds
from flask import Flask, request, Response
import json

app = Flask(__name__)

def DbConnection():
    
    conn = None
    cursor = None

    try:
        conn = mariadb.connect(
                                user=dbcreds.user,
                                password=dbcreds.password,
                                host=dbcreds.host,
                                port=dbcreds.port,
                                database=dbcreds.database)
        cursor = conn.cursor()
    except:
        if (cursor != None):
            cursor.close()
        if (conn != None):
            conn.rollback()
            conn.close()
        else:
            print("Connection failed")

@app.route('/user', methods=['GET','POST','PATCH','DELETE'])
def user_handle():
    conn = None
    cursor = None
    if (request.method == 'GET'):
        conn = mariadb.connect(
                                user=dbcreds.user,
                                password=dbcreds.password,
                                host=dbcreds.host,
                                port=dbcreds.port,
                                database=dbcreds.database)
        cursor = conn.cursor()

        cursor.execute("SELECT * FROM user")
        result = cursor.fetchall()
        cursor.close()
        conn.close()

        user_info = request.args 
        print( user_data)
        return Response(json.dumps( user_data),
                        mimetype="application/json",
                        status=200)

    elif (request.method == 'POST'):
        user_data = request.json 
        user_username = user_data.get("username")
        user_password = user_data.get("password")
        user_bio = user_data.get("bio")
        user_email = user_data.get("email")
        user_birthdate = user_data.get("birthdate")
        cursor = conn.cursor()
        cursor.execute("INSERT INTO user(username, password, bio, email, birthdate) VALUES(?,?,?,?,?)", [ user_username, user_password,  user_bio, user_email,  user_birthdate])
        conn.commit()
        cursor.close()
        return 'User created'
        print(user_data)
        return Response(json.dumps(user_data, user_username, user_password, user_bio, user_email, user_birthdate),
                    mimetype="application/json",
                    status=200)
        
 


        