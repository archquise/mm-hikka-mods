# meta developer: @mm_mods, original by Fl1yd
# meta pic: https://img.icons8.com/emoji/344/grapes-emoji.png

from .. import loader, utils
from random import choice
from time import sleep
from telethon import types
from telethon.tl.types import Message

class GrapesMod(loader.Module):
    """Searching for random pic for your query. Original version/idea: Fl1yd."""

    strings = {"name": "Grapes", 'lade': '🔎 <b>Searching…</b>', 'p-auf': '👾 <b>O0pS, pr0b1em…</b>', 'n-gef': '<b>Ha, stop, not found… :(</b>', 'gef': '<b>Looks like something is found!..</b>', 'q': 'Query:', 'args?': '📝 <b>Where is arguments, sir?</b>'}
    
    strings_ru = {"name": "Grapes", 'lade': '🔎 <b>Ищу…</b>', 'p-auf': '👾 <b>0й, пр06лемkа…</b>', 'n-gef': '<b>А, нет, не нашлось… :(</b>', 'gef': '<b>Кажется, нашлось!..</b>', 'q': 'Запрос:', 'args?': '📝 <b>И где аргументы, сударь?</b>'}

    async def piccmd(self, message: Message):
        """Searching for pics in Yandex."""
        try:
            args = utils.get_args_raw(message)
            if not args:
                await utils.answer(message, self.strings('args?'))
                return
            await utils.answer(message, self.strings('lade'))
            reslt = await message.client.inline_query("pic", args)
            await utils.answer(message, f'{self.strings("gef")}\n{self.strings("q")} {args}')
            sleep(1.5)
            await message.delete()
            await reslt[reslt.index(choice(reslt))].click(utils.get_chat_id(m))
        except:
            await message.respond(self.strings('n-gef'))
            return
            
    async def dpiccmd(self, message: Message):
        """Searching for pics in DuckDuckGo."""
        try:
            args = utils.get_args_raw(message)
            if not args:
                await utils.answer(message, self.strings('args?'))
                return
            await utils.answer(message, self.strings('lade'))
            reslt = await message.client.inline_query("duckpicsbot", args)
            await utils.answer(message, f'{self.strings("gef")}\n{self.strings("q")} {args}')
            sleep(1.5)
            await message.delete()
            await reslt[reslt.index(choice(reslt))].click(utils.get_chat_id(m))
        except:
            await message.respond(self.strings('n-gef'))
            return
