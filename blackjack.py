import random


class Runner:
  def __init__(self):
    self.games = []

  def play_a_game(self):
    game = Game()
    self.games.append(game)


class Game:
  CARDS = '23456789TJQKA'
  CARD_2_VAL = {'2': 2, '3': 3, '4': 4, '5': 5, '6': 6, '7': 7, '8': 8, '9': 9,
                'T': 10, 'J': 10, 'Q': 10, 'K': 10, 'A': 11}

  def __init__(self, num_of_decks=6):
    self.num_of_decks = num_of_decks
    self.shoe = self.CARDS * num_of_decks
    self.shoe = random.sample(self.shoe, len(self.shoe))
    self.discard_pile = []

    self.player = Player()
    self.dealer = Dealer()

    self.count = 0

    # Blackjack variations properties
    self.blackjack_pays = 3 / 2  # Multiplier, 3 to 2

  def deal_card(self) -> str:
    """Function uses the current shoe to get the next card.
    Puts the card into the discard_pile."""

    card = self.shoe.pop()
    self.discard_pile.append(card)
    return card

  def deal(self):
    # Clear previous hands.
    self.player = Player()
    self.dealer = Dealer()

    self.player.cards.append(self.deal_card())  # Up
    self.dealer.cards.append(self.deal_card())  # Down
    self.player.cards.append(self.deal_card())  # Up
    self.dealer.cards.append(self.deal_card())  # Up


class Player:
  """Gives information about the Player's hand."""

  def __init__(self, cards=[]):
    self.cards = cards


class Dealer:
  """Gives information about the Dealer's hand."""

  def __init__(self, cards=[]):
    # Down card, up card, followed by other cards
    self.cards = cards


if __name__ == '__main__':
  print('Welcome to blackjack!')
