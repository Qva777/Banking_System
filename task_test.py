# pip install python-dateutil
from dateutil import parser


def get_date_from_str(input_str: str):
    """ Parses a given string and attempts to convert it into a standard date format (YYYY-MM-DD) """
    input_str = input_str.strip()
    latvian_dates = {
        'gada': '',
        'jūnijā': 'June',
        'maijs': 'May',
    }

    for latvian_word, english_month in latvian_dates.items():
        input_str = input_str.replace(latvian_word, english_month)

    try:
        parsed_date = parser.parse(input_str, fuzzy=True)
        return parsed_date.strftime('%Y-%m-%d')
    except (ValueError, TypeError):
        return None


date_strings = [
    '2023-06-06',
    '2023.06.12',
    '09.06.2023',
    '2023. gada 31. maijs ',
    '21-03-2023',
    '12.06.2023',
    '2023 gada 12 jūnijā.',
    '13th June, 2023',
    'Rudens'
]

for i, date_str in enumerate(date_strings):
    date_result = get_date_from_str(date_str)
    print(f"{i + 1}:\t{date_result if date_result else 'Not a valid date'}")
