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
        user_id = request.args.get('user_id')

        try:
            (conn, cursor) = dbConnect()

            #Inner joined on follwer_id and user_id as the follower, getting the list user_id is following 
            cursor.execute("SELECT * FROM user INNER JOIN follow ON follow.following_id = user.id WHERE following_id=?", [user_id,])
            result = cursor.fetchall()
            # if (result != None):
            #     follows_info = []
            #     for follow in result:
            #         follows = {
            #             "userId": result[0],
            #             "email": result[3],
            #             "username": result[1],
            #             "birthdate": result[6],
            #             "bio": result[2]
            #         }
            #         follows.append(follows_info)
            return Response(json.dumps(result, default=str),
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
        following_id = request.json.get('following_id')
        login_token = request.json.get('loginToken')

        try:
            (conn, cursor) = dbConnect()
            if (login_token !=None and following_id != None):
                # Get user id of user who have successfully logged in 
                cursor.execute("SELECT user_id, loginToken, username FROM user_session INNER JOIN user ON user_session.user_id = user.id WHERE loginToken=?", [login_token,])
                user = cursor.fecthall() 
                user_id = user[0][0]
                # following_id equals the user_id we want to follow, follower_id equals the user_id of who is following you
                cursor.execute("INSERT INTO follows (following_id, follower_id) VALUES(?,?)", [user_id, following_id])
                conn.commit()
                return Response("Following",
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

    elif (request.method == 'DELETE'):
        conn = None
        cursor = None
        following_id = request.json.get('following_id')
        login_token = request.json.get('loginToken')

        try:
            (conn, cursor) = dbConnect()
            if (login_token !=None and following_id != None):
                cursor.execute("SELECT user_id, loginToken, username FROM user_session INNER JOIN user ON user_session.user_id = user.id WHERE loginToken=?", [login_token,])
                user = cursor.fecthall() 
                user_id = user[0][0]
                cursor.execute("DELETE FROM follows WHERE following_id? AND follower_id=?", [user_id, following_id])
                conn.commit()
                return Response("Unfollowed",
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
