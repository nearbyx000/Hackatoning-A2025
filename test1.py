from drone_control_api import Drone
import datetime
import cv2
import numpy as np
import time
import json


def cb(msg):
    global break_flag
    break_flag = True


ip = "10.42.0.1"

people = []
fire = []

order_path = np.array([1, 2, 4, 3, 5, 6, 6, 7, 9, 10, 
         9, 8, 11, 12, 13, 14, 15,
         14, 13, 12, 11, 8, 7, 5, 3, 2, 1]) - 1

# 1 - 0 рад, 2 - 1.57, 3 - 3.14, 4 - -1.57, 5 - -4.71, 
order_yaw = np.array([ 1, 2, 3, 2, 4, 2, 5, 4, 4, 3,
                      2, 4, 2, 4, 4, 4, 3]) - 1

path = np.array([
    [0.0, 0.0], #точка 1
    [0.978, 0.0], #точка 2
    [0.978, 0.721], #точка 3
    [0.978, 4.707], #точка 4
    [2.890, 0.721], #точка 5
    [2.890, 0.0], #точка 6
    [2.890, 1.679], #точка 7
    [3.859, 1.679], #точка 8
    [5.207, 1.679], #точка 9
    [5.207, 0.0], #точка 10
    [3.859, 2.920], #точка 11
    [2.334, 2.920], #точка 12
    [2.334, 4.445], #точка 13
    [5.390, 4.445], #точка 14
    [5.390, 2.920], #точка 15
])

yaw = np.array([0, 1.57, 3.14, -1.57,-4.71,])

client = Drone()

print(client.connect(ip, reset_state=True))

print(client.takeoff())

for i, point_idx in enumerate(order_path):

    x, y = path[point_idx]
    print(f"Полет к следующей точке")
    break_flag = False
    client.go_to_xy_nav_nb(x, y, callback=cb)

    while not break_flag:
        time.sleep(0.05)

    if i < len(order_yaw):
        yaw_idx = order_yaw[i]
        angle = yaw[yaw_idx]
        print(f"Поворот дрона")
        break_flag = False
        client.set_yaw_relative(angle, callback = cb)

        while not break_flag:
            time.sleep(0.05)


    data = client.get_detections()
    if data and "boxes" in data:
        for bbox in data["boxes"]:
            label = bbox["name"]
            pose = client.get_nav_pose()
            if label == "human":
                if pose not in people:
                    people.append({"x": pose[0], "y": pose[1]})
            elif label == "fire":
                if pose not in fire:
                    fire.append({"x": pose[0], "y": pose[1]})
            print(f"Обнаружен объект: {label} в точке {pose}")

print(client.landing())

print(client.disconnect())

# Сохраняем в JSON
with open("people.json", "w") as f:
    json.dump(people, f, indent=2)

with open("fire.json", "w") as f:
    json.dump(fire, f, indent=2)



