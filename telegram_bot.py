"""интерфейс тг бота"""

import asyncio
import os

from aiogram import Bot, Dispatcher, Router
from aiogram.filters import Command
from aiogram.types import Message

from fridge.factory import create_default_service
from fridge.interfaces import FridgeController


class TelegramFridgeBot:
    def __init__(self, token: str, controller: FridgeController) -> None:
        self._token = token
        self._controller = controller
        self._router = Router()
        self._dispatcher = Dispatcher()
        self._dispatcher.include_router(self._router)
        self._register_handlers()

    def _register_handlers(self) -> None:
        self._router.message.register(self.start, Command("start"))
        self._router.message.register(self.help_command, Command("help"))
        self._router.message.register(self.open_command, Command("open"))
        self._router.message.register(self.close_command, Command("close"))
        self._router.message.register(self.status_command, Command("status"))
        self._router.message.register(self.list_command, Command("list"))
        self._router.message.register(self.put_command, Command("put"))
        self._router.message.register(self.take_command, Command("take"))

    async def start(self, message: Message) -> None:
        await self._reply(
            message, "Бот холодильника запущен.\n\n" + self._controller.help_text()
        )

    async def help_command(self, message: Message) -> None:
        await self._reply(message, self._controller.help_text())

    async def open_command(self, message: Message) -> None:
        await self._reply(message, self._controller.open())

    async def close_command(self, message: Message) -> None:
        await self._reply(message, self._controller.close())

    async def status_command(self, message: Message) -> None:
        await self._reply(message, self._controller.status())

    async def list_command(self, message: Message) -> None:
        parts = self._split_command(message.text, maxsplit=1)
        if len(parts) == 1:
            await self._reply(message, self._controller.list_all())
            return
        await self._reply(message, self._controller.list_zone(parts[1]))

    async def put_command(self, message: Message) -> None:
        parts = self._split_command(message.text, maxsplit=2)
        if len(parts) < 3:
            await self._reply(message, "Использование: /put <зона> <предмет>")
            return
        zone_name = parts[1]
        item_name = parts[2]
        await self._reply(message, self._controller.put(zone_name, item_name))

    async def take_command(self, message: Message) -> None:
        parts = self._split_command(message.text, maxsplit=2)
        if len(parts) < 3:
            await self._reply(message, "Использование: /take <зона> <предмет>")
            return
        zone_name = parts[1]
        item_name = parts[2]
        await self._reply(message, self._controller.take(zone_name, item_name))

    @staticmethod
    def _split_command(text: str | None, maxsplit: int) -> list[str]:
        if not text:
            return []
        return text.strip().split(maxsplit=maxsplit)

    @staticmethod
    async def _reply(message: Message, text: str) -> None:
        await message.answer(text)

    async def _run(self) -> None:
        bot = Bot(token=self._token)
        try:
            await bot.delete_webhook(drop_pending_updates=True)
            await self._dispatcher.start_polling(bot)
        finally:
            await bot.session.close()

    def run(self) -> None:
        asyncio.run(self._run())


def main() -> None:
    token = os.getenv("TELEGRAM_BOT_TOKEN", "").strip()
    if not token:
        raise RuntimeError("Не задан TELEGRAM_BOT_TOKEN перед запуском telegram_bot.py")
    controller = create_default_service()
    bot = TelegramFridgeBot(token=token, controller=controller)
    bot.run()


if __name__ == "__main__":
    main()
