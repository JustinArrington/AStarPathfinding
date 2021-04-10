from kivy.app import App

from kivy.uix.scatter import Scatter
from kivy.uix.label import Label
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.textinput import TextInput
from kivy.uix.boxlayout import BoxLayout
from kivy.graphics.vertex_instructions import (Rectangle, Ellipse, Line)
from kivy.graphics.context_instructions import Color
from kivy.core.window import Window
from kivy.animation import Animation
from kivy.clock import Clock
import random

WIDTH, HEIGHT = 900, 900
COLOR_LIGHTBLUE = (30 / 255, 130 / 255, 230 / 255)
COLOR_BLUE = (30 / 255, 30 / 255, 230 / 255)
COLOR_BLACK = (0, 0, 0)
COLOR_RED = (1, 0, 0)
COLOR_WHITE = (1, 1, 1)
n = 15

class ScatterTextWidget(BoxLayout):
    def __init__(self, **kwargs):
        super(ScatterTextWidget, self).__init__(**kwargs)
        self.event = None
        self.label = None
        self.sol = None
        self.squareSize = None
        self.path = None
        self.grid = None

    def changeTextColor(self, *args):
        color = [random.random() for i in range(3)] + [1]
        label = self.ids['topUI']
        label.color = color

    def drawLine(self, x1, y1, x2, y2, width, **kwargs):

        with self.canvas:
            Line(points=[x1, y1, x2, y2], width=width)

    def drawSquare(self, x, y, size, color, **kwargs):

        with self.canvas:
            Color(*color)
            Rectangle(pos=(x, y), size=(size, size))


class SliderApp(App):
    def build(self):
        return ScatterTextWidget()


if __name__ == "__main__":
    Window.size = (900, 1100)
    SliderApp().run()