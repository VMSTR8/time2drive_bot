from aiogram.types import ReplyKeyboardMarkup, KeyboardButton


def generate_start_keyboard() -> ReplyKeyboardMarkup:
    keyboard = ReplyKeyboardMarkup(
        keyboard=[
            [
                KeyboardButton(text='Поиск по ФИО'),
                KeyboardButton(text='Поиск по номеру')
            ]
        ],
        resize_keyboard=True
    )
    return keyboard
