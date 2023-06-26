from aiogram.dispatcher.filters.state import State, StatesGroup


# States for UserInput
class UserInput(StatesGroup):
    waiting_for_region_input = State()
    waiting_for_type_input = State()
    waiting_for_style_input = State()
    waiting_for_price_low_input = State()
    waiting_for_price_high_input = State()