import json.decoder

import akinator.exceptions
from akinator.async_aki import Akinator

from core.singlep import SinglePlayerGame, UNFINISHED
from core.msgmanager import MessageManager
from core.em import ALPHABET, STOP, QUESTION, PN


class AkinatorDiscord(SinglePlayerGame):
	def __init__(self, session):
		super().__init__(session)
		self.akinator = Akinator()
		self.guessed = False

	async def start_game(self):
		await self.akinator.start_game()
		await MessageManager.edit_message(self.message, self.get_board())

		await MessageManager.add_reaction_and_event(self.message,
		                                            ALPHABET["y"],
		                                            self.player.id,
		                                            self.on_yes_reaction)
		await MessageManager.add_reaction_and_event(self.message,
		                                            ALPHABET["n"],
		                                            self.player.id,
		                                            self.on_no_reaction)
		await MessageManager.add_reaction_and_event(self.message, QUESTION,
		                                            self.player.id,
		                                            self.on_dontknow_reaction)
		await MessageManager.add_reaction_and_event(self.message,
		                                            ALPHABET["p"],
		                                            self.player.id,
		                                            self.on_probably_reaction)
		await MessageManager.add_reaction_and_event(self.message,
		                                            ALPHABET["b"],
		                                            self.player.id,
		                                            self.on_back_reaction)
		await MessageManager.add_reaction_and_event(
		    self.message, PN, self.player.id, self.on_probablynot_reaction)
		await MessageManager.add_reaction_and_event(self.message, STOP,
		                                            self.player.id,
		                                            self.on_quit_game)

	async def on_yes_reaction(self):
		self.on_start_move()
		await MessageManager.remove_reaction(self.message, ALPHABET["y"],
		                                     self.player.member)
		await self.answer(0)

	async def on_no_reaction(self):
		self.on_start_move()
		await MessageManager.remove_reaction(self.message, ALPHABET["n"],
		                                     self.player.member)
		await self.answer(1)

	async def on_probably_reaction(self):
		self.on_start_move()
		await MessageManager.remove_reaction(self.message, ALPHABET["p"],
		                                     self.player.member)
		await self.answer(3)

	async def on_probablynot_reaction(self):
		self.on_start_move()
		await MessageManager.remove_reaction(self.message, PN,
		                                     self.player.member)
		await self.answer(4)

	async def on_back_reaction(self):
		self.on_start_move()
		await MessageManager.remove_reaction(self.message, ALPHABET["b"],
		                                     self.player.member)
		await self.answer("b")

	async def on_dontknow_reaction(self):
		self.on_start_move()
		await MessageManager.remove_reaction(self.message, QUESTION,
		                                     self.player.member)
		await self.answer(2)

	async def answer(self, answer):
		try:
			await self.akinator.answer(
			    answer) if answer != "b" else await self.akinator.back()
			await MessageManager.edit_message(self.session.message,
			                                  self.get_board())
			if self.akinator.progression >= 80 or self.akinator.step == 79:
				await self.akinator.win()
				self.guessed = True
				self.game_state = -1
				await self.end_game()
		except (akinator.exceptions.AkiTimedOut, json.decoder.JSONDecodeError):
			self.game_state = -1
			await self.end_game()
		except akinator.exceptions.CantGoBackAnyFurther:
			pass

	def get_board(self):
		content = f"Question {int(self.akinator.step) + 1}: *{self.akinator.question}*\n"
		if self.guessed:
			content = f"Akinator guesses: {self.akinator.first_guess['name']}\n{self.akinator.first_guess['absolute_picture_path']}"
		return content

	async def on_quit_game(self):
		self.game_state = UNFINISHED
		await self.end_game()
