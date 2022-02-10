# Logic

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
from string import ascii_lowercase
from plugins.games import SinglePlayer, Player


class Hangman(SinglePlayer):
  def __init__(self,*args):
    super().__init__(*args, timeout=30.0)
    self.logic = Hangman_Logic()
    for i in range(len(ascii_lowercase)):
      lett = ascii_lowercase[i]
      emoji = getattr(Emote.ALPHABET, lett)
      if i >= 13: return
      self.add_button_event(emoji, self.player, self.on_click, lett)

  async def start_game(self):
    elf = await self.create_elf(await self.msg.channel.send("More Buttons..."))

    for i in range(len(ascii_lowercase)):
      lett = ascii_lowercase[i]
      emoji = getattr(Emote.ALPHABET, lett)
      if i < 13: continue
      elf.add_button_event(emoji, self.player, self.on_click, lett)

    elf.add_button_event(Emote.STOP, self.player, self.on_quit)

    await elf.msg.edit(view=elf)
    await self.msg.edit(content=self.get_board())

  async def on_quit(self, inter):
    self.lose()
    await self.update(inter)

  async def on_click(self, lett, inter):
    elf = self.elf
    self.logic.guess(lett)

    if self.logic.won: self.win()
    elif self.logic.lost: self.lose()

    if inter.view is elf:
      elf.remove_item([b for b in elf.children if b.emoji == getattr(Emote.ALPHABET,lett)][0])
      if elf.children: await elf.update(inter)
      else: await elf.delete()
    else:
      self.remove_item([b for b in self.children if b.emoji == getattr(Emote.ALPHABET,lett)][0])
      await self.update(inter)

  def get_board(self):
    _word = self.logic.current_word
    hngmn = HANGMEN[self.logic.lives]
    word = ""
    for chr in _word: word += ("__ " if chr == "_" else f"{chr} ")
    content = f"```\n{hngmn}\n\nWord: {word}\n```"

    if self.won: content += "```\nYou have won the game!\n```"
    elif self.lost: content += f"```\nYou have lost the game!\nThe word was: '{self.logic.word}'\n```"

    return content
