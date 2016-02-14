import sdl2

class Renderer():
    render_window = None
    render_context = None

    def __init__(self, title, w, h, win_flags, render_flags):
        """Initializes the window and render context"""
        self.render_window = sdl2.SDL_CreateWindow(title.encode(),
            sdl2.WINDOW_POS_CENTERED, sdl2.WINDOW_POS_CENTERED, w, h, win_flags)
        self.render_context = sdl2.SDL_CreateRenderer(self.render_window, -1,
            render_flags)

    def render_board(self, board):
        """
        A 2D board of symbols to render,
        indexed Y first, ala board[y][x]
        """
        pass

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
        """Renderer object destructor"""
        sdl2.SDL_DestroyRenderer(self.render_context)
        sdl2.SDL_DestoryWindow(self.render_window)
