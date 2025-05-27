from aiogram import types
#сам класс альбома
class Album:
	def __init__(self, media_group_id: str):
		# понятно впринципе что это
		self.media_group_id: str = media_group_id
		# список file_id альбома
		self.files: list[str] = []
		self.messages: list[int] = []
	def append(self, message: types.Message) -> None:
		file_id = message.photo[-1].file_id
		message_id = message.message_id
		if file_id not in self.files:
			self.files.append(file_id)
			self.messages.append(message_id)
		
# класс для хранения альбомов
class AlbumStorage:
	def __init__(self, limit: int):
		self.limit: int = limit
		self.albums: list[Album] = []
	
	# доабвление/получение
	def get_or_create(self, media_group_id: str) -> Album:
		# не даем выходить за пределы лимита
		if len(self.albums) >= self.limit: self.albums.pop(0)

		for album in self.albums:
			if album.media_group_id == media_group_id: return album

		new_album = Album(media_group_id=media_group_id)
		self.albums.append(new_album)
		return new_album
	
	# удаление
	def remove_album(self, media_group_id: str) -> Album | None:
		rm_album = None # заглушка
		
		for a in self.albums: 
			if a.media_group_id == media_group_id:
				rm_album = a

		self.albums = [a for a in self.albums if a.media_group_id != media_group_id]
		return rm_album

		
