from core.categ import Minigames
from core.cmd import Command
from core.aki import AkinatorDiscord
from core.singlepses import SinglePlayerSession


class AkinatorCommand(Command):
	bot = None
	name = "akinator"
	help = "Start the akinator to guess with yes/no questions what character you are thinking of. Character can be fictional or real."
	brief = "Start the akinator to guess with yes/no questions what character you are thinking of."
	args = ""
	aliases = ["aki"]
	category = Minigames

	@classmethod
	async def invoke(cls, context):
		message = await context.send("Starting **akinator** minigame")
		#print(message)

		session = SinglePlayerSession(message, "akinator", AkinatorDiscord,
		                              context.author)
		await cls.bot.game_manager.start_session(session)
