#!/bin/sh

if [ ! -d "/app/migrations" ]; then
  echo "Папка migrations не найдена, выполняем aerich init..."
  aerich init -t database.config.TORTOISE_ORM && aerich init-db
else
  echo "Папка migrations найдена, пропускаем init."
fi

exec python main.py
