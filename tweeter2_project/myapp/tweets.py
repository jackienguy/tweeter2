from datetime import datetime
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

@app.route('/api/tweets', methods=['GET', 'POST', 'PATCH', 'DELETE'])
def tweets():
    if (request.method == 'POST'):
        cursor = None
        conn = None
        login_token = request.json.get('loginToken')
        content = request.json.get('content')
        tweet_id = None

        try:
            (conn, cursor) = dbConnect()
            cursor.execute("SELECT user_id, username FROM user INNER JOIN user_session ON user_session.user_id = user.id WHERE user_session.loginToken=?", [login_token,])
            user = cursor.fetchall()
            created_At = datetime.datetime.now()
            user_id = user[0][0]
            cursor.execute("INSERT INTO tweets(user_id, content, created_At) VALUES(?,?,?)",[user_id, content, created_At])
            conn.commit()
            tweet_id = cursor.lastrowid
            createTweet = {
                "tweetId": tweet_id,
                "userId": user[0][0],
                "username": user[0][1],
                "content": content,
                "createdAt": created_At
            }
            return Response(json.dumps(createTweet, default=str),
                            mimetype="applications/json",
                            status=200)

        except ValueError as error:
            print("Error" +str(error))
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
        return ("New tweet created")

    elif (request.method == 'GET'):
        cursor = None
        conn = None
        own_post = True
        not_own_post = True
        user_id = request.args.get('user_id')

        try:
            (conn, cursor) = dbConnect()
            if own_post:
                cursor.execute("SELECT * FROM user INNER JOIN tweets on user.id = tweets.user_Id WHERE user_id=?", [user_id])
                tweet_post = cursor.fetchall()
            elif not_own_post:
                cursor.execute("SELECT * FROM user INNER JOIN tweet on user.id = tweets.user_Id")
                tweet_post = cursor.fetchall()
            return Response(json.dumps(tweet_post, default=str),
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
        return ("Tweet post retrieved")
    
    elif (request.method == 'PATCH'):
        cursor = None
        conn = None
        login_token = request.json.get('loginToken')
        content = request.json.get('content')
        tweet_id = request.json.get('tweet_id')

        try:
            (conn, cursor) = dbConnect()
            cursor.execute("SELECT user_id, FROM user INNER JOIN user_session ON user_session.user_id = user.id WHERE user_session.loginToken=?", [login_token,])
            user = cursor.fetchall()
            user_id = user[0][0]
            cursor.excute("UPDATE tweets SET content=? WHERE tweet_id=? AND user_id=?", [content, tweet_id, user_id])
            conn.commit()
            editedTweet = {
                "tweetId" : tweet_id,
                "content": content
            }
            return Response(json.dumps(editedTweet),
                            mimetype="application/json",
                            status=200,)
        
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
        return ("Tweet edit updated")

    elif (request.method == 'DELETE'):
        cursor = None
        conn = None
        login_token = request.json.get('loginToken')
        tweet_id = request.json.get('tweet_id')

        try:
            (conn, cursor) = dbConnect()
            cursor.execute("SELECT user_id FROM user INNER JOIN user_session ON user_session.user_id = user.id WHERE loginToken=?", [login_token,])
            user_id = cursor.fetchall()
            if login_token !=None:
                cursor.execute("DELETE FROM tweets WHERE id=?", [tweet_id])
                conn.commit()
            else:
                return ("User not authenticated, cannot delete tweet")

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
        return Response("Tweet deleted",
                        mimetype="text/plain",
                        status=200)



