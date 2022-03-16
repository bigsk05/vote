from flask import Flask
import socket

HOST = ("0.0.0.0", 8080)
ADDRESS = "http://{}:{}".format(socket.gethostbyname(socket.gethostname()), HOST[1])
#ADDRESS = "http://{}:{}".format(HOST[0], HOST[1])
app = Flask("Vote Program")
ID = 0
event = {}
judger = {}