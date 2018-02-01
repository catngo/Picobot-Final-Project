# Name: Cat Ngo
# Project: Picobot Project
# Date: November 27th, 2016

import random
import operator

HEIGHT = 25
WIDTH = 25
NUMSTATES = 5


class Program:
    def __init__(self):
        """ Define the class
        """
        self.rules = {}

    def __repr__(self):
        """ To print the rules
        """
        sorted_d = sorted(self.rules.items(), key=operator.itemgetter(0))
        surrounding = ('xxxx', 'Nxxx', 'NExx', 'NxWx', 'xxxS', 'xExS', 'xxWS', 'xExx', 'xxWx')
        RULES = ''
        for state in range(0, 5):
            for pattern in surrounding:
                RULES += str(state) + ' ' + pattern + ' -> '
                RULES += self.rules[(state, pattern)][0] + ' '
                RULES += str(self.rules[(state, pattern)][1]) + '\n'
        return RULES

    def __gt__(self, other):
        """ To tiebreak in sorting
        """
        return random.choice([True, False])

    def __lt__(self, other):
        """ To tie break in sorting
        """
        return random.choice([True, False])

    def randomize(self):
        """ To randomize all 45 possible surroundings and states
        """
        Moves = ('N', 'S', 'W', 'E')
        surrounding = ('xxxx', 'Nxxx', 'NExx', 'NxWx', 'xxxS', 'xExS', 'xxWS', 'xExx', 'xxWx')
        for state in range(5):
            for pattern in surrounding:
                movedir = random.choice(Moves)
                while movedir in pattern:
                    movedir = random.choice(Moves)
                self.rules[(state, pattern)] = (movedir, random.randint(0, 4))

    def getMove(self, state, surrounding):
        """ Return a tuple containing the next move and the new state
        """
        return self.rules[(state, surrounding)]

    def mutate(self):
        """ choose a single rule from self and change the value
        """
        Moves = ('N','S','W','E')
        surrounding = ('xxxx','Nxxx','NExx','NxWx','xxxS','xExS','xxWS','xExx','xxWx')
        state = random.randint(0,4)
        pattern = random.choice(surrounding)
        movedir = random.choice(Moves)
        while movedir in pattern:
            movedir = random.choice(Moves)
        self.rules[(state,pattern)] = (movedir,random.randint(0,4))
    
    def crossover(self,other):
        """ create an offspring as an output that has some rules from other and the rest from other
        """
        offspring = Program()
        crossover_state = random.randint(0,3)
        Moves = ('N','S','W','E')
        surrounding = ('xxxx','Nxxx','NExx','NxWx','xxxS','xExS','xxWS','xExx','xxWx')
        for state in range(crossover_state+1):
            for pattern in surrounding:
                offspring.rules[(state,pattern)] = self.rules[(state,pattern)]
        for state in range(crossover_state+1,5):
            for pattern in surrounding:
                offspring.rules[(state,pattern)] = other.rules[(state,pattern)]
        return offspring

class World:
    def __init__(self, initial_row, initial_col, program):
        """ Define items
        """
        self.prow = initial_row
        self.pcol = initial_col
        self.state = 0
        self.prog = program
        self.room = [ [' ']*WIDTH for row in range(HEIGHT) ]
        for col in range(WIDTH):
            self.room[0][col] = '-'
        for col in range(WIDTH):
            self.room[HEIGHT-1][col] = '-' 
        for row in range(HEIGHT):
            self.room[row][0] = '|'
        for row in range(HEIGHT-1):
            self.room[row][WIDTH -1] = '|'
        self.room[0][0] = '+'
        self.room[0][WIDTH-1] = '+'
        self.room[HEIGHT-1][0] = '+'
        self.room[HEIGHT-1][WIDTH-1] = '+'
        self.room[self.prow][self.pcol] = 'P'
    
    def __repr__(self):
        """ Return a string that shows the maze with spaces as unvisited, o as visited but not there, and current picobot position
        """
        NR = len(self.room)
        NC = len(self.room[0])
        BOARD = ''
        for r in range(NR): # NR = =numrows
            for c in range(NC):  # NC == numcols
                BOARD += self.room[r][c]
            BOARD += '\n'
        return BOARD

    def getCurrentSurroundings(self):
        """ return a surrounding string for current position of Picobot
        """
        state = ''
        if self.prow == 1:
            state += 'N'
        else:
            state += 'x'
        if self.pcol == WIDTH - 2:
            state += 'E'
        else:
            state += 'x'
        if self.pcol == 1:
            state += 'W'
        else:
            state += 'x'
        if self.prow == HEIGHT - 2:
            state += 'S'
        else:
            state += 'x'
        return state
    
    def step(self):
        """ moves Picobot one step, update self.room, state and row and col of Picobot using self.prog
        """
        current_surrounding = self.getCurrentSurroundings()
        NEW = self.prog.getMove(self.state,current_surrounding)
        nextMove = NEW[0]
        nextState = NEW[1]
        self.room[self.prow][self.pcol] = 'o'
        self.state = nextState
        if nextMove == 'N':
            self.prow -= 1
        elif nextMove == 'S':
            self.prow += 1
        elif nextMove == 'W':
            self.pcol -= 1
        else:
            self.pcol += 1
        self.room[self.prow][self.pcol] = 'P'
    
    def run(self,steps):
        """ Simulate the steps over how many runs
        """
        for turn in range(steps):
            self.step()
    
    def fractionVisitedCells(self):
        """ Return floating point that is the fraction of cells in self.room that Picobot has visited
        """
        cellsVisited = 0
        cellsTotal = 23*23
        for col in range(WIDTH):
            for row in range(HEIGHT):
                if self.room[row][col] == 'o' or self.room[row][col] == 'P':
                    cellsVisited += 1
        return cellsVisited/cellsTotal

def get_population(p):
    """ produces p number of random picobot programs
    """
    L = []
    for i in range(p):
        d = Program()
        d.randomize()
        L += [d]
    return L

def evaluateFitness(program,trials,steps):
    """ takes in a Picobot program, a positive integer trials that indicates number of random starting points and steps that indicate how many steps of simulation. Return the average fitness over the number of trials
    """
    totalFitness = 0
    for x in range(trials):
        row = random.randint(1,23) #keeping it inside the room
        col = random.randint(1,23)  #keeping it inside the room
        picobot = World(row,col,program)
        picobot.run(steps)
        totalFitness += picobot.fractionVisitedCells()
    return totalFitness/trials

def GA(popsize,numgens):
    steps = 1000
    trials = 50
    fitRate = 0.1
    mutationRate = 33 # 33 is 33%, and so on.
    Population = get_population(popsize)
    for gen in range(numgens):
        L = []
        for each in range(popsize):
            L += [(evaluateFitness(Population[each],trials,steps),Population[each])]
        LofFitness = []
        for i in range(len(L)):
            LofFitness += [L[i][0]]
        averageFit = sum(LofFitness)/popsize
        maxFit = max(LofFitness)
        print('Generation',gen)
        print('Average fitness:', averageFit)
        print('Best fitness:', maxFit)
        SL = sorted(L)
        SL = SL[-20:]  
        SL = [ x[1] for x in SL ] 
        nextPop = []
        for i in range(len(SL)):
            nextPop += [SL[i]] 
        for newchild in range(180):
            Parent1 = random.choice(SL)
            Parent2 = random.choice(SL)
            offspring = Parent1.crossover(Parent2)
            mut = random.randint(1,100)
            if mut <= mutationRate:
                offspring.mutate()
            nextPop += [offspring]
        Population = nextPop[:]
        nameofFile = "gen" + str(gen) + ".txt"
        # saveToFile(nameofFile, SL[-1])
    return SL[-1]

def saveToFile( filename, p ):
   """ saves the data from Program p
       to a file named filename """
   f = open( filename, "w" )
   print >> f, p  # prints Picobot program from __repr__
   f.close()