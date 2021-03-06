import pprint as pp
import sys

from ch_ss.game_engine.core.board import Board
from ch_ss.game_engine.core.player import Player


class StandardGame:
    def __init__(self) -> None:

        # initialize board, pieces, and players
        self.board = Board(board_config="standard")
        self.white_player = Player("white", self.print_game_state_debug)
        self.black_player = Player("black", self.print_game_state_debug)

        # game level states
        self.move_num = 0
        self.white_states = {
            "en_passant": ("d", True),
            "castling": [True, True, True],  # h1 rook, king, a1 rook (O-O, N/A, O-O-O)
        }
        self.black_states = {
            "en_passant": ("x", False),
            "castling": [True, True, True],  # h8 rook, king, a8 rook (O-O, N/A, O-O-O)
        }
        self.to_move = "white"
        self.consecutive_non_capture_moves = 0

    def play_bot_move(self, player: str) -> None:
        if player == "white":
            pass
        pass

    def play_move(self, player: str, move: str) -> None:
        pass

    def tick(self) -> None:
        pp.pprint("[Game-Tick-%d] %s to move:" % (self.move_num, self.to_move))

        last_move_by = self.to_move
        if self.to_move == "white":

            player_pieces = self.board.get_pieces_by_color("white")
            opp_pieces = self.board.get_pieces_by_color("black")
            en_passant, castling, move = self.white_player.tick(
                self.white_states, player_pieces, opp_pieces, strategy="capturebot5000"
            )
            self.black_states["en_passant"] = en_passant
            self.white_states["castling"] = castling
            self.to_move = "black"

        elif self.to_move == "black":

            player_pieces = self.board.get_pieces_by_color("black")
            opp_pieces = self.board.get_pieces_by_color("white")
            en_passant, castling, move = self.black_player.tick(
                self.black_states, player_pieces, opp_pieces, strategy="capturebot5000"
            )
            self.white_states["en_passant"] = en_passant
            self.black_states["castling"] = castling
            self.to_move = "white"

        else:

            pp.pprint("Error: game.tick() invalid to_move state = %s" % (self.to_move))
            sys.exit()

        if move == "checkmate":
            pp.pprint("Checkmate! %s wins!" % (self.to_move))
            sys.exit()
        if move == "stalemate":
            pp.pprint("Draw, it's a stalemate!")
            sys.exit()

        if "x" in move:
            self.consecutive_non_capture_moves += 1
        else:
            self.consecutive_non_capture_moves = 0

        if self.consecutive_non_capture_moves == 50:
            pp.pprint("Draw, it's a stalemate! 50 moves without capture rule triggered.")
            sys.exit()

        self.board.make_move(move, last_move_by)
        self.move_num += 1

    def print_game_state(self, perspective: str = "white", out_file: str = "board_position.jpg") -> None:
        self.board.to_image(flipped=perspective == "black", out_file=out_file)

    def print_game_state_debug(self, pieces0: dict, pieces1: dict, perspective: str, out_file: str) -> None:
        board = Board(board_config="empty")
        for sid, piece in pieces0.items():
            board.put_piece_by_sid(sid, piece)
        for sid, piece in pieces1.items():
            board.put_piece_by_sid(sid, piece)
        board.to_image(flipped=perspective == "black", out_file=out_file)
