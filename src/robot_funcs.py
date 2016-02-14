def move_up(robot):
	governor.action = 'up'

def move_down(robot):
	governor.action = 'down'

def move_left(robot):
	governor.action = 'left'

def move_right(robot):
	governor.action = 'right'

def reverse_time(ticks):
	governor.action = 'time'
        governor.time_tick = current_tick - ticks

def set_time(tick):
	governor.action = 'time'
        governor.time_tick = tick
