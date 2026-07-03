from __future__ import annotations

import random
from typing import TYPE_CHECKING

from core.constant import StoneColor
from model.entities import Move

if TYPE_CHECKING:
    from ai.class_bot import BotAI
    from model.board_logic import BoardLogic
    from model.entities import Cell

def choose_best_move(board_logic: BoardLogic, bot: BotAI | None = None) -> tuple[int, int] | None:
    """
    Choose the best move for the current player based on heuristic evaluation.
    """
    if bot is None:
        bot = board_logic.current_player

    valid_moves = find_valid_moves(board_logic, bot)

    if not valid_moves:
        return None

    best_score = float("-inf")
    best_moves: list[tuple[int, int]] = []

    color = bot.color

    for cell in valid_moves:
        score = evaluate_move(cell, color, board_logic)

        if score > best_score:
            best_score = score
            best_moves = [(cell.x, cell.y)]
        elif score == best_score:
            best_moves.append((cell.x, cell.y))

    # Nếu có nhiều nước đi cùng số điểm cao nhất, chọn ngẫu nhiên một nước để Bot không bị rập khuôn
    return random.choice(best_moves)


def find_valid_moves(board_logic: BoardLogic, bot: BotAI | None = None) -> list[Cell]:
    """
    Return every empty and valid cell.
    """
    rule = board_logic.rules
    if bot is None:
        bot = board_logic.current_player

    moves: list[Cell] = []

    for row in board_logic.board.board:
        for cell in row:
            x, y = cell.x, cell.y
            if rule.is_empty_cell(x=x, y=y) and rule.is_valid_move(x=x, y=y):
                # Lưu ý: Nếu sau này tối ưu, hãy chuyển is_suicide và is_ko nhận thẳng (x, y) thay vì object Move
                move = Move(x=x, y=y, player=bot)
                if not rule.is_suicide(x=x, y=y, move=move, board=board_logic) and not rule.is_ko(move=move, board=board_logic):
                    moves.append(cell)
    return moves


def evaluate_move(
    cell: Cell,
    color: StoneColor,
    board_logic: BoardLogic,
) -> int:
    """
    Evaluate a candidate move using Go heuristics.
    """
    score = 0

    # 1. Đánh giá vị trí địa lý (Góc, Biên, Trung tâm)
    score += position_score(cell, board_logic.board.rows)

    # 2. Đánh giá sự liên kết cơ bản
    score += friendly_neighbors(cell, color) * 2
    score += enemy_neighbors(cell, color) * 1

    # 3. Đánh giá chiến thuật (Bắt quân, Cứu quân)
    score += tactical_score(cell, color, board_logic)

    return score


def position_score(cell: Cell, board_size: int) -> int:
    """
    Prefer moves on the 3rd and 4th lines (Corners and Sides).
    """
    # Tính khoảng cách từ ô hiện tại đến mép gần nhất (0-indexed)
    dist_x = min(cell.x, board_size - 1 - cell.x)
    dist_y = min(cell.y, board_size - 1 - cell.y)

    # Đường 3 và 4 (index 2 và 3) là những vị trí vàng trong Cờ vây
    if 2 <= dist_x <= 3 and 2 <= dist_y <= 3:
        return 20  # Ưu tiên cao nhất cho Góc và Biên mở rộng
    elif dist_x == 0 or dist_y == 0:
        return 0   # Đường 1 (Sát mép): Rất tệ ở giai đoạn đầu
    elif dist_x == 1 or dist_y == 1:
        return 5   # Đường 2: Trung bình yếu
    else:
        return 10  # Trung tâm: Bình thường (không ưu tiên bằng đường 3-4)


def tactical_score(cell: Cell, color: StoneColor, board_logic: BoardLogic) -> int:
    """
    Evaluate immediate tactical advantages: Capturing enemy stones or saving own stones.
    (Requires board_logic to have a get_group_and_liberties method)
    """
    score = 0
    opponent = StoneColor.WHITE if color == StoneColor.BLACK else StoneColor.BLACK

    # Quét 4 hướng xung quanh ô dự định đặt cờ
    for neighbor in cell.neighbors:
        n_color = neighbor.get_cell_color()
        Cell_group = board_logic.BFS(neighbor.x, neighbor.y)
        if n_color == opponent:
            # Nếu chạm vào quân địch, kiểm tra xem đám quân địch đó còn mấy khí
            _, liberties = Cell_group.group, Cell_group.liberties
            # Nếu địch chỉ còn đúng 1 khí, và khí đó chính là ô này -> Đặt xuống là Ăn quân!
            if len(liberties) == 1 and (cell.x, cell.y) in liberties:
                score += 1000  # Mức điểm tuyệt đối để Bot chớp ngay cơ hội

        elif n_color == color:
            # Nếu chạm vào đồng đội, kiểm tra xem đồng đội có đang hấp hối không
            group, liberties = Cell_group.group, Cell_group.liberties
            # Nếu đồng đội chỉ còn 1 khí, đặt vào đây có thể nối quân và tăng khí
            if len(liberties) == 1 and (cell.x, cell.y) in liberties:
                score += 500   # Ưu tiên cao thứ hai để cứu quân nhà

    return score


def friendly_neighbors(cell: Cell, color: StoneColor) -> int:
    """Count adjacent friendly stones."""
    return sum(1 for neighbor in cell.neighbors if neighbor.get_cell_color() == color)


def enemy_neighbors(cell: Cell, color: StoneColor) -> int:
    """Count adjacent enemy stones."""
    opponent = StoneColor.WHITE if color == StoneColor.BLACK else StoneColor.BLACK
    return sum(1 for neighbor in cell.neighbors if neighbor.get_cell_color() == opponent)