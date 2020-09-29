import pygame
from tkinter import *
from queue import PriorityQueue
class Node:                 #node class to define current position
    def __init__(self,position,gcost=0,hcost=0,parent=()):
        self.gcost=gcost       #gcost is the distance from beginning node
        self.hcost=hcost       #hcost is the distance from end node
        self.position=position #position is a x,y coordinate
        self.parent=parent      #parent is the node that the current node is following
    def __eq__(self, other):        #equivalence operator based on position
        if isinstance(other, Node):
            return self.position==other.position
        return False
    def fcost(self):        #fcost is gcost+hcost
        return self.gcost+self.hcost
    def __lt__(self, other):    #less than operator based on fcost, used in the priority queue
        if isinstance(other, Node):
            if self.fcost!=other.fcost:
                return self.fcost() < other.fcost()
            return self.hcost < other.hcost
        return False
    def __str__(self):
        return "x, y: "+(str)(self.position[0])+" "+(str)(self.position[1])+" "+(str)(self.gcost)+" "

class Grid:
    def __init__(self,window):
        self.window=window
        self.colorboard=[]  #this is for the colors of the maze
        self.board=[]      #this is where the maze solving will take place
        for i in range(20):
            add=[]
            for k in range(20):
                add.append(' ')
            self.board.append(add)      #have board be initially blank
        for i in range(len(self.board)):
            add=[]
            for k in range(len(self.board[i])):
                add.append((255,255,255))  #initially have all colors of the maze be white for blank space
            self.colorboard.append(add)
    def drawGrid(self):         #general method to draw the grid
        for i in range(len(self.board)):
            for k in range(len(self.board[i])):

                pygame.draw.rect(self.window, (0, 0, 0), (k * 50, i * 50, 50, 50))  #in each square have a big black rectangle to serve as a border

                pygame.draw.rect(self.window, self.colorboard[i][k], (k * 50 + 10, i * 50 + 10, 30, 30))#then fill with the appropriate color from color board

    def distance(p1, p2):       #method to calculate distance between two points
        distx = (int)(abs(p1[0] - p2[0]))
        disty = (int)(abs(p1[1] - p2[1]))
        if distx > disty:
            return 14 * disty + 10 * (distx - disty)
        return 14 * distx + 10 * (disty - distx)

    def getNeighbors(self, n):      #method to get all empty neighbors, returns them in a list
        #these arrays store the movement patterns that are allowed in the maze
        #arr1 = [1, -1, 0, 0, 1, -1, 1, -1]
        #arr2 = [1, -1, 1, -1, 0, 0, -1, 1]
        arr1=[1,-1,0,0]
        arr2=[0,0,1,-1]
        col = n.position[0]
        row = n.position[1]
        # print(board[row][col])
        neighbors = []
        for i in range(len(arr1)):      ##check if a neighbor is in bounds or isn't empty, indicated by an "x"
            newrow = row + arr1[i]
            newcol = col + arr2[i]
            # print((str)(newrow)+" "+str(newcol))
            if newrow >= len(self.board) or newrow < 0:
                continue
            if newcol >= len(self.board[newrow]) or newcol < 0:
                continue
            if self.board[newrow][newcol] != "x":
                neighbors.append(Node((newcol, newrow)))
        return neighbors

    def findPath(self,start,target):    #finds a path given a start and target
        open=PriorityQueue()    #have a priority cue of open nodes sorted based on lowest fcost
        closed=[]           #have a list of closed nodes to determine which have already been visited
        begin=Node(start)
        begin.hcost=Grid.distance(start,target)     #only need to initialize hcost, gcost is 0 because it is the starting node
        open.put(begin)
        finish=Node((target))
        while not open.empty():     #while open there are still open nodes
            current=open.get()      #get the lowest fcost node
            closed.append(current)      #put it in closed because it has been visited already
            if current == finish:       #once finished reset all the colors
                while not open.empty():
                    eval=open.get()
                    if self.colorboard[eval.position[1]][eval.position[0]] != (200,200,0):
                        self.colorboard[eval.position[1]][eval.position[0]]=(255,255,255)
                for n in closed:
                    if self.colorboard[n.position[1]][n.position[0]] != (200, 200, 0):
                        self.colorboard[n.position[1]][n.position[0]]=(255,255,255)
                self.drawGrid()
                pygame.display.update()
                Grid.drawPath(self,current.parent,begin)        #draw the path from start to finish, using the parent attribute
                return True;
            if self.colorboard[current.position[1]][current.position[0]]==(0,100,0) or self.colorboard[current.position[1]][current.position[0]]==(255,255,255):
                self.colorboard[current.position[1]][current.position[0]]=(155,0,0) #make closed node red, to indicate its closed
                self.drawGrid()
                pygame.display.update()
            for neighbor in self.getNeighbors(current):     #get the neighbors
                if neighbor in closed:          #if a neighbor has already been visited, don't evaluate it
                    continue
                if self.colorboard[neighbor.position[1]][neighbor.position[0]]==(255,255,255): #make a potentisl neighbor dark green
                    self.colorboard[neighbor.position[1]][neighbor.position[0]]=(0,100,0)
                    self.drawGrid()
                    pygame.display.update()
                newDistanceToNeighbor= current.gcost + Grid.distance((current.position),(neighbor.position)) #calculate gcost for neighbor by utilizing the current node
                other=PriorityQueue()
                foundNeighbor=False             #the following makes sure a neighbor doesn't appear two times in the priority queue
                proxyNeighbor=Node((0,0))
                while not open.empty() and not foundNeighbor:
                    eval=open.get()
                    if eval==neighbor:
                        foundNeighbor=True
                        proxyNeighbor=eval      #if the neighbor is already in the queue
                    else:
                        other.put(eval)
                #if the neighbor is already in the priority queue, make sure you get to it in the most efficient way possible
                if newDistanceToNeighbor<proxyNeighbor.gcost or not foundNeighbor:
                    neighbor.hcost = Grid.distance((neighbor.position), target)
                    neighbor.gcost=newDistanceToNeighbor
                    neighbor.parent=current #set parent to be along the most efficient path
                    other.put(neighbor)
                else:
                    other.put(proxyNeighbor)    #if a better path to neighbor already existed in the queue, keep it
                while not other.empty():
                    open.put(other.get())       #rebuild the open queue
        #if path can't be found, reset all colors and return false
        while not open.empty():
            eval = open.get()
            if self.colorboard[eval.position[1]][eval.position[0]] != (200, 200, 0):
                self.colorboard[eval.position[1]][eval.position[0]] = (255, 255, 255)
        for n in closed:
            if self.colorboard[n.position[1]][n.position[0]] != (200, 200, 0):
                self.colorboard[n.position[1]][n.position[0]] = (255, 255, 255)
        self.drawGrid()
        pygame.display.update()
        return False;
    def drawPath(self,start,end):       #creates green colors across the path
        if start==end:
            return
        col=start.position[0]
        row=start.position[1]
        self.colorboard[row][col]= (90,200,0)   #make the path light green
        self.drawGrid()
        pygame.display.update()
        Grid.drawPath(self,start.parent,end)
def onsubmit():     #get the start and end pairs from the text box
    global start
    global end
    st = e1.get().split(',')
    ed = e2.get().split(',')
    start = (int(st[0]),int(st[1]))
    end = (int(ed[0]),int(ed[1]))
    master.quit()
    master.destroy()

def getPos(point):
    xm=point[0]%50
    ym=point[1]%50
    if xm>=10 and xm<=40 and ym>=10 and ym<=40:
        return((int)(point[0]/50),(int)(point[1]/50))
    else:
        return (-1,-1)


#have a text box prompt for starting and ending position, from 0 to 20 on x and y coordinates
master = Tk()
Label(master, text='Start(x,y):').grid(row=0)
Label(master, text='Finish(x,y)').grid(row=1)
e1 = Entry(master)
e2 = Entry(master)
e1.grid(row=0, column=1)
e2.grid(row=1, column=1)
submit = Button(master, text='Submit', command=onsubmit)
submit.grid(columnspan=2, row=3)
mainloop()
pygame.init()
win=pygame.display.set_mode((1000,1000))
pygame.display.set_caption("window")
g=Grid(win)
g.colorboard[(int)(start[1])][(int)(start[0])]=(200,200,0)
g.colorboard[(int)(end[1])][(int)(end[0])]=(200,200,0)
run=True
while run:
    pygame.time.delay(50)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
    g.drawGrid()
    if pygame.mouse.get_pressed()[0]:
        point=getPos(pygame.mouse.get_pos())        #if you click a square, turn it blue and put an obstacle there
        if point != (-1,-1):
            if g.colorboard[point[1]][point[0]]==(255,255,255):
                g.colorboard[point[1]][point[0]]=(0,200,200)
                g.board[point[1]][point[0]] = 'x'
            elif g.colorboard[point[1]][point[0]]==(0,200,200):     #if you click a square again, it will remove the obstacle
                g.colorboard[point[1]][point[0]] = (255, 255, 255)
                g.board[point[1]][point[0]]=' '
    keys = pygame.key.get_pressed()
    if keys[pygame.K_RETURN]:
        g.findPath(start,end)
    pygame.display.update()
pygame.quit()
