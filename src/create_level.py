from os.path import isfile
from classes import *

def read_level(level_file):
    level = []
    if isfile(level_file):
        with open(level_file, 'r') as f:
            for line in f:
                line = line.replace('\r', '')
                if line == '\n':
                    break
                level.append(line[:-1])
    return level

def create_level(split_level):
    level = Level(ent_field=None, width=len(split_level[0]), height=len(split_level))
    for y in range(len(split_level)):
        for x in range(len(split_level[y])):
            if split_level[y][x] in ('E', 'B', 'W', 'R'):
                point = Point(x, y)
                if split_level[y][x] == 'E':
                    level.add(ExitDoor(level), point)
                if split_level[y][x] == 'B':
                    level.add(Button(level), point)
                if split_level[y][x] == 'W':
                    level.add(Wall(level), point)
                if split_level[y][x] == 'R':
                    level.add(Robot(level), point)
    return level

def setup_level(level_file):
    return create_level(read_level(level_file))
