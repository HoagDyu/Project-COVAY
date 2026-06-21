import random
from typing import List, Optional, Tuple


class RandomBot:
    

    def __init__(self, seed: Optional[int] = None) -> None:
        self._rng = random.Random(seed)

    def select_move(
        self,
        board,
        color: int,
        valid_moves: Optional[List[Tuple[int, int]]] = None,
    ) -> Optional[Tuple[int, int]]:
        """Return a random legal move or None if no move is available."""
        if valid_moves is None:
            valid_moves = [
                (x, y)
                for y in range(board.size)
                for x in range(board.size)
                if board.is_empty(x, y)
            ]

        if not valid_moves:
            return None

        return self._rng.choice(valid_moves)
