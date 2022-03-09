import random, time, hashlib
from flask import make_response, redirect
from __init__ import *
from template import *

@app.route("/user/reg/<string:id>")
def reg(id):
    hash = hashlib.sha1("{}-{}".format(random.randint(0, 10000), time.time()).encode()).hexdigest()
    judger[hash] = {}
    resp = make_response(redirect("{}/user/vote/{}".format(ADDRESS, id), 302))
    resp.delete_cookie("vote-uuid")
    resp.set_cookie("vote-uuid", hash, max_age = 36000)
    return resp

@app.route("/user/vote/<string:id>")
def vote(id):
    try:
        event[int(id)]
    except:
        return "<meta charset\"UTF-8\"/><h1>找不到会话！</h1>".format(ADDRESS)
    else:
        if event[int(id)]["status"]:
            name = event[int(id)]["name"]
            result = VOTE
            return result.format(NAME = name, FORM = "")
        else:
            return'<meta http-equiv="refresh" content="2"\><h1>会话暂未开放！</h1>'
    

@app.route("/user/view/<string:id>")
def view(id):...