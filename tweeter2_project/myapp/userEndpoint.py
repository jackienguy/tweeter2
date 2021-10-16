import mariadb
from myapp import dbcreds
from flask import request, Response
import json
from myapp import app
from uuid import uuid4

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
        id = request.args.get('id')

        try:
            (conn, cursor) = dbConnect()
            if id:
                cursor.execute("SELECT * FROM user WHERE id=?", [id,])
                result = cursor.fetchall()
                return Response(json.dumps(result, default=str),
                                mimetype="application/json",
                                status=200)
            else:
                return('User Id not found')

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
        return("Got user info")
  
    elif (request.method == 'POST'):
        conn = None
        cursor = None
        username = request.json.get("username")
        password = request.json.get("password")
        bio = request.json.get("bio")
        email = request.json.get("email")
        birthdate = request.json.get("birthdate")
        userid = request.json.get("id")

        try:
            (conn, cursor) = dbConnect()
            cursor.execute("INSERT INTO user(username, password, bio, email, birthdate) VALUES(?,?,?,?,?)", [username, password, bio, email, birthdate])
            user_id = cursor.lastrowid #cursor.lastrowid is a read-only property which returns the value generated for the auto increment column user_id by the INSERT statement above
            login_token = uuid4(10).hex
            print('login_token')
            cursor.execute("INSERT INTO user_session(user_id, loginToken) VALUES=?,?",[userid, login_token])
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
        return("New user sucessfully created")
   
    elif (request.method == 'PATCH'):
        conn = None
        cursor = None
        login_token = request.json.get("loginToken")
        username = request.json.get("username")
        password = request.json.get("password")
        bio = request.json.get("bio")
        email = request.json.get("email")
        birthdate = request.json.get("birthdate")
        id = request.json.get("id")
        
        try:
            (conn, cursor) = dbConnect()
            cursor.execute("UPDATE user SET username=?, bio=?, password=?, email=?, birthdate=? WHERE id=?", [id, username, password, bio, email, birthdate])
            conn.commit()
            resp = {
                "loginToken": login_token,
                "username": username,
                "password": password,
                "bio": bio,
                "email": email,
                "birthdate": birthdate
            }
            return Response(resp,
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
        return("User update sucessful")

    elif (request.method == 'DELETE'):
        conn = None
        cursor = None
        login_token = request.json.get("loginToken")
        password = request.json.get('password')
        id = request.json.get('id')

        try:
            (conn, cursor) = dbConnect()
            cursor.execute("DELETE FROM user WHERE id=?",[id,])
            conn.commit()
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
        return("User deleted")



   

    
        
 


        