# import mariadb
# from myapp import dbcreds
# from flask import Flask, request, Response
# import json
# from myapp import app

# def dbConnect():
#     conn = None
#     cursor = None

#     try:
#         conn = mariadb.connect(
#                                 user=dbcreds.user,
#                                 password=dbcreds.password,
#                                 host=dbcreds.host,
#                                 port=dbcreds.port,
#                                 database=dbcreds.database)
#         cursor = conn.cursor()
    
#     except:
#         if (cursor != None):
#             cursor.close()
#         if (conn != None):
#             conn.close()
#         else:
#             return ('Connection failed')
    
#     return (conn, cursor)

# @app.route('/follows', methods=['GET', 'POST', 'DELETE'])
# def getUsersFollowing():
#     if (request.methods == 'GET'):
#         conn = None
#         cursor = None
#         id = request.args.get(id)

#         try:
#             (conn, cursor) = dbConnect()
#             cursor.execute("SELECT * FROM user INNER JOIN follow ON follow.following_id = user.id")