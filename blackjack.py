import random
from enum import Enum
from typing import Set


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
  NUM_CARDS_IN_DECK = 13
  CARD_2_VAL = {'2': 2, '3': 3, '4': 4, '5': 5, '6': 6, '7': 7, '8': 8, '9': 9,
                'T': 10, 'J': 10, 'Q': 10, 'K': 10, 'A': 1}
  BLACKJACK_VAL = 21

  CARD_2_COUNT_SIMPLE = {'2': 1, '3': 1, '4': 1, '5': 1, '6': 1, '7': 0, '8': 0, '9': 0,
                         'T': -1, 'J': -1, 'Q': -1, 'K': -1, 'A': -1}

  def __init__(self, num_of_decks=6, blackjack_pays=3 / 2, player_money=1000):
    self.num_of_decks = num_of_decks
    self.shoe = self.CARDS * num_of_decks
    self.shoe = random.sample(self.shoe, len(self.shoe))
    self.discard_pile = []

    self.player_money = player_money

    self.player_hands = [Hand()]
    self.dealer_hand = Hand()
    self.bet = 0
    # You can only receive one more card after doubling down
    self.is_doubled_down = False
    self.is_split = False

    self.running_count = 0
    self.true_count = 0

    # Blackjack variations properties
    self.blackjack_pays = blackjack_pays  # Multiplier, e.g. 3:2

  def _deal_card(self) -> str:
    """Function uses the current shoe to get the next card.
    Puts the card into the discard_pile."""

    card = self.shoe.pop()
    self.discard_pile.append(card)
    self.running_count += Game.CARD_2_COUNT_SIMPLE[card]
    # True count is the running count divided by the number of decks remaining
    # TODO: Maybe round the number of decks remaining
    self.true_count = self.running_count / (len(self.shoe) / Game.NUM_CARDS_IN_DECK)

    return card

  def deal_hand(self, bet=50):
    # Clear previous hands.
    self.player_hands = [Hand()]
    self.dealer_hand = Hand()
    self.bet = bet

    self.is_doubled_down = False
    self.is_split = False

    self.player_hands[0].cards.append(self._deal_card())  # Up
    self.dealer_hand.cards.append(self._deal_card())  # Down
    self.player_hands[0].cards.append(self._deal_card())  # Up
    self.dealer_hand.cards.append(self._deal_card())  # Up

  def get_allowed_moves_for_hand(self) -> Set[Move]:
    if self.player_hands[0].has_blackjack():
      return {Move.BLACKJACK}
    elif self.player_hands[0].current_highest_val > Game.BLACKJACK_VAL:
      return {Move.BUST}

    moves = {Move.HIT, Move.STAND}
    if self.player_hands[0].cards[0] == self.player_hands[0].cards[1]:
      moves.add(Move.SPLIT)
    if len(self.player_hands[0].cards) == 2:
      moves.add(Move.DOUBLE)

    return moves

  def print_hands(self):
    print('Player hand: %s' % ', '.join(self.player_hands[0].cards))
    print('Dealer hand: %s' % ', '.join(self.dealer_hand.cards))

  def play_hand_randomly(self):
    moves = self.get_allowed_moves_for_hand()
    if moves == {Move.BLACKJACK}:
      self.player_money += self.bet * self.blackjack_pays
    elif moves == {Move.BUST}:
      self.player_money -= self.bet

    # Select move randomly
    move = random.sample(moves, 1)
    if move == Move.STAND:
      self.dealer_hand.finish_as_dealer()
      if self.player_hands[0].current_highest_val == self.dealer_hand.current_highest_val:
        self.print_hands()
        print('Push!\n')
      


class Hand:
  """Gives information about someone's hand."""

  def __init__(self, cards=[]):
    self.cards = cards
    self.current_highest_val = None
    self.current_lowest_val = None

  def _calculate_values_of_hand(self):
    val = sum([Game.CARD_2_VAL[card] for card in self.cards])
    self.current_lowest_val = val
    num_aces = self.cards.count('A')
    for _ in range(num_aces):
      if val + 10 <= Game.BLACKJACK_VAL:
        val = val + 10  # Count this ace as 11
      else:
        break
    self.current_highest_val = val

  def has_blackjack(self):
    if not self.current_lowest_val or not self.current_highest_val:
      self._calculate_values_of_hand()
    val = self.current_highest_val
    if val == Game.BLACKJACK_VAL:
      return True
    else:
      return False

  def finish_as_dealer(self):
    pass


if __name__ == '__main__':
  print('Welcome to blackjack!')
