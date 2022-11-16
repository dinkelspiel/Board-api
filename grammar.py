from flask import Blueprint, Flask, render_template, request, Response, send_file
import mysql.connector
import json, time, uuid
from markupsafe import escape
from functions import isValidSession, getUserPermission

grammar = Blueprint('grammar', __name__, template_folder='templates')
@grammar.route('/api/v1/grammar/creategroup', methods=["PUT"])
def grammarcreategroup():
    if request.json == None:
        return Response(json.dumps("No body was provided"), status=400, mimetype="application/json")

    requestSessionid = request.json.get("sessionid")
    requestGroupName = request.json.get("groupname")
    requestType =      request.json.get("type")
 
    if requestSessionid == None:
        return Response(json.dumps("No sessionid was provided"), status=400, mimetype="application/json")
    if requestGroupName == None:
        return Response(json.dumps("No groupname was provided"), status=400, mimetype="application/json")
    if requestType == None:
        return Response(json.dumps("No type was provided"), status=400, mimetype="application/json")
    
    if not str(requestType).isdigit():
        return Response(json.dumps("Type is not an integer"), status=400, mimetype="application/json")
    
    requestType = int(requestType)
    
    user = isValidSession(requestSessionid)
    if user == False:
        return Response(json.dumps("Invalid session"), status=400, mimetype="application/json")
    
    db = mysql.connector.connect(
        host="localhost",
        user="willem",
        password="Dinkel2006!",
        database="shykeiichicom"
    )

    cursor = db.cursor()
    
    cursor.execute(f"INSERT INTO grammar_groups (name, creatorid, type) VALUES ({requestGroupName}, {user[0]}, {requestType})")
    
    db.commit()
    
    return Response(json.dumps("Created Group"), status=201, mimetype="application/json")
    
    
@grammar.route('/api/v1/grammar/createwords', methods=["PUT"])
def grammarcreatewords():
    if request.json == None:
        return Response(json.dumps("No body was provided"), status=400, mimetype="application/json")

    requestSessionid = request.json.get("sessionid")
    requestWordList = json.loads(request.json.get("wordlist"))
    requestWordGroup =      request.json.get("group")
 
    if requestSessionid == None:
        return Response(json.dumps("No sessionid was provided"), status=400, mimetype="application/json")
    if requestWordList == None:
        return Response(json.dumps("No wordlist was provided"), status=400, mimetype="application/json")
    if requestWordGroup == None:
        return Response(json.dumps("No group was provided"), status=400, mimetype="application/json")
  
    user = isValidSession(requestSessionid)
    if user == False:
        return Response(json.dumps("Invalid session"), status=400, mimetype="application/json")
    
    db = mysql.connector.connect(
        host="localhost",
        user="willem",
        password="Dinkel2006!",
        database="shykeiichicom"
    )

    cursor = db.cursor()
    
    cursor.execute(f"SELECT * FROM grammar_groups WHERE id={requestWordGroup}")
    
    grammar_group = cursor.fetchone()
    
    if(grammar_group[2] != user[0]):
        if(getUserPermission(user[0]) != 1):
            return Response(json.dumps("You cannot modify this group"), status=400, mimetype="application/json")
    
    for word in requestWordList:
        cursor.execute(f"INSERT INTO grammar_gambling_words (word1, word2, correct_word, word_group) VALUES ({word['word1']}, {word['word2']}, {word['correct_word']}, {requestWordGroup})")
    
    db.commit()
    
    return Response(json.dumps("Created Words"), status=201, mimetype="application/json")


@grammar.route('/api/v1/grammar/createwords', methods=["PUT"])
def grammarcreatewords():
    if request.json == None:
        return Response(json.dumps("No body was provided"), status=400, mimetype="application/json")

    requestSessionid = request.json.get("sessionid")
    requestWordList = request.json.get("wordlist")
    requestWordGroup =      request.json.get("group")
 
    if requestSessionid == None:
        return Response(json.dumps("No sessionid was provided"), status=400, mimetype="application/json")
    if requestWordList == None:
        return Response(json.dumps("No wordlist was provided"), status=400, mimetype="application/json")
    if requestWordGroup == None:
        return Response(json.dumps("No group was provided"), status=400, mimetype="application/json")
  
    user = isValidSession(requestSessionid)
    if user == False:
        return Response(json.dumps("Invalid session"), status=400, mimetype="application/json")
    
    db = mysql.connector.connect(
        host="localhost",
        user="willem",
        password="Dinkel2006!",
        database="shykeiichicom"
    )

    cursor = db.cursor()
    
    cursor.execute(f"SELECT * FROM grammar_groups WHERE id={requestWordGroup}")
    
    grammar_group = cursor.fetchone()
    
    if(grammar_group[2] != user[0]):
        if(getUserPermission(user[0]) != 1):
            return Response(json.dumps("You cannot modify this group"), status=400, mimetype="application/json")
    
    for word in requestWordList:
        cursor.execute(f"INSERT INTO grammar_gambling_words (word1, word2, correct_word, word_group) VALUES ({word['word1']}, {word['word2']}, {word['correct_word']}, {requestWordGroup})")
    
    db.commit()
    
    return Response(json.dumps("Created Words"), status=201, mimetype="application/json")

@grammar.route('/api/v1/grammar/getgroups', methods=["GET"])
def grammargetgroups():
    db = mysql.connector.connect(
        host="localhost",
        user="willem",
        password="Dinkel2006!",
        database="shykeiichicom"
    )

    cursor = db.cursor()
    
    cursor.execute(f"SELECT * FROM grammar_groups")
    
    grammar_groups = cursor.fetchall()
    
    grammar_groups_list = []
    
    for x in grammar_groups:
        grammar_groups_list.append({
            "id": x[0],
            "name": x[1],
            "creatorid": x[2],
            "type": x[3]
        })
        
    return grammar_groups_list

@grammar.route('/api/v1/grammar/getgrammar', methods=["GET"])
def grammargetgrammar():
    requestGrammarGroup = request.args.get("group")
    
    if(requestGrammarGroup == None):
        return Response(json.dumps("No grammar group provided"), status=400, mimetype="application/json")
    
    db = mysql.connector.connect(
        host="localhost",
        user="willem",
        password="Dinkel2006!",
        database="shykeiichicom"
    )

    cursor = db.cursor()
    
    cursor.execute(f"SELECT * FROM grammar_gambling_words WHERE word_group={requestGrammarGroup}")
    
    grammar_groups = cursor.fetchall()
    
    grammar_groups_list = []
    
    for x in grammar_groups:
        grammar_groups_list.append({
            "id": x[0],
            "word1": x[1],
            "word2": x[2],
            "correct_word": x[3],
            "word_group": x[4]
        })
        
    return grammar_groups_list