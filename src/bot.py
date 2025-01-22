import os
import asyncio
import datetime

from pyrogram import Client, filters
from pyrogram.raw import functions, types, base

from .access_managers import AccessManager


class SearchBot():
    CHANNELS_HASH = {}

    def __init__(
            self,
            lock: asyncio.Lock,
            username: str,
            api_id: str,
            api_hash: str,
            writer: AccessManager,
            chats: list[str],
            keywords: list[str],
        ) -> None:
        self.app: Client = Client(
            username,
            api_id,
            api_hash,
            phone_number=os.environ.get("PHONE_NUMBER"),
            workdir="sessions"
        )
        self.writer = writer
        self.chats = chats
        self.keywords = keywords
        self.lock = lock

    async def get_messages(self, keyword, peer, count=0) -> types.messages.Messages:
        return await self.app.invoke(
            functions.messages.Search(
                peer=peer,
                q=keyword,
                filter=types.InputMessagesFilterEmpty(),
                min_date=0,
                max_date=0,
                offset_id=0,
                add_offset=0,
                limit=count,
                min_id=0,
                max_id=0,
                hash=0,
            )
        )

    async def resolve_chanel_access_hash(self, channel_name: str) -> str:
        channel_hash = (await self.app.invoke(
                functions.contacts.ResolveUsername(username=channel_name)
            )
        ).chats[0].access_hash
        self.CHANNELS_HASH[channel_name] = channel_hash
        return channel_hash

    async def get_users(self, users):
        return await self.app.invoke(functions.users.GetUsers(id=users))

    async def get_message_link(self, message, chat_name):
        if not isinstance(message.peer_id, types.peer_channel.PeerChannel): return ""
        return (await self.app.invoke(
            functions.channels.ExportMessageLink(
                channel=types.InputChannel(
                    channel_id=message.peer_id.channel_id,
                    access_hash=self.CHANNELS_HASH.get(
                        chat_name, 
                        await self.resolve_chanel_access_hash(chat_name)
                    )
                ),
                id=message.id
            )
        )).link
    
    async def form_data_unit(
        self, 
        chat_name: str,
        keyword: str,
        peer: base.input_peer.InputPeer,
        message: base.message.Message
        ) -> tuple:
        user = (await self.get_users([
            types.InputUserFromMessage(
                peer=peer,
                msg_id=message.id,
                user_id=message.from_id.user_id
            )
        ]))[0]
        return (
            message.from_id.user_id, 
            user.username, 
            f"{user.first_name if user.first_name else ''} {user.last_name if user.last_name else ''}", 
            datetime.datetime.fromtimestamp(message.date).strftime('%Y-%m-%d %H:%M:%S'), 
            keyword, 
            message.message, 
            await self.get_message_link(message, chat_name)
        )

    async def search_messages(self) -> None:
        while self.chats:
            try: 
                async with self.lock:
                    chat = self.chats.pop(0)
                    if not chat: continue
            except IndexError: continue
            peer = await self.app.resolve_peer(chat)
            valid_messages = []
            for keyword in self.keywords:
                pre_messages = await self.get_messages(keyword, peer)
                if not hasattr(pre_messages, "count") or pre_messages.count == 0: continue
                messages = await self.get_messages(keyword, peer, pre_messages.count)
                valid_messages = [message for message in messages.messages if isinstance(message.from_id, types.PeerUser)]
                print(f"\nfound {len(valid_messages)} messages in `{chat}` chat by `{keyword}` keyword")
                
                # app.get_users и functions.users.GetUsers не всегда возвращает весь список(?),
                # поэтому для точности использется get_users по отдельности
                for i, message in enumerate(valid_messages):
                    data = await self.form_data_unit(chat, keyword, peer, message)
                    self.writer.add_data(*data)
                    print(f"processed message {i + 1}/{pre_messages.count}", end="\r")

    def run(self) -> None:
        self.app.start()
        self.app.run(self.search_messages())
        self.app.stop()
