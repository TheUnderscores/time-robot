if step==1:
    if level.spot_has(position + Point(0,1),Robot):
        move_right()
    else:
        move_down()
elif step==2:
    set_time(0)
