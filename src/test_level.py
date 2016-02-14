from level import Level
from button import Button
from point import Point
starting_level = Level()
button1 = Button(starting_level)
button2 = Button(starting_level)
starting_level.add(button1,Point(3,3))
starting_level.add(button2,Point(6,3))
