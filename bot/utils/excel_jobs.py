import os
import re
import pandas as pd


def find_excel_file_by_name(name: str = 'base') -> str | None:
    for ext in ('xlsx', 'xls', 'xlsm'):
        filename = f'{name}.{ext}'
        if os.path.exists(filename):
            return filename
        return None


def regex_plate(text: str) -> str:
    return re.sub(r'\s+', '', text).lower()


def search_by_plate_number(search_text: str) -> list[str]:
    file_path = find_excel_file_by_name('base')
    if not file_path:
        return ['Файл base с Excel-расширением не найден.']

    df = pd.read_excel(file_path)
    result = []

    for _, row in df.iterrows():
        value = str(row.iloc[3])
        regex_value = regex_plate(value)
        if search_text in regex_value:
            filter_result = [str(x) for x in row.values if pd.notna(x)]
            result.append('\n'.join(filter_result))

    return result or ['Ничего не найдено']
