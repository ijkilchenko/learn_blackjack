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

  CARD_2_COUNT_HILOW = {'2': 1, '3': 1, '4': 1, '5': 1, '6': 1, '7': 0, '8': 0, '9': 0,
                        'T': -1, 'J': -1, 'Q': -1, 'K': -1, 'A': -1}

  def __init__(self, num_of_decks=6, blackjack_pays=3 / 2, player_money=1000):
    self.num_of_decks = num_of_decks
    self.shoe = self.CARDS * num_of_decks
    self.shoe = random.sample(self.shoe, len(self.shoe))
    self.discard_pile = []

    self.player_money = player_money
    self._reset_hands()

    self.running_count = 0
    self.true_count = 0

    self.num_of_hands = 0

    # Blackjack variations properties
    self.blackjack_pays = blackjack_pays  # Multiplier, e.g. 3:2

  def _reset_hands(self, bet=0):
    self.bet = bet

    self.player_hands = [Hand(bet=self.bet)]
    self.dealer_hand = Hand()

    self.is_split = False  # Every hand is allowed to be split once.
    # A hand is allowed to be split once more if it did not come from a pair of aces.
    self.is_split_twice = False

  def _deal_card(self) -> str:
    """Function uses the current shoe to get the next card.
    Puts the card into the discard_pile."""

    assert len(self.shoe) > 0, "Tried to deal from an empty shoe!"

    card = self.shoe.pop()
    self.discard_pile.append(card)
    self.running_count += Game.CARD_2_COUNT_HILOW[card]
    # True count is the running count divided by the number of decks remaining.
    # We round the number of decks remaining to the nearest quarter deck.
    self.true_count = self.running_count / round((len(self.shoe) + 1) * 4) / 4 / Game.NUM_CARDS_IN_DECK

    return card

  def deal_hand(self, bet=50):
    self.num_of_hands += 1

    self._reset_hands(bet=bet)

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
    if self.player_hands[0].cards[0] == self.player_hands[0].cards[1] and len(self.player_hands[0].cards) == 2:
      if not self.is_split_twice:  # Not already split twice.
        moves.add(Move.SPLIT)
      # Split once and not from aces.
      elif self.is_split and not self.player_hands[0].cards[0] == 'A':
        moves.add(Move.SPLIT)
    if len(self.player_hands[0].cards) == 2:
      # Only allowed to double down in the beginning.
      moves.add(Move.DOUBLE)

    return moves

  def print_hands(self):
    print('Player hand(s): %s' % list(hand.cards for hand in self.player_hands))
    print('Dealer hand: %s' % ', '.join(self.dealer_hand.cards))

  def play_hand(self, move=None) -> None:
    return _play_hand(self, move)

  def _play_hand(self, move=None) -> None:
    moves = self.get_allowed_moves_for_hand()
    print(moves)
    if moves == {Move.BLACKJACK}:
      self.player_money += self.bet * self.blackjack_pays
      self.print_hands()
      print('Blackjack!\n')
      self.player_hands.pop(0)
      return
    elif moves == {Move.BUST}:
      self.player_money -= self.bet
      self.print_hands()
      print('Bust!\n')
      self.player_hands.pop(0)
      return

    # Select move randomly if not provided
    if not move:
      move = random.sample(moves, 1)[0]
    print(move)
    if move == Move.STAND:
      # Dealer is revealed to the split hands
      # but this does not matter since the dealer's cards are not used in the strategy.
      self.dealer_hand.finish_as_dealer(self)
      self.print_hands()
      if self.player_hands[0].current_highest_val == self.dealer_hand.current_highest_val:
        print('Push!\n')
      elif self.player_hands[0].current_highest_val > self.dealer_hand.current_highest_val or \
          self.dealer_hand.current_lowest_val > Game.BLACKJACK_VAL:
        print('Win!\n')
        self.player_money += self.bet
      else:
        print('Lose!\n')
        self.player_money -= self.bet
      self.player_hands.pop(0)
      return
    elif move == Move.HIT or move == Move.DOUBLE:
      self.print_hands()
      if move == Move.DOUBLE:
        self.bet *= 2
        print('Double!\n')
      print('Hit!\n')
      self.player_hands[0].cards.append(self._deal_card())
      return self._play_hand()
    elif move == Move.SPLIT:
      self.print_hands()

      if not self.is_split:
        self.is_split = True
      else:
        self.is_split_twice = True

      self.player_hands.append(Hand())
      # Move second card in the first hand to the first card in the last hand.
      self.player_hands[-1].cards.append(self.player_hands[0].cards.pop())

      # Deal two new cards.
      self.player_hands[0].cards.append(self._deal_card())
      self.player_hands[-1].cards.append(self._deal_card())

      print('Split!\n')

      self._play_hand()  # Play first hand
      self._play_hand()  # Play second hand
      return


class Hand:
  """Gives information about someone's hand."""

  def __init__(self, bet=0):
    self.cards = []
    self.bet = bet
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
    self._calculate_values_of_hand()

    val = self.current_highest_val
    if val == Game.BLACKJACK_VAL:
      return True
    else:
      return False

  def finish_as_dealer(self, game):
    self._calculate_values_of_hand()
    while self.current_highest_val <= 16:
      self.cards.append(game._deal_card())  # Dealer self hits
      self._calculate_values_of_hand()
    if self.current_highest_val == 17 and 'A' in self.cards:
      self.cards.append(game._deal_card())  # Dealer self hits on soft 17
      self._calculate_values_of_hand()


if __name__ == '__main__':
  print('Welcome to blackjack!')
