from enum import Enum

class StoneColor(Enum): #Tạo class StoneColor theo Enum để tự gợi ý code, vd: khi viết color.StoneColor thì sẽ tự nãy gợi ý là StoneColor.BLACK hay StoneColor.WHITE..., tránh việc code lộn thành Black thường...
    BLACK = 1
    WHITE = 2
    EMPTY = 0

    

class Status(Enum):
    IDLE = 0
    PLAYING = 1
    HUMAN_TURN = 2
    BOT_TURN = 3
    CLEANING = 4
    DONE = 5
    PAUSE = 6

class GameMode(Enum):
    EMPTY = 0
    PVP = 1
    PVE = 2
    

 