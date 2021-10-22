import mariadb
from werkzeug.security import generate_password_hash
from myapp import dbcreds
from flask import request, Response
import json
from myapp import app
import secrets

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

@app.route('/api/user', methods=['POST','GET', 'PATCH', 'DELETE'])
def user():
    if (request.method == 'GET'):
        conn = None
        cursor = None
        user_id = request.args.get('userId')

        try:
            (conn, cursor) = dbConnect()
            cursor.execute("SELECT * FROM user WHERE id=?", [user_id,])
            result = cursor.fetchall()
            if cursor.rowcount > 0:
                user_data = []
                for user in result:
                    users = {
                       " userId": user_id,
                       " email": user[3],
                       " username": user[1],
                       " bio": user[2],
                       " birthdate": user[6],
                    }
                    user_data.append(users)
                return Response(json.dumps(user_data, default=str),
                                mimetype="application/json",
                                status=200)
            else:
                return Response("User id not found",
                                mimetype="text/html",
                                status=400)

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
        username = request.json.get("username")
        password = request.json.get("password")
        bio = request.json.get("bio")
        email = request.json.get("email")
        birthdate = request.json.get("birthdate")

        try:
            (conn, cursor) = dbConnect()
            cursor.execute("INSERT INTO user(username, password, bio, email, birthdate) VALUES(?,?,?,?,?)", [username, password, bio, email, birthdate])
            conn.commit()
            user_id = cursor.lastrowid #cursor.lastrowid is a read-only property which returns the value generated for the auto increment column user_id by the INSERT statement above
            login_token = secrets.token_hex(16)
            cursor.execute("INSERT INTO user_session(user_id, loginToken) VALUES(?,?)",[user_id, login_token])
            conn.commit()
            newUser = {
                "userId": user_id,
                "password": generate_password_hash(password, method='sah256'),
                "bio": bio,
                "email": email,
                "birthdate": birthdate,
                "loginToken": login_token
            }
            return Response(json.dumps(newUser),
                        mimetype="application/json",
                        status=200)
        except ValueError as error:
            print("Error" +str(error))
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
        conn = None
        cursor = None
        login_token = request.json.get("loginToken")
        username = request.json.get("username")
        password = request.json.get("password")
        bio = request.json.get("bio")
        email = request.json.get("email")
        birthdate = request.json.get("birthdate")
        user_id = request.json.get("user_id")
        
        try:
            (conn, cursor) = dbConnect()
            # Get userId to update info
            cursor.execute("SELECT user_id FROM user_session WHERE loginToken=?", [login_token,])
            cursor.execute("UPDATE user SET username=?, bio=?, password=?, email=?, birthdate=? WHERE id=?", [user_id, username, password, bio, email, birthdate])
            conn.commit()
            update = {
                "username": username,
                "password": password,
                "bio": bio,
                "email": email,
                "birthdate": birthdate
            }
            return Response(json.dumps(update),
                        mimetype="application/json",
                        status=200)

        except ValueError as error:
            print("Error" +str(error))
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
        login_token = request.json.get("loginToken")
        password = request.json.get('password')
        user_id = request.json.get('user_id')

        try:
            (conn, cursor) = dbConnect()
            cursor.execute("SELECT user_id, password FROM user INNER JOIN user_session ON user_session.user_id = user.id WHERE loginToken=?", [login_token,])
            conn.commit()
            user = cursor.fetchall()
            if (user != None):
                cursor.execute("DELETE FROM user WHERE id=?",[user_id,])
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




   

    
        
 


        