ef DbConnection():

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
        else:
            ("there's no cursor to begin with")
        if (conn != None):
            conn.rollback()
            conn.close()
        else:
            print("The connection never opened, nothing to close here")
    
def login():
    conn = None
    cursor = None

    try:

        username = input()
        password = input()
        bio = input()
        email = input()
        birthdate = input()

        # Execute for new user creation POST
        cursor.execute("INSERT INTO user(username, password, bio, email, birthdate) VALUES(?,?,?,?,?)", [username, password, bio, email, birthdate])
        if(cursor.rowcount == 1):
            conn.commit()
            print("New user created")
        else:
            print("Something went wrong")

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
        else:
            ("there's no cursor to begin with")
        if (conn != None):
            conn.rollback()
            conn.close()
        else:
            print("The connection never opened, nothing to close here")





#     # Execute for getting user info if log in succesful GET
#     # cursor.execute("SELECT username FROM user WHERE username=?", [username,])

def updateUserInfo():
    conn = None
    cursor = None

    try:
        

#     # Execute for updating user info PATCH
#     cursor.execute("UPDATE user SET username=?, bio=?, password=?, email=?, birthdate=? WHERE id=?", [id, username, bio, password, email, birthdate])
#     if(cursor.rowcount == 1):
#         conn.commit()
#         print("User info updated")
#     else:
#         print("Something went wrong, update not completed")

#     # Execute to delete user DELETE
#     cursor.execute("DELETE FROM user WHERE id=?",[id,])
#     if (cursor.rowcount == 1):
#         conn.commit()
#         print("User deleted")
#     else:
#         print("Something went wrong, cannot delete user")
    

# except mariadb.DataError:
#     print("something went wrong with your data")
# except mariadb.OperationalError:
#     print("opertational error on the connection")
# except mariadb.ProgrammingError:
#     print("apparently, you don't know how to code")
# except mariadb.IntegrityError:
#     print("Error with DB integrity. most likelu constraint failure")
# except:
#     print("Something went wrong")

# finally:
#     if (cursor != None):
#         cursor.close()
#     else:
#         ("there's no cursor to begin with")
#     if (conn != None):
#         conn.rollback()
#         conn.close()
#     else:
#         print("The connection never opened, nothing to close here")