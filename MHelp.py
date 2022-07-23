from .. import loader, utils
from telethon import types
from telethon.tl.types import Message
import re
import os
import requests as rq
from deep_translator import GoogleTranslator as GT
import logging

logger = logging.getLogger(__name__)

# meta developer: @minimaxno
# meta pic: https://img.icons8.com/emoji/344/scroll-emoji.png
# requires: deep-translator


@loader.tds
class MHelpMod(loader.Module):
    """Helps to download mods to file and automaticaly make simple descriptions for your modules."""
    strings = {'name': 'MHelp', 'noname': "🙅🏼‍♂️ <b>You've not setted your GitHub username!</b>", 'norepo': "🗒️ <b>You've not setted your Hikka modules repo!</b>", 'format?': '🚫 <b>Incorrect format!</b>', 'inname': '🤖 <b>Name is incorrect!</b>', '404': '🔦 <b>Requested file not found!</b>', 'lang?': '㊙️ <b>I dunno such language!</b>', 'suc': '👌🏻 <b>Succesful!</b>'}
    strings_ru = {'name': 'MHelp', 'noname': "🙅🏼‍♂️ <b>Ты ещё не установил свой юзернейм на GitHub!</b>", 'norepo': "🗒️ <b>Ты ещё не установил имя репозитария с модулями!</b>", 'format?': '🚫 <b>Неверный формат!</b>', 'inname': '🤖 <b>Некорректное имя</b>', '404': '🔦 <b>Не нашёл такого файла!</b>', 'lang?': '㊙️ <b>Один из введёных языков мне неизвестен!</b>', 'suc': '👌🏻 <b>Успешно!</b>'}
    strings_de = {'name': 'MHelp', 'noname': "🙅🏼‍♂️ <b>Geben Sie Ihren auf GitHub verwendeten Benutzernamen!</b>", 'norepo': "🗒️ <b>Geben Sie den Namen des Repositorys ein, das zum Speichern der Module verwendet wird!</b>", 'format?': '🚫 <b>Ungültiges Format!</b>', 'inname': '🤖 <b>Ungültiger Name!</b>', '404': '🔦 <b>Es gibt keine solche Datei!</b>', 'lang?': '㊙️ <b>Eine der eingegebenen Sprachen ist mir unbekannt!</b>', 'suc': '👌🏻 <b>Erfolgreich!</b>'}
    
    async def client_ready(self, client, db):
        self.client = client
        self.db = db
    
    async def setuncmd(self, m: Message):
        """Configurates GH username."""
        name = utils.get_args_raw(m)
        if (len(name) > 39) or (name[len(name)-1] == '-') or (name[0] == '-') or (name == '') or ('--' in name) or (re.search(name, '[^ a-zA-Z0-9-]')):
            await utils.answer(m, self.strings('inname'))
            return
        else:
            self.set('ghun', name)
            await utils.answer(m, self.strings('suc'))
    
    async def setrepocmd(self, m: Message):
        """Configurates GH repo name."""
        name = utils.get_args_raw(m)
        if (len(name) > 100) or (name[len(name)-1] == '-') or (name[0] == '-') or (name == '') or ('--' in name) or (re.search(name, '[^ a-zA-Z0-9-_.]')):
            await utils.answer(m, self.strings('inname'))
            return
        else:
            self.set('repon', name)
            await utils.answer(m, self.strings('suc'))
    
    async def descrcmd(self, m: Message):
        """Makes decription. Required format:
        emoji > name > description > base language code, language codes to translate automatocally, … """
        if not (self.get("ghun", False)):
            await utils.answer(m, self.strings('noname'))
            return
        if not (self.get("repon", False)):
            await utils.answer(m, self.strings('norepo'))
            return
        prompt = utils.get_args_raw(m)
        try:
            emoji, name, descr, langs = prompt.split(' > ')
        except:
            await utils.answer(m, self.strings('format?'))
        ans = f'{emoji} <b>{name}'+'</b>\n\n'+descr
        if ', ' in langs:
            langs = langs.split(', ')
        else:
            langs = [langs]
        avla = GT().check_supported_languages()
        for i in langs:
            if i not in avla:
                await utils.answer(m, self.strings('lang?'))
                return
        if len(langs) > 1:
            for lang in range(1, len(langs)):
                tren = GT(langs[0], langs[lang])
                tr_descr = "".join(
                [
                    await utils.run_sync(lambda: tren.translate(chunk))
                    for chunk in utils.chunks(descr, 512)
                ]
            )
                ans += '\n\n—\n\n' + tr_descr
        if langs[0] != 'ru':
            download = GT('auto', langs[0]).translate('Скачать')
        else:
            download = 'Скачать'
        for lang in range(1, len(langs)):
            if langs[lang] != 'ru':
                download += ' | ' + GT('ru', langs[lang]).translate('Скачать')
            else:
                download += ' | Скачать'
        link = 'https://raw.githubusercontent.com/'+self.get('ghun')+'/'+self.get('repon')+'/main/'+name+'.py'
        ans += '\n\n—\n\n<b>' + download + '</b>\n<code>.dlmod '+link+'</code>'
        if rq.get(link).status_code != 200:
            await utils.answer(m, self.strings('404'))
            return
        else:
            open(f'{name}.py', 'w').write(rq.get(link).text)
        await m.client.send_file(m.to_id, f'{name}.py', caption=ans, parse_mode='HTML')
        os.remove(f'{name}.py')
        await m.delete()
    
    async def topycmd(self, m: Message):
        """Gets module from link."""
        link = utils.get_args_raw(m)
        if ('github' and 'hikariatama') not in link:
            await utils.answer(m, self.strings('format?'))
            return
        else:
            if rq.get(link).status_code != 200:
                await utils.answer(m, self.strings('404'))
                return
            else:
                open(f'Mod.py', 'w').write(rq.get(link).text)
                await m.client.send_file(m.to_id, f'Mod.py')
                os.remove(f'Mod.py')
                await m.delete()
        
