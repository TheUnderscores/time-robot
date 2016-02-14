if 'future' not in state.keys():
    state['future'] = False
if step == 0 and not state['future']:
    if level.spot_has(position + Point(0,1),Robot):
        governor['action'] = 'right'#move_right()
    else:
        governor['action'] = 'down'
elif step == 2 or step == 1 or state['future']:
    governor['action'] = 'none'
elif step == 3:
    state['future'] = True
    governor['action'] = 'time'
    governor['time_tick'] = 0
    #set_time(0)
#if step%2 == 0:
#    governor['action']='up'
#else:
#    governor['action']='left'
