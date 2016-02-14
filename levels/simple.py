if step == 0:
    if level.spot_has(position + Point(0,1),Robot):
        governor['action'] = 'right'#move_right()
    else:
        governor['action'] = 'down'
elif step == 2 or step == 1:
    governor['action'] = 'none'
elif step == 3:
    governor['action'] = 'time'
    governor['time_tick'] = 0
    #set_time(0)
#if step%2 == 0:
#    governor['action']='up'
#else:
#    governor['action']='left'
