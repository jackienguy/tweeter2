from flask import Flask 

app = Flask(__name__)

import myapp.userEndpoint
import myapp.login
import myapp.follows

