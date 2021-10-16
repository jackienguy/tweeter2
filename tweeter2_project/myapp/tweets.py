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

@app.route('/api/tweets', methods=['GET', 'POST', 'PATCH', 'DELETE'])
def tweets():
    if (request.method == 'POST'):
        cursor = None
        conn = None
        login_token = request.json.get('loginToken')
        content = request.json.get('content')
        id = request.json.get('id')

        try:
            (conn, cursor) = dbConnect()
            cursor.execute("INSERT INTO tweets(user_id, content) VALUES(?,?)",[id, content])
            conn.commit()
            tweet_id = cursor.lastrowid
            createTweet = {
                "tweetId": tweet_id,
                "userId": id,
                "content": content
            }
            return Response(json.dumps(createTweet,
                            mimetype="applications/json",
                            status=200))
            
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
        id = request.json.get('id')

        try:
            (conn, cursor) = dbConnect()
            cursor.execute("SELECT user_id, content FROM user INNER JOIN tweets ON user_id=tweets.userId WHERE id=?", [id,])
            posts = cursor.fetchall()
            return Response(posts, default=str,
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
        return ("Tweet posted")

