from flask import Blueprint, Flask, render_template, request, Response, send_file
import mysql.connector
import json, time, uuid
from markupsafe import escape
from functions import isValidSession, getUserPermission


board = Blueprint('board', __name__, template_folder='templates')

@board.route("/api/v1/board/send", methods=["PUT"])
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
        session = isValidSession(sendersessionid_)
        senderid_ = session[1]

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

@board.route("/api/v1/board/get", methods=["GET"])
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


@board.route("/api/v1/board/getsingle", methods=["GET"])
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


@board.route("/api/v1/board/rate", methods=["PUT"])
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


@board.route("/api/v1/board/delete", methods=["PUT"])
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
        if getUserPermission(user[0]) != 1:
            return Response(json.dumps("You do not own this post"), status=500, mimetype="application/json")
    
    sql = f"DELETE FROM board WHERE id={postid_}"
    
    mycursor.execute(sql)
    mydb.commit()
        
    return Response("Deleted Post", status=200, mimetype="application/json")


@board.route("/api/v1/board/deleterange", methods=["PUT"])
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

    usersession = isValidSession(sessionid_) 
    if(usersession == False):
        return Response(json.dumps("Invalid sessionid"), status=400, mimetype="application/json")
    
    mycursor.execute(f"SELECT * FROM users WHERE id=\"{usersession[1]}\"")

    user = mycursor.fetchone()
    
    if user == None:
        return Response(json.dumps("Invalid sessionid provided 2"), status=400, mimetype="application/json")
    
    if(getUserPermission(user[0]) != 1):
        return Response(json.dumps("User not admin"), status=400, mimetype="application/json")
    
    sql = f"DELETE FROM board WHERE id BETWEEN {minr_} AND {maxr_}"
    
    mycursor.execute(sql)
    mydb.commit()
        
    return Response(f"Deleted Post from {minr_} to {maxr_}", status=200, mimetype="application/json")
