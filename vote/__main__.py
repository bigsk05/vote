import time, webbrowser, threading, sys

from admin import *
from user import *
from resource import *
from __init__ import *

@app.route("/ping")
def ping():
    return str(time.time())

def run():
    app.run(HOST[0], HOST[1])

web = threading.Thread(target = run)
web.daemon = True
web.start()

webbrowser.open("{}/admin".format(ADDRESS))

while True: 
    cmd = input("")
    if cmd == "reboot":
        sys.exit(0)
    else:
        try:
            exec(cmd)
        except Exception as e:
            print(e)