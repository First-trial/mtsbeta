from quart import Quart

app = Quart(__name__)


@app.route("/")
async def index():
	return "hi"

@app.route("/topgg")
async def dbl():
  pass


async def run(leep):
  await app.run_task("0.0.0.0", 8090)
