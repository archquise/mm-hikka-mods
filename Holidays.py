# `7MMM.     ,MMF'`7MMM.     ,MMF'   `7MMM.     ,MMF'              `7MM
# MMMb    dPMM    MMMb    dPMM       MMMb    dPMM                  MM
# M YM   ,M MM    M YM   ,M MM       M YM   ,M MM  ,pW"Wq.    ,M""bMM  ,pP"Ybd
# M  Mb  M' MM    M  Mb  M' MM       M  Mb  M' MM 6W'   `Wb ,AP    MM  8I   `"
# M  YM.P'  MM    M  YM.P'  MM mmmmm M  YM.P'  MM 8M     M8 8MI    MM  `YMMMa.
# M  `YM'   MM    M  `YM'   MM       M  `YM'   MM YA.   ,A9 `Mb    MM  L.   I8
# .JML. `'  .JMML..JML. `'  .JMML.   .JML. `'  .JMML.`Ybmd9'   `Wbmd"MML.M9mmmP'
#
# (c) 2022 — licensed under Apache 2.0 — https://www.apache.org/licenses/LICENSE-2.0

# meta pic: https://img.icons8.com/stickers/344/calendar.png
# meta developer: @mm_mods
# requires: deep-translator beautifulsoup4

__version__ = "1.0.0"

import re
from .. import loader, utils
import bs4
import deep_translator
import requests

from telethon.tl.types import Message
import logging

logger = logging.getLogger(__name__)


@loader.tds
class HolidaysMod(loader.Module):
    """Holidays today."""
    strings = {
        'name': 'Holidays',
        'base': '<b>Holidays today:</b>',
        'lang': 'en',
    }

    strings_ru = {
        'name': 'Holidays',
        'base': '<b>Праздники сегодня:</b>',
        '_cls_doc': 'Показывает праздники сегодня',
        '_cmd_doc_hollist': 'Показывает список праздников',
        'lang': 'ru',
    }

    strings_de = {
        'name': 'Holidays',
        'base': '<b>Feste heute:</b>',
        '_cls_doc': 'Zeigt Feste heute',
        '_cmd_doc_hollist': 'Zeigt eine Liste von Feste',
        'lang': 'de',
    }

    strings_uk = {
        'name': 'Holidays',
        'base': '<b>Святкові дні сьогодні:</b>',
        '_cls_doc': 'Показує святкові дні сьогодні',
        '_cmd_doc_hollist': 'Показує список святкових днів',
        'lang': 'uk',
    }

    strings_uz = {
        'name': 'Holidays',
        'base': '<b>Bugun kunlar:</b>',
        '_cls_doc': 'Bugun kunlarini ko\'rsatadi',
        '_cmd_doc_hollist': 'Bugun kunlar ro\'yxatini ko\'rsatadi',
        'lang': 'uz',
    }


    async def hollistcmd(self, m: Message):
        """Shows holiday list."""
        cookies = {
            '_ym_uid': '16634998731060557833',
            '_ym_d': '1663499873',
            'PHPSESSID': 'f6ot9sp2eur79p06hrvvbu7ap6',
            '_ym_isad': '1',
        }

        headers = {
            'authority': 'kakoysegodnyaprazdnik.ru',
            'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
            'accept-language': 'de-DE,de;q=0.9,en-US;q=0.8,en;q=0.7,ru;q=0.6',
            'referer': 'https://www.google.com/',
            'sec-ch-ua': '"Google Chrome";v="105", "Not)A;Brand";v="8", "Chromium";v="105"',
            'sec-ch-ua-mobile': '?0',
            'sec-ch-ua-platform': '"Windows"',
            'sec-fetch-dest': 'document',
            'sec-fetch-mode': 'navigate',
            'sec-fetch-site': 'cross-site',
            'sec-fetch-user': '?1',
            'upgrade-insecure-requests': '1',
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/105.0.0.0 Safari/537.36',
        }

        holidays = requests.get('https://kakoysegodnyaprazdnik.ru/', cookies=cookies, headers=headers).content
        holidays = bs4.BeautifulSoup(holidays.decode('utf-8', 'ignore'), 'html.parser')
        holidays = holidays.find_all('span', itemprop='text', limit=20)
        hollist = [i.text for i in holidays]
        res = deep_translator.GoogleTranslator(source='auto', target=self.strings['lang']).translate_batch(hollist) if self.strings['lang'] != 'ru' else hollist
        await utils.answer(m, f'{self.strings("base")}\n\n' + '\n'.join(res))
