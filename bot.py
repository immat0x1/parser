import sys
import requests
from bs4 import BeautifulSoup, Comment
from aiogram import Bot, Dispatcher, executor, types
import logging
import base64

b64 = "NTQxMzA5MTI5NjpBQUhTZlFXNEZDbC11eHM2QnNhRmo2WVFBVlZkSVNzbmNzTQ=="
bot = Bot(token=base64.b64decode(base64_message.encode('ascii')).decode('ascii'), parse_mode=types.ParseMode.MARKDOWN_V2)
dp = Dispatcher(bot)
logging.basicConfig(level=logging.INFO)

@dp.message_handler(commands="ugatu")
async def parseUgatu(message: types.Message):
    msg = message.text.split()
    snils = msg[1]
    url = "https://www.ugatu.su/abitur/bachelor-and-specialist/admission-ratings"
    r = requests.get(url)
    options = BeautifulSoup(r.text, 'html.parser').find('select', id="id_specialty").findAll('option')
    options.pop(0)
    ids = sorted(set([k['value'] for k in options]), key=int)
    snils = snils[:3] + "-" + snils[3:6] + "-" + snils[6:9] + " " + snils[9:]
    for id in ids:
        cnt = 1
        institution = "УГАТУ" # Филиал+в+г.+Ишимбае | Филиал+в+г.+Кумертау | УГАТУ
        funding = "Бюджетная+основа" # Полное+возмещение+затрат | Бюджетная+основа
        level = "Бакалавриат" # Бакалавриат | Специалитет
        form = "Очная" # Очная | Заочная | Очно-заочная
        soup = BeautifulSoup(requests.get(url + "/?institution=" + institution + "&funding=" + funding + "&education_level=" + level + "&education_form=" + form + "&specialty=" + id).text, 'html.parser')
        tables = soup.findAll('table')
        info = soup.findAll('div', {"class": "info"})
        if len(tables) == 0: return
        cells = tables[3].findAll('tr')
        for i in cells:
            data = cells[cells.index(i)].findAll('td')
            if snils == data[2].text:
    	        await message.answer(f"`{BeautifulSoup(r.text, 'html.parser').find('option', value=id).text}`" + '\n\n' + f"Место по баллам: {data[0].text}" + '\n' + f"Место по зачислениям: {cnt}" + '\n' + info[3].text.replace('\n', '').replace('  ', '').replace('.', '\n'))
    	        break
            else:
    	        if data[8].text == 'Да':
    	            cnt += 1

@dp.message_handler(commands="ugntu")
async def parseUgntu(message: types.Message):
    msg = message.text.split()
    snils = msg[1]
    url = "https://ams.rusoil.net/abitonline/onlinepeople_list.php"
    comment = BeautifulSoup(requests.get(url).text, 'html.parser').find(text=lambda text:isinstance(text, Comment))
    options = BeautifulSoup("". join(comment), 'html.parser').findAll('option')
    ids = sorted(set([k['value'] for k in options]), key=int)
    for id in ids:
        cnt = 1
        soup = BeautifulSoup(requests.get(url + "?id=" + id).text, 'html.parser')
        cells = soup.findAll('tr')
        for cell in cells:
    	    if snils in cell.text:
    	        num = cells[cells.index(cell)].find('td', align="center").text
    	        await message.answer(f"`{BeautifulSoup(''. join(comment), 'html.parser').find('option', value=id).text}`" + '\n\n' + f"Место по баллам: {num.replace('. ', '')}" + '\n' + f"Место по зачислениям: {cnt}")
    	        break
    	    else:
    	        if "Согласие на зачисление" in cell.text:
    	            cnt += 1

if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)