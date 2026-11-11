colors = {
    "O_piece" : "yellow",
    "I_piece" : "light_blue",
    "T_piece" : "purple",
    "L_piece" : "orange",
    "J_piece" : "blue",
    "S_piece" : "green",
    "Z_piece" : "red"
    }
initial_positions = { # first pair is rotation axis
    "O_piece" : [(5, 21), (5, 20), (6, 21), (6, 20)],
    "I_piece" : [(5, 21), (5, 22), (5, 20), (5, 19)],
    "T_piece" : [(5, 20), (5, 21), (4, 20), (6, 20)],
    "L_piece" : [(5, 20), (4, 20), (6, 20), (6, 21)],
    "J_piece" : [(5, 20), (6, 20), (4, 20), (4, 21)],
    "S_piece" : [(5, 20), (5, 21), (6, 21), (4, 20)],
    "Z_piece" : [(5, 20), (5, 21), (4, 21), (6, 20)]
    }

class Block:
    def __init__(self, x, y, color):
        self.x = x
        self.y = y
        self.color = color
    
class Piece:
    def __init__(self, type):
        self.type = type
        self.blocks = [Block(x, y, colors[type]) for x, y in initial_positions[type]]

    def move(self, direction, board):
        match(direction):
            case "left":
                new_pos = [(b.x - 1, b.y) for b in self.blocks]
                if board.is_valid(new_pos):
                    for b in self.blocks:
                        b.x -= 1

            case "right":
                new_pos = [(b.x + 1, b.y) for b in self.blocks]
                if board.is_valid(new_pos):
                    for b in self.blocks:
                        b.x += 1

            case "down":
                new_pos = [(b.x, b.y - 1) for b in self.blocks]
                if board.is_valid(new_pos):
                    for b in self.blocks:
                        b.y -= 1
                else: 
                    return False
        return True

    def new_positions_rotate(self):
        if self.type == "O_piece":
            res = [[b.x, b.y] for b in self.blocks]
        #elif self.type == "I_piece":
            #add I_piece case
        #    pass
        else:
            offset = (self.blocks[0].x, self.blocks[0].y)
            res = [[b.x - offset[0], b.y - offset[1]] for b in self.blocks]
            for pair in res:
                pair[0], pair[1] = pair[1], -pair[0]
                pair[0] += offset[0]
                pair[1] += offset[1]
        return res
    
    def rotate(self, board):
        possible_new_positions = self.new_positions_rotate()
        if board.is_valid(possible_new_positions):
            for i, b in enumerate(self.blocks):
                b.x = possible_new_positions[i][0]
                b.y = possible_new_positions[i][1]
        else:
            #add attempt to shift piece after rotation (changing possible_new_positions)
            pass