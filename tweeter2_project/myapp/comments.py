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

# @app.route('/api/comments', methods=['GET', 'POST', 'PATCH', 'DELETE'])
# def comment():
#     if (request.method == 'GET'):
#         cursor = None
#         conn = None
#         tweet_id = request.json.get('tweet_id')

#         try:
#             (conn, cursor) = dbConnect()
#             cursor.execute("SELECT * FROM comment INNER JOIN user ON comment.user_id = user.id WHERE comment.tweet_id=?", [tweet_id,])
#             comments = cursor.fetchall()
