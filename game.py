import piece_logic
import board
import random

class Game:
    def __init__(self, seed=None):
        self.rng = random.Random(seed)
        self.board = board.Board()
        self.score = 0
        self.game_over = False
        self.piece = self.get_piece()
        self.held_piece = None

    def get_piece(self):
        return piece_logic.Piece(self.rng.choice(list(piece_logic.initial_positions)))

    # moves down piece if possible, locks it if not, returns number of lines cleared
    def tick(self):
        if not self.piece.move("down", self.board):
            self.board.lock_piece(self.piece)
            nlines = self.board.clear_lines()
            self.score += {0 : 0, 1 : 100, 2 : 300, 3 : 500, 4 : 800}[nlines]
            self.piece = self.get_piece()
            # if next piece has invalid starting positions, end game 
            if not self.board.is_valid([(b.x, b.y) for b in self.piece.blocks]):
                self.game_over = True
            return nlines

    def rotate(self):
        self.piece.rotate(self.board)

    def move_left(self):
        self.piece.move("left", self.board)
    def move_right(self):
        self.piece.move("right", self.board)
    def move_down(self):
        return self.tick()