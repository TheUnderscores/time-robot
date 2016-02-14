import render
import sdl2
import sdl2.ext
import time
import copy

from classes import * #OH NO ITS THE END OF THE WORLD
from switch import Switch
import test_level
import time

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
        self.renderer.render_level(test_level.starting_level)#TODO: get board
        self.renderer.spriteRenderer.render(self.buttons)
        for posAndText in self.buttons_text:
            self.renderer.draw_text(*posAndText)

    def startGame(self, code_string):
        """
        Initiates the main game loop.
        """
        starting_level = Level()
        button1 = Button(starting_level)
        button2 = Button(starting_level)
        robot = Robot(starting_level,code_string)
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
            master_state_i = None
            potential_states = [None for i in range(len(timeline))]
            new_state = copy.deepcopy(timeline.states[-1])
            for robot in new_state.entities(Robot):
                action,amount = robot.run(new_state,
                                          timeline.states.length-1)
                if action in directions_to_additions.keys():
                    direction = directions_to_additions[action]
                    new_pos = robot.position + direction
                    new_state.move(robot,new_pos)
                    if amount is not None:
                        pass #TODO: warn the user about this    
                elif action == 'time':
                    if amount >= len(timeline): #invalid
                        pass #TODO: Warn user
                    else:
                        if potential_states[amount] is None:
                            new_state = potential_states[amount] = copy.deep_copy(timeline.states[amount])
                            for robot in new_state.entities(Robot):
                                robot.master = False
                        new_state = potential_states[amount]
                        dup_rob = copy.deep_copy(robot)
                        dup_rob.level = new_state
                        new_state.add(dup_rob,
                                      robot.position)
                        if robot.master:
                            master_state_i = amount
                elif action == 'none':
                    pass #explicitly stay in the same spot    
                else:
                    pass
                    #Tell the user their program sucks;
                    #the robot does nothing
            if master_state_i is not None:                
                master_state = potential_states[master_state_i]
                #The master robot has traveled back in time
                if master_state_i > 0: 
                    timeline = timeline.previous_state(master_state-1)
                    timeline.add_state(master_state)
                else:
                    #Back to the beginning
                    timeline = Timeline(master_state)
            else:
                #No time travel
                timeline.add_state(new_state)
            new_state = timeline.states[-1]
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
                    running = False
            
            for pos,cell in new_state.cells():
                count_robots = 0
                for ent in cell:
                    if isinstance(ent,Robot):
                        count_robots += 1
                if count_robots > 1:
                    new_state.destroy(pos)
                    #TODO: tell user that their robots have exploded
                    pass
            time.sleep(1)
            self.draw()
