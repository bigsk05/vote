import json
from flask import request, redirect
from __init__ import *

@app.route("/admin")
def admin():
    result = '<meta charset="UTF-8"/><h1>会话列表:</h1>'
    for i in event.keys():
        result += '''<a href="{}/admin/detail/{}">{}</a><br/>'''.format(ADDRESS, i, event[i]["name"])
    result += "<h1>添加会话:</h1>"
    result += '''
        <form action="{}/admin/add">
        会话名:<br>
        <input type="text" name="name">
        <br><br>
        <input type="submit" value="提交">
        </form> 
    '''.format(ADDRESS)
    return result

@app.route("/admin/add")
def add():
    global ID
    name = request.args.get("name")
    if name not in [e["name"] for e in event.values()]:
        idGet = ID
        ID += 1
        event[idGet] = {
            "name": name,
            "member": {},
            "status": False
        }
        return "<meta charset\"UTF-8\"/><h1>会话ID: {0}</h1><br/><a href=\"{1}/admin/detail/{0}\">查看详细</a><br/><a href=\"{1}/admin\">返回管理主页</a>".format(idGet, ADDRESS)
    else:
        return "<meta charset\"UTF-8\"/><h1>会话名已存在！</h1><br/><a href=\"{}/admin\">返回管理主页</a>".format(ADDRESS)

@app.route("/admin/remove/<string:id>")
def remove(id):
    try:
        event[int(id)]
    except:
        return "<meta charset\"UTF-8\"/><h1>找不到会话！</h1><br/><a href=\"{}/admin\">返回管理主页</a>".format(ADDRESS)
    else:
        del event[int(id)]
        return redirect("{}/admin".format(ADDRESS), 302)

@app.route("/admin/detail/<string:id>")
def detail(id):
    try:
        detail = event[int(id)]
    except:
        return "<meta charset\"UTF-8\"/><h1>找不到会话！</h1><br/><a href=\"{}/admin\">返回管理主页</a>".format(ADDRESS)
    else:
        result = "<meta charset\"UTF-8\"/><h1>{0}</h1><h2>ID: {1}</h2><h3>成员列表：</h3>".format(detail["name"], id)
        for i in event[int(id)]["member"].keys():
            maxJudger = "暂未评分"
            maxScore = 0
            for j in judger.keys():
                if judger[j].get(int(id), False):
                    for p in judger[j][int(id)].keys():
                        if p == i:
                            if maxScore < judger[j][int(id)][p]:
                                maxJudger = judger[j]["name"]
                                maxScore = judger[j][int(id)][p]
            result += "<h4>{} <a href=\"{}/admin/rm_member/{}/{}\">删除</a> 打分最高：{} {}分</h4>".format(i, ADDRESS, id, i, maxJudger, maxScore)
        result += ""
        result += '''
        <form action="{0}/admin/add_member/{1}">
        成员名: (批量添加，请使用半角逗号 , 分隔) <br>
        <input type="text" name="name">
        <br><br>
        <input type="submit" value="提交">
        </form> 
        '''.format(ADDRESS, id)
        if event[int(id)]["status"]:
            result += "<a href=\"{}/admin/end/{}\">结束</a><br/>".format(ADDRESS, id)
        else:
            result += "<a href=\"{}/admin/start/{}\">开始</a><br/>".format(ADDRESS, id)
        result += "<a href=\"{}/admin/remove/{}\">删除会话</a><br/>".format(ADDRESS, id)
        result += "<a href=\"{}/admin\">返回管理主页</a>".format(ADDRESS)
        return result

@app.route("/admin/add_member/<string:id>")
def add_member(id):
    try:
        event[int(id)]
    except:
        return "<meta charset\"UTF-8\"/><h1>找不到会话！</h1><a href=\"{}/admin\">返回管理主页</a>".format(ADDRESS)
    else:
        name = request.args.get("name")
        if "," in name:
            names = name.split(",")
            for n in names:
                event[int(id)]["member"][n] = []
        else:
            event[int(id)]["member"][name] = []
        return "<meta charset\"UTF-8\"/><h1>添加成功！</h1><a href=\"{}/admin/detail/{}\">返回详细页</a>".format(ADDRESS, id)

@app.route("/admin/rm_member/<string:id>/<string:name>")
def rm_member(id, name):
    try:
        event[int(id)]
    except:
        return "<meta charset\"UTF-8\"/><h1>找不到会话！</h1><a href=\"{}/admin\">返回管理主页</a>".format(ADDRESS)
    else:
        if name not in event[int(id)]["member"]:
            return "<meta charset\"UTF-8\"/><h1>找不到此成员！</h1><meta http-equiv=\"refresh\" content=\"{}/admin/detail/{}\"\><h3>3秒后返回</h3>".format(ADDRESS, id)
        else:
            del event[int(id)]["member"][name]
            return redirect("{}/admin/detail/{}".format(ADDRESS, id), 302)

@app.route("/admin/start/<string:id>")
def start(id):
    try:
        event[int(id)]
    except:
        return "<meta charset\"UTF-8\"/><h1>找不到会话！</h1><a href=\"{}/admin\">返回管理主页</a>".format(ADDRESS)
    else:
        event[int(id)]["status"] = True
        return redirect("{}/admin/detail/{}".format(ADDRESS, id), 302)

@app.route("/admin/end/<string:id>")
def end(id):
    try:
        event[int(id)]
    except:
        return "<meta charset\"UTF-8\"/><h1>找不到会话！</h1><a href=\"{}/admin\">返回管理主页</a>".format(ADDRESS)
    else:
        event[int(id)]["status"] = False
        return redirect("{}/admin/detail/{}".format(ADDRESS, id), 302)

@app.route("/admin/system")
def system():
    return json.dumps([ID, event, judger]), {"content-type": "application/json"}