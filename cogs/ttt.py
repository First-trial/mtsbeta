from typing import List, Union
import discord
from core.msgmanager import MessageManager
from core.em import REPEAT
from discord.ext import commands
import sys, traceback
from core import Cog
import random


async def o(ctx, *args, **kwargs):
	return ctx.author.id == ctx.bot.author_id


class RestartButton(discord.ui.Button["Restart"]):
	def __init__(self, bb: bool = False):
		self.bb = bb
		super().__init__(style=discord.ButtonStyle.primary,
		                 label="Restart",
		                 emoji=REPEAT,
		                 row=3)

	async def callback(self, interaction):
		assert self.view is not None
		view = self.view
		#await interaction.message.channel.send("Hi.")
		if not interaction.user.id in [view.x.id, view.o.id]:
			return await interaction.response.send_message(
			    "You are not in this game!", ephemeral=True)
		#await view.remove_item(self)
		if self.bb:
			await interaction.message.edit(
			    f"It's your turn!\nYou have `30 seconds` to respond!",
			    view=TicTacToe(view.x, view.o, view.m, view.b))
		else:
			await interaction.message.edit(
			    content=
			    f"Its {view.o.mention}'s turn!\nYou have `30 seconds` to respond!",
			    view=TicTacToe(view.o, view.x, view.m, view.b))
		await interaction.response.send_message(
		    "Successfully started a new match!", ephemeral=True)


class TicTacToeButton(discord.ui.Button['TicTacToe']):
	def __init__(self, x: int, y: int):
		super().__init__(style=discord.ButtonStyle.secondary,
		                 label=' \u200b \u200b ',
		                 row=y)
		self.x = x
		self.y = y

	# This function is called whenever this particular button is pressed
	# This is part of the "meat" of the game logic
	async def my_call(self, interaction: discord.Interaction):
		assert self.view is not None
		view = self.view
		if not interaction.user.id in (view.x.id, view.o.id):
			content = "You are not in this game."
			return await interaction.response.send_message(content=content,
			                                               ephemeral=True)

		view.board[self.y][
		    self.x] = view.X if view.b.user.id != view.x.id else view.O
		self.style = discord.ButtonStyle.danger if view.b.user.id != view.x.id else discord.ButtonStyle.success
		self.label = 'O' if view.b.user.id == view.x.id else "X"
		self.disabled = True
		o = view.o if view.x.id == view.b.user.id else view.x
		content = f"It's now your turn {o.mention}\nYou have 30 seconds to respond."
		winner = view.check_board_winner()
		if winner is not None:
			if (winner == view.X and view.x.id == view.b.user.id) or (
			    winner == view.O and view.o.id == view.b.user.id):
				content = f'I won!'
			elif winner == view.Tie:
				content = "It's a tie!"
			else:
				content = "You won!"

			for child in view.children:
				child.disabled = True
			#view.stop()
			view.current_player = None
			view.add_item(RestartButton(bb=True))
			return await interaction.response.edit_message(content=content,
			                                               view=view)
		row, col = view.my_turn()
		view.board[row][
		    col] = view.X if view.b.user.id == view.x.id else view.O
		if col == 0:
			button, r = view.children[row], row
		elif col == 1:
			button, r = view.children[row + 3], row + 3
		else:
			button, r = view.children[row + 6], row + 6
		button.style = discord.ButtonStyle.danger if view.b.user.id == view.x.id else discord.ButtonStyle.success
		button.label = 'O' if view.b.user.id != view.x.id else "X"
		button.disabled = True
		winner = view.check_board_winner()
		if winner is not None:
			if (winner == view.X and view.x.id == view.b.user.id) or (
			    winner == view.O and view.o.id == view.b.user.id):
				content = f'I won!'
			elif winner == view.Tie:
				content = "It's a tie!"
			else:
				content = "You won!"

			for child in view.children:
				child.disabled = True
			#view.stop()
			view.current_player = None
			view.add_item(RestartButton(bb=True))
			return await interaction.response.edit_message(content=content,
			                                               view=view)
		view.children[r] = button
		return await interaction.response.edit_message(content=content,
		                                               view=view)

	async def callback(self, interaction: discord.Interaction):
		assert self.view is not None
		view: TicTacToe = self.view
		state = view.board[self.y][self.x]
		if state in (view.X, view.O):
			return

		if view.b.user.id in (view.x.id, view.o.id):
			return await self.my_call(interaction)
		print(list(i for i in view.children))
		if view.current_player == view.X and interaction.user.id == view.x.id:
			self.style = discord.ButtonStyle.danger
			self.label = 'X'
			self.disabled = True
			view.board[self.y][self.x] = view.X
			view.current_player = view.O
			content = f"It is now {view.o.mention}'s turn\nYou have `30 seconds` to respond"
		elif view.current_player == view.O and interaction.user.id == view.o.id:
			self.style = discord.ButtonStyle.success
			self.label = 'O'
			self.disabled = True
			view.board[self.y][self.x] = view.O
			view.current_player = view.X
			content = f"It is now {view.x.mention}'s turn\nYou have `30 seconds` to respond"
		else:
			content = "You are not in this game." if interaction.user.id not in (
			    view.x.id, view.o.id) else "It's not your turn now!"
			return await interaction.response.send_message(content=content,
			                                               ephemeral=True)
		winner = view.check_board_winner()
		if winner is not None:
			if winner == view.X:
				content = f'{view.x.mention} won!'
			elif winner == view.O:
				content = f'{view.o.mention} won!'
			else:
				content = "It's a tie!"

			for child in view.children:
				child.disabled = True
			#view.stop()
			view.current_player = None
			view.add_item(RestartButton())
		await interaction.response.edit_message(content=content, view=view)
		#await interaction.message.


# This is our actual board View
class TicTacToe(discord.ui.View):
	# This tells the IDE or linter that all our children will be TicTacToeButtons
	# This is not required
	children: Union[List[TicTacToeButton], RestartButton]
	X = -1
	O = 1
	Tie = 2

	def __init__(self, p1, p2, m, b):
		super().__init__(timeout=30.0)
		self.x, self.o = p1, p2
		self.current_player = self.X
		self.board = [
		    [0, 0, 0],
		    [0, 0, 0],
		    [0, 0, 0],
		]
		self.m, self.b = m, b

		# Our board is made up of 3 by 3 TicTacToeButtons
		# The TicTacToeButton maintains the callbacks and helps steer
		# the actual game.
		for x in range(3):
			for y in range(3):
				self.add_item(TicTacToeButton(x, y))

	# This method checks for the board winner -- it is used by the TicTacToeButton
	def check_board_winner(self):
		for across in self.board:
			value = sum(across)
			if value == 3:
				return self.O
			elif value == -3:
				return self.X

		# Check vertical
		for line in range(3):
			value = self.board[0][line] + self.board[1][line] + self.board[2][
			    line]
			if value == 3:
				return self.O
			elif value == -3:
				return self.X

		# Check diagonals
		diag = self.board[0][2] + self.board[1][1] + self.board[2][0]
		if diag == 3:
			return self.O
		elif diag == -3:
			return self.X

		diag = self.board[0][0] + self.board[1][1] + self.board[2][2]
		if diag == 3:
			return selfp
		elif diag == -3:
			return self.X

		# If we're here, we need to check if a tie was made
		if all(i != 0 for row in self.board for i in row):
			return self.Tie

		return None

	def my_turn(self):
		choices = []
		for rowpos, row in enumerate(self.board):
			for colpos, col in enumerate(row):
				if col == 0:
					choices.append((rowpos, colpos))

		my_choice = random.choice(choices)
		return my_choice

	async def on_timeout(self):
		c = self.b.get_channel(self.m.channel.id)
		v = self
		for childre in v.children:
			childre.disabled = True
		if self.current_player is None:
			self.m = await self.c.fetch_message(self.m.id)

			return await self.m.edit(content=f"{self.m.content}", view=v)

		if self.current_player == self.X:
			co = f"{self.x.mention} didn't moved in `30 seconds` so {self.o.mention} won the game!"
		else:
			co = f"{self.o.mention} didn't moved in `30 seconds` so {self.x.mention} won the game!"
		self.current_player = None
		self.m = await c.fetch_message(self.m.id)

		await self.m.edit(content=f"{co}", view=self)

		print("exp")


class tic(Cog, name="Tictactoe"):
	def __init__(self, bot):
		self.bot = bot

	@commands.group(aliases=["tic", "ttt", "tac", "toe"],
	                invoke_without_command=True)
	@commands.guild_only()
	async def tictactoe(self, ctx, user: discord.Member = None):
		"""mention a user with whom you want to play tictactoe
		"""
		#await ctx.send('Tic Tac Toe: X goes first', view=TicTacToe())

		if not user:
			return await ctx.send(
			    f"Uh oh\nYou missed member argument `{ctx.prefix}{ctx.command} @member`\nare u alone?\nPlay with me by `{ctx.prefix}{ctx.command} ai`"
			)
		if user.id == ctx.author.id:
			return await ctx.send(
			    f"You can't play against yourself!\nare u alone?\nPlay with me by `{ctx.prefix}{ctx.command} ai`"
			)
		if user.bot:
			return await ctx.send(
			    "You can't play against bots, and why do u wanna play with bots?? If u want to then u can play with me"
			)
		p2 = user
		p1 = ctx.author
		m = await ctx.send("Starting...")
		view = TicTacToe(p1, p2, m, self.bot)
		await m.edit(f"it's {p1.mention}'s turn.", view=view)

	@tictactoe.command(name="test", aliases=["t"])
	@commands.check(o)
	async def tictactoe_t(self, ctx, user: discord.Member = None):
		"""mention a user with whom you want to play tictactoe
		"""
		#await ctx.send('Tic Tac Toe: X goes first', view=TicTacToe())

		if not user:
			return await ctx.send(
			    f"Uh oh\nYou missed member argument `{ctx.prefix}{ctx.command} @member`"
			)
		p2 = user
		p1 = ctx.author
		m = await ctx.send("Starting...")
		view = TicTacToe(p1, p2, m, self.bot)
		await m.edit(f"it's {p1.mention}'s turn.", view=view)

	@tictactoe.command(
	    name="ai",
	    aliases=["ui", "<@768680278604382238>", "<@!768680278604382238>"])
	@commands.guild_only()
	async def tictactoe_ai(self, ctx):
		p1, p2 = ctx.author, self.bot.user
		m = await ctx.send("Starting...")
		view = TicTacToe(p1, p2, m, self.bot)
		await m.edit(f"it's your' turn.", view=view)

	@tictactoe.error
	async def ttt_err(self, ctx, exc):
		if isinstance(exc, commands.NoPrivateMessage):
			return await ctx.send(
			    "This command can't be used here,You can use this command in the servers only"
			)
		if isinstance(exc, commands.BotMissingPermissions):
			return await ctx.send("I don't have `manage_messages` for this")
		if isinstance(exc, commands.errors.MemberNotFound):
			return await ctx.reply(
			    "Try that command again and this time, use a real member!")
		print(exc, file=sys.stderr)
		traceback.print_exc()

	@tictactoe_ai.error
	async def tictactoe_ai_error(self, ctx, exc):
		if isinstance(exc, commands.NoPrivateMessage):
			return await ctx.send(
			    "This command can't be used here,You can use this command in the servers only"
			)
		print(exc, file=sys.stderr)
		traceback.print_exc()


def setup(bot):
	bot.add_cog(tic(bot))
