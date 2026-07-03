import importlib
import unittest

from core.constant import Status, StoneColor


class FakeSignal:
    def __init__(self):
        self.slots = []

    def connect(self, slot):
        self.slots.append(slot)

    def emit(self, *args, **kwargs):
        for slot in self.slots:
            slot(*args, **kwargs)


class MockMenuView:
    def __init__(self):
        self.pvp_start_signal = FakeSignal()
        self.pve_start_signal = FakeSignal()


class MockMenuWidget:
    def __init__(self):
        self.size = 5
        self.bot = False
        self.bot_color = StoneColor.EMPTY

    def get_size(self):
        return self.size

    def get_bot(self):
        return self.bot, self.bot_color


class MockBoardWidget:
    def __init__(self):
        self.clicked_signal = FakeSignal()
        self.cell_getter = None
        self.dead_getter = None
        self.update_count = 0

    def set_data_accessors(self, cell_getter, dead_getter):
        self.cell_getter = cell_getter
        self.dead_getter = dead_getter

    def update(self):
        self.update_count += 1


class MockPanelWidget:
    def __init__(self):
        self.resign_signal = FakeSignal()
        self.pass_signal = FakeSignal()
        self.pause_signal = FakeSignal()
        self.done_cleaning_signal = FakeSignal()
        self.turn_updates = []

    def update_turn_display(self, player_color, status, winner_color=StoneColor.EMPTY):
        self.turn_updates.append(
            {
                "player_color": player_color,
                "status": status,
                "winner_color": winner_color,
            }
        )


class MockMainWindow:
    def __init__(self):
        self.menu_view = MockMenuView()
        self.menu_widget = MockMenuWidget()
        self.board_widget = MockBoardWidget()
        self.panel_widget = MockPanelWidget()
        self.errors = []

    def show_error(self, message):
        self.errors.append(message)


class MatchControllerTest(unittest.TestCase):
    def setUp(self):
        self.module = importlib.import_module("controller.game_manager")
        self.view = MockMainWindow()

    def test_game_manager_module_imports_without_pyqt6(self):
        self.assertTrue(hasattr(self.module, "MatchController"))

    def test_game_controller_starts_pvp_match_from_menu_signal(self):
        controller = self.module.GameController(self.view)

        self.view.menu_view.pvp_start_signal.emit()

        self.assertIsNotNone(controller.current_match)
        self.assertEqual(controller.current_match.status, Status.PLAYING)

    def test_match_controller_initializes_view_accessors_and_signals(self):
        controller = self.module.MatchController(view=self.view, game_mode="PVP", size=5)

        self.assertEqual(controller.status, Status.PLAYING)
        self.assertIsNotNone(self.view.board_widget.cell_getter)
        self.assertIsNotNone(self.view.board_widget.dead_getter)
        self.assertIn(controller.handle_click, self.view.board_widget.clicked_signal.slots)
        self.assertIn(controller.handle_resign, self.view.panel_widget.resign_signal.slots)
        self.assertIn(controller.handle_pass, self.view.panel_widget.pass_signal.slots)
        self.assertIn(controller.handle_pause, self.view.panel_widget.pause_signal.slots)
        self.assertIn(controller.end_match, self.view.panel_widget.done_cleaning_signal.slots)

    def test_handle_click_places_stone_and_updates_board(self):
        controller = self.module.MatchController(view=self.view, game_mode="PVP", size=5)
        initial_update_count = self.view.board_widget.update_count

        controller.handle_click(2, 2)

        self.assertEqual(controller.board_logic.board.get_cell_color(2, 2), StoneColor.BLACK)
        self.assertGreater(self.view.board_widget.update_count, initial_update_count)
        self.assertEqual(self.view.errors, [])

    def test_handle_click_invalid_move_shows_error(self):
        controller = self.module.MatchController(view=self.view, game_mode="PVP", size=5)

        controller.handle_click(2, 2)
        controller.handle_click(2, 2)

        self.assertEqual(self.view.errors, ["invalid move"])

    def test_handle_pass_moves_to_cleaning_after_two_passes(self):
        controller = self.module.MatchController(view=self.view, game_mode="PVP", size=5)

        controller.handle_pass()
        controller.handle_pass()

        self.assertEqual(controller.status, Status.CLEANING)
        self.assertTrue(controller.board_logic.is_game_over)

    def test_handle_resign_sets_done_and_winner(self):
        controller = self.module.MatchController(view=self.view, game_mode="PVP", size=5)

        controller.handle_resign()

        self.assertEqual(controller.status, Status.DONE)
        self.assertEqual(controller.winner, StoneColor.WHITE)

    def test_done_cleaning_signal_ends_match(self):
        controller = self.module.MatchController(view=self.view, game_mode="PVP", size=5)

        self.view.panel_widget.done_cleaning_signal.emit()

        self.assertEqual(controller.status, Status.DONE)
        self.assertIn(controller.winner, {StoneColor.BLACK, StoneColor.WHITE})


if __name__ == "__main__":
    unittest.main()
