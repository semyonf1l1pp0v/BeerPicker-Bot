from aiogram import Bot, Dispatcher, executor, types
from aiogram.utils.markdown import hbold
from config import token
from connection import collect_beer

bot = Bot(token=token, parse_mode=types.ParseMode.HTML)
dp = Dispatcher(bot=bot)


@dp.message_handler(commands="start")
async def start(message: types.Message):
    await message.answer("Добрый вечерочек. Давайте подберем пивчик для вас!")


@dp.message_handler(content_types=types.ContentType.TEXT)
async def get_user_beer_region(message: types.Message):
    await message.answer("Итак, для начала нужно определиться с регионом \
                        (Германия, Россия...)\n Введите регион:")
    beer_region = message.text
    await message.answer("Отлично, идем дальше...")
    return beer_region.lower()


@dp.message_handler(content_types=types.ContentType.TEXT)
async def get_user_beer_type(message: types.Message):
    await message.answer("Отлично, следующий вопрос: светлое или темное?\n Ваш выбор:")
    beer_type = message.text
    await message.answer("Принято. Осталось совсем немного!")
    return beer_type.lower() if beer_type.lower() == "светлое" else "темное"


@dp.message_handler(content_types=types.ContentType.TEXT)
async def get_user_beer_style(message: types.Message):
    await message.answer("Глобально пиво можно разделить на три категории:\
                        эль, лагер или смешанное\n Что предпочтете сегодня?:")
    beer_style = message.text
    await message.answer("Мы уже на финишной прямой нашего пивного забега...")
    return beer_style.lower()


@dp.message_handler(content_types=types.ContentType.TEXT)
async def get_user_beer_price_interval(message: types.Message):
    await message.answer("Глобально пиво можно разделить на три категории:\
                        эль, лагер или смешанное\n Что предпочтете сегодня?:")
    beer_style = message.text
    await message.answer("Мы уже на финишной прямой нашего пивного забега...")
    return beer_style.lower()


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
