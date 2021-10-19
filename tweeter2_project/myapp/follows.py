import mariadb
from myapp import dbcreds, login
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

@app.route('/api/follows', methods=['GET', 'POST', 'DELETE'])
def UserFollows():
    if (request.method == 'GET'):
        conn = None
        cursor = None
        user_id = request.args.get('user_id')

        try:
            (conn, cursor) = dbConnect()
            if id:
                #Inner joined on follwer_id as user_id as the follower, getting the list user_id is following 
                cursor.execute("SELECT * FROM user INNER JOIN follow ON follow.follower_id = user.id WHERE following_id=?", [user_id,])
                result = cursor.fetchall()
                return Response(json.dumps(result, default=str),
                            mimetype="application/json",
                            status=200)
            else:
                return("Something went wrong, can't get follows")

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
        return("Follows retrieved")
    
    elif (request.method == 'POST'):
        conn = None
        cursor = None
        following_id = request.json.get('following_id')
        login_token = request.json.get('loginToken')

        try:
            (conn, cursor) = dbConnect()
            if (login_token !=None and following_id != None):
                # Get user id of user who have successfully logged in 
                cursor. execute("SELECT user_id FROM user_session WHERE loginToken=?", [login_token])
                user_id = cursor.fecthone()[0] # only fectch first row user_id 
                # following_id equals the user_id we want to follow, follower_id equals the user_id of who is following you
                cursor.execute("INSERT INTO follows (following_id, follower_id) VALUES(?,?)", [user_id, following_id])
                conn.commit()

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
        return("Follows retrieved")
    
    elif (request.method == 'DELETE'):
        conn = None
        cursor = None
        following_id = request.json.get('following_id')
        login_token = request.json.get('loginToken')

        try:
            (conn, cursor) = dbConnect()
            if (login_token !=None and following_id != None):
                cursor. execute("SELECT user_id FROM user_session WHERE loginToken=?", [login_token])
                user_id = cursor.fetchone()[0]
                cursor.execute("DELETE FROM follows WHERE following_id? AND follower_id=?", [user_id, following_id])
                conn.commit()

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
        return("Unfollowed user")