import json
import time
from nav_api_ws import NavBot

ROBOT_HOST = "192.168.0.10"
ROBOT_PORT = 8765

helper_path = [
    (0.0, 0.0), (0.0, 5.0), (0.0, 1.25), (2.0, 1.25),
    (2.0, 0.8), (3.0, 0.8), (2.5, 3.5), (4.0, 3.5),
    (5.0, 3.5), (5.0, 1.0), (5.0, 1.75), (0.0, 1.75)
]

def load_target_from_json(file_path: str):
    with open(file_path, "r", encoding="utf-8") as f:
        data = json.load(f)
    return float(data["x"]), float(data["y"])

def build_route_to_target(target_x: float, target_y: float):
    route = []
    for point in helper_path:
        route.append(point)
        if (point - (target_x, target_y)) < 1.0:
            route.append((target_x, target_y))
            return route
    route.append((target_x, target_y))
    return route

def dispatch_robot(json_file: str):
    try:
        target_x, target_y = load_target_from_json(json_file)
        print(f"Цель: ({target_x}, {target_y})")

        route = build_route_to_target(target_x, target_y)
        print(f"Маршрут сформирован ({len(route)} точек): {route}")

        bot = NavBot(host=ROBOT_HOST, port=ROBOT_PORT)
        bot.wait_until_ready(timeout=15.0)

        bot.grip()
        bot.navigate_path(route)

        print("Маршрут отправлен, робот выполняет движение...")
        while bot.point_reached() == 0:
            print("Робот в пути...")
            time.sleep(1)

        print("Робот достиг цели!")
        bot.rize()

    except FileNotFoundError:
        print(f"Файл {json_file} не найден!")
    except ConnectionError as e:
        print(f"Ошибка подключения к роботу: {e}")
    except TimeoutError as e:
        print(f"Таймаут ожидания ответа от робота: {e}")
    except Exception as e:
        print(f"Непредвиденная ошибка: {e}")

if __name__ == "__main__":
    dispatch_robot("human.json")
