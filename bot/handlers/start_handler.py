from aiogram import types, Router
from aiogram.filters import CommandStart
from aiogram.fsm.context import FSMContext

from utils.keyboards import generate_start_keyboard

router = Router()


@router.message(CommandStart())
async def start_router(message: types.Message, state: FSMContext) -> None:
    """
    Handles the /start command and sends a welcome message with usage instructions.

    Args:
        message (types.Message): The incoming message that triggered the /start command.
        state (FSMContext): The current finite state machine context.

    Behavior:
        - Clears any previous FSM state.
        - Sends a message explaining how to use the bot.
        - Attaches a start keyboard for user interaction.

    Return:
        None
    """
    await state.clear()
    await message.answer(
        text=f'Чат-бот выполняет функцию поиска участников фестиваля '
             f'по ФИО или по гос. номеру автомобиля.\n\n'
             f'Функция поиска по гос. номеру работает по первым 6-ти '
             f'символам гос. номера.',
        reply_markup=generate_start_keyboard()
    )
