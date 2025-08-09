from drone_control_api import Drone
import numpy as np


order_path = np.array([
    0, 1, 2, 3, 4, 5, 6, 7, 8, 9,
    10, 11, 0
]) 

path = np.array([
    [0.0, 0.0], [0.0, 5.0], [0.0, 1.25], [2.0, 1.25],
    [2.0, 0.8], [3.0, 0.8], [2.5, 3.5], [4.0, 3.5],
    [5.0, 3.5], [5.0, 1.0], [5.0, 1.75], [0.0, 1.75]
]) 

client = Drone()
print(client.connect("192.168.41.21", reset_state=True))
print(client.takeoff())
client.set_height(0.7)

for point_idx in order_path:
    y, x = path[point_idx]
    client.go_to_xy_nav(x, y)

print(client.landing())
print(client.disconnect())
