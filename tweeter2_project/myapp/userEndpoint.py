import mariadb
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
        email= request.json.get("email")
        birthdate = request.json.get("birthdate")

        try:
            (conn, cursor) = dbConnect()
            cursor.execute("INSERT INTO user(username, password, bio, email, birthdate) VALUES(?,?,?,?,?)", [username, password, bio, email, birthdate])
            if (len(username) <2):
                return ("Username is too short")
            elif (len(password) < 8):
                return ("Password need to be at least 8 characters long")
            elif (len(bio) > 150):
                return ("Bio is too long. Maximum 150 characters")
            user_id = cursor.lastrowid #cursor.lastrowid is a read-only property which returns the value generated for the auto increment column user_id by the INSERT statement above
            login_token = secrets.token_hex(16)
            cursor.execute("INSERT INTO user_session(user_id, loginToken) VALUES(?,?)",[user_id, login_token])
            conn.commit()
            newUser = {
                "userId": user_id,
                "password": password,
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
        bio = request.json.get("bio")
        email = request.json.get("email")
        birthdate = request.json.get("birthdate")
        
        try:
            (conn, cursor) = dbConnect()
            # Get userId login token to update info
            cursor.execute("SELECT user_id, loginToken FROM user_session INNER JOIN user ON user_session.user_id = user.id WHERE loginToken=?", [ login_token,])
            user = cursor.fetchall()
            user_id = user[0][0]
            # Update only if there is an input
            if (username != None and user[0][1] == login_token):
                cursor.execute("UPDATE user SET username=? WHERE id=?", [username, user_id])
            if (bio !=None and user[0][1] == login_token):
                cursor.execute("UPDATE user SET bio=? WHERE id=?", [bio, user_id])
            if (email != None and user[0][1] == login_token):
                cursor.execute("UPDATE user SET email=? WHERE id=?", [email, user_id])
            if (birthdate != None and user[0][1] == login_token):
                cursor.execute("UPDATE user SET username=? WHERE id=?", [birthdate, user_id])
            conn.commit()
            cursor.execute("SELECT * FROM user WHERE id=?",[user_id])
            updated_user = cursor.fetchall()
            if cursor.rowcount == 1:
                user_update = {
                    "userId": updated_user[0][0],
                    "email": updated_user[0][3],
                    "username": updated_user[0][1],
                    "bio": updated_user[0][2],
                    "birthdate": updated_user[0][4]
                }
            return Response(json.dumps(user_update),
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

        try:
            (conn, cursor) = dbConnect()
            cursor.execute("SELECT user_id, password, loginToken FROM user INNER JOIN user_session ON user_session.user_id = user.id WHERE loginToken=?", [login_token,])
            user = cursor.fetchall()
            if user[0][1] == password and user[0][2] == login_token:
                cursor.execute("DELETE FROM user WHERE password=?",[password,])
                conn.commit()
                return Response("User successfully deleted",
                                mimetype="text/html",
                                status=200)

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




   

    
        
 


        