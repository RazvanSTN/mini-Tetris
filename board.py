class Board:
    def __init__(self):
        self.occupied_cells = {}

    def lock_piece(self, piece):
        for b in piece.blocks:
            self.occupied_cells[(b.x, b.y)] = b.color

    def is_valid(self, possible_positions):
        for (x, y) in possible_positions:
            if not 1 <= x <= 10 or not 1 <= y or (x, y) in self.occupied_cells:
                return False
        return True
    
    def clear_lines(self):
        return 4 #add line clears that returns number of lines cleared