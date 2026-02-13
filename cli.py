"""Взаимодействие через терминал"""

from fridge.factory import create_default_service


def run_cli() -> None:
    service = create_default_service()
    print("Холодильник готов. help - команды")

    while True:
        try:
            raw = input("fridge> ").strip()
        except (EOFError, KeyboardInterrupt):
            print("\nПока")
            break

        if not raw:
            continue

        parts = raw.split()
        command = parts[0].lower()

        if command in {"exit", "quit"}:
            print("Пока")
            break
        if command == "help":
            print(service.help_text())
            continue
        if command == "open":
            print(service.open())
            continue
        if command == "close":
            print(service.close())
            continue
        if command == "status":
            print(service.status())
            continue
        if command == "list":
            if len(parts) == 1:
                print(service.list_all())
            else:
                print(service.list_zone(parts[1]))
            continue
        if command == "put":
            if len(parts) < 3:
                print("Пример: put <зона> <объект>")
                continue
            zone = parts[1]
            item_name = " ".join(parts[2:])
            print(service.put(zone, item_name))
            continue
        if command == "take":
            if len(parts) < 3:
                print("Пример: take <зона> <объект>")
                continue
            zone = parts[1]
            item_name = " ".join(parts[2:])
            print(service.take(zone, item_name))
            continue

        print("Неизвестная команда. help - команды")


if __name__ == "__main__":
    run_cli()
