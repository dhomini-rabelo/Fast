from datetime import date


fdn = lambda date_number : str(date_number) if int(date_number) >= 10 else f'0{date_number}' # format date number


def format_simple_date(date_obj: date):
    return f'{fdn(date_obj.day)}/{fdn(date_obj.month)}/{date_obj.year}'


def format_simple_date_for_default(date_obj: date):
    return f'{date_obj.year}-{fdn(date_obj.month)}-{fdn(date_obj.day)}'