import pandas as pd

from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import StatesGroup, State
from aiogram.utils.callback_data import CallbackData

from db import DBDriver

instance = CallbackData("button", "action")


class UserInput(StatesGroup):
    file = State()


def get_keyboard():
    keyboard = types.InlineKeyboardMarkup(row_width=1)
    buttons = [
        types.InlineKeyboardButton(text="Добавить сайт", callback_data=instance.new(action="add_site")),
    ]
    keyboard.add(*buttons)
    return keyboard


async def start(message: types.Message):
    await message.answer("Добро пожаловать в TestBot Mayak! Чтобы добавить сайт для парсинга, нажмите кнопку ниже",
                         reply_markup=get_keyboard())


async def from_button(call: types.CallbackQuery, callback_data: dict):
    if callback_data["action"] == "add_site":
        await UserInput.file.set()
        await call.message.answer(
            "Загрузите excel файл или просто перетащите его в диалоговое окно. "
            "Для выхода введите команду /cancel"
        )


async def user_answer(message: types.Message, state: FSMContext):
    await state.update_data(file=message.document)
    data = await state.get_data()
    from bot import bot
    file = await bot.download_file_by_id(data['file']['file_id'])
    await state.finish()
    df = pd.read_excel(file, sheet_name='Лист1')
    await save_to_db(df, message)
    await message.answer("Спасибо, ваш файл принят")


async def save_to_db(dataframe, message):
    driver = DBDriver("sqlite3")
    for index, row in dataframe.iterrows():
        driver.add_url(row)
        await message.answer(list(row))


async def cancel(message: types.Message, state: FSMContext):
    current_state = await state.get_state()
    if current_state is None:
        await message.answer("Нечего отменять")
    else:
        await state.finish()
        await message.answer("Действие отменено")


async def catch_other_message(message: types.Message):
    await message.answer("Неизвестный тип сообщения")
