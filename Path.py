import random

from Grid import Grid
from MinPQ import PriorityQueue


# Using the A* Algorithm, searches an nxn grid with open and closed cells and attempts to find the shortest path
# between the two points.
class Path:
    class Node:
        def __init__(self, c, moves, prev, start, goal):
            self.c = c
            self.moves = moves
            self.prev = prev
            self.priority = c.manhattan(start, goal) + moves

        def __eq__(self, other):  # Comparators for sorting different paths.
            if self.priority == other.priority:
                return True
            else:
                return False
        def __lt__(self, other):
            if self.priority <= other.priority:
                return True
            else:
                return False

        def __gt__(self, other):
            if self.priority >= other.priority:
                return True
            else:
                return False

    def __init__(self, N, blankGrid=False):
        # PQ for sorting different paths.
        self.pq = PriorityQueue()
        self.n = N
        self.closedSet = []
        # Initialize and reset Grid.
        if blankGrid:
            self.grid = Grid(N, 0)
        else:
            self.grid = Grid(N)

        self.resetSearch()
        self.found = False

    # Sets a new goal, randomly. Gets the starting cell from the Grid class. Adds the start cell to the PQ to set up
    # the searching algorithm.
    def resetSearch(self):
        goalX = random.randint(0, self.n - 1)
        goalY = random.randint(0, self.n - 1)
        self.grid.gridReset()
        goalCell = self.grid.getGoal()
        startCell = self.grid.getCell(goalX, goalY)
        # Make sure the goal Cell is at least open.
        self.grid.setClosed(goalX, goalY, False)
        # Initialize a new PQ.
        self.pq = PriorityQueue()
        # Make a new Node at that startCell and add that to the PQ.
        newNode = self.Node(startCell, 0, None, startCell, goalCell)
        self.pq.put(newNode)
        self.closedSet = [newNode.c]
    def blankGrid(self):
        self.grid = Grid(self.n, openChance=0.0)
        self.resetSearch()
        goalCell = self.grid.getCell(self.n - 1, self.n - 1)
        self.pq = PriorityQueue()

        newNode = self.Node(self.grid.getCell(0, 0), 0, None, self.grid.getCell(0, 0), goalCell)
        self.pq.put(newNode)
        self.closedSet = [newNode.c]

    def setClosed(self, x, y, isOpen=False):
        self.grid.setClosed(x, y, isOpen)


    # Runs a single iteration of the A* Algorithm. To find a path immediately, loop through this function. This is
    # split by iteration for visualization purposes.
    def search(self):
        goalCell = self.grid.getGoal()
        searchNode = self.pq.get()
        neighbors = searchNode.c.neighbors()
        for c in neighbors:
            # If the current cell is not the start cell(previous is None) and the cell is not the same as the
            # previous cell( c == searchNode.prev.c), or the cell is not Open, skip iteration without adding to the PQ
            if (searchNode.prev is not None and c == searchNode.prev.c) or not c.isOpen():
                continue
            # If the searchNode cell has a better priority(lower, in this case) than the neighbor that is being
            # searched, skip iteration without adding to the PQ
            #if searchNode.priority < c.manhattan(c, goalCell) + searchNode.moves:
             #   continue
            # Add the neighbor Node to the PQ if it fails the checks above, meaning it is possible it is part of the
            # quickest path.
            if c in self.closedSet:
                continue
            newNode = self.Node(c, searchNode.moves + 1, searchNode, c, goalCell)
            self.pq.put(newNode)
            self.closedSet.append(newNode.c)
    # Adds the current PQ to an array, using Node.prev to navigate back to the beginning of the list, where Node.prev is
    # None.
    def solution(self):
        solution = []
        goal = self.pq.peek()
        while goal is not None:
            solution.append(goal.c)
            goal = goal.prev
        return solution

    def getGrid(self):
        return self.grid
# Use this to iterate through the A* Algorithm. Runs necessary checks and iterates once through the algorithm.
    def runSearch(self):
        # If the size of the PQ is empty, the alg was unable to find a path in the given grid, resulting in a reset
        # of the search.
        if self.pq.size() == 0:
            self.resetSearch()
            return
        # If the best option in the PQ is the goal, we've found the goal. found is used externally to know when to
        # stop seraching.
        if self.pq.peek().c.isGoal:
            self.found = True
            return
        # If the size is not 0, and we still haven't found the goal, run an interation of the A* algorithm.
        self.search()
