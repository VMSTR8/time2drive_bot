## Чат бот Time2drag
Проект создавался для команды time2drag. Это первая и довольно сырая версия, 
но все сделано строго по желанию и запросам руководителя проекта.

На данном этапе отсутствует валидация данных excel таблиц, это так задумано. 
Скорее всего в дальнейшем валидация будет реализована. Так же в будущем 
в планах добавить отправку фотографий автомобилей при выдаче поисковых 
результатов.

## Что бот умеет на данный момент
Администратор загружает в базу данных Excel таблицу с данными участников 
фестиваля. Пользователи чат-бот могут искать участников по ФИО или по гос. 
номеру автомобиля.

## Стэк
* [python 3.13](https://www.python.org/)
* [aiogram 3.20.0.post0](https://docs.aiogram.dev/en/v3.20.0.post0/)
* [tortoise orm 0.22.1](https://tortoise.github.io/)

## Развертывание и запуск чат-бота
Большой нагрузки на бота на данном этапе не предвидится, поэтому работает он 
через polling, а не через webhook.

Если запускаете бота локально, то сначала скачиваете репозиторий себе на 
компьютер и создаете файл переменных виртуального окружения .env в папке 
bot/settings:
```
git clone https://github.com/VMSTR8/time2drive_bot.git
cd bot/settings
touch .env
```
Редактируете только что созданный файл:
```
vim .env
```
Вписываете туда следующие данные:
```
BOT_TOKEN=токен телеграм бота
DATABASE_URL=sqlite://database/botdatabase.sqlite3
ADMIN_ID=telegram id админов (например: 1234567890)
```
Чтобы сохранить и выйти из vim вводите команду :qw

Дальше нужно сделать миграции базы данных. Возвращаемся в папку bot и выполняем 
команды:
```
cd .. # для перехода в папку bot
aerich init -t database.config.TORTOISE_ORM && aerich init-db
```
База данных В С Е. Ну, то есть готова.
Можем запускать бота.
```
python3 main.py
```
## Запуск через Docker
На данный момент образ бота не загружен в docker hub. Короче говоря, CI/CD нет.
Поэтому пропишу только способ локального запуска. Как только все будет настроено, 
отредактирую ридми и дополню инструкцию.

После скачивания репозитория в корневой папке создаете файл docker-compose.yml:
```
touch docker-compose.yml
```

Редактируете его через vim (выше уже писал как, все по аналогии). Вставляете туда 
следующие данные:
```yaml
services:
  bot:
    build: .
    container_name: time2drag_bot
    volumes:
      - ./data/:/app/data/
      - ./data/migrations/:/app/migrations/
    environment:
      - BOT_TOKEN=тут токен телеграм бота
      - DATABASE_URL=sqlite://data/botdatabase.sqlite3
      - ADMIN_ID=тут id'шники админа(ов) (Если несколько, то через запятую, например 1234,3210)
    restart: unless-stopped
```
Переходите в папку bot и в водите следующую команду:
```
cd bot
chmod +x ./entrypoint.sh
```
Это установит флаг "исполняемый" и Docker сможет запустить скрипт.

Возвращаетесь в корневую папку и билдите/запускаете контейнер:
```
cd ..
docker-compose up -d
```

Все. Бот запущен. Подробнее про [compose up смотреть тут](https://docs.docker.com/reference/cli/docker/compose/up/).