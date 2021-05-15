from kivy.app import App

from kivy.uix.scatter import Scatter
from kivy.uix.label import Label
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.textinput import TextInput
from kivy.uix.boxlayout import BoxLayout
from kivy.graphics.vertex_instructions import (Rectangle, Ellipse, Line)
from kivy.graphics.context_instructions import Color
from kivy.core.window import Window
from kivy.config import Config
from kivy.animation import Animation
from kivy.clock import Clock
import random
from Path import Path
from MinPQ import PriorityQueue

WIDTH, HEIGHT = 900, 900
COLOR_LIGHTBLUE = (30 / 255, 130 / 255, 230 / 255)
COLOR_BLUE = (30 / 255, 30 / 255, 230 / 255)
COLOR_BLACK = (0, 0, 0)
COLOR_RED = (1, 0, 0)
COLOR_WHITE = (1, 1, 1)
n = 20


class ScatterTextWidget(BoxLayout):
    def __init__(self, **kwargs):
        super(ScatterTextWidget, self).__init__(**kwargs)
        self.event = None
        self.drawMode = False
        self.label = None
        self.sol = None
        self.squareSize = None
        self.path = None
        self.grid = None
        self.topUILabel = self.ids['topUI']
        self.counter = 0

    def changeTextColor(self, *args):
        color = [random.random() for i in range(3)] + [1]
        label = self.ids['topUI']
        label.color = color

    def refreshClicked(self, **kwargs):
        Clock.unschedule(self.event)
        # self.canvas.clear()
        self.counter = 0
        self.path = Path(n)
        self.grid = self.path.getGrid()
        self.label = self.ids['rLayout']
        self.squareSize = self.label.size[1] / n
        self.drawGrid(self.grid.getGrid())
        self.sol = self.path.solution()
        self.event = Clock.schedule_interval(self.pathSearch, 0.02)

    def drawGridClicked(self, **kwargs):
        self.path = Path(n, blankGrid=True)
        self.label = self.ids['rLayout']
        self.squareSize = self.label.size[1] / n
        #self.path.blankGrid()
        self.grid = self.path.getGrid()
        self.drawGrid(self.grid.getGrid())
        self.sol = self.path.solution()
        self.drawMode = True


    def on_touch_down(self, touch):
        if not self.drawMode:
            super(ScatterTextWidget, self).on_touch_down(touch)
            return
        Clock.unschedule(self.event)
        pos = touch.ox, touch.oy
        print(pos)
        x, y = int(pos[0] / self.squareSize), int((pos[1] - self.label.y) / self.squareSize)
        print("(" + str(x) + ', ' + str(y) + ")")
        if 0 < x < self.squareSize * n and 0 < y < self.squareSize * n:
            self.path.setClosed(x, y)
            self.drawGrid(self.grid.getGrid())

        super(ScatterTextWidget, self).on_touch_down(touch)

    def on_touch_move(self, touch):
        if not self.drawMode:
            super(ScatterTextWidget, self).on_touch_move(touch)
            return
        Clock.unschedule(self.event)
        pos = touch.pos
        # print(pos)
        x, y = int(pos[0] / self.squareSize), int((pos[1] - self.label.y) / self.squareSize)
        print("(" + str(x) + ', ' + str(y) + ")")
        if 0 <= x < self.squareSize * n and 0 <= y < self.squareSize * n:
            self.path.setClosed(x, y)
            self.drawSquare(x=x * self.squareSize, y=y * self.squareSize + self.label.y, size=self.squareSize - 1,
                            color=COLOR_BLACK)
        super(ScatterTextWidget, self).on_touch_move(touch)

    def startSearch(self):
        Clock.unschedule(self.event)
        self.event = Clock.schedule_interval(self.pathSearch, 0.02)

    def pathSearch(self, *args):
        if self.path.found:
            Clock.unschedule(self.event)
            self.drawMode = False
            #del self.grid
            #del self.path
            return
        if self.grid != self.path.grid.getGrid():
            self.grid = self.path.grid.getGrid()
            self.counter = 0
            self.drawGrid(self.grid)
        for c in self.sol:
            self.drawSquare(x=c.x * self.squareSize, y=c.y * self.squareSize + self.label.y, size=self.squareSize - 1,
                            color=COLOR_WHITE)
        self.path.runSearch()
        self.sol = self.path.solution()
        for c in self.sol:
            self.drawSquare(x=c.x * self.squareSize, y=c.y * self.squareSize + self.label.y, size=self.squareSize - 1,
                            color=COLOR_LIGHTBLUE)
        self.topUILabel.text = 'Paths searched: ' + str(self.counter)
        self.counter += 1

    def drawLine(self, x1, y1, x2, y2, width, **kwargs):

        with self.canvas:
            Line(points=[x1, y1, x2, y2], width=width)

    def drawSquare(self, x, y, size, color, **kwargs):

        with self.canvas:
            Color(*color)
            Rectangle(pos=(x, y), size=(size, size))

    def drawGrid(self, grid):
        print('drew grid')
        i = 0
        for x in grid:
            j = 0
            for y in grid[i]:
                if grid[i][j] == 3:
                    self.drawSquare(x=i * self.squareSize, y=j * self.squareSize + self.label.y,
                                    size=self.squareSize - 1, color=COLOR_RED)
                elif grid[i][j] == 2:
                    self.drawSquare(x=i * self.squareSize, y=j * self.squareSize + self.label.y,
                                    size=self.squareSize - 1, color=COLOR_LIGHTBLUE)
                elif grid[i][j] == 1:
                    self.drawSquare(x=i * self.squareSize, y=j * self.squareSize + self.label.y,
                                    size=self.squareSize - 1, color=COLOR_WHITE)
                else:
                    self.drawSquare(x=i * self.squareSize, y=j * self.squareSize + self.label.y,
                                    size=self.squareSize - 1, color=COLOR_BLACK)
                j += 1
            i += 1


class PathfindingApp(App):
    def build(self):
        return ScatterTextWidget()


if __name__ == "__main__":
    Config.set('graphics', 'resizable', False)
    Window.size = (900, 900)
    PathfindingApp().run()
