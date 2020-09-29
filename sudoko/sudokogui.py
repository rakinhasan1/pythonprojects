import pygame
#import sudokosolver
from math import *

class Grid:
    def __init__(self, board,window):
        self.board=board
        self.window=window
        self.colorboard=[]
        for i in range(len(self.board)):
            add=[]
            for k in range(len(self.board[i])):
                add.append((255,255,255))       #white squares
            self.colorboard.append(add)

    def drawGrid(self):     #draw the puzzle
        for i in range(len(self.board)):
            for k in range(len(self.board[i])):
                # pygame.draw.rect(win, (0, 0, 0),(i*60,k*60,60,60))
                # pygame.draw.rect(win,board[i][k],(i*50+(5*i),k*50+(5*k),50,50))
                pygame.draw.rect(self.window, (0, 0, 0), (k * 60, i * 60, 60, 60))
                # pygame.draw.rect(win, (255,255,255), (k * 50 + (5 * k), i * 50 + (5 * i), 50, 50))
                pygame.draw.rect(self.window, self.colorboard[i][k], (k * 60 + 10, i * 60 + 10, 40, 40))
                font = pygame.font.Font('freesansbold.ttf', 12)

                # create a text suface object,
                # on which text is drawn on it.
                text = font.render((str)(self.board[i][k]), True, (0, 0, 0), self.colorboard[i][k]) #output the numbers in the sudoko board

                # create a rectangular object for the
                # text surface object
                textRect = text.get_rect()

                # set the center of the rectangular object.
                textRect.center = (k * 60 + 30, i * 60 + 30)

                self.window.blit(text, textRect)

    def isSafe(self,arr, n, row, col):
        for index in range(len(arr)):       #checks if number is already in the row
            if arr[row][index] == n:
                return False
        for index in range(len(arr)):       #checks if number is already in the column
            if arr[index][col] == n:
                return False
        sqr = (int)(sqrt(len(arr)))     #checks if the number is already in the subsquare
        rstart = row - row % sqr
        cstart = col - col % sqr
        for x in range(rstart, rstart + sqr):
            for y in range(cstart, cstart + sqr):
                if arr[x][y] == n:
                    return False
        return True

    def solveSoduko(self,arr, n):
        row = -1
        col = -1
        noEmptySpaces = True
        for x in range(n):
            for y in range(n):
                if arr[x][y] == 0:      #find first empty space
                    row = x
                    col = y
                    noEmptySpaces = False
                    break
            if not noEmptySpaces:
                break

        if noEmptySpaces:
            return True
        for num in range(1, n + 1):         #plug in numbers 1 through n to the empty space
            if Grid.isSafe(self,arr, num, row, col):
                arr[row][col] = num
                self.colorboard[row][col]=(0,120,0)     #make a solved empty space green
                self.drawGrid()
                pygame.display.update()
                if Grid.solveSoduko(self,arr, n):
                    return True
                else:                           #if the current number fails, reset and try the next number
                    arr[row][col] = 0
                    self.colorboard[row][col] = (255, 255, 255)
                    self.drawGrid()
                    pygame.display.update()
        return False

pygame.init()
win=pygame.display.set_mode((1000,1000))
pygame.display.set_caption("window")
#input the sudoko square
board = [

            [3, 0, 6, 5, 0, 8, 4, 0, 0],
            [5, 2, 0, 0, 0, 0, 0, 0, 0],
            [0, 8, 7, 0, 0, 0, 0, 3, 1],
            [0, 0, 3, 0, 1, 0, 0, 8, 0],
            [9, 0, 0, 8, 6, 3, 0, 0, 5],
            [0, 5, 0, 0, 9, 0, 6, 0, 0],
            [1, 3, 0, 0, 0, 0, 2, 5, 0],
            [0, 0, 0, 0, 0, 0, 0, 7, 4],
            [0, 0, 5, 2, 0, 6, 3, 0, 0]
    ]

'''
board=[
        [7, 8, 0, 4, 0, 0, 1, 2, 0],
        [6, 0, 0, 0, 7, 5, 0, 0, 9],
        [0, 0, 0, 6, 0, 1, 0, 7, 8],
        [0, 0, 7, 0, 4, 0, 2, 6, 0],
        [0, 0, 1, 0, 5, 0, 9, 3, 0],
        [9, 0, 4, 0, 6, 0, 0, 0, 5],
        [0, 7, 0, 3, 0, 0, 0, 1, 2],
        [1, 2, 0, 0, 0, 7, 4, 0, 0],
        [0, 4, 9, 2, 0, 6, 0, 0, 7]
    ]
'''
g=Grid(board,win)
run=True
while run:
    pygame.time.delay(50)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
    win.fill((255, 255, 255))
    g.drawGrid()
    '''
    for i in range(9):
        for k in range(9):
            #pygame.draw.rect(win, (0, 0, 0),(i*60,k*60,60,60))
            #pygame.draw.rect(win,board[i][k],(i*50+(5*i),k*50+(5*k),50,50))
            pygame.draw.rect(win, (0,0,0), (k*60,i*60,60,60))
            #pygame.draw.rect(win, (255,255,255), (k * 50 + (5 * k), i * 50 + (5 * i), 50, 50))
            pygame.draw.rect(win, (255,255,255), (k *60+10, i * 60 +10, 40, 40))
            font = pygame.font.Font('freesansbold.ttf', 12)

            # create a text suface object,
            # on which text is drawn on it.
            text = font.render((str)(board[i][k]), True, (0, 0, 0), (255, 255, 255))

            # create a rectangular object for the
            # text surface object
            textRect = text.get_rect()

            # set the center of the rectangular object.
            textRect.center = (k*60+30, i*60+30)

            win.blit(text, textRect)
            '''
    #right click mouse to solve the maze
    if pygame.mouse.get_pressed()[0]:
        g.solveSoduko(g.board,len(g.board))
    pygame.display.update()
pygame.quit()