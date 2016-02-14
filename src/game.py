import render
import sdl2
import sdl2.ext
import time
import copy

from classes import * #OH NO ITS THE END OF THE WORLD
from switch import Switch
from point import Point

directions_to_additions = {
    'up':    (0,-1),
    'down':  (0,1),
    'left':  (-1,0),
    'right': (1,0)}

import test_level

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
        self.createButton(Point(10, 10), Point(150, 50),
                          onclick_quit,
                          "Quit", Point(50, 10),
                          color=sdl2.ext.Color(255, 0, 0))

        # Create button for running code
        def onclick_runcode(button, event):
            pass#TODO: run player code
        self.createButton(Point(170, 10), Point(150, 50),
                          onclick_runcode,
                          "Run Code", Point(20, 10),
                          color=sdl2.ext.Color(0, 255, 0))

    def quitGame(self):
        """
        Halts game loop.
        """
        quitEvent = sdl2.SDL_Event(sdl2.SDL_QUIT)
        sdl2.SDL_PushEvent(quitEvent)

    def createButton(self, pos, size, onclick,
                     text="", posText=Point(0, 0), color=sdl2.ext.Color(0,0,0)):
        """
        Creates a button that can be clicked by the mouse.
        pos     -- position of button
        posText -- position of text relative to position of button
        """
        newButton = self.uiFactory.from_color(sdl2.ext.CHECKBUTTON,
                                              color,
                                              size=(size.x, size.y))
        newButton.click += onclick
        newButton.position = (pos.x, pos.y)
        self.buttons.append(newButton)
        posText = pos + posText
        self.buttons_text.append((posText.x, posText.y, text))

    def draw(self):
        """
        Draws game elements.
        """
        winSize = self.renderer.render_window.size
        self.renderer.render_context.fill((0, 0, winSize[0], winSize[1]),
                                          color=sdl2.ext.Color(0, 0, 0))
        self.renderer.render_context.fill((0, 70, winSize[0], 10),
                                          color=sdl2.ext.Color(255, 255, 255))
        self.renderer.render_level(test_level.starting_level,
                                   Point(0, 90),
                                   Point(winSize[0], winSize[1]-90))
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
        robot = Robot(None) #TODO: Pass arguments to this
        starting_level.add(button1,Point(3,3))
        starting_level.add(button2,Point(6,3))
        starting_level.add(robot,Point(6,6))
        timeline = Timeline(starting_level)
        running = True
        foo = 0 #DEBUG
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
