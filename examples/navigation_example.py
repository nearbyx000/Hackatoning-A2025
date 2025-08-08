from drone_control_api import Drone
import datetime
import cv2
import time


def cb(msg):
    global break_flag
    break_flag = True


ip = "10.42.0.1"

result = []


client = Drone()

print(client.connect(ip, reset_state=True))

break_flag = False

client.go_to_xy_nav_nb(2.5, 8.5, callback=cb)


while not break_flag:
    data = client.get_detections()
    if data:
        for bbox in data:
            if bbox["name"] == "human":
                pose = client.get_nav_pose()
                result.append(pose)
                print(pose)
    time.sleep(0.05)

print(result)

print(client.landing())

print(client.disconnect())



