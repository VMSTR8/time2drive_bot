import os

from aiogram import types, Router, F
from aiogram.types import Document
from aiogram.fsm.context import FSMContext

import pandas as pd

from tortoise.transactions import in_transaction

from database.models import Event
from settings.settings import ADMIN_ID

router = Router()


@router.message(F.document)
async def excel_router(message: types.Message, state: FSMContext) -> None:
    """
    Handles Excel file uploads from admins, processes the data, and updates the database.

    This function performs the following steps:
    1. Verifies that the sender is an admin using their Telegram user ID.
    2. Checks that the uploaded file is a valid Excel file (.xlsx or .xls).
    3. Downloads the file to a temporary directory.
    4. Reads the Excel file using pandas and preprocesses the data:
       - Drops empty columns.
       - Limits to the first 6 columns.
       - Normalizes fields such as phone numbers and user IDs by removing non-digit characters.
    5. Clears the existing data in the Event table.
    6. Inserts the cleaned records into the database.
    7. Sends a success or error message back to the user.

    Parameters:
        message (types.Message): The Telegram message containing the document.
        state (FSMContext): The current FSM context to reset any previous state.

    Notes:
        - Only users listed in the ADMIN_ID environment variable are allowed to upload files.
        - The file is deleted from disk after processing, regardless of success or failure.

    Raises:
        Any exception that occurs during file download, parsing, or database operations
        is caught and reported back to the user.

    Returns:
        None
    """
    await state.clear()
    if message.from_user.id not in list(map(int, ADMIN_ID.split(','))):
        await message.answer('У вас нет доступа к работе с файлами.')
        return

    document: Document = message.document

    if not document.file_name.endswith((".xlsx", ".xls")):
        await message.answer("Пожалуйста, отправьте файл Excel (.xlsx или .xls).")
        return

    try:
        file_info = await message.bot.get_file(document.file_id)
        file_path = f'temp/{document.file_name}'
        os.makedirs('temp', exist_ok=True)
        await message.bot.download_file(file_info.file_path, destination=file_path)

        df = pd.read_excel(file_path)
        df = df.dropna(axis=1, how='all')
        df = df.iloc[:, :6]

        model_fields = {
            'user_id',
            'name',
            'car',
            'plate_number',
            'phone_number',
            'vip'
        }

        column_mapping = {
            'user_id': 0,
            'name': 1,
            'car': 2,
            'plate_number': 3,
            'phone_number': 4,
            'vip': 5
        }

        for column, idx in column_mapping.items():
            if column in model_fields:
                df[column] = df.iloc[:, idx].astype(str).str.replace(
                    r'\D', '', regex=True
                )

        if len(df.columns) < len(model_fields):
            await message.answer('В файле недостаточно столбцов.')

        records = []
        for index, row in df.iterrows():
            record = {}
            for field in model_fields:
                if field in column_mapping:
                    value = row[df.columns[column_mapping[field]]]
                    if isinstance(value, str):
                        value = value.lower()
                    record[field] = value
            records.append(record)

        async with in_transaction():
            await Event.all().delete()
            for row in records:
                await Event.create(**row)

        await message.answer('Таблица успешно загружена.')

    except Exception as error:
        await message.answer(f'Ошибка при обработке файла:\n{error}')
    finally:
        if os.path.exists(file_path):
            os.remove(file_path)
