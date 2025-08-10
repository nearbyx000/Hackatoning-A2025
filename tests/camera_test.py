from drone_control_api import Drone
import cv2
import numpy as np


ip = "10.42.0.1"

people = []
fire = []

client = Drone()

print(client.connect(ip, reset_state=True))
n=1
while (n != 10):
    print(f"getImage = {client.get_image()}")
    imgg = client.get_image()
    cv2.imshow("imgg", imgg)
    n+=1
print(client.disconnect())





