from drone_control_api import Drone
import numpy as np
import time
import math
import json

order_path = np.array([
    1, 2, 3, 4, 5, 6, 7, 8, 8, 9, 10,
    11, 12, 1
]) - 1
path = np.array([
    [0.0, 0.0], [0.0, 6.0], [0.0, 1.25], [2.0, 1.25],
    [2.0, 0.5], [0.5, 3.0], [2.5, 3.5], [4.0, 3.5],
    [6.0, 3.5], [6.0, 0.0], [6.0, 1.75], [0.0, 1.75]
]) 

client = Drone()
print(client.connect("192.168.41.21", reset_state=True))
print(client.takeoff())
client.set_height(0.5)

for point_idx in order_path:
    y, x = path[point_idx]

    # movement_completed = False

    # def cb(msg):
    #     global movement_completed
    #     movement_completed = True
    # # Старт движения
    client.go_to_xy_nav(x, y)

print(client.landing())
print(client.disconnect())


