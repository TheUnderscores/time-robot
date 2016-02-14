total_robots = 0
for n in level.entities(Robot):
    total_robots += 1

print("robot stuff",state.get('which',''), total_robots)
    
if step == 0 and total_robots == 1:
    state['which'] = 'NE'
    governor['action'] = 'none'
elif (step == 1) and total_robots < 3:
    state['stay'] = False
    if total_robots == 1:        
        governor['action'] = 'left'
    elif total_robots == 2:
        governor['action'] = 'down'
elif step == 2 and total_robots < 3:
    governor['action'] = 'none'    
elif step == 3 and total_robots == 1:
    state['which'] = 'NW'
    governor['action'] = 'time'
    governor['time_tick'] = 0
elif step == 3 and total_robots == 2:
    state['which'] = state['which'].replace('N','S')
    governor['action'] = 'time'
    governor['time_tick'] = 0
elif total_robots == 4 and step <= 3:
    governor['action'] = {'N': 'up', 'S': 'down'}[state['which'][0]]
elif total_robots == 4 and 3 < step <= 8:
    governor['action'] = {'W': 'left', 'E': 'right'}[state['which'][1]]
    if step == 8:
        state['stay'] = True
elif total_robots > 4 and (not state['stay']) and state['which'][0] == 'N':
    governor['action'] = 'up'
