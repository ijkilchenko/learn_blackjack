import random
from enum import Enum
from typing import List


class Move(Enum):
  BLACKJACK = 1
  BUST = 2
  HIT = 3
  STAND = 4
  DOUBLE = 5
  SPLIT = 6
  # TODO: Maybe add insurance and surrender?


class Runner:
  def __init__(self):
    self.games = []

  def play_a_game(self):
    game = Game()
    self.games.append(game)


class Game:
  CARDS = '23456789TJQKA'
  CARD_2_VAL = {'2': 2, '3': 3, '4': 4, '5': 5, '6': 6, '7': 7, '8': 8, '9': 9,
                'T': 10, 'J': 10, 'Q': 10, 'K': 10, 'A': 1}
  BLACKJACK_VAL = 21

  def __init__(self, num_of_decks=6, blackjack_pays=3 / 2):
    self.num_of_decks = num_of_decks
    self.shoe = self.CARDS * num_of_decks
    self.shoe = random.sample(self.shoe, len(self.shoe))
    self.discard_pile = []

    self.player = Player()
    self.dealer = Dealer()

    self.count = 0

    # Blackjack variations properties
    self.blackjack_pays = blackjack_pays  # Multiplier, e.g. 3:2

  def _deal_card(self) -> str:
    """Function uses the current shoe to get the next card.
    Puts the card into the discard_pile."""

    card = self.shoe.pop()
    self.discard_pile.append(card)
    return card

  def deal_hand(self):
    # Clear previous hands.
    self.player = Player()
    self.dealer = Dealer()

    self.player.cards.append(self._deal_card())  # Up
    self.dealer.cards.append(self._deal_card())  # Down
    self.player.cards.append(self._deal_card())  # Up
    self.dealer.cards.append(self._deal_card())  # Up

  def get_allowed_moves_for_hand(self) -> List[Move]:
    if self.player.has_blackjack():
      return [Move.BLACKJACK]

  def play_hand(self, move):
    pass


class Player:
  """Gives information about the Player's hand."""

  def __init__(self, cards=[]):
    self.cards = cards

  def find_highest_val_before_bust(self):
    val = sum([Game.CARD_2_VAL[card] for card in self.cards])
    num_aces = self.cards.count('A')
    for _ in range(num_aces):
      if val + 10 <= Game.BLACKJACK_VAL:
        val = val + 10  # Count this ace as 11
      else:
        break
    return val

  def has_blackjack(self):
    val = self.find_highest_val_before_bust()
    if val == Game.BLACKJACK_VAL:
      return True
    else:
      return False


class Dealer:
  """Gives information about the Dealer's hand."""

  def __init__(self, cards=[]):
    # Down card, up card, followed by other cards
    self.cards = cards


if __name__ == '__main__':
  print('Welcome to blackjack!')
