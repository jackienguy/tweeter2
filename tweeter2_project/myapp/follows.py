import mariadb
from myapp import dbcreds, login
from flask import request, Response
import json
from myapp import app
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

@app.route('/api/follows', methods=['GET', 'POST', 'DELETE'])
def UserFollows():
    if (request.method == 'GET'):
        conn = None
        cursor = None
        user_id = request.args.get('userId')

        try:
            (conn, cursor) = dbConnect()
            #Inner joined on follwer_id and user_id as the follower, getting the list user_id is following 
            cursor.execute("SELECT * FROM user INNER JOIN follow ON follow.following_id = user.id WHERE following_id=?", [user_id,])
            result = cursor.fetchall()
            if cursor.rowcount >0:
                follows_info = []
                for follow in result:
                    follows = {
                        "userId": follow[0],
                        "email": follow[3],
                        "username": follow[1],
                        "birthdate": follow[5],
                        "bio": follow[2]
                    }
                    follows_info.append(follows)
            return Response(json.dumps(follows_info, default=str),
                        mimetype="application/json",
                        status=200)

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
        return Response("Error something went wrong",
                        mimetype="text/plain",
                        status=500)

    
    elif (request.method == 'POST'):
        conn = None
        cursor = None
        following_id = request.json.get('followingId')
        login_token = request.json.get('loginToken')

        try:
            (conn, cursor) = dbConnect()
            # Get user id of user who have successfully logged in 
            cursor.execute("SELECT user_id, loginToken, username FROM user_session INNER JOIN user ON user_session.user_id = user.id WHERE loginToken=?", [login_token,])
            user = cursor.fetchall() 
            user_id = user[0][0]
            if user[0][1] == login_token:
                # following_id equals the user_id we want to follow, follower_id equals the user_id of who is following you
                cursor.execute("INSERT INTO follow (following_id, follower_id) VALUES(?,?)", [user_id, following_id])
                conn.commit()
                return Response("Following user",
                                mimetype="text/html",
                                status=200)
            else:
                return Response("Action denied, you are not authenticated user",
                            mimetype="text/plain",
                            status=400)

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
        return Response("Error something went wrong",
                        mimetype="text/plain",
                        status=500)

    elif (request.method == 'DELETE'):
        conn = None
        cursor = None
        following_id = request.json.get('followingId')
        login_token = request.json.get('loginToken')

        try:
            (conn, cursor) = dbConnect()
            cursor.execute("SELECT user_id, loginToken, username FROM user_session INNER JOIN user ON user_session.user_id = user.id WHERE loginToken=?", [login_token,])
            user = cursor.fetchall() 
            user_id = user[0][0]
            if user[0][1] == login_token:
                cursor.execute("DELETE FROM follows WHERE follower_id=?", [following_id,])
                conn.commit()
                return Response("Unfollowed user",
                                mimetype="text/html",
                                status=200)

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
        return Response("Error something went wrong",
                        mimetype="text/plain",
                        status=500)
