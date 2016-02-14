import sdl2
import sdl2.ext
import ctypes
import sys

from level import Level
from entity import Entity
from point import Point
from robot import Robot
from button import Button
from exitdoor import ExitDoor

class Renderer():
    render_window = None
    render_context = None
    spriteFactory = None
    spriteRenderer = None
    fontManager = None

    def __init__(self, title, w, h, win_flags = 0, render_flags = 0):
        """Initializes the window and render context"""
        self.render_window = sdl2.ext.Window(title, size=(w, h))
        self.render_window.show()

        self.render_context = sdl2.ext.Renderer(self.render_window)

        self.render_context.fill((0, 0, w, h), sdl2.ext.Color(0, 0, 0, 255))

        self.spriteFactory = sdl2.ext.SpriteFactory(sdl2.ext.TEXTURE,
            renderer=self.render_context)

        self.spriteRenderer = self.spriteFactory.create_sprite_render_system(self.render_window)
        self.fontManager = sdl2.ext.FontManager("lib/square-deal.ttf",
                                           size=32,
                                           color=sdl2.ext.Color(255, 255, 255))

    def clearScreen(self, bgcolor=sdl2.ext.Color(0, 0, 0)):
        """
        Color's entire screen in one color (black by default).
        """
        winSize = self.render_window.size
        self.render_context.fill((0, 0, winSize[0], winSize[1]),
                                 color=bgcolor)

    def render_level(self, level, pos, size):
        """
        A 2D level of symbols to render,
        indexed Y first, ala level[y][x].
        pos and size are Point objects.
        """
        lvlSize = Point(level.width, level.height)
        scale = size // lvlSize
        blockSize = scale - (scale // 10)
        for point, stack in level.cells():
            point = (point * scale) + pos
            rect = (point.x, point.y, blockSize.x, blockSize.y)

            if not stack:
                # Light gray
                self.render_context.fill(rect,
                                         color=sdl2.ext.Color(176, 176, 176))
            else:
                ent = stack[len(stack)-1]
                if isinstance(ent, Robot):
                    # Green
                    self.render_context.fill(rect,
                                             color=sdl2.ext.Color(0, 255, 0))
                elif isinstance(ent, Button):
                    # Red... (dark pink)
                    self.render_context.fill(rect,
                                             color=sdl2.ext.Color(255, 0, 0))
                elif isinstance(ent, ExitDoor):
                    # Orange
                    self.render_context.fill(rect,
                                             color=sdl2.ext.Color(255, 140, 0))

    def draw_text(self, x, y, text, color=sdl2.ext.Color(0,0,0)):
        """
        Creates text to render.
        """
        textSprite = self.spriteFactory.from_text(text,
                                                  fontmanager=self.fontManager,
                                                  color=color)
        textSprite.position = (x, y)
        self.spriteRenderer.render(textSprite)

    def draw_text_box(self, x, y, w, h, text):
        """
        Creates a text box to provide player information in text form.
        Caller is responsible for making sure that the provided text
        is small enough to fit within the text box (less that `w` x `h`
        characters)
        """
        pass

    def add_status_text(self, text):
        """
        Add text to global status text box.
        """
        pass

    def __del__(self):
        self.fontManager.close()
