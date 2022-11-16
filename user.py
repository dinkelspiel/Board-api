from flask import Blueprint, Flask, render_template, request, Response, send_file
import mysql.connector
import json, time, uuid
from markupsafe import escape
from functions import isValidSession, isUserAdmin

user = Blueprint('user', __name__, template_folder='templates')

@user.route("/api/v1/user/create", methods=["POST"])
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


@user.route("/api/v1/user/login", methods=["POST"])
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


@user.route("/api/v1/user/validatesession", methods=["POST"])
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

    if(isValidSession(requestSessionid) == False):
        return Response(json.dumps("Invalid sessionid"), status=400, mimetype="application/json")
    
    mycursor.execute("SELECT * FROM users WHERE id=\"" + str(myresult[1]) + "\"")

    myresult = mycursor.fetchone()
    
    mycursor.execute(f"SELECT * FROM elevated_permissions WHERE userid={myresult[0]}")
    
    permission = mycursor.fetchone()
    
    result = {
        "id": myresult[0],
        "username": myresult[1],
        "email": myresult[2],
        "registered": myresult[4],
        "passwordchanged": myresult[5],
        "permission": 0 if permission == None else permission[2]
    }

    return Response(json.dumps(result), status=200, mimetype="application/json")


@user.route("/api/v1/users/getall", methods=["GET"])
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
    
    if(isValidSession(requestSessionid) == False):
        return Response(json.dumps("Invalid sessionid"), status=400, mimetype="application/json")
    
    if(not isUserAdmin(myresult[1])):
        return Response(json.dumps("User not admin"), status=400, mimetype="application/json")
    
    mycursor.execute("SELECT * FROM users")

    myresult = mycursor.fetchall()
    
    users = []
    
    for x in myresult:
        mycursor.execute(f"SELECT * FROM elevated_permissions WHERE userid={x[0]}")
    
        permission = mycursor.fetchone()
    
        result = {
            "id": x[0],
            "username": x[1],
            "email": x[2],
            "registered": x[4],
            "passwordchanged": x[5],
            "permission": 0 if permission == None else permission[2]
        }

        users.append(result)
        
    return Response(json.dumps(users), status=200, mimetype="application/json")

@user.route("/api/v1/users/get", methods=["GET"])
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
    
    if(isValidSession(requestSessionid) == False):
        return Response(json.dumps("Invalid sessionid"), status=400, mimetype="application/json")
    
    if(not isUserAdmin(myresult[1])):
        return Response(json.dumps("User not admin"), status=400, mimetype="application/json")
    
    mycursor.execute(f"SELECT * FROM users WHERE id={requestUserid}")

    user = mycursor.fetchone()

    mycursor.execute(f"SELECT * FROM elevated_permissions WHERE userid={requestUserid}")
    
    permission = mycursor.fetchone()
    
    if(user == None):
        return Response(json.dumps("User not found"), status=400, mimetype="application/json")
    
    result = {
        "id": user[0],
        "username": user[1],
        "email": user[2],
        "registered": user[4],
        "passwordchanged": user[5],
        "permission": 0 if permission == None else permission[2]
    }
        
    return Response(json.dumps(result), status=200, mimetype="application/json")


@user.route("/api/v1/user/delete", methods=["POST"])
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

    if(isValidSession(requestSessionid) == False):
        return Response(json.dumps("Invalid sessionid"), status=400, mimetype="application/json")
    
    if(not isUserAdmin(myresult[1])):
        return Response(json.dumps("User not admin"), status=400, mimetype="application/json")
    
    mycursor.execute(f"SELECT * FROM users WHERE id=\"{requestUserID}\"")
    
    myresult = mycursor.fetchone()
    
    if(myresult == None):
        return Response(json.dumps("Userid to remove is not valid"), status=400, mimetype="application/json")

    mycursor.execute(f"DELETE FROM users WHERE id={requestUserID}")
    
    mydb.commit()
        
    return Response(json.dumps("User removed"), status=200, mimetype="application/json")


@user.route("/api/v1/admin/user/edit", methods=["POST"])
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
    requestEditPermission = request.json.get("permission")
    requestEditPassword = request.json.get("password")

    mydb = mysql.connector.connect(
        host="localhost",
        user="willem",
        password="Dinkel2006!",
        database="shykeiichicom"
    )
    
    mycursor = mydb.cursor()

    if(isValidSession(requestSessionid) == False):
        return Response(json.dumps("Invalid sessionid"), status=400, mimetype="application/json")
    
    if(not isUserAdmin(myresult[1])):
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


@user.route("/api/v1/user/forgotpassword", methods=["POST"])
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

    if(isValidSession(requestSessionid) == False):
        return Response(json.dufmps("Invalid sessionid"), status=400, mimetype="application/json")
    
    if(not isUserAdmin(myresult[1])):
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


@user.route("/api/v1/user/changepassword", methods=["POST"])
def userchangepassword():
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

    mycursor.execute(f"SELECT * FROM forgot_password WHERE address=\"{requestAddress}\"")

    forgot_password_object = mycursor.fetchone()
    
    if forgot_password_object == None:
        return Response(json.dumps("Invalid address"), status=400, mimetype="application/json")

    curtime = int( time.time() )
    mycursor.execute(f"UPDATE users SET password=\"{requestPassword}\" WHERE id=\"{forgot_password_object[1]}\"")
    mycursor.execute(f"UPDATE users SET passwordchanged=\"{curtime}\" WHERE id=\"{forgot_password_object[1]}\"")
    mycursor.execute(f"DELETE FROM forgot_password WHERE address=\"{requestAddress}\"")
    mycursor.execute(f"DELETE FROM sessions WHERE userid=\"{forgot_password_object[1]}\"")

    mydb.commit()
        
    return Response(json.dumps("Password Update"), status=200, mimetype="application/json")
