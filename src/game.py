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

class GUIButton:
    buttonObj = None
    text = ""
    textPos = Point(0, 0)

    def __init__(self, pos, size, onclick, uiFactory,
                 text="",
                 textPos=Point(0, 0),
                 color=sdl2.ext.Color(255,255,255),
                 textColor=sdl2.ext.Color(0,0,0)):
        """
        Create a new GUI button object
        """
        self.buttonObj = uiFactory.from_color(sdl2.ext.CHECKBUTTON,
                                         color,
                                         size=(size.x, size.y))
        self.buttonObj.click += onclick
        self.buttonObj.position = (pos.x, pos.y)
        self.text = text
        self.textPos = pos + textPos

    def draw(self, renderer):
        """
        Draws the button.
        """
        renderer.spriteRenderer.render(self.buttonObj)
        renderer.draw_text(self.textPos.x, self.textPos.y, self.text)

class Game:
    renderer = None
    uiFactory = None
    uiProcessor = None
    buttons = []
    level = None
    hasWon = False
    hasLost = False
    paused = False

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
        self.buttons.append(GUIButton(Point(10, 10),
                                      Point(150, 50),
                                      onclick_quit,
                                      self.uiFactory,
                                      text="Quit",
                                      textPos=Point(50, 10),
                                      color=sdl2.ext.Color(255, 0, 0)))

        # Create button for running code
        def onclick_runcode(button, event):
            pass#TODO: run player code
        self.buttons.append(GUIButton(Point(170, 10),
                                      Point(150, 50),
                                      onclick_runcode,
                                      self.uiFactory,
                                      text="Run Code",
                                      textPos=Point(20, 10),
                                      color=sdl2.ext.Color(0, 255, 0)))

        # Create pause button
        def onclick_pause(button, event):
            self.paused = not self.paused
        self.buttons.append(GUIButton(Point(330, 10),
                                      Point(150, 50),
                                      onclick_pause,
                                      self.uiFactory,
                                      text="Pause",
                                      textPos=Point(40, 10),
                                      color=sdl2.ext.Color(0, 0, 255)))

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
        self.renderer.clearScreen()
        winSize = self.renderer.render_window.size
        self.renderer.render_context.fill((0, 70, winSize[0], 10),
                                          color=sdl2.ext.Color(255, 255, 255))
        self.renderer.render_level(self.level,
                                   Point(0, 90),
                                   Point(winSize[0], winSize[1]-90))
        for b in self.buttons:
            b.draw(self.renderer)

        if self.paused:
            self.renderer.draw_textWithOutline(200, 250, "Paused", size=150)
        if self.hasWon:
            self.renderer.draw_textWithOutline(150, 250, "Youre Winner!", size=100)
        elif self.hasLost:
            self.renderer.draw_textWithOutline(70, 225, "Youre a Disgrace", size=100)
            self.renderer.draw_textWithOutline(120, 325, "to Your Family", size=100)

    def startGame(self, level_file, code_file):
        """
        Initiates the main game loop.
        """
        self.hasWon = False
        self.hasLost = False
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
                buttonObjs = [b.buttonObj for b in self.buttons]
                self.uiProcessor.dispatch(buttonObjs, e)
            if not (self.hasWon or self.hasLost or self.paused):
                status = self.updateEntities()
                if status == "win":
                    self.hasWon = True
                elif status == "lose":
                    self.hasLost = True
            time.sleep(0.5)
            self.draw()

    def updateEntities(self):
        master_state_i = None
        potential_states = [None] * len(self.timeline)
        old_state = self.timeline.states[-1]
        new_state = copy.deepcopy(old_state)
        for pos,rob in new_state.entities_pos(Robot):
            new_state.remove(rob,pos)
        for pos,robot in self.timeline.states[-1].entities_pos(Robot):
            action,amount = robot.run(len(self.timeline)-1,new_state,copy.deepcopy(old_state),pos)
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
                    print("Robot is traveling to {} and master is {}".format(amount, robot.master))
            elif action == 'none':
                new_robot = copy.deepcopy(robot)
                new_state.add(new_robot,robot.position(old_state))
            else:
                print("Your program sucks user")
                new_robot = copy.deepcopy(robot)
                new_state.add(new_robot,robot.position(old_state))
                #the robot does nothing

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
                return "win"
                    
        for pos,cell in new_state.cells():
            robots = []
            for ent in cell:
                if isinstance(ent,Robot):
                    robots.append(ent)
            if len(robots) > 1:
                masterDead = False
                for r in robots:
                    if r.master:
                        masterDead = True
                        break
                new_state.destroy(pos)
                if masterDead:
                    print("Your master robot has exploded")
                    return "lose"
                else:
                    print("Your robots have exploded")
        self.level = new_state
        return "continue"
