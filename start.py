from time import sleep

drone = Drone()
drone.connect("192.168.0.100")

# Асинхронно запускаем взлёт
drone.takeoff_nb(callback=lambda resp: print("Взлёт завершён:", resp))

# Пока дрон взлетает — делаем что-то ещё
for i in range(5):
    drone.set_diod(1, 0, 0)  # красный
    sleep(0.5)
    drone.set_diod(0, 1, 0)  # зелёный
    sleep(0.5)

# Ждём завершения взлёта, если нужно, через feedback
print("Статус взлёта:", drone.takeoff_feedback())

drone.disconnect()
