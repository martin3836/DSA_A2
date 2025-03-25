import copy
from a1_partc import Queue
from a1_partd import overflow

def copy_board(board):
    """
    Creates a deep copy of the given board.

    Parameters:
    board (list of list of int): The game board to be copied.

    Returns:
    list of list of int: A deep copy of the given board.
    """
    return copy.deepcopy(board)

def evaluate_board(board, player):
    """
    Evaluates the board for a given player.

    Parameters:
    board (list of list of int): The game board to be evaluated.
    player (int): The player for whom the board is being evaluated. 
                  Positive values represent the player, negative values represent the opponent.

    Returns:
    int or float: The score of the board. A higher score indicates a better board state for the player.
                  Returns float('inf') if the player has won, float('-inf') if the opponent has won.
    """
    score = 0
    for row in board:
        for cell in row:
            if cell * player > 0:
                score += abs(cell)
            elif cell * player < 0:
                score -= abs(cell)
    
    if all(cell * player > 0 for row in board for cell in row if cell != 0):
        return float('inf')  
    elif all(cell * player < 0 for row in board for cell in row if cell != 0):
        return float('-inf')  
    
    return score

class GameTree:
    class Node:
        def __init__(self, board, depth, player, tree_height=4,move=None):
            """
            Initializes a node in the game tree.

            Parameters:
            board (list of list of int): The game board at this node.
            depth (int): The depth of this node in the game tree.
            player (int): The player making the move at this node. 
                          Positive values represent the player, negative values represent the opponent.
            tree_height (int, optional): The maximum height of the game tree. Default is 4.
            move (tuple of int, optional): The move that led to this node. Default is None.

            Attributes:
            board (list of list of int): The game board at this node.
            depth (int): The depth of this node in the game tree.
            player (int): The player making the move at this node.
            children (list of Node): The child nodes of this node.
            score (int or None): The score of this node. Default is None.
            move (tuple of int or None): The move that led to this node. Default is None.
            """
            self.board = board
            self.depth = depth 
            self.player = player  
            self.children = []
            self.score = None
            self.move = move  
            
            if depth < tree_height - 1 and not self.is_terminal():
                self.generate_children(tree_height)

        def is_terminal(self):
            """
            Checks if the node is a terminal node (i.e., no further moves possible).

            Returns:
            bool: True if the node is terminal, False otherwise.
            """
            return all(cell > 0 for row in self.board for cell in row) or \
                all(cell < 0 for row in self.board for cell in row)

        def generate_children(self, tree_height):
            """
            Generates child nodes for the current node.

            Parameters:
            tree_height (int): The maximum height of the game tree.
            """            
            for r in range(len(self.board)):
                for c in range(len(self.board[r])):
                    if self.board[r][c] * self.player > 0:
                        new_board = self.simulate_move(r, c)
                        self.children.append(GameTree.Node(new_board, self.depth + 1, self.player, tree_height,move=(r, c)))

        def simulate_move(self, row, col):
            """
            Creates a deep copy of the given board.

            Parameters:
            board (list of list of int): The game board to be copied.

            Returns:
            list of list of int: A deep copy of the given board.
            """
            new_board = [row.copy() for row in self.board]
            new_board[row][col] += self.player
            return self.overflow(new_board)

        def overflow(self, board):
            """
            Handles the overflow logic from Assignment 1.

            Parameters:
            board (list of list of int): The game board to handle overflow.

            Returns:
            list of list of int: The game board after handling overflow.
            """
            tmpQ=Queue()
            overflow(board,tmpQ)
            return board

    def __init__(self, board, player, tree_height = 4):
        """
        Initializes the game tree.

        Parameters:
        board (list of list of int): The initial game board.
        player (int): The player making the first move. 
                      Positive values represent the player, negative values represent the opponent.
        tree_height (int, optional): The maximum height of the game tree. Default is 4.
        """
        self.player = player
        self.board = copy_board(board)
        self.root = self.Node(board, 0, player, tree_height)


    def get_move(self):
        """
        Uses the minimax algorithm to find the best move.

        Returns:
        tuple of int: The best move for the player.
        """
        self.minimax(self.root, True)
        best_move = max(self.root.children, key=lambda child: child.score)
        return best_move.move


    def minimax(self, node, maximizing):
        """
        Minimax algorithm with depth-first traversal.

        Parameters:
        node (Node): The current node in the game tree.
        maximizing (bool): True if the current move is maximizing, False if minimizing.

        Returns:
        int: The score of the node.
        """
        if not node.children:
            node.score = evaluate_board(node.board, node.player)
            return node.score

        if maximizing:
            node.score = max(self.minimax(child, False) for child in node.children)
        else:
            node.score = min(self.minimax(child, True) for child in node.children)

        return node.score

    def clear_tree(self):
        """Clears the tree for garbage collection."""
        self.root = None
    
