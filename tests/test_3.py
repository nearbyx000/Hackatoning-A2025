
#111A777&Sa$

from drone_control_api import Drone
import numpy as np
import time
import math

order_path = np.array([0, 1, 2, 3, 4, 5, 6, 7, 7, 8, 9, 10, 11, 12, 13, 0]) 
order_yaw = np.array([1, 4, 3, 4, 3, 5, 3, 1, 3, 4, 1]) - 1
yaw_angles = np.array([0, math.radians(90), math.radians(-90), math.radians(180), math.radians(45)])

path = np.array([
    [0.0, 0.0], [0.0, 5.0], [0.0, 1.25], [2.0, 1.25],
    [2.0, 0.8], [3.0, 0.8], [2.5, 3.5], [4.0, 3.5],
    [5.0, 3.5], [5.0, 1.0], [5.0, 3.0], [2.5, 3.0], [2.5, 1.75], [0.0, 1.75]
])

client = Drone()
print(client.connect("192.168.41.21", reset_state=True))
print(client.takeoff())
client.set_height(0.5)
time.sleep(5.0)

for i, point_idx in enumerate(order_path):
    x, y = path[point_idx]
    
    # Создаем флаг для каждой итерации
    movement_event = {"completed": False}
    
    def movement_callback(msg):
        movement_event["completed"] = True
    
    # Запускаем движение
    client.go_to_xy_nav_nb(x, y, callback=movement_callback)
    print(f"Полет к точке: {point_idx} ({x}, {y})")
    
    # Ждем достижения точки
    while not movement_event["completed"]:
        time.sleep(0.1)
    
    # Выполняем поворот после достижения точки
    if i < len(order_yaw):
        yaw_idx = order_yaw[i]
        yaw_angle = yaw_angles[yaw_idx]
        
        rotation_event = {"completed": False}
        
        def rotation_callback(msg):
            rotation_event["completed"] = True
        
        client.set_yaw_nb(yaw_angle, callback=rotation_callback)
        print(f"Поворот на {math.degrees(yaw_angle):.1f}°")
        
        # Ждем завершения поворота
        while not rotation_event["completed"]:
            time.sleep(0.1)

print(client.landing())
print(client.disconnect())