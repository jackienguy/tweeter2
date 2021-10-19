from flask import Flask 

app = Flask(__name__)

import myapp.userEndpoint
import myapp.login
import myapp.follows
import myapp.followers
import myapp.tweets
import myapp.tweetLikes
import myapp.comments
import myapp.commentLikes

