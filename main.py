import os
import asyncio
import dotenv

from src.bot import SearchBot
from src.access_managers import *

dotenv.load_dotenv("bot.env", override=True)
dotenv.load_dotenv(override=True)

chats_file = "res/chats.list"
keywords_file = "res/keywords.list"

API_ID = os.getenv("API_ID")
API_HASH = os.getenv("API_HASH")
USERNAME = os.getenv("USERNAME")
FILENAME = "data.xlsx"
COLUMNS = ['ID', 'Username', 'Name', 'Date', 'Keyword', 'Massage', 'Link']


def main():
    lock = asyncio.Lock()
    chats = FileManager.get_data(chats_file)
    writer = XlsxManager(FILENAME, COLUMNS)
    keywords = FileManager.get_data(keywords_file)
    proxy={
        "scheme": os.getenv("PROXY_SCHEME"), 
        "hostname": os.getenv("PROXY_HOSTNAME"), 
        "port": int(os.getenv("PROXY_PORT")), 
        "username": os.getenv("PROXY_USERNAME"), 
        "password": os.getenv("PROXY_PASSWORD")
    }
    bot = SearchBot(
        lock,
        USERNAME,
        proxy,
        writer,
        chats,
        keywords,
    )
    bot.run()


if __name__ == '__main__':
    main()
