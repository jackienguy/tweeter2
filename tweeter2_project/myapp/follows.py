import mariadb
from myapp import dbcreds, login
from flask import request, Response
import json
from myapp import app

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

@app.route('/api/follows', methods=['GET', 'POST', 'DELETE'])
def getUserFollows():
    if (request.method == 'GET'):
        conn = None
        cursor = None
        id = request.args.get('id')

        try:
            (conn, cursor) = dbConnect()
            if id:
                cursor.execute("SELECT * FROM user INNER JOIN follow ON follow.following_id =?", [id,])
                result = cursor.fetchall()
                return Response(json.dumps(result, default=str),
                            mimetype="application/json",
                            status=200)
            else:
                return("Something went wrong, can't get follows")

        except ConnectionError:
            print("Error occured trying to connect to database")
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
        return("Follows retrieved")
    
    elif (request.method == 'POST'):
        conn = None
        cursor = None
        following_id = request.json.get('following_id')
        login_token = request.json.get('loginToken')

        try:
            (conn, cursor) = dbConnect()
            if login_token !="":
                cursor. execute("SELECT user_id FROM user_session WHERE loginToken=?", [login_token])


        except ConnectionError:
            print("Error occured trying to connect to database")
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
        return("Follows retrieved")
    
    elif (request.method == 'DELETE'):
        conn = None
        cursor = None
        following_id = request.json.get('following_id')
        login_token = request.json.get('loginToken')

        try:
            (conn, cursor) = dbConnect()
            if (request.json.get('loginToken' != None)):
                cursor. execute("SELECT user_id FROM user_session WHERE loginToken=?", [login_token])
                userId = cursor.fetchall()
                cursor.execute("DELETE FROM follows WHERE user_id? AND following_id=?", [userId, following_id])
                conn.commit()

        except ConnectionError:
            print("Error occured trying to connect to database")
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
        return("Unfollowed user")