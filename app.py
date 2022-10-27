from flask import Flask, render_template, request, Response
import json, time
from markupsafe import escape
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

posts = []
posts = json.loads(open("data.json", "r").read())

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/send", methods=["PUT"])
def sendpost():
    print(request.json)
    message_ = request.json.get('message')
    sender_ = request.json.get("sender")
    ip_ = request.remote_addr

    if(message_ == None):
        return Response(json.dumps("No message provided"), status=400, mimetype='application/json')
    
    if(sender_ != None):
        if(len(sender_) > 30):
            return Response(json.dumps("Sender name too long"), status=400, mimetype='application/json')
            
    if(len(message_) > 300):
        return Response(json.dumps("Message is too long"), status=400, mimetype="application/json")
    
    posts.append({
        "message": message_,
        "sender": sender_,
        "ip": ip_,
        "posttime": int( time.time() )
    })
    file = open("data.json", "w")
    print(posts)
    file.write(json.dumps(posts))
    
    return Response("Created", status=201)

@app.route("/get", methods=["GET"])
def getposts():
    start = escape(request.args.get("start"))
    
    if(not start.isdecimal()):
        return Response(json.dumps("Not a number"), status=400, mimetype="application/json")
    
    startint = int(start)
    endint = 0
    
    if(startint + 10 > len(posts)):
        endint = len(posts) - 1
    else:
        endint = startint + 10
 
    if(startint == endint + 1):
        return Response(json.dumps("No more posts"), status=204, mimetype="application/json")
    
    return Response(json.dumps(posts[::-1][startint:endint]), status=200, mimetype="application/json")