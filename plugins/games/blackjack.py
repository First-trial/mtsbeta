import random


# Basic Logic

suits = ('Hearts', 'Diamonds', 'Spades', 'Clubs')

ranks = ('Two', 'Three', 'Four', 'Five', 'Six', 'Seven', 'Eight', 'Nine',
         'Ten', 'Jack', 'Queen', 'King', 'Ace')

values = {
    'Two': 2,
    'Three': 3,
    'Four': 4,
    'Five': 5,
    'Six': 6,
    'Seven': 7,
    'Eight': 8,
    'Nine': 9,
    'Ten': 10,
    'Jack': 10,
    'Queen': 10,
    'King': 10,
    'Ace': 11
}

suits_ = {
  'Hearts': "♥",
  "Spades": "♠",
  "Clubs": "♣",
  "Diamonds": "♦"
}

values_ = {
    'Two': 2,
    'Three': 3,
    'Four': 4,
    'Five': 5,
    'Six': 6,
    'Seven': 7,
    'Eight': 8,
    'Nine': 9,
    'Ten': 10,
    'Jack': "J",
    'Queen': "Q",
    'King': "K",
    'Ace': "A"
}


class Card:
  def __init__(self, suit, rank):
    self.suit = suit
    self.rank = rank

  def __str__(self):
    return suits_[self.suit] + " " + str(values_[self.rank])


class Deck():
  def __init__(self):
    self.deck = []
    for suit in suits:
      for rank in ranks:
        self.deck.append(Card(suit, rank))

  def __str__(self):
    composition = ''  # set the deck comp as an empty string
    for card in self.deck:
      composition += '\n' + str(card)
    return "The deck has: " + composition

  def shuffle(self):
    random.shuffle(self.deck)

  def deal(self):
    card = self.deck.pop()
    return card

class Hand:
  def __init__(self):
    self.cards = []  # start with 0 cards in hand

  def add_card(self, card):
    self.cards.append(card)

  def get_value(self):
    a = b = 0
    for card in self.cards:
      if card.rank == 'Ace':
        a += 1
        b += 11
      else:
        a += values[card.rank]
        b += values[card.rank]

    if b > 21:
      b = a

    return a, b

class Blackjack_Logic:
  def __init__(self):
    self.player_turn = True
    self.deck = Deck()
    self.deck.shuffle()

    self.player_hands = [Hand()]
    self.player_hands[0].add_card(self.deck.deal())
    self.player_hands[0].add_card(self.deck.deal())

    self.dealer_hand = Hand()
    self.dealer_hand.add_card(self.deck.deal())
    self.dealer_hand.add_card(self.deck.deal())

  def can_split(self):
    return self.player_hands[0].cards[0].rank == self.player_hands[0].cards[1].rank

  def split_hand(self):
    self.player_hands.append(Hand())
    card = self.player_hands[0].cards[0]
    self.player_hands[1].cards.append(card)
    self.player_hands[0].cards.remove(card)

  def hit(self, hand=0):
    self.player_hands[hand].add_card(self.deck.deal())

  def stand(self):
    self.dealer_turn()

  def is_player_busted(self):
    busted = True
    for hand in self.player_hands:
      if hand.get_value()[0] <= 21 or hand.get_value()[1] <= 21:
        busted = False

    return busted

  def is_dealer_busted(self):
    return self.dealer_hand.get_value()[0] > 21 and self.dealer_hand.get_value()[1] > 21


  def dealer_turn(self):
    self.player_turn = False
    while self.dealer_hand.get_value()[0] < 17 or self.dealer_hand.get_value()[1] < 17:
      self.dealer_hand.add_card(self.deck.deal())


  def get_game_result(self):
    if self.is_player_busted() and self.is_dealer_busted(): return "DRAW"
    elif self.is_player_busted(): return "LOSE"
    elif self.is_dealer_busted(): return "WIN"

    max_hand_value = 0
    for hand in self.player_hands:
      if max_hand_value < max(hand.get_value()) <= 21: max_hand_value = max(hand.get_value())

    if max(self.dealer_hand.get_value()) < max_hand_value: return "WIN"

    if max(self.dealer_hand.get_value()) == max_hand_value: return "DRAW"

    return "LOSE"

  def has_ended_in_draw(self):
    result = self.get_game_result()
    return result == "DRAW"

  def has_player_won(self):
    result = self.get_game_result()
    return result == "WIN"


from plugins.games import AiPlayer


class Blackjack(AiPlayer):
  def __init__(self,*args):
    super().__init__(*args, timeout=30.0)
    self.blackjack = Blackjack()
    self.players[-1].name = "dealer"
    # self.add_button_event

# Soon™
