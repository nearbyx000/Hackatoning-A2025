from drone_control_api import Drone

ip = "192.168.41.21"

client = Drone()

print(client.connect(ip, reset_state=True))


n = 0
while n < 10:
    print(client.get_nav_pose())



with open("resu.txt","w",encoding ="UTF-8") as file:
    print(client.get_nav_pose(), file=file)