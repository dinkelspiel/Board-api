from flask import Blueprint, Flask, render_template, request, Response, send_file
import mysql.connector
import json, time, uuid
from markupsafe import escape

def getUserPermission(userid):
    mydb = mysql.connector.connect(
        host="localhost",
        user="willem",
        password="Dinkel2006!",
        database="shykeiichicom"
    )
        
    mycursor = mydb.cursor()

    mycursor.execute(f"SELECT * FROM elevated_permissions WHERE userid={userid}")
    
    permission = mycursor.fetchone()
    
    if(permission == None):
        return 0

    return permission[2]

def isValidSession(sessionid):
    mydb = mysql.connector.connect(
        host="localhost",
        user="willem",
        password="Dinkel2006!",
        database="shykeiichicom"
    )
    
    mycursor = mydb.cursor()

    mycursor.execute(f"SELECT * FROM sessions WHERE sessionid={sessionid}")

    myresult = mycursor.fetchone()
    
    if myresult == None:
        return False
    
    if(int(time.time() - int(myresult[2])) > 2419200):
        mycursor.execute(f"DELETE FROM sessions WHERE sessionid={sessionid}")
        return False
    
    return {
        "sessionid": myresult[0],
        "userid": myresult[1],
        "timestamp": myresult[2]
    }