from template import *
from __init__ import *

@app.route("/resource/jquery.js")
def jquery():
    #return JQUERY, {"content-type": "text/javascript"}
    with open("vote/jquery.js", "r") as fb:
        return fb.read(), {"content-type": "text/javascript"}