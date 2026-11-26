class Board:
    def __init__(self):
        self.occupied_cells = []

    def lock_piece(self, piece):
        for b in piece.blocks:
            self.occupied_cells.append([b.x, b.y, b.color])

    def is_block_in_board(self, pos_tuple):
        return any((x, y) == pos_tuple for x, y, _ in self.occupied_cells)

    def is_valid(self, possible_positions):
        for (x, y) in possible_positions:
            if not 1 <= x <= 10 or not 1 <= y or self.is_block_in_board((x, y)):
                return False
        return True
    
    def clear_lines(self):
        ncleared = 0
        lines = [0] * 25 # counts how many blocks are on a line
        for pos in self.occupied_cells:
            lines[pos[1]] += 1
        for y, line_count in enumerate(lines):
            if line_count == 10:
                ncleared += 1
                to_delete = []
                for item in self.occupied_cells:
                    if item[1] == y:
                        to_delete.append(item) #save to_delete items first so as not to change list while iterating
                for item in to_delete:
                    self.occupied_cells.remove(item)
                for block in self.occupied_cells:
                    if block[1] > y:
                        block[1] -= 1
        return ncleared