import mariadb
from myapp import dbcreds
from flask import request, Response
import json
from myapp import app

# POST to log in user with username and password combo
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
def login():
    if (request.method == 'POST'):
        conn = None
        cursor = None
        username = request.json.get('username')
        password = request.json.get('password')
        login_token = 123

        try:
            (conn, cursor) = dbConnect()
            cursor.execute("SELECT * FROM user WHERE username=?",[username,])
            result = cursor.fetchall()
            return Response(json.dumps(result, default=str),
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
        return ("Login failed")

def delete_login_session():
    if (request.method == 'DELETE'):
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