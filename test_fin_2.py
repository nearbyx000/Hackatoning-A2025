from drone_control_api import Drone
import numpy as np
import time
import math
import json
import os

z = 0.5                
ang_h = math.radians(60)    
ang_v = math.radians(45)    
width, height = 640, 480   

def save_people():
    with open("people.json", "w") as f:
        json.dump(people, f, indent=2)

def save_fire():
    with open("fire.json", "w") as f:
        json.dump(fire, f, indent=2)

def is_new_object(obj_list, x, y, threshold=1.0):
    for obj in obj_list:
        if math.hypot(obj["x"] - x, obj["y"] - y) <= threshold:
            return False
    return True

def pixel_to_global(px_x, px_y, x_d, y_d):
    delta_x_angle = (px_x - width/2) / width * ang_h
    delta_y_angle = (px_y - height/2) / height * ang_v 

    distance_forward = z / math.tan(math.pi/2 - delta_y_angle)
    lateral_offset = math.tan(delta_x_angle) * distance_forward

    x_obj = x_d + distance_forward
    y_obj = y_d + lateral_offset
    
    return x_obj, y_obj

def process_detections(client, people, fire):
    data = client.get_detections()
    if data and "boxes" in data:
        pose_nav = client.get_nav_pose()
        x_d, y_d = pose_nav[0], pose_nav[1]

        for bbox in data["boxes"]:
            label = bbox["name"]
            px_x = bbox["center"]["x"]
            px_y = bbox["center"]["y"]

            x_obj, y_obj = pixel_to_global(px_x, px_y, x_d, y_d)

            if label == "human" and is_new_object(people, x_obj, y_obj):
                people.append({"x": x_obj, "y": y_obj})
                print(f"Человек: ({x_obj:.2f}, {y_obj:.2f})")
                save_people()

            elif label == "fire" and is_new_object(fire, x_obj, y_obj):
                fire.append({"x": x_obj, "y": y_obj})
                print(f"Очаг: ({x_obj:.2f}, {y_obj:.2f})")
                save_fire()

order_path = np.array([
    0, 1, 2, 3, 4, 5, 6, 7, 8, 9,
    10, 11, 12, 0
]) 

path = np.array([
    [0.0, 0.0], [0.0, 3.0], [0.0, 1.25], [2.0, 1.25],
    [3.0, 0.8], [2.5, 3.5], [4.0, 3.5], [5.0, 3.5],
    [5.0, 1.0], [5.0, 3.0], [2.5, 3.0], [2.5, 1.75], [0.0, 1.75], 
])

people = []
fire = []
return_start_index = 10

if not os.path.exists("people.json"):
    save_people()

if not os.path.exists("fire.json"):
    save_fire()

client = Drone()
print(client.connect("192.168.41.21", reset_state=True))
print(client.takeoff())
client.set_height(0.5)

for i, point_idx in enumerate(order_path):
    y, x = path[point_idx]
    
    movement_event = {"completed": False}
    
    def movement_callback(msg):
        movement_event["completed"] = True

    client.go_to_xy_nav_nb(x, y, callback=movement_callback)

    while not movement_event["completed"]:
        data = client.get_detections()
        print(client.get_nav_pose())
        if data and "boxes" in data:
            process_detections(client, people, fire)
        time.sleep(0.05)

print(client.landing())
print(client.disconnect())