# Logic
import discord
from plugins.games import LogicBase


class Hangman_Logic(LogicBase):
  def __init__(self):
    self.lives = 10
    self.word = self.get_random_word()
    self.current_word = ["_" for i in self.word]
    self.guessed = []

  def guess(self, char):
    if char in self.guessed:
      return

    if char not in self.word:
      self.lives -= 1
      self.guessed.append(char)
      return

    for i in range(len(self.word)):
      if self.word[i] == char:
        self.current_word[i] = char
      self.guessed.append(char)

  @property
  def won(self):
    return "_" not in self.current_word

  @property
  def lost(self):
    return self.lives <= 0


HANGMAN0 = "_______"


HANGMAN1 = "  |\n" \
           "  |\n" \
           "  |\n" \
           "  |\n" \
           " _|_ _ _"


HANGMAN2 = " _____\n" \
           " |\n" \
           " |\n" \
           " |\n" \
           " |\n" \
           "_|_ _ _"


HANGMAN3 = " _____\n" \
           " |/\n" \
           " |\n" \
           " |\n" \
           " |\n" \
           "_|_ _ _"


HANGMAN4 = " _____\n" \
           " |/  |\n" \
           " |\n" \
           " |\n" \
           " |\n" \
           "_|_ _ _"


HANGMAN5 = " _____\n" \
           " |/  |\n" \
           " |   0\n" \
           " |\n" \
           " |\n" \
           "_|_ _ _"


HANGMAN6 = " _____\n" \
           " |/  |\n" \
           " |   o\n" \
           " |   |\n" \
           " |\n" \
           "_|_ _ _"


HANGMAN7 = " _____\n" \
           " |/  |\n" \
           " |   o\n" \
           " |  /|\n" \
           " |\n" \
           "_|_ _ _"


HANGMAN8 = " _____\n" \
           " |/  |\n" \
           " |   o\n" \
           " |  /|\\ \n" \
           " |\n" \
           "_|_ _ _"


HANGMAN9 = " _____\n" \
           " |/  |\n" \
           " |   o\n" \
           " |  /|\\ \n" \
           " |  /\n" \
           "_|_ _ _"


HANGMAN10 = " _____\n" \
            " |/  |\n" \
            " |   o\n" \
            " |  /|\\ \n" \
            " |  / \\ \n" \
            "_|_ _ _"


HANGMEN = [
  HANGMAN10, HANGMAN9, HANGMAN8, HANGMAN7, HANGMAN6, HANGMAN5, HANGMAN4,
  HANGMAN3, HANGMAN2, HANGMAN1, HANGMAN0
]


# Main Game

from config import Emote
from models import balance
from string import ascii_lowercase
from plugins.games import SinglePlayer, Player


class Hangman(SinglePlayer):
  def __init__(self,*args, coins):
    super().__init__(*args, timeout=30.0)
    self.logic = Hangman_Logic()
    for lett in ascii_lowercase:
      emoji = getattr(Emote.ALPHABET, lett)
      if lett not in ["u","v","w","x","y","z"]:
        self.add_button_event(emoji, self.player, self.on_click, lett)

    self.add_item(discord.ui.Button(emoji=Emote.ARROW_LEFT, disabled=True))
    self.add_item(discord.ui.Button(label="\u200b", disabled=True))
    self.add_button_event(Emote.STOP, self.player, self.on_quit,)
    self.add_item(discord.ui.Button(label="\u200b", disabled=True))
    self.add_button_event(Emote.ARROW_RIGHT, self.player, self.on_next,)
    self.bet = coins

  async def start_game(self):
    pg = self.create_page()

    for i in range(len(ascii_lowercase)):
      lett = ascii_lowercase[i]
      emoji = getattr(Emote.ALPHABET, lett)
      if lett not in ["u","v","w","x","y","z"]: continue
      row = (1 if lett in ["u","v","w"] else 2)
      self.add_button_event(emoji, self.player, self.on_click, lett, page=pg, row=row)

    self.add_button_event(Emote.ARROW_LEFT, self.player, self.on_prev, page=pg,row=3)
    self.add_button(Emote.STOP, self.player, page=pg,row=3)
    pg.cont.append(discord.ui.Button(emoji=Emote.ARROW_RIGHT, disabled=True,row=3))

    await self.msg.edit(content=await self.get_board())

  async def on_quit(self, inter):
    self.lose()
    await self.update(inter)

  async def on_next(self, inter):
    await self.pages[-1].show(inter)

  async def on_prev(self, inter):
    await self.pages[-1].show(inter,self.pages[-1].backup,)

  async def on_click(self, lett, inter):
    pg = self.pages[-1]
    self.logic.guess(lett)

    if self.logic.won: self.win()
    elif self.logic.lost: self.lose()

    [b for b in self.children if str(b.emoji) == getattr(Emote.ALPHABET,lett)][0].disabled=True

    await self.update(inter)

  async def get_board(self):
    _word = self.logic.current_word
    hngmn = HANGMEN[self.logic.lives]
    word = ""
    lang=(await self.get_lang()).plugins.games
    for chr in _word: word += ("__ " if chr == "_" else f"{chr} ")
    word = lang.hangman.word.format(word=word)
    content = f"```\n{hngmn}\n\n{word}\n```"
    w_was = lang.hangman.word_was.format(word=f"'{self.logic.word}'")

    if self.won: content += f"```\n{lang.won}\n```"
    elif self.lost: content += f"```\n{lang.lost}\n{w_was}\n```"

    if self.bet:
      u=balance.get(uid=self.player)

      if self.won:
        content+=f"```\n{lang.coins.won.format(coins=self.bet)}\n```"
        await u.update(hand=(await u).hand+(self.bet*2))
      elif self.lost:
        content+=f"```\n{lang.coins.lose.format(coins=self.bet)}\n```"
        # Nothing here cuz we already took money from user

    return content
