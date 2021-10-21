import mariadb
from myapp import dbcreds
from flask import request, Response
import json
from myapp import app
import datetime

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

@app.route('/api/comments', methods=['GET', 'POST', 'PATCH', 'DELETE'])
def comment():
    if (request.method == 'GET'):
        cursor = None
        conn = None
        tweet_id = request.args.get('tweet_id')

        try:
            (conn, cursor) = dbConnect()
            cursor.execute("SELECT * FROM comment INNER JOIN user ON user.id = comment.user_id INNER JOIN tweets ON comment.user_id = tweets.user_id WHERE tweet_id=?", [tweet_id,])
            comments = cursor.fetchall()
            return Response(json.dumps(comments, default=str),
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
        cursor = None
        conn = None
        login_Token = request.json.get('loginToken')
        tweet_id = request.json.get('tweet_id')
        content = request.json.get('content')

        try:
            (conn, cursor) = dbConnect()
            cursor.execute("SELECT user_id, loginToken, username FROM user_session INNER JOIN user ON user_session.user_id = user.id WHERE loginToken=?", [login_Token,])
            user = cursor.fetchall()
            user_id = user[0][0]
            created_At = datetime.datetime.now()
            if user[0][1] == login_Token:
                cursor.execute("INSERT INTO comment(user_id, tweet_id, content, created_At) VALUES(?,?,?,?)",[user_id, tweet_id, content, created_At])
                conn.commit()
                comment_id = cursor.lastrowid
                resp = {
                    "commentId": comment_id,
                    "tweetId": tweet_id,
                    "userId": user_id,
                    "username": user[0][2],
                    "content": content,
                    "createdAt": created_At
                }
                return Response(json.dumps(resp, default=str),
                                mimetype="application/json",
                                status=201)
            else:
                return Response("Action denied, you are not authenticated user",
                            mimetype="text/plain",
                            status=401)
        
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

    elif (request.method == 'PATCH'):
        cursor = None
        conn = None
        login_token = request.json.get('loginToken')
        comment_id = request.json.get('comment_id')
        content = request.json.get('content')

        try:
            (conn, cursor) = dbConnect()
            cursor.execute("SELECT user_id, loginToken, username FROM user_session INNER JOIN user ON user_session.user_id = user.id WHERE loginToken=?", [ login_token,])
            user = cursor.fetchall()
            user_id = user[0][0]
            # Need to get user_id associated to the comment_id
            cursor.execute("SELECT * FROM comment WHERE id=?",[comment_id,])
            commenter = cursor.fetchall()
            created_At = datetime.datetime.now()
            # To check permissio, verify login token as well as the user_id matches comment.user_id
            if user[0][1] == login_token and user_id == commenter[0][2]:
                cursor.execute("UPDATE comment SET content=? WHERE id=?", [content, comment_id,])
                conn.commit()
                editedComment = {
                    "commentId": comment_id,
                    "tweetId": commenter[0][1],
                    "userId": user_id,
                    "username": user[0][2],
                    "content": content,
                    "createdAt": created_At
                }
                return Response(json.dumps(editedComment, default=str),
                                mimetype="application/json",
                                status=20)
            else:
                return Response("Action denied, you are not authenticated user",
                                mimetype="text/plain",
                                status=401)

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
            cursor.execute("SELECT user_id, loginToken, username FROM user_session INNER JOIN user ON user_session.user_id = user.id WHERE loginToken=?", [ login_token,])
            user = cursor.fetchall()
            user_id = user[0][0]
            cursor.execute("SELECT * FROM comment WHERE id=?",[comment_id,])
            commenter = cursor.fetchall()
            if user[0][1] == login_token and user_id == commenter[0][2]:
                cursor.execute("DELETE FROM comment WHERE id=?", [comment_id])
                conn.commit()
                return Response("Comment deleted",
                                mimetype="text/html",
                                status=200)
            else:
                return Response("Action denied, you are not authenticated user",
                            mimetype="text/plain",
                            status=401)

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



