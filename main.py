import openai
from aiogram import Bot, types
from aiogram.dispatcher import Dispatcher
from aiogram.utils import executor
import aiohttp

token = "<токен бота>"
openai.api_key = "<токен openai>"
proxy_url = "http://proxy.server:3128"
GET_IP_URL = 'http://bot.whatismyipaddress.com/'
bot = Bot(token=token, proxy=proxy_url)
dp = Dispatcher(bot)


# увімкнення проксі для https://www.pythonanywhere.com/ що аб'юзить порт telegram api
async def fetch(url, proxy=None, proxy_auth=None):
    async with aiohttp.ClientSession() as session:
        async with session.get(url, proxy=proxy, proxy_auth=proxy_auth) as response:
            return await response.text()


# фільтр тексту
def get_text(text):
    if text[:12] == "Картоплику, ":
        return ("--force_ua", text[12:].strip())
    elif text[:10] == "Картоплик ":
        return ("--force_ua", text[10:].strip())
    elif text[:10] == ":noprefix ":
        return ("--noprefix", text[10:].strip())
    else:
        return ("nth", "488")


# надання відповіді openai
def get_openai_responce(text):
    resp = openai.Completion.create(
                model="text-davinci-003",
                prompt=text,
                temperature=0.9,
                max_tokens=1000,
                top_p=1,
                frequency_penalty=0.0,
                presence_penalty=0.6,
                stop=[" You:", " AI:"]
    )
    return resp


# прийом перевірочної команди
@dp.message_handler(commands=['ty_de'])
async def echo(message: types.Message):
    # ip = await fetch(GET_IP_URL)
    # ip = await fetch(GET_IP_URL, bot.proxy, bot.proxy_auth)
    await message.answer("Я тутай")
    try:
        response = get_openai_responce("hehe")
    except openai.error.AuthenticationError:
        await message.answer("Виплюнувся токен openai")
    except:
        await message.answer("Невідома помилка команди /ty_de, пишіть розрабу або тому хто його знає")
    print("на связі))")



# main message handler #
@dp.message_handler()
async def send(message: types.Message):
    (parameter, text) = get_text(message.text)
    if text != "488" and parameter == "--force_ua":
        chat_name = message.chat.title if message.chat.title != None else "пп"
        print("\nПослано запит на openai API ...        ", message.from_user.full_name, "@"+message.from_user.username, "|", chat_name)
        try:
            response = get_openai_responce( "дай відповідь українською мовою, "+text )
            await message.answer(response['choices'][0]['text'])
        except openai.error.AuthenticationError:
            await message.answer("Сервер сплюнув токен, пишіть розрабу чи тому хто його знає щоб вставив новий")
        except:
            await message.answer("Невідома помилка модуля send, пишіть розрабу або тому хто його знає")
        else:
            print("текст:\n>"+text+"\n")
            # print(response)
    elif text != "488" and parameter == "--noprefix":
        chat_name = message.chat.title if message.chat.title != None else "пп"
        print("\nПослано --noprefix запит на openai API ...        ", message.from_user.full_name, "@"+message.from_user.username, "|", chat_name)
        try:
            response = get_openai_responce( text )
            await message.answer(response['choices'][0]['text'])
        except openai.error.AuthenticationError:
            await message.answer("Сервер сплюнув токен, пишіть розрабу чи тому хто його знає щоб вставив новий")
        except:
            await message.answer("Невідома помилка модуля send, пишіть розрабу або тому хто його знає")
        else:
            print("текст:\n>"+text+"\n")
            # print(response)
    else:
        print("не канає")


executor.start_polling(dp, skip_updates=True)