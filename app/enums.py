from enum import Enum


class TournamentStatus(str, Enum):
    CREATED = "created"
    STARTED = "started"
    FINISHED = "finished"


class GameResult(str, Enum):
    UNKNOWN = "unknown"
    WHITE_WINS = "white_wins"
    BLACK_WINS = "black_wins"
    DRAW = "draw"
    BOTH_WIN = "both_win"
    BOTH_LOSE = "both_lose"


class ScoringStatus(str, Enum):
    UNKNOWN = "unknown"
    ABSENT = "absent"
    BYE = "bye"
    READY = "ready"
    PAIRED = "paired"
