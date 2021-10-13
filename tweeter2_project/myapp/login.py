import mariadb
from myapp import dbcreds
from flask import Flask, request, Response
import json
import re
from myapp import app

app = Flask(__name__)

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

# @app.route('/login', methods=['DELETE'])
# def login():
#     if (request.method == 'POST'):
#         conn = None
#         cursor = None
#         username = request.json.get('username')
#         password = request.json.get('password')

#        try:
#            (conn, cursor) = dbConnect()
#             cursor.execute("SELECT * FROM user WHERE username=?",[username,])


def delete_login_session():
    if (request.method == 'DELETE'):
        conn = None
        cursor = None

        try:
            (conn, cursor) = dbConnect()
            cursor.execute("DELETE login_token FROM user_session")
            conn.commit()
            cursor.close()
            
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