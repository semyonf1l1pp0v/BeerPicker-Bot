from aiogram import Bot, Dispatcher, executor, types
from aiogram.utils.markdown import hbold
from config import token
from connection import collect_beer

bot = Bot(token=token, parse_mode=types.ParseMode.HTML)
dp = Dispatcher(bot=bot)


@dp.message_handler(commands="start")
async def start(message: types.Message):
    await message.answer("Добрый вечерочек. Какой пивандесик интересует?")

# ("Название", "Регион", "Тип", "Стиль", "Крепость", "Цена со скидкой", "Цена без скидки", "Объем")
@dp.message_handler(commands="allbeer")
async def start(message: types.Message):
    await message.answer("Щас посмотрим че у нас тут есть")
    call = collect_beer('', '', 0, 1000000)
    for i in range(len(call)):
        beer_card = f"Название: {hbold(call[i][1])}\n"\
                    f"Регион: {call[i][2]}\n"\
                    f"Тип: {call[i][3]}\n"\
                    f"Стиль: {call[i][4]}\n"\
                    f"Крепость: {call[i][5]}\n"\
                    f"Цена со скидкой: {call[i][6]}\n" \
                    f"Цена без скидки: {call[i][7]}\n" \
                    f"Объем: {call[i][8]}\n"

        await message.answer(beer_card)


def main():
    executor.start_polling(dp)


main()
