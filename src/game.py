import render
import sdl2
import sdl2.ext
import time
import copy

from classes import * #OH NO ITS THE END OF THE WORLD
from switch import Switch

directions_to_additions = {
    'up':    (0,-1),
    'down':  (0,1),
    'left':  (-1,0),
    'right': (1,0)}

class Game:
    renderer = None
    uiFactory = None
    uiProcessor = None
    buttons = []
    buttons_text = []

    def __init__(self):
        """
        Initializes the game.
        """
        self.renderer = render.Renderer("Time Robot", 800, 600)#TODO: window and render flags
        self.uiFactory = sdl2.ext.UIFactory(self.renderer.spriteFactory)
        self.uiProcessor = sdl2.ext.UIProcessor()

        # Create quit button
        def onclick_quit(button, event):
            self.quitGame()

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
        self.buttons_text.append((x, y, text))

    def draw(self):
        """
        Draws game elements.
        """
        self.renderer.render_board(None)#TODO: get board
        self.renderer.spriteRenderer.render(self.buttons)
        for posAndText in self.buttons_text:
            self.renderer.draw_text(*posAndText)

    def startGame(self):
        """
        Initiates the main game loop.
        """
        starting_level = Level()
        button1 = Button(starting_level)
        button2 = Button(starting_level)
        robot = Robot() #TODO: Pass arguments to this
        starting_level.add(button1,Point(3,3))
        starting_level.add(button2,Point(6,3))
        starting_level.add(robot,Point(6,6))
        timeline = Timeline(starting_level)
        running = True
        while running:
            events = sdl2.ext.get_events()
            for e in events:
                if e.type == sdl2.SDL_QUIT:
                    print("Exiting game...")
                    running = False
                    break
                self.uiProcessor.dispatch(self.buttons, e)
            new_state = copy.deepcopy(timeline.states[-1])
            for robot in new_state.entities(Robot):
                action,amount = robot.run(new_state,
                                          timeline.states.length-1)
                p = None

            self.draw()
