import render
import sdl2
import sdl2.ext
import time
import copy

import create_level

from classes import * #OH NO ITS THE END OF THE WORLD
from switch import Switch
from point import Point

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
    level = None

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
        self.renderer.render_level(self.level,
                                   Point(0, 90),
                                   Point(winSize[0], winSize[1]-90))
        self.renderer.spriteRenderer.render(self.buttons)
        for posAndText in self.buttons_text:
            self.renderer.draw_text(*posAndText)

    def startGame(self, level_file, code_file):
        """
        Initiates the main game loop.
        """
        with open(code_file, 'r') as f:
            code_string = f.read()
        self.level = create_level.setup_level(level_file, code_string)
        self.timeline = Timeline(self.level)
        self.draw()
        running = True
        while running:
            events = sdl2.ext.get_events()
            for e in events:
                if e.type == sdl2.SDL_QUIT:
                    print("Exiting game...")
                    running = False
                    break
                self.uiProcessor.dispatch(self.buttons, e)
            running &= self.harryPotter()
            time.sleep(1)
            self.draw()

    def harryPotter(self):
        master_state_i = None
        potential_states = [None] * len(self.timeline)
        old_state = self.timeline.states[-1]
        new_state = copy.deepcopy(old_state)
        for pos,rob in new_state.entities_pos(Robot):
            new_state.remove(rob,pos)
            print("length of timeline", len(self.timeline))#DEBUG
        for robot in self.timeline.states[-1].entities(Robot):
            action,amount = robot.run(len(self.timeline)-1)
            if action in directions_to_additions.keys():
                direction = directions_to_additions[action]
                new_pos = robot.position(old_state) + Point(*direction)
                if (new_pos.x >= 0 and new_pos.x < new_state.width and
                    new_pos.y >= 0 and new_pos.y < new_state.height and
                    not new_state.spot_has(new_pos,Wall)):                    
                    new_robot = copy.deepcopy(robot)
                    #new_robot.__level = new_state
                    new_state.add(new_robot,new_pos)
                    if amount is not None:
                        print("WARN: Was told to move, but amount is also set. Possible bug")
                else:
                    new_robot = copy.deepcopy(robot)
                    new_state.add(new_robot,robot.position(old_state))
                    print("WARN: invalid move (into boundry or wall), staying still")                                  
            elif action == 'time':
                if amount >= len(self.timeline): #invalid
                    print("tried to travel to the future(just wait)")
                else:
                    if potential_states[amount] is None:
                        new_state = potential_states[amount] = copy.deepcopy(self.timeline.states[amount])
                        for flbrobot in new_state.entities(Robot):
                            flbrobot.master = False
                        new_state = potential_states[amount]
                        dup_rob = copy.deepcopy(robot)
                        new_state.add(dup_rob,
                                      robot.position(old_state))
                    if robot.master:
                        master_state_i = amount
            elif action == 'none':
                new_robot = copy.deepcopy(robot)
                new_state.add(new_robot,robot.position(old_state))
            else:
                print("Your program sucks user")
                new_robot = copy.deepcopy(robot)
                new_state.add(new_robot,robot.position(old_state))
                #the robot does nothing

        print("END OF FOR")#DEBUG
        print("master_state_i", master_state_i)
        if master_state_i is not None:                
            master_state = potential_states[master_state_i]
            #The master robot has traveled back in time
            if master_state_i > 0: 
                self.timeline = self.timeline.previous_state(master_state-1)
                self.timeline.add_state(master_state)
            else:
                #Back to the beginning
                self.timeline = Timeline(master_state)
        else:
            #No time travel
            self.timeline.add_state(new_state)
            new_state = self.timeline.states[-1]
            #^sets new state again in case time travel happenend
        all_buttons_pressed = True
        for pos,ent in new_state.entities_pos(Button):
            all_buttons_pressed &= new_state.spot_has(pos,Robot)
        if all_buttons_pressed: #Oh man!
            master_on_exit = False
            for pos,ent in new_state.entities_pos(ExitDoor):
                if new_state.spot_has(pos,Robot):
                    master_on_exit = True                     
                    break
            if master_on_exit: #YOU WIN
                print("YOU'RE WINNER!")
                return False
                    
        for pos,cell in new_state.cells():
            count_robots = 0
            for ent in cell:
                if isinstance(ent,Robot):
                    count_robots += 1
            if count_robots > 1:
                new_state.destroy(pos)
                print("Your robots have exploded")
        self.level = new_state
        for pos,robot in new_state.entities_pos(Robot):
            print("a robot position: {},{}".format(pos.x,pos.y)) #DEBUG
        return True
