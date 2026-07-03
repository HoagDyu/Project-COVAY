import unittest

from ai.bot_algorithm import choose_best_move, find_valid_moves
from ai.class_bot import BotAI
from core.constant import StoneColor
from model.board_logic import BoardLogic


class BotAlgorithmTest(unittest.TestCase):
    def setUp(self):
        self.board_logic = BoardLogic(size=3)

    def fill_board(self):
        player = self.board_logic.player_1
        for row in self.board_logic.board.board:
            for cell in row:
                cell.set_stone_color(player)

    def test_find_valid_moves_returns_all_empty_cells(self):
        moves = find_valid_moves(self.board_logic)

        self.assertEqual(len(moves), 9)

    def test_choose_best_move_returns_coordinate_when_move_exists(self):
        move = choose_best_move(self.board_logic)

        self.assertIsNotNone(move)
        self.assertIsInstance(move, tuple)
        self.assertEqual(len(move), 2)
        x, y = move
        self.assertTrue(0 <= x < 3)
        self.assertTrue(0 <= y < 3)

    def test_choose_best_move_returns_none_when_board_is_full(self):
        self.fill_board()

        move = choose_best_move(self.board_logic)

        self.assertIsNone(move)

    def test_bot_ai_select_move_returns_coordinate_when_move_exists(self):
        bot = BotAI(color=StoneColor.WHITE)

        move = bot.select_move(self.board_logic)

        self.assertIsNotNone(move)
        self.assertIsInstance(move, tuple)

    def test_bot_ai_select_move_returns_none_when_board_is_full(self):
        bot = BotAI(color=StoneColor.WHITE)
        self.fill_board()

        move = bot.select_move(self.board_logic)

        self.assertIsNone(move)


if __name__ == "__main__":
    unittest.main()
