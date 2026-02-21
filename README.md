# Модель холодильника (ООП+SOLID)

## Функционал

- Открыть/закрыть дверцу
- Положить предмет в зону
- Взять предмет из зоны
- Показать список предметов

Зоны:
- main
- door 
- medicine 

## Как запустить

1) В терминале:
Запуск:
python cli.py


2) Телеграм бот:
https://t.me/fredthefridge_bot
или:
Установить зависимости:
pip install -r requirements.txt

Прописать токен бота:
в файле telegram_bot.py или в cmd перед запуском set TELEGRAM_BOT_TOKEN=токен 

Запуск:
python telegram_bot.py


## Команды терминала

- `open`
- `close`
- `put <зона> <объект>`
- `take <зона> <объект>`
- `list [зона]`
- `status`
- `help`
- `exit`

## Команды тг-бота

- `/start`
- `/help`
- `/open`
- `/close`
- `/put <зона> <объект>`
- `/take <зона> <объект>`
- `/list [зона]`
- `/status`

## Соответствие принципам SOLID

SRP: классы зон управляют только хранением; Fridge управляет состоянием холодильника; FridgeService форматирует ответы; cli.py и telegram_bot.py отвечают только за пользовательский интерфейс.

OCP: новые типы зон можно добавлять через наследование от BaseZone и подключение через фабрику без изменения Fridge.

LSP: MainZone, DoorZone, MedicineZone взаимозаменяемы через интерфейс Zone.

ISP: операции с дверью и операции хранения разделены (DoorManager, StorageManager).

DIP: FridgeService зависит от абстракций (DoorManager, StorageManager), а не от конкретной реализации.


