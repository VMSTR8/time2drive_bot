from aiogram import types, Router, F
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup

from utils.excel_jobs import search_by_plate_number

router = Router()


class PlateSearch(StatesGroup):
    waiting_for_plate = State()


@router.message(F.text == 'Поиск по номеру')
async def ask_plate(message: types.Message, state: FSMContext):
    await state.clear()
    await state.set_state(PlateSearch.waiting_for_plate)
    await message.answer('Введи гос. номер автомобиля:')


@router.message(PlateSearch.waiting_for_plate)
async def process_plate_input(message: types.Message, state: FSMContext):
    search_text = message.text.strip().lower()
    results = search_by_plate_number(search_text)

    if search_text in {
        'поиск по фио',
    }:
        await message.answer('Вы вышли из режима поиска по номеру авто.')
        await state.clear()
        return

    for result in results:
        await message.answer(result)
