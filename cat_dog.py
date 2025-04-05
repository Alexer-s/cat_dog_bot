import os
import requests

from dotenv import load_dotenv
from telegram import ReplyKeyboardMarkup
from telegram.ext import (
    ApplicationBuilder, CommandHandler,
    filters, MessageHandler
)


load_dotenv()

token = os.getenv('TOKEN', 'token')
ADMIN_ID = int(os.getenv('ADMIN_ID', '12345'))
kit_dog_aplication = ApplicationBuilder().token(token).build()
data: dict[int, dict] = {}
buttons = ReplyKeyboardMarkup(
    [['Покажи котика', 'Покажи собачку',],],
    resize_keyboard=True
)


def add_data(update):
    if data.get(update.effective_chat.id) is None:
        data[update.effective_chat.id] = {
            'name': update.effective_chat.username,
            'count': 0
        }


async def reporting(update, context):
    if update.effective_chat.id == ADMIN_ID:
        if data:
            message = f'Количество гостей - {len(data)}:'
            for user_data in data.values():
                message += f"\n- {user_data['name']} - количество заказов: {user_data['count']}"
            await context.bot.send_message(
                ADMIN_ID,
                text=message,
                reply_markup=buttons,
            )
        else:
            await context.bot.send_message(
                ADMIN_ID,
                text='Посещений нет.',
                reply_markup=buttons,
            )
    else:
        await context.bot.send_message(
            update.effective_chat.id,
            text='Нет прав!',
            reply_markup=buttons,
        )


async def start(update, context):
    add_data(update)
    message = ('Привет, я бот, который постарается улучшить твое настроение. '
               'Просто нажимай кнопки и получай удовольствие.')
    await context.bot.send_message(
        update.effective_chat.id,
        text=message,
        reply_markup=buttons
    )


async def send_cat_dog(update, context):
    add_data(update)
    data[update.effective_chat.id]['count'] += 1
    if update.effective_message.text == 'Покажи котика':
        url = 'https://api.thecatapi.com/v1/images/search'
    else:
        url = 'https://api.thedogapi.com/v1/images/search'
    user_chat_id = update.effective_chat.id
    cat_photo_url = requests.get(url).json()[0].get('url')
    await context.bot.send_photo(
        user_chat_id,
        cat_photo_url,
    )


cat_dog_handler = MessageHandler(
    filters.Text(['Покажи котика', 'Покажи собачку']),
    send_cat_dog
)
reporting_handler = MessageHandler(
    filters.Text(['Отчет',]),
    reporting
)
start_handler = CommandHandler('start', start)
kit_dog_aplication.add_handler(cat_dog_handler)
kit_dog_aplication.add_handler(reporting_handler)
kit_dog_aplication.add_handler(start_handler)

kit_dog_aplication.run_polling()
