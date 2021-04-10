import random


class Grid:
    class Cell:
        # Creates a new Cell, requiring current (x,y), if the Cell is open, n size in the nxn grid, and a reference
        # to the Grid that is creating the Cell
        def __init__(self, isOpen, x, y, N, outer_instance):
            self.open = isOpen
            self.x = x
            self.y = y
            self.n = N
            self.isGoal = False
            self.isPath = False
            self.outer_instance = outer_instance

        # Function to find distance between two Cells.
        def manhattan(self, start, goal):
            return abs(goal.x - self.x) + abs(goal.y - self.y) - abs(start.x - self.x) - abs(start.y - self.y)

        def isOpen(self):
            return self.open

        def setOpen(self, toSet):
            self.open = toSet

        def openPath(self):
            self.isPath = True

        # Uses simple arithmetic to find if there is a Cell above, below, or on the right or left. Returns those
        # cells if they exist.
        def neighbors(self):
            array = []
            if self.x > 0:
                array.append(self.outer_instance.grid[self.x - 1][self.y])
            if self.x < self.n - 1:
                array.append(self.outer_instance.grid[self.x + 1][self.y])
            if self.y > 0:
                array.append(self.outer_instance.grid[self.x][self.y - 1])
            if self.y < self.n - 1:
                array.append(self.outer_instance.grid[self.x][self.y + 1])
            return array

        # Helper toString function for debugging.
        def __str__(self):
            return "open: " + str(self.open) + " x: " + str(self.x) + " y: " + str(self.y)

    # Creates an empty array, sets n in the nxn array, and initailizes some variables.
    def __init__(self, n):
        self.grid = [[]]
        self.n = n
        self.goalX = None
        self.goalY = None

    # Resets the grid, finding a new goalCell, and reinitializing the grid itself. Sets goalCell isGoal to True,
    # and opens it.
    def gridReset(self):
        self.goalX = random.randint(0, self.n - 1)
        self.goalY = random.randint(0, self.n - 1)
        print("New goal: ", self.goalX, self.goalY)
        self.grid = [[self.Cell(random.random() > .15, y, x, self.n, self)
                      for x in range(self.n)] for y in range(self.n)]
        self.grid[self.goalX][self.goalY].isGoal = True
        self.grid[self.goalX][self.goalY].open = True

    # Returns Cell at (x,y)
    def getCell(self, x, y):
        return self.grid[x][y]

    # Returns Cell at goal.
    def getGoal(self):
        return self.grid[self.goalX][self.goalY]

    # Returns the grid, reformatted, using 3 for the goalCell, 1 if the Cell is simply Open, and 0 otherwise.
    def getGrid(self):
        copy = [[0 for x in range(self.n)] for y in range(self.n)]
        for x in range(self.n):
            for y in range(self.n):
                if self.grid[x][y].isGoal:
                    copy[x][y] = 3
                elif self.grid[x][y].isOpen():
                    copy[x][y] = 1
                else:
                    copy[x][y] = 0
        return copy


if __name__ == '__main__':
    grid = Grid(5)
    grid.gridReset()
    print(*(grid.Cell(True, 4, 3, 5, grid).neighbors()), sep='\n')
