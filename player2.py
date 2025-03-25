from a2_partb import GameTree

class PlayerTwo:

    def __init__(self, name = "P2 Bot", difficulty = 4):
        self.name = name
        self.difficulty = difficulty

    def get_name(self):
        return self.name

    def get_play(self, board):
        tree = GameTree(board, -1, tree_height= self.difficulty)
        (row,col) = tree.get_move()
        tree.clear_tree()
        return (row,col)