from flask import request, redirect
from __init__ import *
from database import *

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
            result += "<h4>{}</h4>".format(i)
        result += ""
        result += '''
        <form action="{0}/admin/add_member/{1}">
        成员名:<br>
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
        event[int(id)]["member"][name] = []
        return "<meta charset\"UTF-8\"/><h1>添加成功！</h1><a href=\"{}/admin/detail/{}\">返回详细页</a>".format(ADDRESS, id)


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