import os
import sys

if not sys.path[0] in os.environ["PATH"].split(":"):
    print(os.path.abspath(os.curdir + "/src"))
    sys.path.append(os.path.abspath(os.curdir + "/src"))

import render

my_render = render.Renderer("Muh title", 640, 480)

input()
