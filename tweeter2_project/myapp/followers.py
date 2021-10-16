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

@app.route('/api/followers', methods=['GET'])
def getUserFollowers():
    if (request.method == 'GET'):
        cursor = None
        conn = None
        id = request.args.get('id')

        try:
            (conn, cursor) = dbConnect()
            if id:
                cursor.execute("SELECT * FROM user INNER JOIN follow ON follow.follower_id =?", [id,])
                result = cursor.fetchall()
                return Response(result, Default=str,
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
        return("Followers retrieved")
