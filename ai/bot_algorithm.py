from __future__ import annotations

import random
from typing import TYPE_CHECKING

from core.constant import StoneColor

if TYPE_CHECKING:
    from model.board_logic import BoardLogic
    from model.entities import Cell


def choose_best_move(
    board_logic: BoardLogic,
) -> tuple[int, int] | None:
    """
    Choose the best move for the current player.
    """

    valid_moves = find_valid_moves(board_logic)

    if not valid_moves:
        return None

    best_score = float("-inf")
    best_moves: list[tuple[int, int]] = []

    color = board_logic.current_player.color

    for cell in valid_moves:
        score = evaluate_move(cell, color, board_logic)

        if score > best_score:
            best_score = score
            best_moves = [(cell.x, cell.y)]

        elif score == best_score:
            best_moves.append((cell.x, cell.y))

    return random.choice(best_moves)


def find_valid_moves(
    board_logic: BoardLogic,
) -> list[Cell]:
    """
    Return every empty cell.
    """

    moves: list[Cell] = []

    for row in board_logic.board.board:
        for cell in row:
            if cell.is_blank:
                moves.append(cell)

    return moves


def evaluate_move(
    cell: Cell,
    color: StoneColor,
    board_logic: BoardLogic,
) -> int:
    """
    Evaluate a candidate move.
    """

    score = 0

    score += center_score(cell, board_logic)

    score += friendly_neighbors(cell, color) * 3

    score += enemy_neighbors(cell, color) * 2

    return score


def center_score(
    cell: Cell,
    board_logic: BoardLogic,
) -> int:
    """
    Prefer moves near the center.
    """

    center_x = board_logic.board.rows // 2
    center_y = board_logic.board.cols // 2

    distance = abs(cell.x - center_x) + abs(cell.y - center_y)

    return max(0, 10 - distance)


def friendly_neighbors(
    cell: Cell,
    color: StoneColor,
) -> int:
    """
    Count adjacent friendly stones.
    """

    return sum(
        1
        for neighbor in cell.neighbors
        if neighbor.get_cell_color() == color
    )


def enemy_neighbors(
    cell: Cell,
    color: StoneColor,
) -> int:
    """
    Count adjacent enemy stones.
    """

    opponent = (
        StoneColor.WHITE
        if color == StoneColor.BLACK
        else StoneColor.BLACK
    )

    return sum(
        1
        for neighbor in cell.neighbors
        if neighbor.get_cell_color() == opponent
    )
