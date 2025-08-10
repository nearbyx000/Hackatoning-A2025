# from drone_control_api import Drone
# import time
# import cv2
# import math
# import json
# ip = "192.168.41.21"

# z = 0.5                
# ang_h = math.radians(60)    
# ang_v = math.radians(45)    
# width, hight = 640, 480 
# people = []
# fire = []

# def is_new_object(obj_list, x, y, threshold=0.4):
#     for obj in obj_list:
#         if math.hypot(obj["x"] - x, obj["y"] - y) <= threshold:
#             return False
#     return True

# def process_detections(client, current_yaw, people, fire):
#     detected_px_x = None
#     data = client.get_detections()
#     if data and "boxes" in data:
#         pose_nav = client.get_nav_pose()
#         x_d, y_d = pose_nav[0], pose_nav[1]

#         for bbox in data["boxes"]:
#             label = bbox["name"]
#             px_x = bbox["center"]["x"]
#             px_y = bbox["center"]["y"]

#             x_obj, y_obj = pixel_to_global(px_x, px_y, x_d, y_d, current_yaw)

#             if label == "human" and is_new_object(people, x_obj, y_obj):
#                 people.append({"x": x_obj, "y": y_obj})
#                 print(f"Человек: ({x_obj:.2f}, {y_obj:.2f})")

#             elif label == "fire" and is_new_object(fire, x_obj, y_obj):
#                 fire.append({"x": x_obj, "y": y_obj})
#                 print(f"Очаг: ({x_obj:.2f}, {y_obj:.2f})")

#             detected_px_x = px_x  

#     return detected_px_x

# def pixel_to_global(px_x, px_y, x_d, y_d, yaw_d):
#     delta_x_angle = (px_x - width/2) / width * ang_h
#     delta_y_angle = (px_y - hight/2) / hight * ang_v

#     distance_forward = z / math.tan(math.pi/2 - delta_y_angle)
#     lateral_offset = math.tan(delta_x_angle) * distance_forward

#     x_obj = x_d + distance_forward * math.cos(yaw_d) - lateral_offset * math.sin(yaw_d)
#     y_obj = y_d + distance_forward * math.sin(yaw_d) + lateral_offset * math.cos(yaw_d)
    
#     return x_obj, y_obj

# client = Drone()

# print(client.connect(ip, reset_state=True))

# n = 0
# while n < 10:
#     print(client.get_nav_pose())
#     print(f"getImage = {client.get_image()}")
#     process_detections(client, 0.0, people, fire)

#     imgg = client.get_image()
#     cv2.imshow("imgg", imgg)
#     cv2.waitKey(1)
    

#     time.sleep(0.033)

# print(client.disconnect())

# with open("people.json", "w") as f:
#     json.dump(people, f, indent=2)
# with open("fire.json", "w") as f:
#     json.dump(fire, f, indent=2)

from drone_control_api import Drone
import time
import cv2
import math
import json
import os

ip = "192.168.41.21"
z = 0.5                
ang_h = math.radians(60)    
ang_v = math.radians(45)    
width, height = 640, 480 
people = []
fire = []

def save_people():
    with open("people.json", "w") as f:
        json.dump(people, f, indent=2)

def save_fire():
    with open("fire.json", "w") as f:
        json.dump(fire, f, indent=2)

def is_new_object(obj_list, x, y, threshold=0.4):
    for obj in obj_list:
        if math.hypot(obj["x"] - x, obj["y"] - y) <= threshold:
            return False
    return True

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
                save_people()  # Сразу сохраняем в файл

            elif label == "fire" and is_new_object(fire, x_obj, y_obj):
                fire.append({"x": x_obj, "y": y_obj})
                print(f"Очаг: ({x_obj:.2f}, {y_obj:.2f})")
                save_fire()  # Сразу сохраняем в файл

            detected_px_x = px_x  

    return detected_px_x

def pixel_to_global(px_x, px_y, x_d, y_d, yaw_d):
    delta_x_angle = (px_x - width/2) / width * ang_h
    delta_y_angle = (px_y - height/2) / height * ang_v

    distance_forward = z / math.tan(math.pi/2 - delta_y_angle)
    lateral_offset = math.tan(delta_x_angle) * distance_forward

    x_obj = x_d + distance_forward * math.cos(yaw_d) - lateral_offset * math.sin(yaw_d)
    y_obj = y_d + distance_forward * math.sin(yaw_d) + lateral_offset * math.cos(yaw_d)
    
    return x_obj, y_obj

# Инициализация файлов (если не существуют)
if not os.path.exists("people.json"):
    with open("people.json", "w") as f:
        json.dump([], f)

if not os.path.exists("fire.json"):
    with open("fire.json", "w") as f:
        json.dump([], f)

client = Drone()
print(client.connect(ip, reset_state=True))

n = 0
while n < 20:
    print(client.get_nav_pose())
    print(f"getImage = {client.get_image()}")
    process_detections(client, 0.0, people, fire)

    img = client.get_image()
    cv2.imshow("Video Stream", img)
    cv2.waitKey(1)
    
    time.sleep(0.033)
    n += 1

print(client.disconnect())