import sys
import numpy as np
sys.path.insert(0, "World")
sys.path.insert(0, "World/Robot")
sys.path.insert(0, "World/Robot/Behavior")
sys.path.insert(0, "World/Robot/Car_State")
sys.path.insert(0, "World/Robot/Sensor")
sys.path.insert(0, "Screen")
sys.path.insert(0, "Inputs")
sys.path.insert(0, "Resources/Extra_Py_Files")
from world import World
from screen import Window
from input import Inputs

# Set up World
Sim = World()

# create display window
WIDTH, HEIGHT = np.array([800, 600])

window = Window(WIDTH, HEIGHT, "Mobile Robot")
# load all world objects inside Window
window.loadCar(Sim.car.state)
window.loadCarSensors(Sim.car.sensors)
window.loadObstacles(Sim.obstacles)
window.loadGoal(Sim.goal)

input = Inputs()
loop = 0


while not input.Exit:
    #  all events detection
    input.process()
    #  update world
    Sim.update(window.frameRate)
    #  make all draw changes and calculate framerate
    window.draw(Sim.car.state, Sim.car.sensors)
