from os import stat
import mariadb
from myapp import dbcreds
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

@app.route('/api/tweet-likes', methods=['POST','GET', 'DELETE'])
def tweetLikes():
    if (request.method == 'GET'):
        conn = None
        cursor = None
        tweet_id = request.args.get('tweetId')

        try:
            (conn, cursor) = dbConnect()
            cursor.execute("SELECT user_id, username FROM user INNER JOIN tweet_like ON tweet_like.user_id=user.id WHERE tweet_id=?", [tweet_id,])
            result = cursor.fetchall()
            if cursor.rowcount > 0:
                like_list = []
                for likes in result:
                    resp = {
                        "tweetId": tweet_id,
                        "userId": likes[0],
                        "username": likes[1]
                    }
                    like_list.append(resp)
            return Response(json.dumps(like_list, default=str),
                            mimetype="application/JSON",
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
        login_token = request.json.get('loginToken')
        tweet_id = request.json.get('tweet_id')

        try: 
            (conn, cursor) = dbConnect()
            cursor.execute("SELECT user_id, loginToken, username FROM user_session INNER JOIN user ON user_session.user_id = user.id WHERE loginToken=?", [login_token,])
            user = cursor.fetchall()
            user_id = user[0][0]
            if user[0][1] == login_token:
                cursor.execute("INSERT INTO tweet_like(tweet_id, user_id) VALUES(?,?)",[tweet_id, user_id])
                conn.commit()
                return Response("Liked Tweet",
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
        tweet_id = request.json.get('tweet_id')

        try: 
            (conn, cursor) = dbConnect()
            cursor.execute("SELECT user_id, loginToken FROM user_session INNER JOIN user ON user_session.user_id = user.id WHERE loginToken=?", [login_token,])
            user = cursor.fetchall()
            user_id = user[0][0]
            if user[0][1] == login_token:
                cursor.execute("DELETE FROM tweet_like WHERE tweet_id=? AND user_id=?",[tweet_id, user_id])
                conn.commit()
                return Response("Unliked Tweet",
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

