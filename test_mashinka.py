import json
import time
from robot_api.rf_bot_api import NavBot

ROBOT_HOST = "127.0.0.1"
ROBOT_PORT = 8765

def load_target_from_json(file_path: str):
    with open(file_path, "r", encoding="utf-8") as f:
        data = json.load(f)
    return float(data["x"]), float(data["y"])

def dispatch_robot(json_file: str):
    try:
        # Загрузка цели
        target_x, target_y = load_target_from_json(json_file)
        print(f"Цель: ({target_x}, {target_y})")

        # Инициализация и подключение
        bot = NavBot(host=ROBOT_HOST, port=ROBOT_PORT)
        
        # Ожидание готовности с проверкой ошибок
        ready_status = bot.wait_until_ready(timeout=15.0)
        if ready_status == -1:
            raise RuntimeError("Ошибка инициализации робота")
        elif ready_status == 0:
            raise TimeoutError("Робот не ответил в течение 15 секунд")

        # Функция проверки статуса
        def check_status(status, operation_name):
            if status == -1:
                raise RuntimeError(f"Ошибка операции: {operation_name}")
            return status

        # Захват объекта
        grip_status = bot.grip()
        check_status(grip_status, "grip")

        # Навигация к цели
        nav_status = bot.navigate(target_x, target_y)  # Передаем координаты
        check_status(nav_status, "navigate")

        # Мониторинг выполнения с повторной проверкой при ошибках
        print("Робот начал движение к цели...")
        max_retries = 3
        retry_count = 0
        
        while True:
            status = bot.point_reached()
            
            if status == 1:
                print("Цель достигнута!")
                break
                
            elif status == 0:
                print("Робот в пути...")
                retry_count = 0  # Сброс счетчика при успешном статусе
                bot.get_pose()
                time.sleep(1)
                
            elif status == -1:
                retry_count += 1
                print(f"Ошибка навигации ({retry_count}/{max_retries}), повторная проверка...")
                
                if retry_count >= max_retries:
                    raise RuntimeError("Не удалось получить статус навигации после нескольких попыток")
                
                time.sleep(0.5)  # Задержка перед повторной проверкой
                
            else:
                raise RuntimeError(f"Неизвестный статус: {status}")

        # Подъем объекта
        rize_status = bot.rize()
        check_status(rize_status, "rize")

        print("Робот успешно завершил миссию!")

    except FileNotFoundError:
        print(f"Файл {json_file} не найден!")
    except ConnectionError as e:
        print(f"Ошибка подключения к роботу: {e}")
    except TimeoutError as e:
        print(f"Таймаут ожидания ответа от робота: {e}")
    except RuntimeError as e:
        print(f"Ошибка выполнения команды: {e}")
    except Exception as e:
        print(f"Непредвиденная ошибка: {e}")

if __name__ == "__main__":
    dispatch_robot("human.json")