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
2) __name__ == __main__ for parser.py + 
3) Split telegram_bot.py in 4? (states.py + , handlers.py ?, exceptions.py, main.py ?)
'''

bot = Bot(token=token, parse_mode=types.ParseMode.HTML)
storage = MemoryStorage()
dp = Dispatcher(bot=bot, storage=storage)


async def analyze_text_data(message):
    if message.text.replace(' ', '').lower() == "неважно":
        output = ''
    else:
        output = message.text.replace(' ', '').lower()
    await UserInput.next()
    sleep(2)
    return output


# Command /start to say hello and start interacting
@dp.message_handler(commands="start")
async def start(message: types.Message):
    await UserInput.waiting_for_region_input.set()
    await message.answer(f"Привет. Прямо сейчас в нашей базе содержится \
6059 разновидностей пива. Давайте подберем пиво для вас!")
    sleep(2)
    await bot.send_message(message.chat.id,
                           "Введите регион (Германия, Россия, ...)\nНе важно? Так и напишите:")


# Wait for user to write beer region
@dp.message_handler(state=UserInput.waiting_for_region_input)
async def get_user_beer_region(message: types.Message, state: FSMContext):
    beer_region = await analyze_text_data(message)
    await state.update_data(beer_region=beer_region)
    await bot.send_message(message.chat.id,
                           "Хорошо, следующий вопрос: светлое или темное (или не важно?)\nВаш выбор:")


# Wait for user to write beer style
@dp.message_handler(state=UserInput.waiting_for_type_input)
async def get_user_beer_type(message: types.Message, state: FSMContext):
    beer_type = await analyze_text_data(message)
    await message.answer("Принято. Осталось совсем немного!")
    await state.update_data(beer_type=beer_type)
    await bot.send_message(message.chat.id,
                           "Эль? Лагер? Может быть смешанное? А может все равно (не важно)?\nВыбирайте:")


# Wait for user to write beer type
@dp.message_handler(state=UserInput.waiting_for_style_input)
async def get_user_beer_style(message: types.Message, state: FSMContext):
    beer_style = await analyze_text_data(message)
    await state.update_data(beer_style=beer_style)
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
    sleep(2)
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
        sleep(1)
        await message.answer("И ваша рекомендация на сегодня...")
        sleep(2)
        call = collect_beer('*', region, beer_type, beer_style, low, high)
        ind = random.randint(0, len(call) - 1)
        beer_card = f"Название: {hbold(call[ind][1])}\n" \
                    f"Регион: {call[ind][2]}\n" \
                    f"Тип: {call[ind][3]}\n" \
                    f"Стиль: {call[ind][4]}\n" \
                    f"Крепость: {call[ind][5]}\n" \
                    f"Цена со скидкой: {call[ind][6]}\n" \
                    f"Цена без скидки: {call[ind][7]}\n" \
                    f"Объем: {call[ind][8]}\n" \
                    f"Изображение: {call[ind][9]}\n"

        await message.answer(beer_card)
        sleep(1)
    await message.answer("Для того, чтобы попробовать снова, введите '/start'")


def main():
    executor.start_polling(dp, skip_updates=True)


main()
