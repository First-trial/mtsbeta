from flask import Flask as Quart, request
from threading import Thread
import os
from discord.ext.commands import Bot

app = Quart(__name__)

@app.route("/")
def index():
	return "hi"

@app.route("/topgg", methods=["POST"])
def dbl():
  """"""
  h=request.headers.get("Authorization")
  print(request.headers)
  print(request.data)
  if h==os.environ.get("_ttpw") or h==os.environ.get("sbl_tok"):
    print(request.data)
    #app.bot.dispatch("voted", request.data)
  return "hehr"


def ru():
  app.run("0.0.0.0", 8090)#,loop=app.bot.loop)

def run(bot: Bot):
  setattr(app,"bot",bot)
  @bot.event
  async def on_voted(data):
    print(data)
  Thread(target=ru).start()