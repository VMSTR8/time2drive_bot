from asyncio import sleep

from aiogram import types, Router, F
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup

from tortoise.expressions import Q

from database.models import Event

router = Router()


class Search(StatesGroup):
    """
    FSM states for user search flow.

    States:
        waiting_for_plate: Awaiting input of a license plate.
        waiting_for_name: Awaiting input of a participant's full name.
    """
    waiting_for_plate = State()
    waiting_for_name = State()


def format_event_entry(entry) -> str:
    """
    Formats a database event entry into a human-readable message.

    Args:
        entry: A single Event instance containing participant data.

    Returns:
        str: A formatted string with participant details, ready to be sent as a message.
    """
    name = ' '.join(word.capitalize() for word in str(entry.name).split())
    car = str(entry.car).capitalize()
    plate = str(entry.plate_number).upper()
    phone = entry.phone_number
    vip = '<b>⚠️ Является VIP⚠️ </b>' if str(entry.vip) not in (None, 'nan', '') else ''

    try:
        user_id = int(float(entry.user_id))
    except (ValueError, TypeError):
        user_id = 'Не присвоен'

    return (
        f'Номер участника: {user_id}\n'
        f'ФИО: {name}\n'
        f'Авто: {car}\n'
        f'Гос. номер: {plate}\n'
        f'Номер телефона: {phone}\n'
        f'{vip}'
    )


@router.message(F.text == 'Поиск по номеру')
async def ask_plate(message: types.Message, state: FSMContext) -> None:
    """
    Initiates the vehicle registration plate search by setting the appropriate FSM state.

    Args:
        message (types.Message): The user's message triggering the search.
        state (FSMContext): The current FSM context.

    Return:
        None
    """
    await state.clear()
    await state.set_state(Search.waiting_for_plate)
    await message.answer('Введите гос. номер автомобиля:')


@router.message(F.text == 'Поиск по ФИО')
async def ask_name(message: types.Message, state: FSMContext) -> None:
    """
    Initiates the name search by setting the appropriate FSM state.

    Args:
        message (types.Message): The user's message triggering the search.
        state (FSMContext): The current FSM context.

    Return:
        None
    """
    await state.clear()
    await state.set_state(Search.waiting_for_name)
    await message.answer('Введите ФИО участника:')


@router.message(Search.waiting_for_plate)
async def process_plate_search(message: types.Message, state: FSMContext) -> None:
    """
    Processes the user input for vehicle registration plate search and returns matching entries.

    Args:
        message (types.Message): The message containing the license plate.
        state (FSMContext): The current FSM context.

    Behavior:
        - Converts input to lowercase and strips whitespace.
        - Matches it against the beginning of each stored plate number.
        - Sends formatted results back to the user.

    Return:
        None
    """
    try:
        search_text = message.text.strip().lower()
    except AttributeError:
        await message.answer(
            'Поиск по номеру прекращен, так как был отправлен '
            'не текстовый тип данных.'
        )
        await state.clear()
        return

    all_entries = await Event.all()

    results = [
        entry for entry in all_entries
        if search_text in str(entry.plate_number).lower().replace(' ', '')[:6]
    ]

    if not results:
        await message.answer('Ничего не найдено по введенному номеру.')
        return

    for entry in results:
        await message.answer(format_event_entry(entry))
        await sleep(0.5)


@router.message(Search.waiting_for_name)
async def process_name_search(message: types.Message, state: FSMContext) -> None:
    """
    Processes the user input for name search and returns matching entries.

    Args:
        message (types.Message): The message containing the name.
        state (FSMContext): The current FSM context.

    Behavior:
        - Converts input to lowercase and strips whitespace.
        - Performs a case-insensitive partial match in the database.
        - Sends formatted results back to the user.
    Return:
        None
    """
    try:
        search_text = message.text.strip().lower()
    except AttributeError:
        await message.answer(
            'Поиск по ФИО прекращен, так как был отправлен '
            'не текстовый тип данных.'
        )
        await state.clear()
        return

    results = await Event.filter(
        Q(name__icontains=search_text)
    ).all()

    if not results:
        await message.answer('Ничего не найдено по введенным ФИО.')

    for entry in results:
        await message.answer(format_event_entry(entry))
        await sleep(0.5)
