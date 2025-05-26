from Albums import * # моя недо-библиотека

import asyncio
from aiogram import Bot, Dispatcher, types, Router
from aiogram.filters.command import Command
from aiogram.filters import *
from aiogram import F
from aiogram.utils.media_group import MediaGroupBuilder
from dotenv import load_dotenv
from os import getenv

load_dotenv()

bot = Bot(token=getenv("TOKEN"))
dp = Dispatcher()
router = Router()

Albums = AlbumStorage(limit=50)

# прием альбомов
@router.message(F.media_group_id,  or_f(F.photo, F.video))
async def get_album(message: types.Message):
	if message.photo or message.video:
		album = Albums.get_or_create(message.media_group_id)
		message_media = (message.video or message.photo[-1]).file_id
		album.append(message_media)

# отправка альбомов под спойлером
@router.message(Command("sp"), F.reply_to_message.photo, F.media_group_id.as_("media_group_id"))
async def group_spoiler(message: types.Message,  media_group_id: str):
	album_builder = MediaGroupBuilder(caption=f"from: {message.reply_to_message.from_user.username or message.reply_to_message.from_user.full_name} \
								  ({message.from_user.username or message.from_user.full_name})")
	album = Albums.get_or_create(media_group_id=media_group_id)	
	[album_builder.add_photo(media=photo) for photo in album.files]
	await message.answer_media_group(media=album_builder.build())

# обычная обработка сообщений
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