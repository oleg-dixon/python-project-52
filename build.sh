#!/usr/bin/env bash

# Установка uv
curl -LsSf https://astral.sh/uv/install.sh | sh
source $HOME/.local/bin/env

# Установка зависимостей проекта
make install

# Применение миграций
make migrate

# Сборка статики для продакшн
