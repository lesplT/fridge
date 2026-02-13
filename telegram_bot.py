"""Тг бот интерфейс"""

import asyncio
import os

from telegram import Update
from telegram.ext import Application, CommandHandler, ContextTypes

from fridge.factory import create_default_service
from fridge.interfaces import FridgeController


def ensure_event_loop() -> None:
    """если нет loop'а, то он создается"""
    try:
        loop = asyncio.get_event_loop()
        if loop.is_closed():
            raise RuntimeError
    except RuntimeError:
        asyncio.set_event_loop(asyncio.new_event_loop())


class TelegramFridgeBot:
    def __init__(self, token: str, controller: FridgeController) -> None:
        self._token = token
        self._controller = controller

    async def start(self, update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
        await self._reply(update, "Холодильник готов.\n\n" + self._controller.help_text())

    async def help_command(
        self, update: Update, context: ContextTypes.DEFAULT_TYPE
    ) -> None:
        await self._reply(update, self._controller.help_text())

    async def open_command(
        self, update: Update, context: ContextTypes.DEFAULT_TYPE
    ) -> None:
        await self._reply(update, self._controller.open())

    async def close_command(
        self, update: Update, context: ContextTypes.DEFAULT_TYPE
    ) -> None:
        await self._reply(update, self._controller.close())

    async def status_command(
        self, update: Update, context: ContextTypes.DEFAULT_TYPE
    ) -> None:
        await self._reply(update, self._controller.status())

    async def list_command(
        self, update: Update, context: ContextTypes.DEFAULT_TYPE
    ) -> None:
        if context.args:
            await self._reply(update, self._controller.list_zone(context.args[0]))
            return
        await self._reply(update, self._controller.list_all())

    async def put_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
        if len(context.args) < 2:
            await self._reply(update, "Пример: /put <зона> <объект>")
            return
        zone = context.args[0]
        item_name = " ".join(context.args[1:])
        await self._reply(update, self._controller.put(zone, item_name))

    async def take_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
        if len(context.args) < 2:
            await self._reply(update, "Пример: /take <зона> <объект>")
            return
        zone = context.args[0]
        item_name = " ".join(context.args[1:])
        await self._reply(update, self._controller.take(zone, item_name))

    async def _reply(self, update: Update, text: str) -> None:
        if update.message is not None:
            await update.message.reply_text(text)

    def run(self) -> None:
        ensure_event_loop()
        app = Application.builder().token(self._token).build()
        app.add_handler(CommandHandler("start", self.start))
        app.add_handler(CommandHandler("help", self.help_command))
        app.add_handler(CommandHandler("open", self.open_command))
        app.add_handler(CommandHandler("close", self.close_command))
        app.add_handler(CommandHandler("status", self.status_command))
        app.add_handler(CommandHandler("list", self.list_command))
        app.add_handler(CommandHandler("put", self.put_command))
        app.add_handler(CommandHandler("take", self.take_command))
        app.run_polling(drop_pending_updates=True)


def main() -> None:
    token = os.getenv("TELEGRAM_BOT_TOKEN", "tokenhere").strip()
    if not token:
        raise RuntimeError("Не указан токен бота")
    controller = create_default_service()
    bot = TelegramFridgeBot(token=token, controller=controller)
    bot.run()


if __name__ == "__main__":
    main()
