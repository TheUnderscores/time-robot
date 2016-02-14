import render
import sdl2
import sdl2.ext

class Game:
    renderer = None
    uiFactory = None
    uiProcessor = None
    spriteRenderer = None#TODO: move to render.Renderer
    buttons = []

    def __init__(self):
        """
        Initializes the game.
        """
        self.renderer = render.Renderer("Time Robot", 800, 600)#TODO: window and render flags
        self.uiFactory = sdl2.ext.UIFactory(self.renderer.spriteFactory)
        self.uiProcessor = sdl2.ext.UIProcessor()
        self.spriteRenderer = self.renderer.spriteFactory.create_sprite_render_system(self.renderer.render_window)

        # Create quit button
        def onclick_quit(button, event):
            print("HERE")
            self.quitGame()
            print("LOL")

        self.createButton(0, 0, 50, 50, onclick_quit, "Quit", color=sdl2.ext.Color(255, 0, 0))
        

    def quitGame(self):
        """
        Halts game loop.
        """
        quitEvent = sdl2.SDL_Event(sdl2.SDL_QUIT)
        sdl2.SDL_PushEvent(quitEvent)

    def createButton(self, x, y, w, h, onclick, text="", color=sdl2.ext.Color(0,0,0)):
        """
        Creates a button that can be clicked by the mouse.
        """
        newButton = self.uiFactory.from_color(sdl2.ext.CHECKBUTTON,
                                              color,
                                              size=(w, h))
        newButton.click += onclick
        self.buttons.append(newButton)

    def startGame(self):
        """
        Initiates the main game loop.
        """
        running = True
        while running:
            events = sdl2.ext.get_events()
            for e in events:
                if e.type == sdl2.SDL_QUIT:
                    print("QUIT")
                    running = False
                    break
                self.uiProcessor.dispatch(self.buttons, e)
            self.renderer.render_board(None)#TODO: get board
            self.spriteRenderer.render(self.buttons)
