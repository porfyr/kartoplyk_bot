import openai
import aiohttp
import datetime
from aiogram import Bot, types
from aiogram.dispatcher import Dispatcher
from aiogram.utils import executor


token = "<>"
openai.api_key = "<>"
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
def get_text(message: types.Message):
    text = message.text
    if text[:12] == "Картоплику, ":
        return ("--force_ua", text[12:].strip())
    elif text[:10] == "Картоплик ":
        return ("--force_ua", text[10:].strip())
    elif text[:10] == ":noprefix ":
        return ("--noprefix", text[10:].strip())
    elif message.chat.type == "private":
        return ("--force_ua", text.strip())
    elif message.reply_to_message != None and message.reply_to_message.from_user.username == "kartoplyk_bot":
        return ("--force_ua", text.strip())
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
    await message.answer("На связі")
    try:
        _ = get_openai_responce("hehe")
    except openai.error.AuthenticationError:
        await message.answer("Виплюнувся токен openai")
    except RuntimeWarning:
            await message.answer("Перевикористано токен openai, потрібно вставити новий з іншого акаунту")
    except Exception as e:
        await message.answer("Хз чому не роблю, будіть розраба")
        print("\n!{")
        print(e)
        print("}!\n")
        _ = get_openai_responce("hehe")
    print("на связі))")



# main message handler #
@dp.message_handler()
async def reaction(message: types.Message):
    (parameter, text) = get_text(message)
    t0 = datetime.datetime.now()
    prefix = "дай відповідь українською мовою, " if parameter == "--force_ua" else ""
    if text != "488":
        chat_name = message.chat.title if message.chat.title != None else "пп"
        print("\nПослано "+(parameter+" " if parameter == "--noprefix" else "")+"запит на openai API ...        ", str(chat_name), "|", datetime.datetime.now().strftime("%m.%d %H:%M:%S"))
        print("текст: "+text)
        try:
            response = get_openai_responce(prefix+text)
            await message.reply(response['choices'][0]['text'])
        except openai.error.AuthenticationError:
            await message.answer("Сервер сплюнув токен, пишіть розрабу чи тому хто його знає щоб вставив новий")
        except RuntimeWarning:
            await message.answer("Швидше всього перевикористано токен openai, потрібно вставити новий з іншого акаунта")
        except:
            await message.answer("В такому разі хз чому не робе, будіть розраба")
        else:
            d_time = round((datetime.datetime.now() - t0).total_seconds())
            print("\n"+"текст: "+text)
            print("Отвєт:", response['choices'][0]['text'][1:]+"\n"+"Δ", str(d_time)+"s"+"\n")
    else:
        print("не канає")



executor.start_polling(dp, skip_updates=True)

#Δ