import sdl2
import sdl2.ext
import ctypes
import sys

from level import Level
from entity import Entity
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

        self.render_context.draw_rect((0, 0, w, h), sdl2.ext.Color(0, 0, 0, 0))

        self.spriteFactory = sdl2.ext.SpriteFactory(sdl2.ext.TEXTURE,
            renderer=self.render_context)

        self.spriteRenderer = self.spriteFactory.create_sprite_render_system(self.render_window)
        self.fontManager = sdl2.ext.FontManager("lib/square-deal.ttf",
                                           size=32,
                                           color=sdl2.ext.Color(255, 255, 255))

    def render_level(self, level):
        """
        A 2D level of symbols to render,
        indexed Y first, ala level[y][x]
        """
        level_texture = sdl2.SDL_CreateTexture(self.render_context.renderer,
            sdl2.SDL_PIXELFORMAT_RGB24, sdl2.SDL_TEXTUREACCESS_TARGET,
            5 * level.width - 1, 5 * level.height - 1)

        old_target = self.render_context.rendertarget

        sdl2.SDL_SetRenderTarget(self.render_context.renderer, level_texture)

        temp_rect = sdl2.SDL_Rect(x = 0, y = 0, w = 4, h = 4)

        for point, stack in level.cells():
            if not stack:
                # Light gray
                temp_color = sdl2.SDL_SetRenderDrawColor(
                    self.render_context.renderer, ctypes.c_ubyte(0xb0),
                    ctypes.c_ubyte(0xb0), ctypes.c_ubyte(0xb0), ctypes.c_ubyte(0))
            elif isinstance(stack[0], Robot):
                # Green
                temp_color = sdl2.SDL_SetRenderDrawColor(
                    self.render_context.renderer, ctypes.c_ubyte(0),
                    ctypes.c_ubyte(0xff), ctypes.c_ubyte(0), ctypes.c_ubyte(0))
            elif isinstance(stack[0], Button):
                # Red... (dark pink)
                temp_color = sdl2.SDL_SetRenderDrawColor(
                    self.render_context.renderer, ctypes.c_ubyte(0xff),
                    ctypes.c_ubyte(0), ctypes.c_ubyte(0), ctypes.c_ubyte(0))
            elif isinstance(stack[0], ExitDoor):
                # Orange
                temp_color = sdl2.SDL_SetRenderDrawColor(
                    self.render_context.renderer, ctypes.c_ubyte(0xff),
                    ctypes.c_ubyte(0x8c), ctypes.c_ubyte(0), ctypes.c_ubyte(0))

            temp_rect.x = point.x * 5;
            temp_rect.y = point.y * 5;
            sdl2.SDL_RenderDrawRect(self.render_context.renderer,
                ctypes.byref(temp_rect))

        sdl2.SDL_SetRenderTarget(self.render_context.renderer,
            ctypes.byref(old_target))

        temp_rect.x = 0; temp_rect.y = 0; temp_rect.w = 400; temp_rect.h = 400;

        sdl2.SDL_RenderCopy(self.render_context.renderer,
            ctypes.byref(level_texture), None, ctypes.byref(temp_rect))
        """
        textureSprite = self.spriteFactory.create_texture_sprite(
            self.render_context, (5 * level.width - 1, 5 * level.height - 1),
            pformat=sdl2.SDL_PIXELFORMAT_RGB24,
            access=sdl2.SDL_TEXTUREACCESS_TARGET)
        textureSprite.texture = level_texture
        self.spriteRenderer.render(textureSprite)
        """

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
