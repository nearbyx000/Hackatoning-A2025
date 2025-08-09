from drone_control_api import Drone
import numpy as np
import time
import math
import json

order_path = np.array([
    1, 2, 3, 4, 5, 6, 7, 8, 8, 9, 10,
    11, 12, 1
]) - 1

order_yaw = np.array([
    1, 4, 3, 4, 3, 5, 3, 1, 3, 4, 1,
    1, 1, 1
]) - 1

yaw_angles = np.array([0, math.radians(90), math.radians(-90), math.radians(180), math.radians(45),])

path = np.array([
    [0.0, 0.0], [0.0, 6.0], [0.0, 1.25], [2.0, 1.25],
    [2.0, 0.5], [0.5, 3.0], [2.5, 3.5], [4.0, 3.5],
    [6.0, 3.5], [6.0, 0.0], [6.0, 1.75], [0.0, 1.75]
]) 

client = Drone()
print(client.connect("10.42.0.1", reset_state=True))
print(client.takeoff())
time.sleep(5.0)

for i, point_idx in enumerate(order_path):
    x, y = path[point_idx]
    movement_completed = False

    def cb(msg):
        global movement_completed
        movement_completed = True
    # Старт движения
    client.go_to_xy_nav_nb(x, y, callback=cb)

    rotation_completed = False
    def rotation_callback(msg):
        global rotation_completed
        rotation_completed = True
    
    yaw_idx = order_yaw[i]
    yaw_angle = yaw_angles[yaw_idx]
    client.set_yaw_nb(yaw_angle, callback=rotation_callback)

print(client.landing())
print(client.disconnect())

