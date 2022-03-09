import time
from database import *

from admin import *
from user import *
from __init__ import *

@app.route("/ping")
def ping():
    return str(time.time())

app.run(HOST[0], HOST[1])
