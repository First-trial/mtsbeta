from core.categ import Minigames
from core.cmd import Command
from core.hangman import HangmanDiscord
from core.singlepses import SinglePlayerSession


class HangmanCommand(Command):
	bot = None
	name = "hangman"
	help = "Play hangman against the bot, check out the rules with the rules command."
	brief = "Play hangman against the bot."
	args = ""
	category = Minigames

	@classmethod
	async def invoke(cls, context):
		message = await context.send("Starting **hangman** minigame")

		session = SinglePlayerSession(message, "hangman", HangmanDiscord,
		                              context.author)
		await cls.bot.game_manager.start_session(session)
