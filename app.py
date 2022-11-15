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

@app.route("/reply.html", methods=["GET"])
def replyhtml():
    return send_file("./22widissisnu/" + "reply.html")

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

@app.route("/pages/reply/reply.js", methods=["GET"])
def pagesreplyreplyjs():
    return send_file("./22widissisnu/" + "pages/reply/reply.js")

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

@app.route("/forgotpasswd.html", methods=["GET"])
def scriptsheaderjs():
    return send_file("./22widissisnu/" + "forgotpasswd.html")

@app.route("/pages/forgotpasswd/forgotpasswd.js", methods=["GET"])
def scriptsheaderjs():
    return send_file("./22widissisnu/" + "pages/forgotpasswd/forgotpasswd.js")

@app.route("/api/v1/board/send", methods=["PUT"])
def sendpost():
    message_ = request.json.get("message")
    sendersessionid_ = request.json.get("sessionid")
    senderid_ = None
    ip_ = request.remote_addr
    parentid_ = request.json.get("parentid")

    if(message_ == None):
        return Response(json.dumps("No message provided"), status=400, mimetype='application/json')
    
    if(len(message_) > 300):
        return Response(json.dumps("Message is too long"), status=400, mimetype="application/json")

    mydb = mysql.connector.connect(
        host="localhost",
        user="willem",
        password="Dinkel2006!",
        database="shykeiichicom"
    )

    mycursor = mydb.cursor()

    if sendersessionid_ != None:

        mycursor.execute(f"SELECT * FROM sessions WHERE sessionid=\"{sendersessionid_}\"")

        myresult = mycursor.fetchone()

        if(myresult != None):
            if(int(time.time() - int(myresult[2])) > 2419200):
                mycursor.execute("DELETE FROM sessions WHERE sessionid=\"{sendersessionid_}\"")
                return Response(json.dumps("Sessionid expired"), status=500, mimetype="application/json")

            senderid_ = myresult[1]

    curtime = int( time.time() )
    sql = ""
    if(parentid_ == None):
        if(senderid_ != None):
            sql = f"INSERT INTO board (userid, senderip, message, timestamp) VALUES (\"{senderid_}\", \"{ip_}\", \"{message_}\", \"{curtime}\")"
        else:
            sql = f"INSERT INTO board (senderip, message, timestamp) VALUES (\"{ip_}\", \"{message_}\", \"{curtime}\")"
    else:
        if(senderid_ != None):
            sql = f"INSERT INTO board (userid, senderip, message, timestamp, parentid) VALUES (\"{senderid_}\", \"{ip_}\", \"{message_}\", \"{curtime}\", \"{parentid_}\")"
        else:
            sql = f"INSERT INTO board (senderip, message, timestamp, parentid) VALUES (\"{ip_}\", \"{message_}\", \"{curtime}\", \"{parentid_}\")"
    mycursor.execute(sql)

    mydb.commit()
        
    return Response("Created", status=201)

@app.route("/api/v1/board/get", methods=["GET"])
def getposts():
    start = escape(request.args.get("start"))
    parentid = escape(request.args.get("parentid"))
    
    sessionid = escape(request.args.get("sessionid"))
    
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

    mycursor = mydb.cursor(buffered=True)

    mycursor.execute(f"SELECT Count(id) FROM board")

    myresult = mycursor.fetchone()
    
    if(startint + 10 > myresult[0]): # Might have to change myresult heads up
        endint = myresult[0] - 1
    else:
        endint = startint + 10
    
    if(startint == endint + 1):
        return Response(json.dumps("No more posts"), status=204, mimetype="application/json")
    
    user = None
    
    if(sessionid != None):
        mycursor.execute(f"SELECT * FROM sessions WHERE sessionid=\"{sessionid}\"")

        usersession = mycursor.fetchone()

        usersessionid = None

        if(usersession != None):
            if(int(time.time() - int(usersession[2])) > 2419200):
                mycursor.execute("DELETE FROM sessions WHERE sessionid=\"{sessionid}\"")
                return Response(json.dumps("Sessionid expired"), status=400, mimetype="application/json")
            usersessionid = usersession[1]

        mycursor.execute(f"SELECT * FROM users WHERE id=\"{usersessionid}\"")

        user = mycursor.fetchone()
    
    if(str(parentid) == "None"):
        mycursor.execute(f"SELECT * FROM board WHERE parentid is NULL ORDER BY id desc limit 10 OFFSET {startint}")
    else:
        mycursor.execute(f"SELECT * FROM board WHERE parentid={parentid} ORDER BY id desc limit 10 OFFSET {startint}")

    myresult = mycursor.fetchall()
    
    for i in range(len(myresult)):
        mycursor.execute(f"SELECT COUNT(*) FROM ratings WHERE postid=\"{myresult[i][0]}\" AND rating=1;")

        positiveratings = mycursor.fetchone()[0];
        
        mycursor.execute(f"SELECT COUNT(*) FROM ratings WHERE postid=\"{myresult[i][0]}\" AND rating=0;")

        negativeratings = mycursor.fetchone()[0];
        
        userrating = None
        if user != None:
            mycursor.execute(f"SELECT rating FROM ratings WHERE userid=\"{user[0]}\" AND postid=\"{myresult[i][0]}\"")

            userrating = mycursor.fetchone();
            if(userrating != None):
                userrating = userrating[0]
        
        mycursor.execute(f"SELECT COUNT(parentid) FROM board WHERE parentid={myresult[i][0]}")
    
        replycount = mycursor.fetchone();

        mycursor.execute(f"SELECT parentid FROM board WHERE id={myresult[i][0]}")

        postparentid = mycursor.fetchone();

        if(myresult[i][1] != None):
            mycursor.execute(f"SELECT username FROM users WHERE id=\"{myresult[i][1]}\"")
        
        myresult[i] = {
            "id": myresult[i][0], 
            "userid": myresult[i][1],
            "username": mycursor.fetchone()[0] if myresult[i][1] != None else myresult[i][1], 
            "ip": myresult[i][2], 
            "message": myresult[i][3], 
            "timestamp": myresult[i][4], 
            "replycount": replycount[0], 
            "parentid": postparentid[0],
            "userrating": userrating,
            "positiveratings": positiveratings,
            "negativeratings": negativeratings
        }
    
    return Response(json.dumps(myresult), status=200, mimetype="application/json")


@app.route("/api/v1/board/getsingle", methods=["GET"])
def getpost():
    postid_ = escape(request.args.get("postid"))
    sessionid = escape(request.args.get("sessionid"))
    
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
    
    
    user = None
    
    if(sessionid != None):
        mycursor.execute(f"SELECT * FROM sessions WHERE sessionid=\"{sessionid}\"")

        usersession = mycursor.fetchone()

        usersessionid = None

        if(usersession != None):
            if(int(time.time() - int(usersession[2])) > 2419200):
                mycursor.execute("DELETE FROM sessions WHERE sessionid=\"{sessionid}\"")
                return Response(json.dumps("Sessionid expired"), status=400, mimetype="application/json")
            usersessionid = usersession[1]

        else:
            return Response(json.dumps("Invalid sessionid provided"), status=400, mimetype="application/json")
                
        mycursor.execute(f"SELECT * FROM users WHERE id=\"{usersessionid}\"")

        user = mycursor.fetchone()
    
    
    mycursor.execute(f"SELECT * FROM board WHERE id={postid}")
    
    myresult = mycursor.fetchone()

    mycursor.execute(f"SELECT COUNT(parentid) FROM board WHERE parentid={myresult[0]}")

    replycount = mycursor.fetchone();
    
    mycursor.execute(f"SELECT parentid FROM board WHERE id={myresult[0]}")

    postparentid = mycursor.fetchone();
    
    mycursor.execute(f"SELECT COUNT(*) FROM ratings WHERE postid=\"{postid_}\" AND rating=1;")

    positiveratings = mycursor.fetchone()[0];
    
    mycursor.execute(f"SELECT COUNT(*) FROM ratings WHERE postid=\"{postid_}\" AND rating=0;")

    negativeratings = mycursor.fetchone()[0];

    userrating = None
    if user != None:
        mycursor.execute(f"SELECT rating FROM ratings WHERE userid=\"{user[0]}\" AND postid=\"{myresult[0]}\"")

        userrating = mycursor.fetchone();
        if(userrating != None):
            userrating = userrating[0]
    
    mycursor.execute(f"SELECT username FROM users WHERE id=\"{myresult[1]}\"")
    myresult = {
        "id": myresult[0], 
        "userid": myresult[1],
        "username": mycursor.fetchone()[0], 
        "ip": myresult[2], 
        "message": myresult[3], 
        "timestamp": myresult[4], 
        "replycount": replycount[0], 
        "parentid": postparentid[0],
        "userrating": userrating,
        "positiveratings": positiveratings,
        "negativeratings": negativeratings
    }

    return Response(json.dumps(myresult), status=200, mimetype="application/json")


@app.route("/api/v1/board/rate", methods=["PUT"])
def ratepost():
    rating_ = request.json.get("rating")
    sendersessionid_ = request.json.get("sessionid")
    postid_ = request.json.get("postid")

    if(rating_ == None):
        return Response(json.dumps("No message provided"), status=400, mimetype='application/json')
    
    if(sendersessionid_ == None):
        return Response(json.dumps("No Sessionid provided"), status=400, mimetype="application/json")

    if(postid_ == None):
        return Response(json.dumps("No postid provided"), status=400, mimetype="application/json")

    mydb = mysql.connector.connect(
        host="localhost",
        user="willem",
        password="Dinkel2006!",
        database="shykeiichicom"
    )

    mycursor = mydb.cursor()

    mycursor.execute(f"SELECT * FROM sessions WHERE sessionid=\"{sendersessionid_}\"")

    usersession = mycursor.fetchone()

    usersessionid = None

    if(usersession != None):
        if(int(time.time() - int(usersession[2])) > 2419200):
            mycursor.execute("DELETE FROM sessions WHERE sessionid=\"{sendersessionid_}\"")
            return Response(json.dumps("Sessionid expired"), status=400, mimetype="application/json")
        usersessionid = usersession[1]

    else:
        return Response(json.dumps("Invalid sessionid provided"), status=400, mimetype="application/json")
            
    mycursor.execute(f"SELECT * FROM users WHERE id=\"{usersessionid}\"")

    user = mycursor.fetchone()
    
    if user == None:
        return Response(json.dumps("Invalid sessionid provided 2"), status=400, mimetype="application/json")

    mycursor.execute(f"SELECT * FROM ratings WHERE postid=\"{postid_}\" AND userid=\"{user[0]}\"")

    rating = mycursor.fetchone()
    
    mycursor.execute(f"SELECT * FROM board WHERE id=\"{postid_}\"")

    post = mycursor.fetchone()

    if post == None:
        return Response(json.dumps("Post was not found"), status=500, mimetype="application/json")
    
    if rating != None:
        print(f"{rating[4]} {0 if rating_ == False else 1}")
        if rating[4] == (0 if rating_ == False else 1):
            return Response("Nothing changed", status=204)
    
    sql = ""
    curtime = int( time.time() )
    if rating != None:
        sql = f"UPDATE ratings SET rating=\"{0 if rating_ == False else 1}\" WHERE postid=\"{postid_}\" AND userid=\"{user[0]}\""
    else:
        sql = f"INSERT INTO ratings (postid, userid, senderid, rating, timestamp) VALUES (\"{postid_}\", \"{user[0]}\", \"{post[1]}\", \"{0 if rating_ == False else 1}\", \"{curtime}\")"

    mycursor.execute(sql)
    mydb.commit()
        
    return Response("Updated post rating" if rating == None else "Rated post", status=200 if rating == None else 201)


@app.route("/api/v1/board/delete", methods=["PUT"])
def boarddelete():
    sessionid_ = request.json.get("sessionid")
    postid_ = request.json.get("postid")

    if(sessionid_ == None):
        return Response(json.dumps("No Sessionid provided"), status=400, mimetype="application/json")

    if(postid_ == None):
        return Response(json.dumps("No postid provided"), status=400, mimetype="application/json")

    mydb = mysql.connector.connect(
        host="localhost",
        user="willem",
        password="Dinkel2006!",
        database="shykeiichicom"
    )

    mycursor = mydb.cursor()

    mycursor.execute(f"SELECT * FROM sessions WHERE sessionid=\"{sessionid_}\"")

    usersession = mycursor.fetchone()

    usersessionid = None

    if(usersession != None):
        if(int(time.time() - int(usersession[2])) > 2419200):
            mycursor.execute("DELETE FROM sessions WHERE sessionid=\"{sessionid_}\"")
            return Response(json.dumps("Sessionid expired"), status=400, mimetype="application/json")
        usersessionid = usersession[1]

    else:
        return Response(json.dumps("Invalid sessionid provided"), status=400, mimetype="application/json")
            
    mycursor.execute(f"SELECT * FROM users WHERE id=\"{usersessionid}\"")

    user = mycursor.fetchone()
    
    if user == None:
        return Response(json.dumps("Invalid sessionid provided 2"), status=400, mimetype="application/json")
    
    
    mycursor.execute(f"SELECT * FROM board WHERE id=\"{postid_}\"")

    post = mycursor.fetchone()

    if post == None:
        return Response(json.dumps("Post was not found"), status=500, mimetype="application/json")
    
    if post[1] != user[0]:
        if user[0] != 1:
            return Response(json.dumps("You do not own this post"), status=500, mimetype="application/json")
    
    sql = f"DELETE FROM board WHERE id={postid_}"
    
    mycursor.execute(sql)
    mydb.commit()
        
    return Response("Deleted Post", status=200, mimetype="application/json")


@app.route("/api/v1/board/deleterange", methods=["PUT"])
def boarddeleterange():
    sessionid_ = request.json.get("sessionid")
    minr_ = request.json.get("min")
    maxr_ = request.json.get("max")

    if(sessionid_ == None):
        return Response(json.dumps("No Sessionid provided"), status=400, mimetype="application/json")

    if(minr_ == None):
        return Response(json.dumps("No min provided"), status=400, mimetype="application/json")

    if(maxr_ == None):
        return Response(json.dumps("No max provided"), status=400, mimetype="application/json")


    mydb = mysql.connector.connect(
        host="localhost",
        user="willem",
        password="Dinkel2006!",
        database="shykeiichicom"
    )

    mycursor = mydb.cursor()

    mycursor.execute(f"SELECT * FROM sessions WHERE sessionid=\"{sessionid_}\"")

    usersession = mycursor.fetchone()

    usersessionid = None

    if(usersession != None):
        if(int(time.time() - int(usersession[2])) > 2419200):
            mycursor.execute("DELETE FROM sessions WHERE sessionid=\"{sessionid_}\"")
            return Response(json.dumps("Sessionid expired"), status=400, mimetype="application/json")
        usersessionid = usersession[1]

    else:
        return Response(json.dumps("Invalid sessionid provided"), status=400, mimetype="application/json")
            
    mycursor.execute(f"SELECT * FROM users WHERE id=\"{usersessionid}\"")

    user = mycursor.fetchone()
    
    if user == None:
        return Response(json.dumps("Invalid sessionid provided 2"), status=400, mimetype="application/json")
    
    if user[0] != 1:
        return Response(json.dumps("User not admin"), status=400, mimetype="application/json")
    
    sql = f"DELETE FROM board WHERE id BETWEEN {minr_} AND {maxr_}"
    
    mycursor.execute(sql)
    mydb.commit()
        
    return Response(f"Deleted Post from {minr_} to {maxr_}", status=200, mimetype="application/json")


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

@app.route("/api/v1/users/get", methods=["GET"])
def usersget():
    if request.args == None:
        return Response(json.dumps("No arguments were provided"), status=400, mimetype="application/json")

    requestSessionid = request.args.get("sessionid")
    requestUserid = request.args.get("userid")
 

    if 'sessionid' in request.args:
        requestSessionid = str(escape(request.args["sessionid"])).lower()
    else:
        return Response(json.dumps("No sessionid was provided."), status=400, mimetype='application/json')

    if 'userid' in request.args:
        requestUserid = str(escape(request.args["userid"])).lower()
    else:
        return Response(json.dumps("No userid was provided."), status=400, mimetype='application/json')

    mydb = mysql.connector.connect(
        host="localhost",
        user="willem",
        password="Dinkel2006!",
        database="shykeiichicom"
    )
    
    mycursor = mydb.cursor()

    mycursor.execute("SELECT * FROM sessions WHERE sessionid=\"" + requestSessionid + "\"")

    myresult = mycursor.fetchone()
    
    # print(requestSessionid)
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
    
    mycursor.execute(f"SELECT * FROM users WHERE id={requestUserid}")

    user = mycursor.fetchone()
    
    if(user == None):
        return Response(json.dumps("User not found"), status=400, mimetype="application/json")
    
    result = {
        "id": user[0],
        "username": user[1],
        "email": user[2],
        "registered": user[4],
        "passwordchanged": user[5] 
    }
        
    return Response(json.dumps(result), status=200, mimetype="application/json")


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

    print(requestSessionid)
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

    mycursor.execute(f"DELETE FROM users WHERE id={requestUserID}")
    
    mydb.commit()
        
    return Response(json.dumps("User removed"), status=200, mimetype="application/json")


@app.route("/api/v1/admin/user/edit", methods=["POST"])
def userupdate():
    if request.json == None:
        return Response(json.dumps("No body was provided"), status=400, mimetype="application/json")

    requestSessionid = request.json.get("sessionid")
 
    if requestSessionid == None:
        return Response(json.dumps("No sessionid was provided"), status=400, mimetype="application/json")


    requestEditUserIDOriginal = request.json.get("edituserid")
 
    if requestEditUserIDOriginal == None:
        return Response(json.dumps("No userid to edit was provided"), status=400, mimetype="application/json")

    requestEditUserID = request.json.get("userid")
    requestEditUsername = request.json.get("username")
    requestEditEmail = request.json.get("email")
    requestEditPassword = request.json.get("password")

    mydb = mysql.connector.connect(
        host="localhost",
        user="willem",
        password="Dinkel2006!",
        database="shykeiichicom"
    )
    
    mycursor = mydb.cursor()

    mycursor.execute("SELECT * FROM sessions WHERE sessionid=\"" + requestSessionid + "\"")

    print(requestSessionid)
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
    
    
    mycursor.execute(f"SELECT * FROM users WHERE id=\"{requestEditUserIDOriginal}\"")  
    
    myresult = mycursor.fetchone()
    
    if(myresult == None):
        return Response(json.dumps("Userid to edit is not valid"), status=400, mimetype="application/json")

    if requestEditUsername != None:
        mycursor.execute(f"UPDATE users SET username={requestEditUsername} where id={requestEditUserIDOriginal}")
    if requestEditEmail != None:
        mycursor.execute(f"UPDATE users SET email={requestEditEmail} where id={requestEditUserIDOriginal}")
    if requestEditPassword != None:
        curtime = int( time.time() )
        mycursor.execute(f"UPDATE users SET password={requestEditPassword} where id={requestEditUserIDOriginal}")
        mycursor.execute(f"UPDATE users SET passwordchanged={curtime} where id={requestEditUserIDOriginal}")
    if requestEditUserID != None:
        mycursor.execute(f"UPDATE users SET id={requestEditUserID} where id={requestEditUserIDOriginal}")
    
    mydb.commit()
        
    return Response(json.dumps("User edit"), status=200, mimetype="application/json")


@app.route("/api/v1/user/forgotpassword", methods=["POST"])
def userforgotpassword():
    if request.json == None:
        return Response(json.dumps("No body was provided"), status=400, mimetype="application/json")

    requestSessionid = request.json.get("sessionid")
 
    if requestSessionid == None:
        return Response(json.dumps("No sessionid was provided"), status=400, mimetype="application/json")

    requestUserID = request.json.get("userid")
 
    if requestUserID == None:
        return Response(json.dumps("No userid was provided"), status=400, mimetype="application/json")

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
    
    useradmin = {
        "id": myresult[0],
        "username": myresult[1],
        "email": myresult[2],
        "registered": myresult[4],
        "passwordchanged": myresult[5] 
    }
    
    if(useradmin["id"] != 1):
        return Response(json.dumps("User not admin"), status=400, mimetype="application/json")
    
    
    mycursor.execute(f"SELECT * FROM users WHERE id=\"{requestUserID}\"")  
    
    myresult = mycursor.fetchone()
    
    if(myresult == None):
        return Response(json.dumps("Userid is not valid"), status=400, mimetype="application/json")

    address = uuid.uuid4().hex
    curtime = int( time.time() )
    sql = f"INSERT INTO forgot_password (userid, address, timestamp) VALUES (\"{requestUserID}\", \"{address}\", \"{curtime}\")"
    mycursor.execute(sql)

    mydb.commit()
        
    return Response(json.dumps(f"https://22widi.ssis.nu/forgotpasswd.html?id={address}"), status=200, mimetype="application/json")


@app.route("/api/v1/user/changepassword", methods=["POST"])
def userupdate():
    if request.json == None:
        return Response(json.dumps("No body was provided"), status=400, mimetype="application/json")

    requestAddress = request.json.get("address")
 
    if requestAddress == None:
        return Response(json.dumps("No address was provided"), status=400, mimetype="application/json")

    requestPassword = request.json.get("password")
 
    if requestPassword == None:
        return Response(json.dumps("No password was provided"), status=400, mimetype="application/json")

    mydb = mysql.connector.connect(
        host="localhost",
        user="willem",
        password="Dinkel2006!",
        database="shykeiichicom"
    )
    
    mycursor = mydb.cursor()

    mycursor.execute(f"SELECT * FROM forgot_password WHERE address={requestAddress}")

    forgot_password_object = mycursor.fetchone()
    
    if forgot_password_object == None:
        return Response(json.dumps("Invalid address"), status=400, mimetype="application/json")

    curtime = int( time.time() )
    mycursor.execute(f"UPDATE users SET password={requestPassword} where id={forgot_password_object[1]}")
    mycursor.execute(f"UPDATE users SET passwordchanged={curtime} where id={forgot_password_object[1]}")
    mycursor.execute(f"DELETE FROM forgot_password WHERE address={requestAddress}")

    mydb.commit()
        
    return Response(json.dumps("Password Update"), status=200, mimetype="application/json")


app.run(host="192.168.144.6", port="8080")
