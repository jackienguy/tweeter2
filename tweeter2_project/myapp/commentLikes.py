from os import stat
import mariadb
from myapp import dbcreds
from flask import request, Response
import json
from myapp import app
from myapp.comments import comment

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

@app.route('/api/comment-likes', methods=['GET','POST', 'DELETE'])
def commentLikes():
    if (request.method == 'GET'):
        conn = None
        cursor = None
        comment_id = request.args.get('comment_id')

        try:
            (conn, cursor) = dbConnect()
            cursor.execute('SELECT user_id, username FROM user INNER JOIN comment_like on comment_like.user_Id = user.id WHERE comment_id=?',[comment_id,])
            result = cursor.fetchall()
            likes = {
            "commentId": comment_id,
            "userId": result[0][0],
            "username": result[0][1]
             }
            return Response(json.dumps(likes, default=str),
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
        login_token = request.json.get('loginToken')
        comment_id = request.json.get('comment_id')

        try: 
            (conn, cursor) = dbConnect()
            cursor.execute("SELECT user_id, loginToken, username FROM user_session INNER JOIN user ON user_session.user_id = user.id WHERE loginToken=?", [login_token,])
            user = cursor.fetchall()
            user_id = user[0][0]
            if user[0][1] == login_token:
                cursor.execute("INSERT INTO comment_like(comment_id, user_id) VALUES(?,?)",[comment_id, user_id])
                conn.commit()
                resp = {
                    "commentId": comment_id,
                    "userId": user_id,
                    "username": user[0][2]              
                }
                return Response(json.dumps(resp),
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
        cursor = None
        conn = None
        login_token = request.json.get('loginToken')
        comment_id = request.json.get('comment_id')

        try: 
            (conn, cursor) = dbConnect()
            cursor.execute("SELECT user_id, loginToken FROM user_session INNER JOIN user ON user_session.user_id = user.id WHERE loginToken=?", [login_token,])
            user = cursor.fetchall()
            user_id = user[0][0]
            cursor.execute("SELECT user_id FROM comment_like WHERE comment_Id=?",[comment_id,])
            liker = cursor.fetchall()
            if user[0][1] == login_token and user_id == liker[0][0]:
                cursor.execute("DELETE FROM comment_like WHERE comment_Id=?",[comment_id,])
                conn.commit()
                return Response("Unliked comment",
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





