from aiogram import Bot, Dispatcher, executor, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher import FSMContext
from aiogram.utils.markdown import hbold
import random
from time import sleep
from states import *
from config import token
from connection import collect_beer


# TODO:
'''
1) Take care of all user input exceptions
2) __name__ == __main__ for parser.py
3) Split telegram_bot.py in 4? (states.py + , handlers.py ?, exceptions.py, main.py ?)
'''

bot = Bot(token=token, parse_mode=types.ParseMode.HTML)
storage = MemoryStorage()
dp = Dispatcher(bot=bot, storage=storage)


# Command /start to say hello and start interacting
@dp.message_handler(commands="start")
async def start(message: types.Message):
    await UserInput.waiting_for_region_input.set()
    await message.answer("Добрый вечерочек. Давайте подберем пивчик для вас!")
    sleep(random.randint(1, 2))
    await bot.send_message(message.chat.id,
                           "Итак, для начала нужно определиться с регионом (Германия, Россия...)\nВведите регион:")


# Wait for user to write beer region
@dp.message_handler(state=UserInput.waiting_for_region_input)
async def get_user_beer_region(message: types.Message, state: FSMContext):
    beer_region = message.text.replace(' ', '').lower()
    await UserInput.next()
    await message.answer("Отлично, идем дальше...")
    await state.update_data(beer_region=beer_region)
    sleep(random.randint(1, 2))
    await bot.send_message(message.chat.id,
                           "Хорошо, следующий вопрос: светлое или темное?\nВаш выбор:")


# Wait for user to write beer style
@dp.message_handler(state=UserInput.waiting_for_type_input)
async def get_user_beer_type(message: types.Message, state: FSMContext):
    beer_type = message.text.replace(' ', '').lower()
    await UserInput.next()
    await message.answer("Принято. Осталось совсем немного!")
    await state.update_data(beer_type=beer_type)
    sleep(random.randint(1, 2))
    await bot.send_message(message.chat.id,
                           "Глобально пиво можно разделить на три категории: эль, лагер или смешанное\nЧто предпочтете сегодня?:")


# Wait for user to write beer type
@dp.message_handler(state=UserInput.waiting_for_style_input)
async def get_user_beer_style(message: types.Message, state: FSMContext):
    beer_style = message.text.replace(' ', '').lower()
    await UserInput.next()
    await state.update_data(beer_style=beer_style)
    await message.answer("Мы уже на финишной прямой нашего пивного забега...")
    sleep(random.randint(1, 2))
    await bot.send_message(message.chat.id, "Введите минимальную сумму, которую вы готовы потратить (только число):")


# Wait for user to write low beer price
@dp.message_handler(state=UserInput.waiting_for_price_low_input)
async def get_user_beer_price_low(message: types.Message, state: FSMContext):
    beer_price_low = message.text
    await UserInput.next()
    await state.update_data(beer_price_low=beer_price_low)
    await message.answer("А теперь введите максимальную сумму:")


# Wait for user to write high beer price and then give recommendations
@dp.message_handler(state=UserInput.waiting_for_price_high_input)
async def get_user_beer_price_high(message: types.Message, state: FSMContext):
    beer_price_high = message.text
    await UserInput.next()
    await state.update_data(beer_price_high=beer_price_high)

    await bot.send_message(message.chat.id, "Щас посмотрим че у нас тут есть")
    sleep(random.randint(1, 2))
    data = await state.get_data()

    region = data.get("beer_region")
    beer_type = data.get("beer_type")
    beer_style = data.get("beer_style")
    beer_price_low = data.get("beer_price_low")
    beer_price_high = data.get("beer_price_high")
    low = min(beer_price_low, beer_price_high)
    high = max(beer_price_low, beer_price_high)

    if collect_beer('count(*)', region, beer_type, beer_style, low, high)[0][0] == 0:
        await message.answer("По вашему запросу ничего не найдено")
    else:
        await message.answer(f"Рекомендаций по вашему запросу: "
                             f"{collect_beer('count(*)', region, beer_type, beer_style, low, high)[0][0]}")

        call = collect_beer('*', region, beer_type, beer_style, low, high)
        for i in range(len(call)):
            beer_card = f"Название: {hbold(call[i][1])}\n" \
                        f"Регион: {call[i][2]}\n" \
                        f"Тип: {call[i][3]}\n" \
                        f"Стиль: {call[i][4]}\n" \
                        f"Крепость: {call[i][5]}\n" \
                        f"Цена со скидкой: {call[i][6]}\n" \
                        f"Цена без скидки: {call[i][7]}\n" \
                        f"Объем: {call[i][8]}\n"

            await message.answer(beer_card)


def main():
    executor.start_polling(dp, skip_updates=True)


main()
