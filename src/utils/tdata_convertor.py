from pathlib import Path
import asyncio

from pyrogram.client import Client
from opentele.td.tdesktop import TDesktop

PATH = r""

class TDesktop(TDesktop):
    def __init__(self, *args, **kargs):
        super().__init__(*args, *kargs)

    async def ToPyrogram(self, session, is_bot=False) -> Client:
        account = self.mainAccount
        app = Client(session, account.api.api_id, account.api.api_hash)

        await app.storage.open()

        await app.storage.dc_id(account.authKey.dcId)
        await app.storage.test_mode(False)
        await app.storage.auth_key(account.authKey.key)
        await app.storage.user_id(account.UserId)
        await app.storage.is_bot(is_bot)
        await app.storage.date(0)
        await app.storage.api_id(app.api_id)

        await app.storage.save()
        await app.storage.close()

        return app

async def main():
    app = await TDesktop(PATH).ToPyrogram(Path(PATH).name)
    
    async with app:
        print(await app.get_me())


if __name__ == "__main__":
    asyncio.run(main())