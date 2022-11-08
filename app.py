from flask import Flask, render_template, request, Response, send_file
import mysql.connector
import json, time, uuid
from markupsafe import escape
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

posts = []
posts = json.loads(open("data.json", "r").read())

@app.route("/admin.html", methods=["GET"])
def adminhtml():
    return send_file("./22widissisnu/" + "admin.html")

@app.route("/board.html", methods=["GET"])
def boardhtml():
    return send_file("./22widissisnu/" + "board.html")

@app.route("/medialog.html", methods=["GET"])
def medialoghtml():
    return send_file("./22widissisnu/" + "medialog.html")

@app.route("/login.html", methods=["GET"])
def loginhtml():
    return send_file("./22widissisnu/" + "login.html")

@app.route("/index.html", methods=["GET"])
def indexhtml():
    return send_file("./22widissisnu/" + "index.html")

@app.route("/pages/login/login.css", methods=["GET"])
def pagesloginlogincss():
    return send_file("./22widissisnu/" + "pages/login/login.css")

@app.route("/pages/login/login.js", methods=["GET"])
def pagesloginloginjs():
    return send_file("./22widissisnu/" + "pages/login/login.js")

@app.route("/pages/board/board.js", methods=["GET"])
def pagesboardboardjs():
    return send_file("./22widissisnu/" + "pages/board/board.js")

@app.route("/pages/board/board.css", methods=["GET"])
def pagesboardboardcss():
    return send_file("./22widissisnu/" + "pages/board/board.css")

@app.route("/pages/admin/admin.css", methods=["GET"])
def pagesadminadmincss():
    return send_file("./22widissisnu/" + "pages/admin/admin.css")

@app.route("/pages/admin/admin.js", methods=["GET"])
def pagesadminadminjs():
    return send_file("./22widissisnu/" + "pages/admin/admin.js")

@app.route("/pages/index/index.css", methods=["GET"])
def pagesindexindexcss():
    return send_file("./22widissisnu/" + "pages/index/index.css")

@app.route("/pages/index/images/login.png", methods=["GET"])
def pagesindeximagesloginpng():
    return send_file("./22widissisnu/" + "pages/index/images/login.png")

@app.route("/pages/index/images/board.png", methods=["GET"])
def pagesindeximagesboardpng():
    return send_file("./22widissisnu/" + "pages/index/images/board.png")

@app.route("/pages/medialog/medialog.css", methods=["GET"])
def pagesmedialogmedialogcss():
    return send_file("./22widissisnu/" + "pages/medialog/medialog.css")

@app.route("/images/light.svg", methods=["GET"])
def imageslightsvg():
    return send_file("./22widissisnu/" + "images/light.svg")

@app.route("/images/favicon.png", methods=["GET"])
def imagesfaviconpng():
    return send_file("./22widissisnu/" + "images/favicon.png")

@app.route("/images/dark.svg", methods=["GET"])
def imagesdarksvg():
    return send_file("./22widissisnu/" + "images/dark.svg")

@app.route("/images/youtube.png", methods=["GET"])
def imagesyoutubepng():
    return send_file("./22widissisnu/" + "images/youtube.png")

@app.route("/styles/styles_dark.css", methods=["GET"])
def stylesstyles_darkcss():
    return send_file("./22widissisnu/" + "styles/styles_dark.css")

@app.route("/styles/global.css", methods=["GET"])
def stylesglobalcss():
    return send_file("./22widissisnu/" + "styles/global.css")

@app.route("/styles/styles_light.css", methods=["GET"])
def stylesstyles_lightcss():
    return send_file("./22widissisnu/" + "styles/styles_light.css")

@app.route("/scripts/candyland.js", methods=["GET"])
def scriptscandylandjs():
    return send_file("./22widissisnu/" + "scripts/candyland.js")

@app.route("/scripts/theme.js", methods=["GET"])
def scriptsthemejs():
    return send_file("./22widissisnu/" + "scripts/theme.js")

@app.route("/scripts/init.js", methods=["GET"])
def scriptsinitjs():
    return send_file("./22widissisnu/" + "scripts/init.js")

@app.route("/scripts/hash.js", methods=["GET"])
def scriptshashjs():
    return send_file("./22widissisnu/" + "scripts/hash.js")

@app.route("/scripts/login.js", methods=["GET"])
def scriptsloginjs():
    return send_file("./22widissisnu/" + "scripts/login.js")

@app.route("/scripts/header.js", methods=["GET"])
def scriptsheaderjs():
    return send_file("./22widissisnu/" + "scripts/header.js")

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
    parentid = escape(request.args.get("parentid"))
    
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
    
    if(startint + 10 > myresult[0]): # Might have to change myresult heads up
        endint = myresult[0] - 1
    else:
        endint = startint + 10
 
    if(startint == endint + 1):
        return Response(json.dumps("No more posts"), status=204, mimetype="application/json")
    
    if(parentid == None):
        mycursor.execute(f"SELECT * FROM board ORDER BY id desc limit 10 OFFSET {startint}")
    else:
        mycursor.execute(f"SELECT * FROM board WHERE parentid={parentid} ORDER BY id desc limit 10 OFFSET {startint}")

    myresult = mycursor.fetchall()
    
    for i in range(len(myresult)):
        if(myresult[i][1] == None):
            continue
        
        mycursor.execute(f"SELECT username FROM users WHERE id=\"{myresult[i][1]}\"")
        myresult[i] = (myresult[i][0], mycursor.fetchone(), myresult[i][2], myresult[i][3], myresult[i][4])
    
    return Response(json.dumps(myresult), status=200, mimetype="application/json")


@app.route("/api/v1/board/getsingle", methods=["GET"])
def getpost():
    postid_ = escape(request.args.get("postid"))
    
    if(not postid_.isdecimal()):
        return Response(json.dumps("Postid is not a number"), status=400, mimetype="application/json")
    
    postid = int(postid_)

    mydb = mysql.connector.connect(
        host="localhost",
        user="willem",
        password="Dinkel2006!",
        database="shykeiichicom"
    )

    mycursor = mydb.cursor()
    
    mycursor.execute(f"SELECT * FROM board WHERE id={postid}")
    
    myresult = mycursor.fetchone()

    print(str(myresult))
    
    # mycursor.execute(f"SELECT username FROM users WHERE id=\"{myresult[i][1]}\"")
    # myresult[i] = (myresult[i][0], mycursor.fetchone(), myresult[i][2], myresult[i][3], myresult[i][4])
    
    return Response(json.dumps(myresult), status=200, mimetype="application/json")


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
    
    if myresult == None:
        return Response(json.dumps("Invalid sessionid"), status=400, mimetype="application/json")
   
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


@app.route("/api/v1/users/getall", methods=["GET"])
def usersgetall():
    if request.args == None:
        return Response(json.dumps("No arguments were provided"), status=400, mimetype="application/json")

    requestSessionid = request.args.get("sessionid")
 
    if 'sessionid' in request.args:
        requestSessionid = str(escape(request.args["sessionid"])).lower()
    else:
        return Response(json.dumps("No sessionid was provided."), status=400, mimetype='application/json')

    mydb = mysql.connector.connect(
        host="localhost",
        user="willem",
        password="Dinkel2006!",
        database="shykeiichicom"
    )
    
    mycursor = mydb.cursor()

    mycursor.execute("SELECT * FROM sessions WHERE sessionid=\"" + requestSessionid + "\"")

    myresult = mycursor.fetchone()
    
    if myresult == None:
        return Response(json.dumps("Invalid sessionid"), status=400, mimetype="application/json")
   
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
    
    if(result["id"] != 1):
        return Response(json.dumps("User not admin"), status=400, mimetype="application/json")
    
    mycursor.execute("SELECT * FROM users")

    myresult = mycursor.fetchall()
    
    users = []
    
    for x in myresult:
        result = {
            "id": x[0],
            "username": x[1],
            "email": x[2],
            "registered": x[4],
            "passwordchanged": x[5] 
        }

        users.append(result)
        
    return Response(json.dumps(users), status=200, mimetype="application/json")


@app.route("/api/v1/user/delete", methods=["POST"])
def userremove():
    if request.json == None:
        return Response(json.dumps("No body was provided"), status=400, mimetype="application/json")

    requestSessionid = request.json.get("sessionid")
 
    if requestSessionid == None:
        return Response(json.dumps("No sessionid was provided"), status=400, mimetype="application/json")

    requestUserID = request.json.get("removeuserid")
 
    if requestUserID == None:
        return Response(json.dumps("No removeuserid was provided"), status=400, mimetype="application/json")


    mydb = mysql.connector.connect(
        host="localhost",
        user="willem",
        password="Dinkel2006!",
        database="shykeiichicom"
    )
    
    mycursor = mydb.cursor()

    mycursor.execute("SELECT * FROM sessions WHERE sessionid=\"" + requestSessionid + "\"")

    myresult = mycursor.fetchone()
    
    if myresult == None:
        return Response(json.dumps("Invalid sessionid"), status=400, mimetype="application/json")
   
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
    
    if(result["id"] != 1):
        return Response(json.dumps("User not admin"), status=400, mimetype="application/json")
    
    
    mycursor.execute(f"SELECT * FROM users WHERE id=\"{requestUserID}\"")
    
    myresult = mycursor.fetchone()
    
    if(myresult == None):
        return Response(json.dumps("Userid to remove is not valid"), status=400, mimetype="application/json")

    print(requestUserID)
    mycursor.execute(f"DELETE FROM users WHERE id={requestUserID}")
    
    mydb.commit()
        
    return Response(json.dumps("User removed"), status=200, mimetype="application/json")


app.run(host="192.168.144.6", port="8080")
