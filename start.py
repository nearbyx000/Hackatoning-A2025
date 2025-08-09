from drone_control_api import Drone

ip = "10.42.0.1"

client = Drone()

print(client.connect(ip, reset_state=True))

n = 0
while n < 10:
    print(client.get_nav_pose())