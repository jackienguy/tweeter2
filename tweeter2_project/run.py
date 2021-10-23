from myapp import app
import sys

app.run()

if(len(sys.argv) > 1):
    mode = sys.argv[1]
    if (mode == "production"):
        import bjoern
        host = "0.0.0.0"
        port = 5001
        print("Server is running in production")
        bjoern.run(app, host, port)
    elif(mode == "testing"):
        from flask_cors import CORS
        CORS(app)
        print("Server is running in testing mode")
        app.run(debug=True)
    else:
        print("Invalid mode arguments, please choose either 'production' or 'testing'")
        exit()
else:
    print("No arguement was provided")
    exit()