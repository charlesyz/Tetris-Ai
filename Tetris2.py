from random import randrange as rand
import pygame, sys
import copy
from Neural import Network
from Neural import Individual
from Neural import Population

sz  = 15 # cell size
cols = 10
rows = 20
maxfps = 30
START_DELAY = 500
MIN_DELAY = 20
POP_SIZE = 100
MAXCOUNT = maxfps / ( START_DELAY / 1000)
#
colors = ['white','red','brown','cyan','orange','magenta','yellow','green'];
tetrominoes = [
        [[[0,0,0,0], [0,0,0,0], [0,0,0,0], [0,0,0,0]],
        [[0,1,1,0], [0,1,1,0], [0,1,1,0], [0,1,1,0]],
        [[0,1,1,0], [0,1,1,0], [0,1,1,0], [0,1,1,0]],
        [[0,0,0,0], [0,0,0,0], [0,0,0,0], [0,0,0,0]]],

        [[[0,0,0,0], [0,0,2,0], [0,0,0,0], [0,0,2,0]],
        [[2,2,2,2], [0,0,2,0], [2,2,2,2], [0,0,2,0]],
        [[0,0,0,0], [0,0,2,0], [0,0,0,0], [0,0,2,0]],
        [[0,0,0,0], [0,0,2,0], [0,0,0,0], [0,0,2,0]]],

        [[[0,0,0,0], [0,0,3,0], [0,0,0,0], [0,0,3,0]],
        [[0,0,3,3], [0,0,3,3], [0,0,3,3], [0,0,3,3]],
        [[0,3,3,0], [0,0,0,3], [0,3,3,0], [0,0,0,3]],
        [[0,0,0,0], [0,0,0,0], [0,0,0,0], [0,0,0,0]]],

        [[[0,0,0,0], [0,0,0,4], [0,0,0,0], [0,0,0,4]],
        [[0,4,4,0], [0,0,4,4], [0,4,4,0], [0,0,4,4]],
        [[0,0,4,4], [0,0,4,0], [0,0,4,4], [0,0,4,0]],
        [[0,0,0,0], [0,0,0,0], [0,0,0,0], [0,0,0,0]]],

        [[[0,0,0,0], [0,0,5,0], [0,0,0,5], [0,5,5,0]],
        [[0,5,5,5], [0,0,5,0], [0,5,5,5], [0,0,5,0]],
        [[0,5,0,0], [0,0,5,5], [0,0,0,0], [0,0,5,0]],
        [[0,0,0,0], [0,0,0,0], [0,0,0,0], [0,0,0,0]]],

        [[[0,0,0,0], [0,0,6,6], [0,6,0,0], [0,0,6,0]],
        [[0,6,6,6], [0,0,6,0], [0,6,6,6], [0,0,6,0]],
        [[0,0,0,6], [0,0,6,0], [0,0,0,0], [0,6,6,0]],
        [[0,0,0,0], [0,0,0,0], [0,0,0,0], [0,0,0,0]]],

        [[[0,0,0,0], [0,0,7,0], [0,0,7,0], [0,0,7,0]],
        [[0,7,7,7], [0,0,7,7], [0,7,7,7], [0,7,7,0]],
        [[0,0,7,0], [0,0,7,0], [0,0,0,0], [0,0,7,0]],
        [[0,0,0,0], [0,0,0,0], [0,0,0,0], [0,0,0,0]]]
]

def toPiece(piece, rotation):
    p = []
    for x in range(0, 4):
        p.append(piece[x][rotation])
    return p

def newGrid():
    grid = []
    for x in range(rows):
        row = []
        for y in range(cols):
            row.append(0)
        grid.append(row)
    return grid

def collision(grid, piece, offx, offy ):
    for y, r in enumerate(piece):
        for x, c in enumerate(r):
            try:
                if c and grid[y + offy][x + offx]:
                    return True
                if c and (x + offx < 0): #for some reason going negative doesnt count as index error
                    return True
            except IndexError:
                if c: #If out of bounds AND the current location is a part of the tetromino (there is white space)
                    return True
    return False

def removeRow(grid, y):
    del grid[y]
    return [[0 for i in range(cols)]] + grid



# COPYING CAUSES REFERENCE ERRORS - WHY DOES THIS CHANGE THE ACTUAL GRID?
def merge(a, b, offx, offy):
    d = a
    e = b
    for y, r in enumerate(e):
        for x, c in enumerate(r):
            try:
                if c:
                    d[y + offy][x + offx] = c
            except IndexError:
                if c:
                    print("ERROR MERGING AT " + x + " " + y)
    return d

class Tetris(object):
    def __init__(self, draw):
        pygame.init()
        pygame.key.set_repeat(250, 100)
        self.width = sz * (cols + 10)
        self.height = sz * (rows)
        self.shouldDraw = draw
        self.myfont = pygame.font.Font(pygame.font.get_default_font(), 12)
        self.screen = pygame.display.set_mode((self.width, self.height))
        pygame.event.set_blocked(pygame.MOUSEMOTION)

        self.pop = Population(POP_SIZE)

        self.init()

    def newPiece(self):
        #print("New Piece")
        self.curr = self.next[:]
        #self.next = tetrominoes[rand(len(tetrominoes))]
        self.played += 1
        if self.played > len(self.pop.data):
            self.played = 0                                         # could cause fitness problems - probably not though
        self.next = tetrominoes[self.pop.data[self.played]]

        self.curr_x = int(cols / 2 - 2)
        self.curr_y = 0
        self.rotation = 0
        if collision(self.grid, toPiece(self.curr,self.rotation) , self.curr_x, self.curr_y):
            self.gameover = True

    def init(self):
        #print("initialized")
        self.grid = newGrid()
        self.played = 0
        self.next = tetrominoes[self.pop.data[self.played]]
        self.newPiece()
        self.level = 1
        self.score = 0
        self.lines = 0
        self.gameover = False
        pygame.time.set_timer(pygame.USEREVENT, START_DELAY)
        self.timeAlive = 0

    def draw(self, m, offx, offy):
        for y, r in enumerate(m):
            for x, c in enumerate(r):
                if c:
                    rect = pygame.Rect((offx + x) * sz, (offy + y) * sz, sz, sz)
                    pygame.draw.rect(self.screen, pygame.Color(colors[c]), rect, 0)

    def move(self, dir):
        x = self.curr_x + dir
        # if out of bounds or hitting another piece, revert
        if collision(self.grid, toPiece(self.curr, self.rotation), x, self.curr_y):
                x = self.curr_x
        self.curr_x = x

    def checkClear(self):
        cleared = 0
        while 1:
            for y, r in enumerate(self.grid):
                if 0 not in r:
                    self.grid = removeRow(self.grid, y)
                    cleared += 1
                    break
            else:
                break

        if cleared > 0:
            scores = [0,40,100,300,1200]
            self.score += scores[cleared] * (self.level)
            self.lines += cleared
            self.level = self.lines // 6 + 1
            #delay = START_DELAY - (START_DELAY / 20) * (self.level - 1)
            #delay = MIN_DELAY if delay < MIN_DELAY else delay
            #pygame.time.set_timer(pygame.USEREVENT, delay)

    def gravity(self):
        y = self.curr_y + 1
        # if landed on something, merge the piece to the grid and check cleared rows
        if collision(self.grid, toPiece(self.curr, self.rotation), self.curr_x, y):
            self.grid = merge(self.grid, toPiece(self.curr, self.rotation), self.curr_x, self.curr_y)
            self.checkClear()
            self.newPiece()

        else:
            self.curr_y = y

    def printScores(self, i):
        # print next piece
        text = self.myfont.render('Next Piece:', False, (0, 0, 0))
        self.screen.blit(text, (cols * sz + 30, 10))
        self.draw(toPiece(self.next, 0), cols + 1, 0)
        # scores
        text = self.myfont.render('Score: ' + str(self.score + self.timeAlive), False, (0, 0, 0))
        self.screen.blit(text, (cols * sz + 30, 100))
        text = self.myfont.render('Level: ' + str(self.level), False, (0, 0, 0))
        self.screen.blit(text, (cols * sz + 30, 120))
        text = self.myfont.render('Lines Complete: ' + str(self.lines), False, (0, 0, 0))
        self.screen.blit(text, (cols * sz + 30, 140))
        text = self.myfont.render('Gen : ' + str(self.pop.gen) + ' person: ' + str(i + 1), False, (0, 0, 0))
        self.screen.blit(text, (cols * sz + 30, 160))
        text = self.myfont.render('Best Score: ' + str(self.pop.globalBest), False, (0, 0, 0))
        self.screen.blit(text, (cols * sz + 30, 180))
        text = self.myfont.render('pieces played: ' + str(self.pop.pop[i].timeAlive), False, (0, 0, 0))
        self.screen.blit(text, (cols * sz + 30, 200))
        text = self.myfont.render('Last gen best: ' + str(self.pop.currentBest), False, (0, 0, 0))
        self.screen.blit(text, (cols * sz + 30, 220))

    def neuralInput(self, individual):

        # merge the current piece to the grid and change all the colours to 1
        n = copy.deepcopy(self.grid)
        p = toPiece(self.curr, self.rotation)
        for i, r in enumerate(n):
            for j, q in enumerate(r):
                if q:
                    n[i][j] = 1
        #make the current piece 1, all other pieces 2
        for i, r in enumerate(p):
            for j, q in enumerate(r):
                if q:
                    n[i][j] = 2

        n = merge(n, p, self.curr_x, self.curr_y)[:]

        event = individual.brain.output(n)
        str = " "
        if event == 0:
            str = "left"
            self.move(-1)
        elif event == 1:
            str = "right"
            self.move(+1)
        elif event == 3:        #essentially do nothing
            str = "down"
            #self.gravity()
        elif event == 2:
            str = "rotate"
            self.newRotation = self.rotation + 1
            if self.newRotation > 3:
                self.newRotation = 0
            if not collision(self.grid, toPiece(self.curr, self.newRotation), self.curr_x, self.curr_y):
                self.rotation = self.newRotation

        text = self.myfont.render("move " + str, False, (0, 0, 0))
        self.screen.blit(text, (cols * sz + 10, 250))


    def keyboardInput(self, Play):
        events = pygame.event.get()
        for event in events:
            if event.type == pygame.USEREVENT:
                self.gravity()

            elif event.type == pygame.KEYDOWN and Play:
                if event.key == pygame.K_ESCAPE:
                    sys.stdin.read(1)
                #if event.key == pygame.K_LEFT:
                #    self.move(-1)
                #elif event.key == pygame.K_RIGHT:
                #    self.move(+1)
                #elif event.key == pygame.K_DOWN:
                #    self.gravity()
                #elif event.key == pygame.K_UP:
                #    self.newRotation = self.rotation + 1
                #    if self.newRotation > 3:
                #        self.newRotation = 0
                #   if not collision(self.grid, toPiece(self.curr, self.newRotation), self.curr_x, self.curr_y):
                #       self.rotation = self.newRotation

    def play(self):
        self.gameover = False
        COUNT = 0
        dont_burn_my_cpu = pygame.time.Clock()
        while 1:
            # Running simulation for the entire population (not showing)
            for i in range(self.pop.size):
                while 1:

                    pygame.time.set_timer(pygame.USEREVENT, START_DELAY)
                    if self.gameover:
                        print("Fitness:", self.pop.pop[i].fitness)
                        self.init()
                        break
                    else:

                        self.screen.fill((255, 255, 255))
                        self.draw(self.grid, 0, 0)
                        self.draw(toPiece(self.curr, self.rotation), self.curr_x, self.curr_y)
                        pygame.draw.line(self.screen, (0, 0, 0), (cols * sz + 2, 0), (cols * sz + 2, self.height))

                        self.printScores(0)

                        self.neuralInput(self.pop.pop[i])
                        self.timeAlive += 1
                        self.pop.pop[i].timeAlive = self.played
                        self.pop.pop[i].score = self.score
                        self.pop.pop[i].lines = self.lines
                        self.pop.pop[i].level = self.level
                        self.pop.pop[i].setFitness()

                        pygame.display.update()

                        #do gravity stuff
                        COUNT += 1
                        if COUNT > MAXCOUNT:
                            COUNT = 0
                            self.gravity()

                        dont_burn_my_cpu.tick(10000)

            self.pop.setBest()

            #show best run
            pygame.time.set_timer(pygame.USEREVENT, START_DELAY)
            while 1:
                if self.gameover:
                    print("Fitness:", self.pop.pop[0].fitness)
                    self.init()
                    break
                elif self.shouldDraw:
                    self.screen.fill((255, 255, 255))
                    # sys.stdin.read(1)
                    self.draw(self.grid, 0, 0)
                    self.draw(toPiece(self.curr, self.rotation), self.curr_x, self.curr_y)
                    pygame.draw.line(self.screen, (0, 0, 0), (cols * sz + 2, 0), (cols * sz + 2, self.height))

                    self.printScores(0)
                    pygame.display.update()

                self.neuralInput(self.pop.pop[0])
                self.timeAlive += 1
                self.pop.pop[0].timeAlive = self.played
                self.pop.pop[0].score = self.score
                self.pop.pop[0].lines = self.lines
                self.pop.pop[0].level = self.level
                self.pop.pop[0].setFitness()
                # print(i)
                self.keyboardInput(True)
                pygame.display.update()

                dont_burn_my_cpu.tick(maxfps)

            self.pop.evolve()





if __name__ == '__main__':
    App = Tetris(True)
    App.play()