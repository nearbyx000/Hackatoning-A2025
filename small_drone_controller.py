# robot_controller.py

from nav_api_ws import NavBot
import time

# IP-адрес и порт робота (можно вынести в конфиг)
ROBOT_HOST = "192.168.0.10"
ROBOT_PORT = 8765

def dispatch_robot_to_person(x: float, y: float):
    """
    Отправляет мобильного робота к указанным координатам человека.
    """
    print(f"Отправка мобильного робота к человеку в точку ({x}, {y})...")
    try:
        # [cite_start]Подключение к роботу [cite: 7]
        bot = NavBot(host=ROBOT_HOST, port=ROBOT_PORT) 
        
        # [cite_start]Ожидание готовности робота [cite: 13, 19]
        bot.wait_until_ready(timeout=15.0) 
        
        # [cite_start]Команда движения к цели [cite: 45]
        bot.navigate(x, y) 
        
        # Можно добавить ожидание прибытия, если это нужно
        # [cite_start]while bot.point_reached() == 0: [cite: 63, 67]
        #     print("Робот в пути...")
        #     time.sleep(1)
        # print("Робот прибыл к цели!")

        print(f"Команда роботу на перемещение к ({x}, {y}) успешно отправлена.")

    except ConnectionError as e:
        [cite_start]print(f"Ошибка подключения к роботу: {e}") # [cite: 140]
    except TimeoutError as e:
        [cite_start]print(f"Таймаут ожидания ответа от робота: {e}") # [cite: 140]
    except Exception as e:
        print(f"Произошла непредвиденная ошибка при управлении роботом: {e}")