from flask import Flask, render_template, request, Response
import mysql.connector
import json, time, uuid
from markupsafe import escape
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

posts = []
posts = json.loads(open("data.json", "r").read())

@app.route("/")
def index2():
    return render_template("index.html")

@app.route("/index.html")
def index():
    return render_template("index.html")

@app.route("/api/v1/board/send", methods=["PUT"])
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

@app.route("/api/v1/board/get", methods=["GET"])
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

@app.route("/api/v1/user/create", methods=["POST"])
def createuser():
    if request.json == None:
        return Response(json.dumps("No body was provided"), status=400, mimetype="application/json")

    requestUsername = request.json.get("username")
    requestEmail = request.json.get("email")
    requestPassword = request.json.get("password")

    if requestUsername == None:
        return Response(json.dumps("No username was provided"), status=400, mimetype="application/json")

    if requestEmail == None:
        return Response(json.dumps("No email was provided"), status=400, mimetype="application/json")

    if requestPassword == None:
        return Response(json.dumps("No password was provided"), status=400, mimetype="application/json")


    mydb = mysql.connector.connect(
        host="localhost",
        user="willem",
        password="Dinkel2006!",
        database="shykeiichicom"
    )
    
    mycursor = mydb.cursor()

    mycursor.execute("SELECT * FROM users WHERE email=\"" + requestEmail + "\"")

    myresult = mycursor.fetchone()
    
    if myresult != None:
        return Response(json.dumps("User already exists with this email"), status=500, mimetype="application/json")

    mycursor.execute("SELECT * FROM users WHERE username=\"" + requestUsername + "\"")

    myresult = mycursor.fetchone()
    
    if myresult != None:
        return Response(json.dumps("User already exists with this username"), status=500, mimetype="application/json")

    curtime = int( time.time() )
    print(requestPassword)
    sql = f"INSERT INTO users (username, email, password, registered, passwordchanged) VALUES (\"{requestUsername}\", \"{requestEmail}\", \"{requestPassword}\", \"{curtime}\", \"{curtime}\")"
    mycursor.execute(sql)

    mydb.commit()
    
    return Response(json.dumps("User created"), status=201, mimetype="application/json")


@app.route("/api/v1/user/login", methods=["POST"])
def loginuser():
    if request.json == None:
        return Response(json.dumps("No body was provided"), status=400, mimetype="application/json")

    requestEmail = request.json.get("email")
    requestPassword = request.json.get("password")

    if requestEmail == None:
        return Response(json.dumps("No email was provided"), status=400, mimetype="application/json")

    if requestPassword == None:
        return Response(json.dumps("No password was provided"), status=400, mimetype="application/json")


    mydb = mysql.connector.connect(
        host="localhost",
        user="willem",
        password="Dinkel2006!",
        database="shykeiichicom"
    )
    
    mycursor = mydb.cursor()

    mycursor.execute("SELECT * FROM users WHERE email=\"" + requestEmail + "\"")

    myresult = mycursor.fetchone()
    
    if myresult == None:
        return Response(json.dumps("No user exists with this email"), status=400, mimetype="application/json")

    print(myresult)

    curtime = int( time.time() )
    print(requestPassword)
    sql = f"INSERT INTO sessions (sessionid, userid, timestamp) VALUES (\"{str(uuid.uuid4())}\", )"
    mycursor.execute(sql)

    mydb.commit()
    
    return Response(json.dumps("User created"), status=201, mimetype="application/json")


app.run(host="192.168.144.6", port="8080")
