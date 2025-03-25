#   Author: Catherine Leung
#   This is the game that you will code the bots to play.  You can also play against your bot
#   To run the game you will need pygames installed.  See: https://pypi.org/project/pygame/
#   Once you have pygames, you can run the game by using the command:
#   python game.py
#   
#   the gem images used are from opengameart.org by qubodup
#   https://opengameart.org/content/rotating-crystal-animation-8-step,
#   https://creativecommons.org/licenses/by/3.0/

import pygame
import sys
import math
import copy

from a1_partd import overflow
from a1_partc import Queue
from player1 import PlayerOne
from player2 import PlayerTwo 

class Dropdown:
    def __init__(self, x, y, width, height, options):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.options = options
        self.current_option = 0

    def draw(self, window):
        pygame.draw.rect(window, BLACK, (self.x, self.y, self.width, self.height), 2)
        font = pygame.font.Font(None, 36)
        text = font.render(self.options[self.current_option], 1, BLACK)
        window.blit(text, (self.x + 5, self.y + 5))

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            x, y = event.pos
            if self.x < x < self.x + self.width and self.y < y < self.y + self.height:
                self.current_option = (self.current_option + 1) % len(self.options)

    def get_choice(self):
        return self.current_option

class Button:
    def __init__(self, x, y, width, height, text, callback):
        self.rect = pygame.Rect(x, y, width, height)
        self.text = text
        self.callback = callback
        self.font = pygame.font.Font(None, 36)
        self.color = (200, 200, 200)
        self.hover_color = (150, 150, 150)
        self.active_color = self.color

    def draw(self, window):
        pygame.draw.rect(window, self.active_color, self.rect)
        text_surf = self.font.render(self.text, True, (0, 0, 0))
        text_rect = text_surf.get_rect(center=self.rect.center)
        window.blit(text_surf, text_rect)

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            if self.rect.collidepoint(event.pos):
                self.callback()
        elif event.type == pygame.MOUSEMOTION:
            if self.rect.collidepoint(event.pos):
                self.active_color = self.hover_color
            else:
                self.active_color = self.color

class Board:
    def __init__(self,width,height, p1_sprites, p2_sprites):
        self.width = width
        self.height = height
        self.board = [[0 for _ in range(width)] for _ in range(height)]
        self.p1_sprites = p1_sprites
        self.p2_sprites = p2_sprites
        self.board[0][0] = 1
        self.board[self.height-1][self.width-1] = -1
        self.turn = 0
        self.history = []

    def get_board(self):
        current_board = []
        for i in range(self.height):
            current_board.append(self.board[i].copy())
        return current_board

    def valid_move(self, row,col,player):
        if row >= 0  and row < self.height and col >= 0 and col < self.width and (self.board[row][col]==0 or self.board[row][col]/abs(self.board[row][col]) == player):
            return True
        return False

    def add_piece(self, row, col, player, bot_move=False):
        if self.valid_move(row, col, player):
            if not bot_move:
                self.history.append(copy.deepcopy(self.board)) 
            self.board[row][col] += player
            self.turn += 1
            return True
        return False

    def check_win(self):
        if(self.turn > 0):
            num_p1 = 0
            num_p2 = 0
            for i in range(self.height):
                for j in range(self.width):
                    if(self.board[i][j] > 0):
                        if num_p2 > 0:
                            return 0
                        num_p1 += 1
                    elif(self.board[i][j] < 0):
                        if num_p1 > 0:
                            return 0
                        num_p2 += 1
            if(num_p1 == 0):
                return -1
            if(num_p2== 0):
                return 1
        return 0

    def do_overflow(self,q):
        oldboard = []
        for i in range(self.height):
            oldboard.append(self.board[i].copy())
        numsteps = overflow(self.board, q)
        if(numsteps != 0):
            self.set(oldboard)
        return numsteps
    
    def set(self, newboard):
        for row in range(self.height):
            for col in range(self.width):
                self.board[row][col] = newboard[row][col]

    def draw(self, window, frame):
        for row in range(GRID_SIZE[0]):
            for col in range(GRID_SIZE[1]):
                rect = pygame.Rect(col * CELL_SIZE + X_OFFSET, row * CELL_SIZE+Y_OFFSET, CELL_SIZE, CELL_SIZE)
                pygame.draw.rect(window, BLACK, rect, 1)
        for row in range(self.height):
            for col in range(self.width):
                if self.board[row][col] != 0:
                    rpos = row * CELL_SIZE + Y_OFFSET
                    cpos = col * CELL_SIZE + X_OFFSET
                    if self.board[row][col] > 0:
                        sprite = p1_sprites
                    else:
                        sprite = p2_sprites
                    if abs(self.board[row][col]) == 1:
                        cpos += CELL_SIZE //2 - 16
                        rpos += CELL_SIZE //2 - 16
                        window.blit(sprite[math.floor(frame)], (cpos, rpos))
                    elif abs(self.board[row][col]) == 2:
                        cpos += CELL_SIZE //2 - 32
                        rpos += CELL_SIZE //2 - 16
                        window.blit(sprite[math.floor(frame)], (cpos, rpos))
                        cpos += 32
                        window.blit(sprite[math.floor(frame)], (cpos, rpos))

                    elif abs(self.board[row][col]) == 3:
                        cpos += CELL_SIZE //2 - 16
                        rpos += 8
                        window.blit(sprite[math.floor(frame)], (cpos, rpos))
                        cpos = col * CELL_SIZE + X_OFFSET + CELL_SIZE //2 - 32
                        rpos += CELL_SIZE //2
                        window.blit(sprite[math.floor(frame)], (cpos, rpos))
                        cpos += 32
                        window.blit(sprite[math.floor(frame)], (cpos, rpos))
                    elif abs(self.board[row][col]) == 4:
                        cpos += CELL_SIZE //2 - 32
                        rpos += 8
                        window.blit(sprite[math.floor(frame)], (cpos, rpos))
                        rpos += CELL_SIZE //2
                        window.blit(sprite[math.floor(frame)], (cpos, rpos))
                        cpos += 32
                        window.blit(sprite[math.floor(frame)], (cpos, rpos))
                        rpos -= CELL_SIZE //2
                        window.blit(sprite[math.floor(frame)], (cpos, rpos))




# Constants
GRID_SIZE = (5, 6)
CELL_SIZE = 100
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
X_OFFSET = 0
Y_OFFSET = 100
FULL_DELAY = 5
EASY = 2
NORMAL = 3
HARD = 4

# hate the colours?  there are other options.  Just change the lines below to another colour's file name.  
# the following are available blue, pink, yellow, orange, grey, green
p1spritesheet = pygame.image.load('blue.png')
p2spritesheet = pygame.image.load('pink.png')
p1_sprites = []
p2_sprites = []


player_id = [1 , -1]


for i in range(8):
    curr_sprite = pygame.Rect(32*i,0,32,32)
    p1_sprites.append(p1spritesheet.subsurface(curr_sprite))
    p2_sprites.append(p2spritesheet.subsurface(curr_sprite))    


frame = 0

# Initialize Pygame
pygame.init()
window = pygame.display.set_mode((1200,800))

# Create buttons for difficulty
def increase_p1_difficulty():
    bots[0].difficulty = min(bots[0].difficulty + 1, HARD)

def decrease_p1_difficulty():
    bots[0].difficulty = max(bots[0].difficulty - 1, EASY)

def increase_p2_difficulty():
    bots[1].difficulty = min(bots[1].difficulty + 1, HARD)

def decrease_p2_difficulty():
    bots[1].difficulty = max(bots[1].difficulty - 1, EASY)

buttons = [
    Button(880, 110, 50, 30, '+', increase_p1_difficulty),
    Button(940, 110, 50, 30, '-', decrease_p1_difficulty),
    Button(880, 170, 50, 30, '+', increase_p2_difficulty),
    Button(940, 170, 50, 30, '-', decrease_p2_difficulty),
    Button(0,600,150,50, "Undo Move", lambda: undo_move(choice[0] == 1 or choice[1] == 1))
]

def get_difficulty_text(tree_height):
    if tree_height == EASY:
        return "Easy"
    elif tree_height == NORMAL:
        return "Normal"
    elif tree_height == HARD:
        return "Hard"
    else:
        return str(tree_height)
    
def undo_move(bot_turn=False):

    if board.history:
        board.board = board.history.pop()
        board.turn -= 1
        if bot_turn:
            board.turn -= 1
            status[1] = ""
        return True

    return False


pygame.font.init()
font = pygame.font.Font(None, 36)  # Change the size as needed
bigfont = pygame.font.Font(None, 108)
# Create the game board
# board = [[0 for _ in range(GRID_SIZE[0])] for _ in range(GRID_SIZE[1])]
player1_dropdown = Dropdown(650, 100, 200, 50, ['Human', 'AI'])
player2_dropdown = Dropdown(650, 160, 200, 50, ['Human', 'AI'])

status=["",""]
board = Board(GRID_SIZE[1], GRID_SIZE[0], p1_sprites, p2_sprites)
# Game loop
running = True
overflow_boards = Queue()
overflowing = False
numsteps = 0
has_winner = False
bots = [PlayerOne(), PlayerTwo()]
grid_col = -1
grid_row = -1
choice = [None, None]
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        else:
            player1_dropdown.handle_event(event)
            player2_dropdown.handle_event(event)
            choice[0] = player1_dropdown.get_choice()
            choice[1] = player2_dropdown.get_choice()
            for button in buttons:
                button.handle_event(event)
            if event.type == pygame.MOUSEBUTTONDOWN:
                x,y = event.pos
                row = y - Y_OFFSET
                col = x - X_OFFSET    
                grid_row, grid_col = row // CELL_SIZE, col // CELL_SIZE

    player1_dropdown.draw(window)
    player2_dropdown.draw(window)
    for button in buttons:
        button.draw(window)

    win = board.check_win()
    if win != 0:
        winner = 1
        if win == -1:
            winner = 2
        has_winner = True

    if not has_winner:
        if overflowing:
            status[0] = "Overflowing"
            if not overflow_boards.is_empty():
                if repeat_step == FULL_DELAY:
                    next = overflow_boards.dequeue()
                    board.set(next)
                    repeat_step = 0
                else:
                    repeat_step += 1
            else:
                overflowing = False

        else:
            current_player = board.turn % 2
            status[0] = "Player " + str(current_player + 1) + "'s turn"
            make_move = False
            if choice[current_player] == 1:
                (grid_row,grid_col) = bots[current_player].get_play(board.get_board())
                status[1] = "Bot chose row {}, col {}".format(grid_row, grid_col)
                if not board.valid_move(grid_row, grid_col, player_id[current_player]):
                       has_winner = True
                       # if p1 makes an invalid move, p2 wins.  if p2 makes an invalid move p1 wins
                       winner = ((current_player + 1) % 2) + 1 
                else:
                    make_move = True
            else:
                if board.valid_move(grid_row, grid_col, player_id[current_player]):
                    make_move = True

            if make_move:
                board.add_piece(grid_row, grid_col, player_id[current_player], choice[current_player] == 1)
                numsteps = board.do_overflow(overflow_boards)
                if numsteps != 0:
                    overflowing = True
                    repeat_step = 0
                grid_row = -1
                grid_col = -1

    # Draw the game board
    window.fill(WHITE)
    board.draw(window,frame)
    window.blit(p1_sprites[math.floor(frame)], (600, 100))
    window.blit(p2_sprites[math.floor(frame)], (600, 160))
    frame = (frame + 0.5) % 8
    player1_dropdown.draw(window)
    player2_dropdown.draw(window)

    total_moves = font.render(f"Total number of moves in the game: {board.turn}", True, (0,0,0,0))
    window.blit(total_moves, (700, 700))


    elapsed_time_ms = pygame.time.get_ticks()
    elapsed_time_sec = elapsed_time_ms // 1000  # Convert to seconds

    minutes = elapsed_time_sec // 60
    seconds = elapsed_time_sec % 60
    timer_text = font.render(f"Total Time: {minutes:02}:{seconds:02}", True, (0,0,0,0))

    window.blit(timer_text, (20, 20))
    
    if choice[0] == 1:
        buttons[0].draw(window)
        buttons[1].draw(window)
        p1_difficulty = font.render(f"Difficulty: {get_difficulty_text(bots[0].difficulty)}", True, BLACK)
        window.blit(p1_difficulty, (1000, 110))
    
    if choice[1] == 1:
        buttons[2].draw(window)
        buttons[3].draw(window)
        p2_difficulty = font.render(f"Difficulty: {get_difficulty_text(bots[1].difficulty)}", True, BLACK)
        window.blit(p2_difficulty, (1000, 170))
    
    buttons[4].draw(window)

    if not has_winner:  
        text = font.render(status[0], True, (0, 0, 0))  # Black color
        window.blit(text, (X_OFFSET, 750 ))
        text = font.render(status[1], True, (0, 0, 0))  # Black color
        window.blit(text, (X_OFFSET,  700 ))
    else:
        text = bigfont.render("Player " + str(winner)  + " wins!", True, (0, 0, 0))  # Black color
        window.blit(text, (300, 250))




    pygame.display.update()
    pygame.time.delay(100)

pygame.quit()
sys.exit()
