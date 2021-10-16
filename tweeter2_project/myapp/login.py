import mariadb
from myapp import dbcreds
from flask import request, Response
import json
from myapp import app
from uuid import uuid4

from myapp.userEndpoint import user

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
def user_login():
    if (request.method == 'POST'):
        conn = None
        cursor = None
        email = request.json.get('email')
        password = request.json.get('password')
        
        try:
            (conn, cursor) = dbConnect()
            cursor.execute("SELECT * FROM user WHERE email=?",[email,])
            user = cursor.fetchall()
            conn.commit()
            if user['email'] == email and user['password'] == password:
                login_token = uuid4().hex
                print (login_token) 
                return Response(json.dumps(user, default=str),
                                mimetype="application/json",
                                status=200)  
            else: 
                return ("Login unsuccessful, please try again")
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
        login_token = request.json.get('')

        try:
            (conn, cursor) = dbConnect()
            cursor.execute("DELETE login_token FROM user_session")
            conn.commit()
            resp = {
               " loginToken" : login_token
            }
            return Response(json.dumps(resp),
                                mimetype="application/json",
                                status=200)
            
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
    else:
        return("Session end unsuccessful")