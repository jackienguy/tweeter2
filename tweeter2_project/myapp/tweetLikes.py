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

@app.route('/api/tweetLikes', methods=['POST','GET', 'DELETE'])
def tweetLikes():
    if (request.method == 'GET'):
        conn = None
        cursor = None
        tweet_id = request.args.get('tweet_id')

        try:
            (conn, cursor) = dbConnect()
            cursor.execute("SELECT user_id, username FROM user INNER JOIN tweet_like ON tweet_like.user_id=user.id WHERE tweet_id=?", [tweet_id,])
            likes = cursor.fetchall()
            resp = {
                "tweetId": likes[0][0],
                "userId": likes[0][1],
                "username":''
            }
            return Response(json.dumps(resp, default=str),
                            mimetypes="application/JSON",
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
        return ("likes retrieved")

    elif (request.method == 'POST'):
        cursor = None
        conn = None
        login_token = request.json.get('loginToken')
        tweet_id = request.json.get('tweet_id')

        try: 
            (conn, cursor) = dbConnect()
            cursor.execute("SELECT user_id, loginToken FROM user_session INNER JOIN user ON user_session.user_id = user.id")
            user = cursor.fetchall()
            user_id = user[0][0]
            if user[0][1] == login_token:
                cursor.execute("INSERT INTO tweet_like(tweet_id, user_id) VALUES(?,?)",[tweet_id, user_id])
                conn.commit()
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
        return ("Tweet liked")

    elif (request.method == 'DELETE'):
        cursor = None
        conn = None
        login_token = request.json.get('loginToken')
        tweet_id = request.json.get('tweet_id')

        try: 
            (conn, cursor) = dbConnect()
            cursor.execute("SELECT user_id, loginToken FROM user_session INNER JOIN user ON user_session.user_id = user.id")
            user = cursor.fetchall()
            user_id = user[0][0]
            if user[0][1] == login_token:
                cursor.execute("DELETE FROM tweet_like WHERE tweet_id=? AND user_id=?",[tweet_id, user_id])
                conn.commit()
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
        return ("Unlike tweet")
