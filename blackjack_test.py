import unittest

from blackjack import Move, Game, Hand


class GameTest(unittest.TestCase):
  NUM_CARDS_IN_DECK = 13

  def test_cards_setup(self):
    game = Game()
    self.assertEqual(len(game.CARD_2_VAL.keys()), len(game.CARDS))
    self.assertEqual(len(game.CARDS), self.NUM_CARDS_IN_DECK)

  def test_shoe_setup(self):
    game1 = Game(num_of_decks=1)
    self.assertEqual(len(game1.shoe), len(game1.CARDS))

    game2 = Game(num_of_decks=2)
    self.assertEqual(len(game2.shoe), 2 * len(game2.CARDS))

    self.assertTrue(game2.shoe.count('A'), 2)

  def test_deal_card(self):
    game1 = Game(num_of_decks=1)
    for _ in range(self.NUM_CARDS_IN_DECK):
      game1._deal_card()
    self.assertEqual(len(game1.shoe), 0)
    self.assertEqual(len(game1.discard_pile), self.NUM_CARDS_IN_DECK)

  def test_calculate_values_of_hand(self):
    game1 = Game()

    game1.player_hands = [Hand()]

    game1.player_hands[0].cards = ['2', 'J']  # 12
    game1.player_hands[0]._calculate_values_of_hand()
    self.assertEqual(game1.player_hands[0].current_highest_val, 12)

    game1.player_hands[0].cards = []  # 0
    game1.player_hands[0]._calculate_values_of_hand()
    self.assertEqual(game1.player_hands[0].current_highest_val, 0)

    game1.player_hands[0].cards = ['A', '2']  # 13
    game1.player_hands[0]._calculate_values_of_hand()
    self.assertEqual(game1.player_hands[0].current_highest_val, 13)

    game1.player_hands[0].cards = ['A', '2', 'A']  # 14
    game1.player_hands[0]._calculate_values_of_hand()
    self.assertEqual(game1.player_hands[0].current_highest_val, 14)

  def test_has_blackjack(self):
    game1 = Game()

    game1.player_hands[0].cards = ['A', 'J']  # 21
    game1.player_hands[0]._calculate_values_of_hand()
    self.assertTrue(game1.player_hands[0].has_blackjack())

    game1.player_hands[0].cards = ['A', 'T']  # 21
    game1.player_hands[0]._calculate_values_of_hand()
    self.assertTrue(game1.player_hands[0].has_blackjack())

    game1.player_hands[0].cards = ['2', 'J']  # 12
    game1.player_hands[0]._calculate_values_of_hand()
    self.assertFalse(game1.player_hands[0].has_blackjack())

    game1.player_hands[0].cards = ['2', 'J', '9']  # 21
    game1.player_hands[0]._calculate_values_of_hand()
    self.assertTrue(game1.player_hands[0].has_blackjack())

    game1.player_hands[0].cards = ['2', 'J', '9']  # 21
    game1.player_hands[0]._calculate_values_of_hand()
    self.assertTrue(game1.player_hands[0].has_blackjack())

    game1.player_hands[0].cards = []  # 0
    game1.player_hands[0]._calculate_values_of_hand()
    self.assertFalse(game1.player_hands[0].has_blackjack())

    game1.player_hands[0].cards = ['A', '2']  # 13
    game1.player_hands[0]._calculate_values_of_hand()
    self.assertFalse(game1.player_hands[0].has_blackjack())

  def test_get_allowed_moves_for_hand(self):
    game1 = Game()
    game1.player_hands[0].cards = ['A', 'J']  # 21
    self.assertEqual(game1.get_allowed_moves_for_hand(), {Move.BLACKJACK})

    game1 = Game()
    game1.player_hands[0].cards = ['A', 'T']  # 21
    self.assertEqual(game1.get_allowed_moves_for_hand(), {Move.BLACKJACK})

    game1 = Game()
    game1.player_hands[0].cards = ['2', 'J']  # 12
    self.assertEqual(game1.get_allowed_moves_for_hand(), {Move.HIT, Move.STAND, Move.DOUBLE})

    game1 = Game()
    game1.player_hands[0].cards = ['6', '6']  # 12
    self.assertEqual(game1.get_allowed_moves_for_hand(), {Move.HIT, Move.STAND, Move.SPLIT, Move.DOUBLE})

    game1 = Game()
    game1.player_hands[0].cards = ['T', '2', 'T']  # 13
    self.assertEqual(game1.get_allowed_moves_for_hand(), {Move.BUST})


if __name__ == '__main__':
  unittest.main()
