import logging
from telethon.tl.types import Message
from .. import loader, utils

# meta developer: @minimaxno
# meta pic: https://img.icons8.com/emoji/344/bullseye.png

def getnum(list: list, needle: str) -> int:
    for i in range(0, len(list)):
        if list[i] == needle:
            return i

@loader.tds
class DicedestroyerMod(loader.Module):
    """Keeps your chat clean from dices, darts and so on."""
    strings = {'name': 'Dicedestroyer', 'on': '🤐 <b>Now I will delete dices.</b>', 'off': '🎲 <b>Now I will no more delete dices.</b>', 'rights?': '🤷🏼‍♂️ <b>I need rights to delete messages.</b>'}
    strings_ru = {'name': 'Dicedestroyer', 'on': '🤐 <b>Теперь удаляю кубики.</b>', 'off': '🎲 <b>Теперь не удаляю кубики.</b>', 'rights?': '🤷🏼‍♂️ <b>Эх, щас бы права на удаление сообщений…</b>'}
    
    async def client_ready(self, client, db):
        self.client = client
        self.db = db
        if not self.get('würf.sper', False):
            self.set('würf.sper', [])
    
    async def deldicecmd(self, m: Message):
        """Set deleting dices in this chat on/off."""
        if str(utils.get_chat_id(m)) not in self.get('würf.sper'):
            if not m.is_private:
                c = await m.get_chat()
                if c.admin_rights or c.creator:
                    if c.admin_rights.delete_messages == False:
                        return await utils.answer(m, self.strings('rights?'))

                else:
                    return await utils.answer(m, self.strings('rights?'))
            wsperr = self.get('würf.sper')
            wsperr.append(str(utils.get_chat_id(m)))
            self.set('würf.sper', wsperr)
            await utils.answer(m, self.strings('on'))
        else:
            wsperr = self.get('würf.sper')
            del wsperr[getnum(wsperr, str(utils.get_chat_id(m)))]
            self.set('würf.sper', wsperr)
            await utils.answer(m, self.strings('off'))
    
    async def watcher(self, m: Message):
        if (
            not isinstance(m, Message)
            or not m.dice
            or m.out
            or str(utils.get_chat_id(m)) not in self.get("würf.sper")
            ):
            return
        try:
            await m.delete()
        except:
            return
