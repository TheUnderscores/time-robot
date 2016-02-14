governor['action'] = 'up'
if step%3 == 2:
    governor['action'] = 'time'
    governor['time_tick'] = 0

