# ---------------------------------------------------------------------------------
#  ,_     _          
#  |\_,-~/          
#  / _  _ |    ,--.  🌐 This module was loaded through https://t.me/hikkamods_bot
# (  @  @ )   / ,-'  🔓 Not licensed.
#  \  _T_/-._( (     
#  /         `. \    ⚠️ Owner of this bot doesn't take responsibility for any
# |         _  \ |   errors caused by this module or this module being non-working
#  \ \ ,  /      |   and doesn't take ownership of any copyrighted material.
#   || |-_\__   /    
#  ((_/`(____,-'     
# ---------------------------------------------------------------------------------
# Name: GoogleTrans
# Description: Advanced Google Translate module!
# Author: GD-alt
# Commands:
#  .autotranslate | .deflang   | .silentmode | .subsmode
# .markmode   | .atlist        | .translate
# ---------------------------------------------------------------------------------

# meta developer: @minimaxno
# meta pic: https://img.icons8.com/color/344/translate-text.png
# requires: deep-translator


import logging
import deep_translator
from telethon.tl.types import Message
from .. import loader, utils, translations

translator = deep_translator.GoogleTranslator()
available_languages = translator.get_supported_languages(as_dict=True)
logger = logging.getLogger(__name__)


def get_key(dictionary: dict, needle: str) -> str:
    return next((key for key, value in dictionary.items() if value == needle), None)


@loader.tds
class GoogleTranslateMod(loader.Module):
    """Advanced Google Translate module!"""

    strings = {
        "name": "Google Translate",
        "load": "🔄 <b>Translating…</b>",
        "args": "🚫 <b>No arguments, no reply…</b>",
        "args2": "🚫 <b>No arguments…</b>",
        "no_lang": "📕 <b>No such language!</b>",
        "setted": "🔤 <b>Your main language is updated!</b>",
        "silent": "🔇 <b>OK, I won't dispay translation message!</b>",
        "unsilent": "🔊 <b>OK, I will dispay translation message!</b>",
        "mark": "🔇 <b>OK, I won't dispay «translated» mark!</b>",
        "unmark": "🔊 <b>OK, I will dispay «translated» mark!</b>",
        "tr-ed": "<b>Translated:</b>",
        "added": "➕ <b>Chat added to autotranslate list!</b>",
        "changed": "〰️ <b>Autotranslate configuration changed!</b>",
        "deled": "➖ <b>Chat deleted from autotranslate list!</b>",
        "alheader": "📃 <b>Chats, in which autotranslate is activated:</b>",
        "subscribe": "🖋️ <b>Now I'll keep original text while autotranslating.</b>",
        "unsubscribe": (
            "🖋️ <b>Now I won't keep original text while autotranslating.</b>"
        ),
    }

    strings_ru = {
        "name": "Google Translate",
        "load": "🔄 <b>Перевожу…</b>",
        "args": "🚫 <b>Ни аргумента, ни ответа…</b>",
        "args2": "🚫 <b>Нет аргумента…</b>",
        "no_lang": "📕 <b>Я не знаю такого языка!</b>",
        "setted": "🔤 <b>Ваш основной язык обновлён!</b>",
        "silent": "🔇 <b>Хорошо, теперь не отображаю сообщение о переводе!</b>",
        "unsilent": "🔊 <b>Хорошо, теперь отображаю сообщение о переводе!</b>",
        "mark": "🔇 <b>Хорошо, теперь не отображаю пометку «переведено»!</b>",
        "unmark": "🔊 <b>Хорошо, теперь отображаю пометку «переведено»!</b>",
        "tr-ed": "<b>Переведено:</b>",
        "added": "➕ <b>Чат добавлен в список автоперевода!</b>",
        "changed": "〰️ <b>Конфигурация автоперевода изменена!</b>",
        "deled": "➖ <b>Чат убран из списка автоперевода!</b>",
        "alheader": "📃 <b>Список чатов, в которых активен автоперевод:</b>",
        "subscribe": "🖋️ <b>Теперь я сохраняю оригинальный текст при автопереводе.</b>",
        "unsubscribe": (
            "🖋️ <b>Теперь я не сохраняю оригинальный текст при автопереводе.</b>"
        ),
    }

    async def client_ready(self, client, db):
        self._client = client
        self._db = db
        if not self.get("deflang", False):
            self.set("deflang", "en")

        if not self.get("silence", False):
            self.set("silence", False)

        if not self.get("mark", False):
            self.set("mark", True)

        if not self.get("s-script", False):
            self.set("s-script", False)

        if not self.get("tr_cha", False):
            self.set("tr_cha", {})

    async def setdeflangcmd(self, message: Message):
        """Use language code with this command to switch basic translation language."""
        lang = utils.get_args_raw(message)
        if lang not in available_languages.values:
            await utils.answer(message, self.strings("nolang"))
        else:
            self.set("deflang", lang)
            await utils.answer(message, self.strings("setted"))

    async def autotranslatecmd(self, message: Message):
        """Use language code with this command to add this chat to autotranslate list."""
        lang = utils.get_args_raw(message)
        if (str(utils.get_chat_id(message)) in self.get("tr_cha")) and not lang:
            tr_cha = self.get("tr_cha")
            del tr_cha[str(utils.get_chat_id(message))]
            self.set("tr_cha", tr_cha)
            await utils.answer(message, self.strings("deled"))
            return

        if ";" not in lang:
            stla = "auto"
            fila = self.get("deflang")
        else:
            stla, fila = lang.split(";", 1)
            if not stla:
                stla = "auto"

            if not fila:
                fila = self.get("deflang")

        if fila not in available_languages.values():
            await utils.answer(message, self.strings("no_lang"))
            return

        if (stla != "auto") and (stla not in available_languages.values()):
            await utils.answer(message, self.strings("no_lang"))
            return

        lang = f"{stla};{fila}"
        tr_cha = tco = self.get("tr_cha")
        tr_cha.update({str(utils.get_chat_id(message)): lang})
        self.set("tr_cha", tr_cha)
        if str(utils.get_chat_id(message)) not in tco.keys():
            await utils.answer(message, self.strings("added"))
        else:
            await utils.answer(message, self.strings("changed"))

    async def deflangcmd(self, message: Message):
        """Use language code with this command to switch basic translation language."""
        lang = utils.get_args_raw(message)
        if lang not in available_languages.values():
            await utils.answer(message, self.strings("nolang"))
        else:
            self.set("deflang", lang)
            await utils.answer(message, self.strings("setted"))

    async def silentmodecmd(self, message):
        """Use this command to switch between silent/unsilent mode."""
        if self.get("silence"):
            self.set("silence", False)
            await utils.answer(message, self.strings("unsilent"))
        else:
            self.set("silence", True)
            await utils.answer(message, self.strings("silent"))

    async def subsmodecmd(self, message):
        """Use this command to switch autotranslate subscription mode."""
        if self.get("s-script"):
            self.set("s-script", False)
            await utils.answer(message, self.strings("unsubscribe"))
        else:
            self.set("s-script", True)
            await utils.answer(message, self.strings("subscribe"))

    async def markmodecmd(self, message):
        """Use this command to switch between showing/unshowing «translated» mark."""
        if self.get("mark"):
            self.set("mark", False)
            await utils.answer(message, self.strings("mark"))
        else:
            self.set("mark", True)
            await utils.answer(message, self.strings("unmark"))

    async def atlistcmd(self, message: Message):
        """Sends a list of chats, in which autotranslate is turned on."""
        laco = self._db.get(translations.__name__, "lang", "en")
        autotranslate = self.get("tr_cha")
        alist = self.strings("alheader") + "\n"
        avlad = deep_translator.GoogleTranslator().get_supported_languages(as_dict=True)
        for i in autotranslate.keys():
            st_la, fi_la = autotranslate[i].split(";")
            if st_la == "auto":
                if laco == "ru":
                    st_la = "авто"
            elif laco == "ru":
                st_la = f"{get_key(avlad, st_la)} language"
                st_la = (
                    deep_translator.GoogleTranslator("en", "ru")
                    .translate(st_la)
                    .replace("язык", "")
                )
            else:
                st_la = get_key(avlad, st_la)
            if laco == "ru":
                fi_la = f"{get_key(avlad, fi_la)} language"
                fi_la = (
                    deep_translator.GoogleTranslator("en", "ru")
                    .translate(fi_la)
                    .replace("язык", "")
                )
            else:
                fi_la = get_key(avlad, fi_la)

            type_ = (
                "user"
                if getattr(await self._client.get_entity(int(i)), "first_name", False)
                else "chat"
            )

            alist += (
                f'<a href="tg://openmessage?{type_}_id={i.replace("-100", "")}">id{i.replace("-100", "")}</a>:'
                f" {st_la} » {fi_la}" + "\n"
            )

        await utils.answer(message, alist)

    async def translatecmd(self, message: Message):
        """In fact, it translates. Use (start;final) to mark the start and end language of the translation.
        Leave the start language blank to define it automatically."""
        reply = await message.get_reply_message()
        prompt = utils.get_args_raw(message)
        if not prompt and reply is None:
            await utils.answer(message, self.strings("args"))

        if prompt and prompt.startswith("("):
            lafo, prompt = prompt.split(")", 1)
            if ";" not in lafo:
                prompt = f"({lafo}){prompt}"
                stal = "auto"
                finl = self.get("deflang")
            else:
                lafo = lafo.replace("(", "", 1)
                stal, finl = lafo.split(";", 1)
                if not stal:
                    stal = "auto"

                if not finl:
                    finl = self.get("deflang")

                if (
                    (stal or finl) not in available_languages.values()
                    and (stal != "auto")
                    and (finl not in available_languages.values())
                ):
                    await utils.answer(
                        message,
                        self.strings("no_lang") + "\n" + stal + " " + finl,
                    )
                    return
        else:
            stal = "auto"
            finl = self.get("deflang")

        if not self.get("silence"):
            await utils.answer(message, self.strings("load"))

        if not prompt:
            if reply is None:
                await utils.answer(message, self.strings("args"))
                return
            else:
                prompt = reply.raw_text

        translator = deep_translator.GoogleTranslator(stal, finl)
        translated = translator.translate(prompt)

        if self.get("mark"):
            translated = f'{self.strings("tr-ed")}\n{translated}'

        await utils.answer(message, translated)

    async def watcher(self, message: Message):
        if (
            not getattr(message, "raw_text", False)
            or not message.out
            or str(utils.get_chat_id(message)) not in self.get("tr_cha").keys()
            or message.raw_text.split(maxsplit=1)[0].lower() in self.allmodules.commands
            or (message.text[0] == '/') or (message.text == '')
            ):
            return

        stla, fila = self.get("tr_cha")[str(utils.get_chat_id(message))].split(";")

        tren = deep_translator.GoogleTranslator(stla, fila)
        translated = "".join(
            [
                await utils.run_sync(lambda: tren.translate(chunk))
                for chunk in utils.chunks(message.raw_text, 512)
            ]
        )

        if self.get("s-script"):
            translated = (
                message.raw_text + "\n\n" + self.strings("tr-ed") + "\n\n" + translated
            )

        try:
            await utils.answer(message, translated)
        except:
        	return