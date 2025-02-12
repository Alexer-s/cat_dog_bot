import os
import requests

from dotenv import load_dotenv
from telegram import ReplyKeyboardMarkup
from telegram.ext import (
    ApplicationBuilder, CommandHandler,
    filters, MessageHandler
)


load_dotenv()

# URL_CAT = 'https://api.thecatapi.com/v1/images/search'
# URL_DOG = 'https://api.thedogapi.com/v1/images/search'
token = os.getenv('TOKEN', 'token')
# kit_dog_bot = Bot(token=token)
kit_dog_aplication = ApplicationBuilder().token(token).build()


async def start(update, context):
    message = ('Привет, я бот, который постарается улучшить твое настроение. '
               'Просто нажимай кнопки и получай удовольствие.')
    buttons = ReplyKeyboardMarkup(
        [['Покажи котика', 'Покажи собачку',],],
        resize_keyboard=True
    )
    await context.bot.send_message(
        update.effective_chat.id,
        text=message,
        reply_markup=buttons
    )


async def send_cat_dog(update, context):
    if update.effective_message.text == 'Покажи котика':
        url = 'https://api.thecatapi.com/v1/images/search'
    else:
        url = 'https://api.thedogapi.com/v1/images/search'
    user_chat_id = update.effective_chat.id
    cat_photo_url = requests.get(url).json()[0].get('url')
    await context.bot.send_photo(user_chat_id, cat_photo_url)


cat_dog_handler = MessageHandler(
    filters.Text(['Покажи котика', 'Покажи собачку']),
    send_cat_dog
)
start_handler = CommandHandler('start', start)
kit_dog_aplication.add_handler(cat_dog_handler)
kit_dog_aplication.add_handler(start_handler)

kit_dog_aplication.run_polling()
