from drone_control_api import Drone
import numpy as np
import time
import math
import json

z = 0.5                
ang_h = math.radians(60)    
ang_v = math.radians(45)    
width, hight = 640, 480     

def is_new_object(obj_list, x, y, threshold=0.4):
    for obj in obj_list:
        if math.hypot(obj["x"] - x, obj["y"] - y) <= threshold:
            return False
    return True

def pixel_to_global(px_x, px_y, x_d, y_d, yaw_d):
    delta_x_angle = (px_x - width/2) / width * ang_h
    delta_y_angle = (px_y - hight/2) / hight * ang_v

    distance_forward = z / math.tan(math.pi/2 - delta_y_angle)
    lateral_offset = math.tan(delta_x_angle) * distance_forward

    x_obj = x_d + distance_forward * math.cos(yaw_d) - lateral_offset * math.sin(yaw_d)
    y_obj = y_d + distance_forward * math.sin(yaw_d) + lateral_offset * math.cos(yaw_d)
    
    return x_obj, y_obj

def process_detections(client, current_yaw, people, fire):
    detected_px_x = None
    data = client.get_detections()
    if data and "boxes" in data:
        pose_nav = client.get_nav_pose()
        x_d, y_d = pose_nav[0], pose_nav[1]

        for bbox in data["boxes"]:
            label = bbox["name"]
            px_x = bbox["center"]["x"]
            px_y = bbox["center"]["y"]

            x_obj, y_obj = pixel_to_global(px_x, px_y, x_d, y_d, current_yaw)

            if label == "human" and is_new_object(people, x_obj, y_obj):
                people.append({"x": x_obj, "y": y_obj})
                print(f"Человек: ({x_obj:.2f}, {y_obj:.2f})")

            elif label == "fire" and is_new_object(fire, x_obj, y_obj):
                fire.append({"x": x_obj, "y": y_obj})
                print(f"Очаг: ({x_obj:.2f}, {y_obj:.2f})")

            detected_px_x = px_x  

    return detected_px_x

order_path = np.array([
    0, 1, 2, 3, 4, 5, 6, 7, 7, 8, 9,
    10, 11, 12, 13, 0
]) 

order_yaw = np.array([
    1, 4, 3, 4, 3, 5, 3, 1, 3, 4, 1,
]) - 1

path = np.array([
    [0.0, 0.0], [0.0, 6.0], [0.0, 1.25], [2.0, 1.25],
    [2.0, 0.5], [0.5, 3.0], [2.5, 3.5], [4.0, 3.5],
    [5.0, 3.5], [5.0, 1.0], [5.0, 3.0], [2.5, 3.0], [2.5, 1.75], [0.0, 1.75], 
])

yaw_angles = np.array([ math.radians(0), math.radians(90), math.radians(-90), math.radians(180), math.radians(45),])

people = []
fire = []
return_start_index = 11  

client = Drone()
print(client.connect("192.168.41.21", reset_state=True))
print(client.takeoff())
client.set_height(0.5)

for i, point_idx in enumerate(order_path):
    forward_phase = i < return_start_index
    x, y = path[point_idx]
    movement_completed = False

    def cb(msg):
        global movement_completed
        movement_completed = True

    client.go_to_xy_nav_nb(x, y, callback=cb)

    object_detected = False
    detected_px_x = None

    while not movement_completed:
        if forward_phase:
            data = client.get_detections()
            if data and "boxes" in data:
                client.go_to_xy_nav_cancel()
                object_detected = True
                movement_completed = True
                detected_px_x = process_detections(client, yaw_angles[order_yaw[i]], people, fire)
        time.sleep(0.05)

    if object_detected and forward_phase and detected_px_x is not None:
        if detected_px_x <= width/2:
            yaw_angle = yaw_angles[order_yaw[i - 1]] - math.pi/2
        else:
            yaw_angle = yaw_angles[order_yaw[i - 1]] + math.pi/2

        rotation_completed = False
        def rotation_callback(msg):
            global rotation_completed
            rotation_completed = True

        client.set_yaw_nb(yaw_angle, callback=rotation_callback)
        while not rotation_completed:
            time.sleep(0.05)

        process_detections(client, yaw_angle, people, fire)

        movement_completed = False
        client.go_to_xy_nav_nb(x, y, callback=cb)
        while not movement_completed:
            time.sleep(0.05)

    if i < len(order_yaw):
        yaw_idx = order_yaw[i]
        yaw_angle = yaw_angles[yaw_idx]

        rotation_completed = False
        def rotation_callback(msg):
            global rotation_completed
            rotation_completed = True

        client.set_yaw_nb(yaw_angle, callback=rotation_callback)
        while not rotation_completed:
            time.sleep(0.05)

        process_detections(client, yaw_angle, people, fire)

print(client.landing())
print(client.disconnect())

with open("people.json", "w") as f:
    json.dump(people, f, indent=2)
with open("fire.json", "w") as f:
    json.dump(fire, f, indent=2)

