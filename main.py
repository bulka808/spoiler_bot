import asyncio
from aiogram import Bot, Dispatcher, types, Router
from aiogram.filters.command import Command
from aiogram import F
from dotenv import load_dotenv
from os import getenv

load_dotenv()

bot = Bot(token=getenv("TOKEN"))
dp = Dispatcher()
router = Router()

@router.message(Command("sp"), F.reply_to_message.photo[-1].file_id.as_("photo"))
async def spoiler(message: types.Message, photo: str):
    if not message.reply_to_message.has_media_spoiler:
        # шлем сообщение сос спойлером
        await message.answer_photo(
            photo=photo,
            caption=f"from: {message.reply_to_message.from_user.username or message.reply_to_message.from_user.full_name} \
            ({message.from_user.username or message.from_user.full_name})",
            has_spoiler=True
        )
        # удаляем оригинальное сообщение и с командой
        await bot.delete_message(message_id=message.reply_to_message.message_id, chat_id=message.chat.id)
        await bot.delete_message(message_id=message.message_id, chat_id=message.chat.id)


async def main():
    dp.include_router(router)
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())