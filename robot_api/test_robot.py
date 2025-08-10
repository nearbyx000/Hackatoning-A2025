# robot_controller.py

from nav_api_ws import NavBot
import time

# IP-адрес и порт робота (можно вынести в конфиг)
ROBOT_HOST = "192.168.0.10"
ROBOT_PORT = 8765

import numpy as np
order_path = np.array([
    0, 1, 2, 3, 4, 5, 6, 7, 8, 9,
    10, 11, 0
]) 

path = np.array([
    [0.0, 0.0], [0.0, 5.0], [0.0, 1.25], [2.0, 1.25],
    [2.0, 0.8], [3.0, 0.8], [2.5, 3.5], [4.0, 3.5],
    [5.0, 3.5], [5.0, 1.0], [5.0, 1.75], [0.0, 1.75]
]) 

def dispatch_robot_to_person(x: float, y: float):
    print(f"Отправка в точку ({x}, {y})...")
    try:
        # [cite_start]Подключение к роботу [cite: 7]
        bot = NavBot(host=ROBOT_HOST, port=ROBOT_PORT) 
        
        # [cite_start]Ожидание готовности робота [cite: 13, 19]
        bot.wait_until_ready(timeout=15.0) 
        
        bot.grip()
        # [cite_start]Команда движения к цели [cite: 45]
        bot.navigate(x, y) 
        
        # Можно добавить ожидание прибытия, если это нужно
        while bot.point_reached() == 0: 
            print("Робот в пути...")
            time.sleep(1)
        print("Робот прибыл к цели!")
        bot.rize()

        print(f"Команда роботу на перемещение к ({x}, {y}) успешно отправлена.")

    except ConnectionError as e:
        print(f"Ошибка подключения к роботу: {e}") 
    except TimeoutError as e:
        print(f"Таймаут ожидания ответа от робота: {e}")
    except Exception as e:
        print(f"Произошла непредвиденная ошибка при управлении роботом: {e}")