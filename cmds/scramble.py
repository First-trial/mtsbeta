from core.categ import Minigames
from core.cmd import Command
from core.scramble import ScrambleDiscord
from core.singlepses import SinglePlayerSession


class ScrambleCommand(Command):
    bot = None
    name = "scramble"
    help = "Unscramble the letters of a random word, check out the rules with the rules command."
    brief = "Unscramble the letters of a random word."
    args = ""
    category = Minigames

    @classmethod
    async def invoke(cls, context):
        message = await context.send("Starting **scramble** minigame")

        session = SinglePlayerSession(message, "scramble", ScrambleDiscord, context.author)
        await cls.bot.game_manager.start_session(session)