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
    message_ = request.json.get("message")
    sendersessionid_ = request.json.get("sessionid")
    senderid_ = None
    ip_ = request.remote_addr

    if(message_ == None):
        return Response(json.dumps("No message provided"), status=400, mimetype='application/json')
    
    if(len(message_) > 300):
        return Response(json.dumps("Message is too long"), status=400, mimetype="application/json")

    if sendersessionid_ != None:
        mydb = mysql.connector.connect(
            host="localhost",
            user="willem",
            password="Dinkel2006!",
            database="shykeiichicom"
        )
    
        mycursor = mydb.cursor()

        mycursor.execute(f"SELECT * FROM sessions WHERE sessionid=\"{sendersessionid_}\"")

        myresult = mycursor.fetchone()

        if(myresult != None):
            if(int(time.time() - int(myresult[2])) > 2419200):
                mycursor.execute("DELETE FROM sessions WHERE sessionid=\"{sendersessionid_}\"")
                return Response(json.dumps("Sessionid expired"), status=500, mimetype="application/json")

            senderid_ = myresult[1]
            
    mydb = mysql.connector.connect(
        host="localhost",
        user="willem",
        password="Dinkel2006!",
        database="shykeiichicom"
    )

    mycursor = mydb.cursor()

    curtime = int( time.time() )
    sql = ""
    if(senderid_ != None):
        sql = f"INSERT INTO board (userid, senderip, message, timestamp) VALUES (\"{senderid_}\", \"{ip_}\", \"{message_}\", \"{curtime}\")"
    else:
        sql = f"INSERT INTO board (senderip, message, timestamp) VALUES (\"{ip_}\", \"{message_}\", \"{curtime}\")"
    mycursor.execute(sql)

    mydb.commit()
        
    return Response("Created", status=201)

@app.route("/api/v1/board/get", methods=["GET"])
def getposts():
    start = escape(request.args.get("start"))
    
    if(not start.isdecimal()):
        return Response(json.dumps("Not a number"), status=400, mimetype="application/json")
    
    startint = int(start)
    endint = 0
    
    mydb = mysql.connector.connect(
        host="localhost",
        user="willem",
        password="Dinkel2006!",
        database="shykeiichicom"
    )

    mycursor = mydb.cursor()

    mycursor.execute(f"SELECT Count(id) FROM board")

    myresult = mycursor.fetchone()
    
    print(myresult)
    
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
        return Response(json.dumps("No user exists with this email!"), status=400, mimetype="application/json")

    if(myresult[3] != requestPassword):
        return Response(json.dumps("Invalid password!"), status=400, mimetype="application/json")

    curtime = int( time.time() )
    sessionid = str(uuid.uuid4())
    sql = f"INSERT INTO sessions (sessionid, userid, timestamp) VALUES (\"{sessionid}\", \"{myresult[0]}\", \"{curtime}\")"
    mycursor.execute(sql)

    mydb.commit()
    
    return Response(json.dumps(sessionid), status=201, mimetype="application/json")


@app.route("/api/v1/user/validatesession", methods=["POST"])
def validatesession():
    if request.json == None:
        return Response(json.dumps("No body was provided"), status=400, mimetype="application/json")

    requestSessionid = request.json.get("sessionid")
 

    if requestSessionid == None:
        return Response(json.dumps("No sessionid was provided"), status=400, mimetype="application/json")


    mydb = mysql.connector.connect(
        host="localhost",
        user="willem",
        password="Dinkel2006!",
        database="shykeiichicom"
    )
    
    mycursor = mydb.cursor()

    mycursor.execute("SELECT * FROM sessions WHERE sessionid=\"" + requestSessionid + "\"")

    myresult = mycursor.fetchone()
   
    if(int(time.time() - int(myresult[2])) > 2419200):
        mycursor.execute("DELETE FROM sessions WHERE sessionid=\"" + requestSessionid + "\"")
        return Response(json.dumps("Sessionid expired"), status=500, mimetype="application/json")

    mycursor.execute("SELECT * FROM users WHERE id=\"" + str(myresult[1]) + "\"")

    myresult = mycursor.fetchone()
    
    result = {
        "id": myresult[0],
        "username": myresult[1],
        "email": myresult[2],
        "registered": myresult[4],
        "passwordchanged": myresult[5] 
    }

    return Response(json.dumps(result), status=200, mimetype="application/json")

app.run(host="192.168.144.6", port="8080")
