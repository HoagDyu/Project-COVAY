from __future__ import annotations

from collections import deque

from core.constant import StoneColor
from .entities import Cell, CellGroup, Move, Player
from .rules import Rules


class Board:
    def __init__(self, rows: int = 19, cols: int = 19):
        self.rows = rows
        self.cols = cols
        self.board: list[list[Cell]] = [
            [Cell(x=x, y=y) for y in range(cols)]
            for x in range(rows)
        ]
        self._link_neighbors()

    def _link_neighbors(self) -> None:
        for x in range(self.rows):
            for y in range(self.cols):
                self.board[x][y].neighbors = [
                    self.board[nx][ny]
                    for nx, ny in self.iter_neighbor_positions(x, y)
                ]

    def iter_neighbor_positions(self, x: int, y: int):
        for nx, ny in ((x - 1, y), (x + 1, y), (x, y - 1), (x, y + 1)):
            if 0 <= nx < self.rows and 0 <= ny < self.cols:
                yield nx, ny

    def get_cell(self, x: int, y: int) -> Cell:
        if 0 <= x < self.rows and 0 <= y < self.cols:
            return self.board[x][y]
        raise ValueError("Cell position is outside the board")

    def get_cell_color(self, x: int, y: int) -> StoneColor:
        return self.get_cell(x=x, y=y).get_cell_color()

    def is_dead_cell(self, x: int, y: int) -> bool:
        return self.get_cell(x=x, y=y).is_dead_mark

    def group_liberties(self, group: list[Cell]) -> int:
        liberties: set[tuple[int, int]] = set()
        for cell in group:
            for neighbor in cell.neighbors:
                if neighbor.is_blank:
                    liberties.add((neighbor.x, neighbor.y))
        return len(liberties)


class BoardLogic:
    def __init__(self, size: int = 19):
        self.board = Board(size, size)
        self.player_1: Player = Player(color=StoneColor.BLACK)
        self.player_2: Player = Player(color=StoneColor.WHITE)
        self.current_player: Player = self.player_1
        self.next_player: Player = self.player_2
        self.move_history: list[Move] = []
        self.game_over: bool = False
        self.rules = Rules(self.board)

    def switch_turn(self) -> None:
        self.current_player, self.next_player = self.next_player, self.current_player

    def _place_stone(self, move: Move) -> bool:
        if move.x is None or move.y is None:
            return False
        self.board.get_cell(move.x, move.y).set_stone_color(move.player)
        return True

    def _get_captured_groups(self, x: int, y: int) -> list[list[Cell]]:
        placed_cell = self.board.get_cell(x, y)
        if placed_cell.is_blank:
            return []

        opponent_color = self.next_player.color
        captured_groups: list[list[Cell]] = []
        checked_positions: set[tuple[int, int]] = set()

        for neighbor in placed_cell.neighbors:
            if neighbor.color != opponent_color:
                continue

            if (neighbor.x, neighbor.y) in checked_positions:
                continue

            cell_group = self.BFS(x=neighbor.x, y=neighbor.y)
            for cell in cell_group.group:
                checked_positions.add((cell.x, cell.y))

            if cell_group.liberties == 0:
                captured_groups.append(cell_group.group)

        return captured_groups

    def process_move(self, x: int, y: int) -> bool:
        if not self.rules.is_valid_move(x, y):
            return False
        if not self.rules.is_empty_cell(x, y):
            return False

        move = Move(player=self.current_player, x=x, y=y)
        if self.rules.is_ko(move, self):
            return False

        self._place_stone(move)

        captured_groups = self._get_captured_groups(x, y)
        prisoner_count = 0
        for group in captured_groups:
            prisoner_count += self._remove_group(group)

        if prisoner_count == 0 and self.get_liberties(x, y) == 0:
            self.board.get_cell(x, y).clear_stone()
            return False

        self.current_player.prisoner += prisoner_count
        self.move_history.append(move)
        self.switch_turn()
        return True

    def process_pass(self) -> bool:
        self.pass_turn()
        if len(self.move_history) >= 2 and self.move_history[-1].is_pass and self.move_history[-2].is_pass:
            self.game_over = True
        return self.game_over

    def pass_turn(self) -> None:
        self.move_history.append(Move(player=self.current_player, x=None, y=None, is_pass=True))
        self.switch_turn()

    def resign(self) -> bool:
        pass

    def BFS(self, x: int, y: int) -> CellGroup:
        start = self.board.get_cell(x, y)
        if start.is_blank:
            return CellGroup(group=[], liberties=0)

        color = start.get_cell_color()
        group: list[Cell] = []
        liberties: set[tuple[int, int]] = set()
        visited: set[tuple[int, int]] = {(x, y)}
        queue = deque([start])

        while queue:
            cell = queue.popleft()
            group.append(cell)

            for neighbor in cell.neighbors:
                key = (neighbor.x, neighbor.y)
                if neighbor.is_blank:
                    liberties.add(key)
                elif neighbor.get_cell_color() == color and key not in visited:
                    visited.add(key)
                    queue.append(neighbor)

        return CellGroup(group=group, liberties=len(liberties))

    def get_liberties(self, x: int, y: int) -> int:
        return self.BFS(x, y).liberties

    def get_group(self, x: int, y: int) -> list[Cell]:
        return self.BFS(x, y).group

    def process_dead_group(self, x: int, y: int) -> bool:
        try:
            dead_group = self.get_group(x=x, y=y)
            if not dead_group:
                return False

            player_color = dead_group[0].color
            prisoner_count = self._remove_group(dead_group)

            if player_color == self.player_1.color:
                self.player_2.prisoner += prisoner_count
            else:
                self.player_1.prisoner += prisoner_count
            return True
        except ValueError:
            return False
    

    def _remove_group(self, dead_group: list[Cell]) -> int:
        prisoner = 0
        for cell in dead_group:
            cell.clear_stone()
            prisoner += 1
        return prisoner

    def remove_dead_group(self, x: int, y: int) -> int:
        return self._remove_group(self.get_group(x, y))

    def calculate_all_territory(self) -> list[float]:
        pass

    def process_end_match(self) -> None:
        pass

    def get_current_player_color(self) -> StoneColor:
        return self.current_player.color

    def get_current_player(self) -> Player:
        return self.current_player


board_logic = BoardLogic
