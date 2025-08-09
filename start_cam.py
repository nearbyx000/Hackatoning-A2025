from drone_control_api import Drone
import time
import cv2

ip = "10.42.0.1"

client = Drone()

print(client.connect(ip, reset_state=True))

n = 0
while n < 10:
    print(client.get_nav_pose())
    print(f"getImage = {client.get_image()}")
    imgg = client.get_image()
    cv2.imshow("imgg", imgg)

    time.sleep(0.5)
