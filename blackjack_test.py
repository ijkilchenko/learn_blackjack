import unittest

from blackjack import Game


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

  def test_find_highest_val_before_bust(self):
    game1 = Game()

    game1.player.cards = ['2', 'J']  # 12
    self.assertEqual(game1.player.find_highest_val_before_bust(), 12)

    game1.player.cards = []  # 0
    self.assertEqual(game1.player.find_highest_val_before_bust(), 0)

    game1.player.cards = ['A', '2']  # 13
    self.assertEqual(game1.player.find_highest_val_before_bust(), 13)

    game1.player.cards = ['A', '2', 'A']  # 14
    self.assertEqual(game1.player.find_highest_val_before_bust(), 14)

  def test_has_blackjack(self):
    game1 = Game()

    game1.player.cards = ['A', 'J']  # 21
    self.assertTrue(game1.player.has_blackjack())

    game1.player.cards = ['A', 'T']  # 21
    self.assertTrue(game1.player.has_blackjack())

    game1.player.cards = ['2', 'J']  # 12
    self.assertFalse(game1.player.has_blackjack())

    game1.player.cards = ['2', 'J', '9']  # 21
    self.assertTrue(game1.player.has_blackjack())

    game1.player.cards = ['2', 'J', '9']  # 21
    self.assertTrue(game1.player.has_blackjack())

    game1.player.cards = []  # 0
    self.assertFalse(game1.player.has_blackjack())

    game1.player.cards = ['A', '2']  # 13
    self.assertFalse(game1.player.has_blackjack())


if __name__ == '__main__':
  unittest.main()
