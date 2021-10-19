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
        tweet_id = request.args.get('tweet_id')

        try:
            (conn, cursor) = dbConnect()
            if tweet_id:
                cursor.execute("SELECT * from tweet_like INNER JOIN WHERE tweet_id=?", [tweet_id])
                likes = cursor.fetchall()
                return Response(likes, default=str,
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

    # elif (request.method == 'POST'):
    #     cursor = None
    #     conn = None
    #     login_token = request.json.get('loginToken')
    #     tweet_id = request.json.get('tweet_id')

    #     try: 
    #         (conn, cursor) = dbConnect()
    #         cursor.execute('INSERT')
        
        
    #     except ConnectionError:
    #         print("Error occured trying to connect to database")
    #     except mariadb.DataError:
    #         print("something went wrong with your data")
    #     except mariadb.OperationalError:
    #         print("opertational error on the connection")
    #     except mariadb.ProgrammingError:
    #         print("apparently, you don't know how to code")
    #     except mariadb.IntegrityError:
    #         print("Error with DB integrity. most likelu constraint failure")
    #     except:
    #         print("Something went wrong")

    #     finally:
    #         if (cursor != None):
    #             cursor.close()
    #         if (conn != None):
    #             conn.rollback()
    #             conn.close()
    #         else:
    #             print("Failed to read data")
    #     return ("likes retrieved")
