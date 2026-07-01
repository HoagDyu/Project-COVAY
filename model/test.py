import unittest

from core.constant import StoneColor
from model.board_logic import BoardLogic
from model.entities import Move


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

    def test_process_move_accepts_normal_non_capture_move(self):
        is_valid = self.logic.process_move(2, 2)

        self.assertTrue(is_valid)
        self.assertEqual(self.logic.board.get_cell_color(2, 2), StoneColor.BLACK)
        self.assertEqual(self.logic.get_current_player_color(), StoneColor.WHITE)

    def test_process_move_rejects_suicide_and_clears_stone(self):
        self.place(0, 1, self.white)
        self.place(1, 0, self.white)
        self.place(1, 2, self.white)
        self.place(2, 1, self.white)

        is_valid = self.logic.process_move(1, 1)

        self.assertFalse(is_valid)
        self.assertEqual(self.logic.board.get_cell_color(1, 1), StoneColor.EMPTY)

    def test_process_move_rejects_ko_from_rules(self):
        self.logic.move_history = [
            Move(player=self.black, x=2, y=2),
            Move(player=self.white, x=4, y=4),
        ]

        is_valid = self.logic.process_move(2, 2)

        self.assertFalse(is_valid)
        self.assertEqual(self.logic.board.get_cell_color(2, 2), StoneColor.EMPTY)

    def test_process_dead_group_removes_group(self):
        self.place(1, 1, self.white)
        self.place(1, 2, self.white)

        is_valid = self.logic.process_dead_group(1, 1)

        self.assertTrue(is_valid)
        self.assertEqual(self.logic.board.get_cell_color(1, 1), StoneColor.EMPTY)
        self.assertEqual(self.logic.board.get_cell_color(1, 2), StoneColor.EMPTY)

    def test_remove_dead_group_returns_removed_count(self):
        self.place(1, 1, self.white)
        self.place(1, 2, self.white)

        removed_count = self.logic.remove_dead_group(1, 1)

        self.assertEqual(removed_count, 2)
        self.assertEqual(self.logic.board.get_cell_color(1, 1), StoneColor.EMPTY)
        self.assertEqual(self.logic.board.get_cell_color(1, 2), StoneColor.EMPTY)

    def test_process_pass_ends_game_after_two_consecutive_passes(self):
        first_pass_ended_game = self.logic.process_pass()
        second_pass_ended_game = self.logic.process_pass()

        self.assertFalse(first_pass_ended_game)
        self.assertTrue(second_pass_ended_game)
        self.assertTrue(self.logic.game_over)
        self.assertEqual(len(self.logic.move_history), 2)


class BoardLogicTerritoryTest(unittest.TestCase):
    def setUp(self):
        self.logic = BoardLogic(size=5)
        self.black = self.logic.player_1
        self.white = self.logic.player_2

    def place(self, x, y, player):
        self.logic.board.get_cell(x, y).set_stone_color(player)

    def fill_board(self, player):
        for x in range(self.logic.board.rows):
            for y in range(self.logic.board.cols):
                self.place(x, y, player)

    def clear(self, x, y):
        self.logic.board.get_cell(x, y).clear_stone()

    def test_bfs_blank_group_returns_black_border_for_enclosed_point(self):
        self.fill_board(self.black)
        self.clear(1, 1)

        region, border_colors = self.logic.BFS_blank_group(1, 1)

        self.assertEqual(region, {(1, 1)})
        self.assertEqual(border_colors, {StoneColor.BLACK})

    def test_bfs_blank_group_returns_two_border_colors_for_neutral_region(self):
        self.fill_board(self.black)
        self.clear(1, 1)
        self.place(2, 1, self.white)

        region, border_colors = self.logic.BFS_blank_group(1, 1)

        self.assertEqual(region, {(1, 1)})
        self.assertEqual(border_colors, {StoneColor.BLACK, StoneColor.WHITE})

    def test_calculate_all_territory_counts_black_and_white_regions(self):
        self.fill_board(self.black)
        self.clear(1, 1)

        self.place(2, 3, self.white)
        self.place(3, 2, self.white)
        self.place(3, 4, self.white)
        self.place(4, 3, self.white)
        self.clear(3, 3)

        black_territory, white_territory = self.logic.calculate_all_territory()

        self.assertEqual(black_territory, 1)
        self.assertEqual(white_territory, 1)

    def test_calculate_all_territory_ignores_neutral_region(self):
        self.fill_board(self.black)
        self.clear(1, 1)
        self.place(2, 1, self.white)

        black_territory, white_territory = self.logic.calculate_all_territory()

        self.assertEqual(black_territory, 0)
        self.assertEqual(white_territory, 0)

    def test_calculate_all_territory_does_not_count_empty_board_as_white(self):
        black_territory, white_territory = self.logic.calculate_all_territory()

        self.assertEqual(black_territory, 0)
        self.assertEqual(white_territory, 0)


if __name__ == "__main__":
    unittest.main()
