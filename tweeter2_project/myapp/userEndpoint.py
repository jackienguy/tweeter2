import mariadb
from myapp import dbcreds
from flask import Flask, request, Response
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

@app.route('/api/user', methods=['GET', 'POST', 'PATCH', 'DELETE'])
def find_user():
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
    else:
        return('Could not load info')

def signUp():
    if (request.method == 'POST'):
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
            resp = {
                "username": username,
                "password": password,
                "bio": bio,
                "email": email,
                "birthdate": birthdate
            }
            return Response(json.dumps(resp),
                        mimetype="application/json",
                        status=200)
        
            # # INPUT CODE for valid valid entry
            # ePattern = "[A-Za-Z0-9._]+@[A-Za-z]+\.(com|ca)"
            # if (re.fullmatch(ePattern, user_email)):
            #     print('valid email')
            # else:
            #     return('invalid email')
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
    else:
        return('Sign up failed')

def edit_user():
    if (request.method == 'PATCH'):
        conn = None
        cursor = None
        login_token = request.json.get("loginToken")
        username = request.json.get("username")
        password = request.json.get("password")
        bio = request.json.get("bio")
        email = request.json.get("email")
        birthdate = request.json.get("birthdate")
        
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
            return Response(json.dumps(resp),
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
    else: 
        return("Could not update user info")

def delete_user(id):
    if (request.method == 'DELETE'):
        conn = None
        cursor = None
        login_token = request.json.get("loginToken")
        password = request.json.get('password')

        try:
            (conn, cursor) = dbConnect()
            cursor.execute("DELETE FROM user WHERE id=?",[id,])
            conn.commit()
            resp = {
                "loginToken": login_token,
                "password": password
            }
            return Response(json.dumps(resp),
                        mimetype="application/json",
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
    else:
        return("Failed to delete user")

   

    
        
 


        