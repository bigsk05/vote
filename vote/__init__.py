from flask import Flask

HOST = ("localhost", 8080)
ADDRESS = "http://{}:{}".format(HOST[0], HOST[1])
app = Flask("Vote Program")
ID = 0
event = {}
judger = {}