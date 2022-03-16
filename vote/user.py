import time, hashlib, qrcode, io, base64
from flask import make_response, redirect, request
from __init__ import *
from template import *

@app.route("/user/reg/<string:id>")
def reg(id):
    try:
        event[int(id)]
    except:
        return "<meta charset\"UTF-8\"/><h1>找不到会话！</h1>"
    else:
        name = event[int(id)]["name"]
        result = REG
        form = "姓名:<input type=\"text\" name=\"name\">"
        return result.format(NAME = name, FORM = form, ACTION = '{}/user/reg_process/{}'.format(ADDRESS, id))

@app.route("/user/reg_process/<string:id>")
def reg_process(id):
    name = request.args.get('name')
    hash = hashlib.sha1("{}-{}".format(name, time.time()).encode()).hexdigest()
    judger[hash] = {}
    judger[hash]["name"] = name
    resp = make_response(redirect("{}/user/vote/{}".format(ADDRESS, id), 302))
    resp.delete_cookie("vote-uuid")
    resp.set_cookie("vote-uuid", hash, max_age = 36000)
    return resp

@app.route("/user/vote/<string:id>")
def vote(id):
    try:
        event[int(id)]
    except:
        return "<meta charset\"UTF-8\"/><h1>找不到会话！</h1>"
    else:
        vote_uuid = request.cookies.get('vote-uuid')
        if vote_uuid not in judger.keys():
            return redirect("{}/user/reg/{}".format(ADDRESS, id), 302)
        if len(judger[vote_uuid].keys()) != 1:
            return "<meta charset\"UTF-8\"/><h1>感谢参与本次会话！</h1>"
        if event[int(id)]["status"]:
            name = event[int(id)]["name"]
            result = VOTE
            form = ""
            for i in event[int(id)]["member"].keys():
                form += "{0}:<input type=\"number\" name=\"{0}\" value=90 max=\"100.00\" step=\"0.01\">".format(i)
            return result.format(NAME = name, FORM = form, ACTION = '{}/user/vote_post/{}'.format(ADDRESS, id))
        else:
            return '<meta http-equiv="refresh" content="2"\><h1>会话暂未开放！</h1>'

@app.route("/user/vote_post/<string:id>")
def vote_post(id):
    vote_uuid = request.cookies.get('vote-uuid')
    judger[vote_uuid][int(id)] = {}
    for i in event[int(id)]["member"].keys():
        judger[vote_uuid][int(id)][i] = float(request.args.get(i))
    for i in event[int(id)]["member"].keys():
        event[int(id)]["member"][i].append(float(request.args.get(i)))
    return redirect("{}/user/vote/{}".format(ADDRESS, id), 302)

@app.route("/user/view/<string:id>")
def view(id):
    try:
        event[int(id)]
    except:
        return "<meta charset\"UTF-8\"/><h1>找不到会话！</h1>"
    else:
        result = ""
        i = 0
        for m in event[int(id)]["member"].keys():
            if len(event[int(id)]["member"][m]):
                if len(event[int(id)]["member"][m]) <= 2:
                    result += 'arrVisitors[{}] = "{}, {}";'.format(i, m, sum(event[int(id)]["member"][m]) / (len(event[int(id)]["member"][m])))
                    i += 1
                else:
                    sumup = sum(event[int(id)]["member"][m]) - max(event[int(id)]["member"][m]) - min(event[int(id)]["member"][m])
                    result += 'arrVisitors[{}] = "{}, {}";'.format(i, m, sumup / (len(event[int(id)]["member"][m]) - 2))
                    i += 1
        width = 100 * len(event[int(id)]["member"])
        qr = qrcode.QRCode(     
            version = 1,     
            error_correction = qrcode.constants.ERROR_CORRECT_L,     
            box_size = 10,     
            border = 1, 
        )
        qr.make(fit=True) 
        text = '{}/user/reg/{}'.format(ADDRESS, id)
        qr.add_data(text)
        img = qr.make_image()

        buf = io.BytesIO()
        img.save(buf, format='PNG')
        image_stream = buf.getvalue()
        heximage = base64.b64encode(image_stream)
        return VIEW.format(result, width, text, heximage.decode(), 200, ADDRESS, "/resource/jquery.js")