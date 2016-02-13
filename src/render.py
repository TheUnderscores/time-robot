def render_board(board):
    """
    A 2D board of symbols to render,
    indexed Y first, ala board[y][x]
    """
    pass

def create_button(x, y, w, h, text, on_click):
    """
    Creates an on screen button, at (X, Y) on the screen that is
    `w` x `h`, containing the text `text`, and provided call-back
    in `on_click`
    """
    pass

def draw_text_box(x, y, w, h, text):
    """
    Creates a text box to provide player information in text form.
    Caller is responsible for making sure that the provided text
    is small enough to fit within the text box (less that `w` x `h`
    characters)
    """
    pass
