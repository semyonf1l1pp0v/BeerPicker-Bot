from aiogram import Bot, Dispatcher, executor, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Text
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.types import ParseMode
from aiogram.utils.markdown import hbold
from config import token
from connection import collect_beer

bot = Bot(token=token, parse_mode=types.ParseMode.HTML)
storage = MemoryStorage()
dp = Dispatcher(bot=bot, storage=storage)


# определение состояний
class UserInput(StatesGroup):
    waiting_for_region_input = State()
    waiting_for_type_input = State()
    waiting_for_style_input = State()
    waiting_for_price_low_input = State()
    waiting_for_price_high_input = State()


@dp.message_handler(commands="start")
async def start(message: types.Message):
    await UserInput.waiting_for_region_input.set()
    await message.answer("Добрый вечерочек. Давайте подберем пивчик для вас!")
    await bot.send_message(message.chat.id,
                           "Итак, для начала нужно определиться с регионом (Германия, Россия...)\nВведите регион:")


# обработчик пользовательского ввода
@dp.message_handler(state=UserInput.waiting_for_region_input)
async def get_user_beer_region(message: types.Message, state: FSMContext):
    beer_region = message.text.strip().lower()
    await UserInput.next()
    await message.answer("Отлично, идем дальше...")
    await state.update_data(beer_region=beer_region)
    await bot.send_message(message.chat.id,
                           "Хорошо, следующий вопрос: светлое или темное?\nВаш выбор:")
    # return beer_region


@dp.message_handler(state=UserInput.waiting_for_type_input)
async def get_user_beer_type(message: types.Message, state: FSMContext):
    beer_type = message.text.strip().lower() if message.text.strip().lower() == "светлое" else "темное"
    # await UserInput.next()
    await message.answer("Принято. Осталось совсем немного!")
    await state.update_data(beer_type=beer_type)

    await bot.send_message(message.chat.id, "Щас посмотрим че у нас тут есть")
    region = await state.get_data()
    region1 = region.get("beer_region")
    beer_type = await state.get_data()
    beer_type1 = beer_type.get("beer_type")
    call = collect_beer(region1, beer_type1, 80, 200)
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
    # return beer_type


#
# @dp.message_handler(state=UserInput.waiting_for_style_input)
# async def get_user_beer_style(message: types.Message, state: FSMContext):
#     await bot.send_message(message.chat.id,
#                            "Глобально пиво можно разделить на три категории: эль, лагер или смешанное\nЧто предпочтете сегодня?:")
#     beer_style = message.text
#     await UserInput.next()
#     await message.answer("Мы уже на финишной прямой нашего пивного забега...")
#     await state.update_data(beer_style=beer_style)
#     return beer_style
#
#
# @dp.message_handler(state=UserInput.waiting_for_region_input)
# async def get_user_beer_price_interval(message: types.Message, state: FSMContext):
#     await bot.send_message(message.chat.id, "Введите минимальную сумму, которую вы готовы потратить (только число):")
#     beer_price_low = message.text
#     await UserInput.next()
#     await message.answer("А теперь введите максимальную сумму:")
#     await state.update_data(beer_price_low=beer_price_low)
#     beer_price_high = message.text
#     await state.update_data(beer_price_high=beer_price_high)
#     beer_price_interval = [beer_price_low, beer_price_high]
#     await state.finish()
#     return beer_price_interval


# async def recommend_beer(message: types.Message, state: FSMContext):


# async def recommend(message: types.Message):
#     await bot.send_message(message.chat.id, "Щас посмотрим че у нас тут есть")
#     call = collect_beer(get_user_beer_region, '', 0, 1000000)
#     for i in range(len(call)):
#         beer_card = f"Название: {hbold(call[i][1])}\n" \
#                     f"Регион: {call[i][2]}\n" \
#                     f"Тип: {call[i][3]}\n" \
#                     f"Стиль: {call[i][4]}\n" \
#                     f"Крепость: {call[i][5]}\n" \
#                     f"Цена со скидкой: {call[i][6]}\n" \
#                     f"Цена без скидки: {call[i][7]}\n" \
#                     f"Объем: {call[i][8]}\n"
#
#         await message.answer(beer_card)

# await bot.send_message(message.chat.id, "Хорошо, следующий вопрос: светлое или темное?\n Ваш выбор:")
# beer_type = message.text.lower() if message.text.lower() == "светлое" else "темное"
# await message.answer("Принято. Осталось совсем немного!")
#
# await bot.send_message(message.chat.id, "Глобально пиво можно разделить на три категории:\
#                             эль, лагер или смешанное\n Что предпочтете сегодня?:")
# beer_style = message.text
# await message.answer("Мы уже на финишной прямой нашего пивного забега...")
#
# await bot.send_message(message.chat.id, "Введите минимальную сумму, которую вы готовы потратить (только число):")
# beer_price_low = message.text
# await message.answer("А теперь введите максимальную сумму:")
# beer_price_high = message.text
# price_interval = [beer_price_low, beer_price_high]
#
# await bot.send_message(message.chat.id, "Щас посмотрим че у нас тут есть")
# call = collect_beer(beer_region, '', 0, 1000000)
# for i in range(len(call)):
#     beer_card = f"Название: {hbold(call[i][1])}\n" \
#                 f"Регион: {call[i][2]}\n" \
#                 f"Тип: {call[i][3]}\n" \
#                 f"Стиль: {call[i][4]}\n" \
#                 f"Крепость: {call[i][5]}\n" \
#                 f"Цена со скидкой: {call[i][6]}\n" \
#                 f"Цена без скидки: {call[i][7]}\n" \
#                 f"Объем: {call[i][8]}\n"
#
#     await message.answer(beer_card)


#
# @dp.message_handler(content_types=types.ContentType.TEXT)
# async def get_user_beer_region(message: types.Message):
#     await bot.send_message(message.chat.id, "Итак, для начала нужно определиться с регионом \
#                         (Германия, Россия...)\n Введите регион:")
#     beer_region = message.text
#     await message.answer("Отлично, идем дальше...")
#     return beer_region.lower()
#
#
# @dp.message_handler(content_types=types.ContentType.TEXT)
# async def get_user_beer_type(message: types.Message):
#     await bot.send_message(message.chat.id, "Отлично, следующий вопрос: светлое или темное?\n Ваш выбор:")
#     beer_type = message.text
#     await message.answer("Принято. Осталось совсем немного!")
#     return beer_type.lower() if beer_type.lower() == "светлое" else "темное"
#
#
# @dp.message_handler(content_types=types.ContentType.TEXT)
# async def get_user_beer_style(message: types.Message):
#     await bot.send_message(message.chat.id, "Глобально пиво можно разделить на три категории:\
#                             эль, лагер или смешанное\n Что предпочтете сегодня?:")
#     beer_style = message.text
#     await message.answer("Мы уже на финишной прямой нашего пивного забега...")
#     return beer_style.lower()
#
#
# @dp.message_handler(content_types=types.ContentType.TEXT)
# async def get_user_beer_price_interval(message: types.Message):
#     await bot.send_message(message.chat.id, "Введите минимальную сумму, которую вы готовы потратить (только число):")
#     beer_price_low = message.text
#     await message.answer("А теперь введите максимальную сумму:")
#     beer_price_high = message.text
#     price_interval = [beer_price_low, beer_price_high]
#     return price_interval
#
#
# async def recommend(message: types.Message):
#     await bot.send_message(message.chat.id, "Щас посмотрим че у нас тут есть")
#     call = collect_beer(get_user_beer_region(), '', 0, 1000000)
#     for i in range(len(call)):
#         beer_card = f"Название: {hbold(call[i][1])}\n" \
#                     f"Регион: {call[i][2]}\n" \
#                     f"Тип: {call[i][3]}\n" \
#                     f"Стиль: {call[i][4]}\n" \
#                     f"Крепость: {call[i][5]}\n" \
#                     f"Цена со скидкой: {call[i][6]}\n" \
#                     f"Цена без скидки: {call[i][7]}\n" \
#                     f"Объем: {call[i][8]}\n"
#
#         await message.answer(beer_card)
#

# ("Название", "Регион", "Тип", "Стиль", "Крепость", "Цена со скидкой", "Цена без скидки", "Объем")
# @dp.message_handler(commands="allbeer")
# async def start(message: types.Message):
#     await message.answer("Щас посмотрим че у нас тут есть")
#     call = collect_beer('', '', 0, 1000000)
#     for i in range(len(call)):
#         beer_card = f"Название: {hbold(call[i][1])}\n"\
#                     f"Регион: {call[i][2]}\n"\
#                     f"Тип: {call[i][3]}\n"\
#                     f"Стиль: {call[i][4]}\n"\
#                     f"Крепость: {call[i][5]}\n"\
#                     f"Цена со скидкой: {call[i][6]}\n" \
#                     f"Цена без скидки: {call[i][7]}\n" \
#                     f"Объем: {call[i][8]}\n"
#
#         await message.answer(beer_card)
def main():
    executor.start_polling(dp, skip_updates=True)


main()
