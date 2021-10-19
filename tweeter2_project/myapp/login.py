import mariadb
from myapp import dbcreds
from flask import request, Response
import json
from myapp import app
import secrets
from werkzeug.security import generate_password_hash, check_password_hash

def dbConnect():
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
            conn.close()
        else:
            return ('Connection failed')
    
    return (conn, cursor)

@app.route('/api/login', methods=['POST','DELETE'])
def login_session():
    if (request.method == 'POST'):
        conn = None
        cursor = None
        email = request.json.get('email')
        password = request.json.get('password')
        user_id = request.json.get('user_id')
        user = None
        
        try:
            (conn, cursor) = dbConnect()
            cursor.execute("SELECT * FROM user WHERE email=?",[email,])
            conn.commit()
            user = cursor.fetchall()
            login_token = secrets.token_hex(16)
            print (login_token) 
            if (user != None): #If user exist
                if check_password_hash(user.password, password): #Want to check the password entered equals password stored  
                    cursor.execute("INSERT INTO user_session(user_id, loginToken) VALUES(?,?)", [user_id, login_token])
                    conn.commit()
                    resp = {
                        "userId" : user_id,
                        "username": user[1],
                        "email" : user[3],
                        "bio": user[2],
                        "birthdate": user[6],
                        "loginToken ": login_token
                    }
                return Response(json.dumps(resp, default=str),
                                mimetype="application/json",
                                status=200)  
            else: 
                return ("Username or password inccorect, please try again")
        except ValueError as error:
            print("Error" +str(error))
        except mariadb.DataError:
            print("something went wrong with your data")
        except mariadb.OperationalError:
            print("opertational error on the connection")
        except mariadb.ProgrammingError:
            print("apparently, you don't know how to code")
        except mariadb.IntegrityError:
            print("Error with DB integrity. most likelu constraint failure")
        except:
            print("Something went wrong")

        finally:
            if (cursor != None):
                cursor.close()
            if (conn != None):
                conn.rollback()
                conn.close()
            else:
                print("Failed to read data")

        return ("Login success")

    elif (request.method == 'DELETE'):
        conn = None
        cursor = None
        login_token = request.json.get('loginToken')

        try:
            (conn, cursor) = dbConnect()
            cursor.execute("DELETE * FROM user_session WHERE loginToken=?", [login_token,])
            conn.commit()
          
        except mariadb.DataError:
            print("something went wrong with your data")
        except mariadb.OperationalError:
            print("opertational error on the connection")
        except mariadb.ProgrammingError:
            print("apparently, you don't know how to code")
        except mariadb.IntegrityError:
            print("Error with DB integrity. most likelu constraint failure")
        except:
            print("Something went wrong")

        finally:
            if (cursor != None):
                cursor.close()
            if (conn != None):
                conn.rollback()
                conn.close()
            else:
                print("Failed to read data")
    return Response("You are logged out",
                    mimetype="application/json",
                    status=200)