# Lab2-Shaders
# Graficas por computadora 
# Esteban Aldana Guerra 20591

from gl import *

r = Render()
r.glLoad("./planeta.obj", tras=(300, 395, 0), size=(280, 280, 280), shape=jupiter)
r.finish(filename="final.bmp")
