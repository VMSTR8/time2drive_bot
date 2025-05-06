from aiogram import types, Router
from aiogram.filters import CommandStart
from aiogram.fsm.context import FSMContext

from utils.keyboards import generate_start_keyboard

router = Router()


@router.message(CommandStart())
async def start_router(message: types.Message, state: FSMContext):
    await state.clear()
    user = message.from_user.first_name
    await message.answer(
        text=f'Привет {user}',
        reply_markup=generate_start_keyboard()
    )
