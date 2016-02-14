import sdl2
import sdl2.ext
import sys

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

    def render_level(self, board):
        """
        A 2D board of symbols to render,
        indexed Y first, ala board[y][x]
        """
        pass

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
