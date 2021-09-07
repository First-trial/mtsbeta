from flask import Flask as Quart
from threading import Thread

app = Quart(__name__)


@app.route("/")
def index():
	return "hi"

@app.route("/topgg")
def dbl():
  """"""
  pass


def ru():
  app.run("0.0.0.0", 8090)

def run(bot):
  setattr(app,"bot",bot)
  Thread(target=ru).start()