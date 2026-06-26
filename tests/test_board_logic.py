import unittest

from core.constant import StoneColor
from model.board_logic import BoardLogic


class BoardLogicBFSTest(unittest.TestCase):
    def setUp(self):
        self.logic = BoardLogic(size=5)
        self.black = self.logic.player_1
        self.white = self.logic.player_2

    def place(self, x, y, player):
        self.logic.board.get_cell(x, y).set_stone_color(player)

    def test_board_links_corner_edge_and_center_neighbors(self):
        self.assertEqual(len(self.logic.board.get_cell(0, 0).neighbors), 2)
        self.assertEqual(len(self.logic.board.get_cell(0, 2).neighbors), 3)
        self.assertEqual(len(self.logic.board.get_cell(2, 2).neighbors), 4)

    def test_bfs_returns_single_stone_group_and_liberties(self):
        self.place(2, 2, self.black)

        result = self.logic.BFS(2, 2)

        self.assertEqual([(cell.x, cell.y) for cell in result.group], [(2, 2)])
        self.assertEqual(result.liberties, 4)

    def test_bfs_returns_connected_group_with_unique_liberties(self):
        self.place(1, 1, self.black)
        self.place(1, 2, self.black)

        result = self.logic.BFS(1, 1)
        positions = {(cell.x, cell.y) for cell in result.group}

        self.assertEqual(positions, {(1, 1), (1, 2)})
        self.assertEqual(result.liberties, 6)

    def test_bfs_does_not_cross_opponent_stones(self):
        self.place(1, 1, self.black)
        self.place(1, 2, self.black)
        self.place(2, 1, self.white)

        result = self.logic.BFS(1, 1)
        positions = {(cell.x, cell.y) for cell in result.group}

        self.assertEqual(positions, {(1, 1), (1, 2)})
        self.assertNotIn((2, 1), positions)

    def test_get_group_uses_bfs(self):
        self.place(3, 3, self.white)
        self.place(3, 4, self.white)

        group = self.logic.get_group(3, 3)

        self.assertEqual({(cell.x, cell.y) for cell in group}, {(3, 3), (3, 4)})

    def test_get_liberties_returns_zero_for_surrounded_group(self):
        self.place(1, 1, self.black)
        self.place(0, 1, self.white)
        self.place(2, 1, self.white)
        self.place(1, 0, self.white)
        self.place(1, 2, self.white)

        self.assertEqual(self.logic.get_liberties(1, 1), 0)

    def test_process_move_captures_group_with_no_liberties(self):
        self.place(1, 1, self.white)
        self.place(0, 1, self.black)
        self.place(1, 0, self.black)
        self.place(1, 2, self.black)

        is_valid = self.logic.process_move(2, 1)

        self.assertTrue(is_valid)
        self.assertEqual(self.logic.board.get_cell_color(1, 1), StoneColor.EMPTY)


if __name__ == "__main__":
    unittest.main()
