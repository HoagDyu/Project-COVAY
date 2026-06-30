from __future__ import annotations

from model.board_logic import BoardLogic

from .bot_algorithm import choose_best_move


class BotAI:
    """Basic Bot AI."""

    def select_move(
        self,
        board_logic: BoardLogic,
    ) -> tuple[int, int] | None:
        """
        Return the coordinate (x, y) chosen by the bot.

        Parameters
        ----------
        board_logic : BoardLogic
            Current game state.

        Returns
        -------
        tuple[int, int] | None
            Selected move or None if no move exists.
        """
        return choose_best_move(board_logic)