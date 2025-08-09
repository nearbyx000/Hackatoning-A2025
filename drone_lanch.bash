#!/bin/bash

# Загружаем переменные среды из .bashrc
source ~/.bashrc

# Запускаем скрипт 1 в фоновом режиме
./autonomous_ws/launch_navigation.bash &

# Запускаем скрипт 2 в фоновом режиме
./autonomous_ws/launch_detection.bash &

echo "Два скрипта запущены параллельно. Дрон готовится к запуску."