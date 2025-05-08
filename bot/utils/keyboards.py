from aiogram.types import ReplyKeyboardMarkup, KeyboardButton


def generate_start_keyboard() -> ReplyKeyboardMarkup:
    """
    Generates the start keyboard markup with search options.

    Returns:
        ReplyKeyboardMarkup: A keyboard with two buttons:
            - Search by Name
            - Search by Plate Number
    """
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
