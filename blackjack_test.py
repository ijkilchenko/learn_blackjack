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
      game1.deal_card()
    self.assertEqual(len(game1.shoe), 0)
    self.assertEqual(len(game1.discard_pile), self.NUM_CARDS_IN_DECK)


if __name__ == '__main__':
  unittest.main()
