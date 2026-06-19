from .entities import Cell, Move, Player, CellGroup
from ..core.constant import StoneColor, Status
from .rules import Rules

class Board:
    def __init__(self, rows: int = 19, cols: int = 19):
        self.rows = rows
        self.cols = cols
        self.board: list[list[Cell]] = []
        for x in range(rows):
            row: list[Cell] = []
            for y in range(cols):
                cell = Cell(x=x,y=y)
                row.append(cell)
            self.board.append(row)

    #dieu kien ham place_stone:
    #1. cell phai trong board, kiem tra vi tri x, y co hop le hay khong
    #2. cell không được nằm cùng một ô với một quân cờ của đối thủ
    #3. ăn quân: check xung quanh có hết khí không, nếu hết khí thì xóa quân bị ăn
    #4. ktra nước đi tự tử: Sau khi ăn,  nếu quân mình đặt không có khí -> tự tử -> không hợp lệ -> báo lỗi
     
    
    #tra ve cell tai vi tri x, y, neu khong hop le tra ve None
    def get_cell(self, x: int, y: int) -> Cell:
        if 0 <= x < self.rows and 0 <= y < self.cols:
            return self.board[x][y]
        raise ValueError("Không tìm thấy Cell")
        
    
    def get_cell_color(self, x: int, y: int) -> StoneColor:
        cell_color = self.get_cell(x=x,y=y).get_cell_color()
        return cell_color

    


class BoardLogic:
    def __init__(self, player_1: Player , player_2: Player, size: int = 19):
        self.board = Board(size, size)
        self.player_1 = player_1 
        self.player_2 = player_2 
        self.current_player: Player = player_1
        self.cell_groups: list[CellGroup] = []
        self.move_history: list[Move] = []
        self.game_over: bool = False
        self.rules = Rules(self.board)

    #dat quan co len ban co  
    def _place_stone(self, move:Move) -> None:
            if move.x is None or move.y is None:
                raise ValueError("Nước đi không hợp lệ")
            cell = self.board.get_cell(move.x, move.y)
            setattr(cell, "stone_color", self.current_player.color)
    
    #Lay quan het khi cua doi thu, neu co het khi thi xoa quan do
    def _get_captured_groups(self, x: int, y: int) -> list[list[Cell]]:
        cell = self.board.get_cell(x, y)
        if getattr(cell, "stone_color", None) is None:
            return []
        if cell.get_cell_color() == self.current_player.color:
            return []

        if self.current_player.color == StoneColor.BLACK:
            opponent_color = StoneColor.WHITE
        else:
            opponent_color = StoneColor.BLACK

        #Xem xung quanh cell, neu co quan doi thu het khi thi xoa quan do
        captured_groups: list[list[Cell]] = []
        for neighbor in cell.neighbors:
            if neighbor.get_cell_color() == opponent_color:
                group = self.get_group(neighbor.x, neighbor.y) #
                liberties = self.group_liberties(group) #check khí
                if liberties == 0: #nếu hết khí 
                    captured_groups.append(group) # thi them group vào danh sách captured_groups

        return captured_groups
    
        

    #Xoa cac quan co bi an, tra ve danh sach vi tri cac quan co bi an
    def _remove_captured_groups(self, groups: list[list[Cell]]) -> list[tuple[int, int]]:
        captured_positions: list[tuple[int, int]] = []
        for group in groups:
            for cell in group:
                captured_positions.append((cell.x, cell.y))
                cell.clear_stone() #xóa quân cờ trên ô đó
        return captured_positions


    def process_move(self, x: int, y: int) -> bool:
        #cell phai o trong board
        if not self.rules.is_valid_move(x, y):
            print("Vị trí ({x}, {y}), không hợp lệ.")
            return False
        #cell phai trong va khong co quan co
        if not self.rules.is_empty_cell(x, y):
            print("Vị trí ({x}, {y}), đã có quân cờ.")
            return False

        #dat move
        move = Move(player=self.current_player, x=x, y=y)
        self._place_stone(move)

        #kiem tra an quan
        captured_groups = self._get_captured_groups(x, y)

        #kiem tra tu tu
        if not captured_groups and self.get_liberties(x, y) == 0:
            print("Nước đi ({x}, {y}) là tự tử.")
            return False

        self.move_history.append(move)
        return True    
    
    #Xử lý nước đi pass, trả về True nếu cả hai người chơi đều pass liên tiếp, ngược lại trả về False
    def process_pass(self) -> bool:
        self.move_history.append(Move(player=self.current_player, x=None, y=None))
        if len(self.move_history) >= 2:
            last_move = self.move_history[-1]
            second_last_move = self.move_history[-2]
            if last_move.x is None and last_move.y is None and second_last_move.x is None and second_last_move.y is None:
                self.game_over = True
                return True
        return False
    
    #Xử lý nước đi pass, không cần trả về giá trị nào
    def pass_turn(self) -> None:
        self.move_history.append(Move(player=self.current_player, x=None, y=None))
        if len(self.move_history) >= 2:
            last_move = self.move_history[-1]
            second_last_move = self.move_history[-2]
            if last_move.x is None and last_move.y is None and second_last_move.x is None and second_last_move.y is None:
                self.game_over = True
        self.current_player = self.player_1 if self.current_player == self.player_2 else self.player_2
    
    #Xử lý kết thúc trận đấu, tính điểm và xác định người chiến thắng
    def get_liberties(self, x: int, y: int, player: Player | None = None) -> int:
        cell = self.board.get_cell(x, y)
        if player is None:
            player = self.current_player
        if cell.get_cell_color() != player.color:
            return 0
        group = self.get_group(x, y)
        return self.group_liberties(group)

    #lay danh sach cac quan co cung group voi cell tai vi tri x, y
    def get_group(self, x: int, y: int) -> list[Cell]:
        pass
    
    def process_remove_dead_group(self, x: int, y: int) -> bool:
        pass

    def remove_dead_group(self, x: int, y: int) -> int:
        pass

    def process_end_match(self) -> None:
        pass

    def calculate_all_territory(self) -> list[float]:
        pass

    def get_current_player_color(self) -> StoneColor:
        return self.current_player.color
