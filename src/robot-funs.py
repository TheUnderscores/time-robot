def move_up(robot):
	govenor.action = 'up'

def move_down(robot):
	govenor.action = 'down'

def move_left(robot):
	govenor.action = 'left'

def move_right(robot):
	govenor.action = 'right'

def reverse_time(ticks):
	govenor.action = 'time'
        govenor.time_tick = current_tick - ticks

def set_time(tick):
	govenor.action = 'time'
        govenor.time_tick = tick
