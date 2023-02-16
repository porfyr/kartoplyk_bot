import openai
from aiogram import Bot, types
from aiogram.dispatcher import Dispatcher
from aiogram.utils import executor
import aiohttp

token = "6115860961:AAHMUTS-glE7t7sH80fGCHgWlplLUPVsDUI"
openai.api_key = "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"
proxy_url = "http://proxy.server:3128"
GET_IP_URL = 'http://bot.whatismyipaddress.com/'

bot = Bot(token=token, proxy=proxy_url)
dp = Dispatcher(bot)

async def fetch(url, proxy=None, proxy_auth=None):
    async with aiohttp.ClientSession() as session:
        async with session.get(url, proxy=proxy, proxy_auth=proxy_auth) as response:
            return await response.text()

def get_text(text):
    if text[:12] == "Картоплику, ":
        return text[12:].strip()
    elif text[:10] == "Картоплик ":
        return text[10:].strip()
    else:
        return "488"

@dp.message_handler(commands=['ty_de'])
async def echo(message: types.Message):
    await message.answer("Ти опять виходиш на связь мудила")
    print("на связі")
    

@dp.message_handler()
async def send(message: types.Message):
    text = get_text(message.text)
    if text != "488":
        print("\nПослано запит на openai API ...")
        response = openai.Completion.create(
            model="text-davinci-003",
            prompt="дай відповідь українською мовою, "+text, #"The following is a conversation with an AI assistant. The assistant is helpful, creative, clever, and very friendly.\n\nHuman: Hello, who are you?\nAI: I am an AI created by OpenAI. How can I help you today?\nHuman: I'd like to cancel my subscription.\nAI:",
            temperature=0.9,
            max_tokens=1000,
            top_p=1,
            frequency_penalty=0.0,
            presence_penalty=0.6,
            stop=[" You:", " AI:"]
        )
        await message.answer(response['choices'][0]['text'])
        print("текст:\n>"+text)
        print(response)
    else:
        print("\n\nФаріон не одобрила, пішов нахуй\n")


executor.start_polling(dp, skip_updates=True)
