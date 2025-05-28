from datetime import datetime, date



from typing import Optional
from datetime import date

def pet_birthday(
    birthday: Optional[date],
    birth_year: Optional[int],
    birth_month: Optional[int]
) -> tuple[Optional[date], Optional[int], Optional[int]]:
    """
    Returns (birthday, birth_year, birth_month)

    If full birthday is provided, uses that.
    Otherwise returns (None, birth_year, birth_month) for partial input.
    """
    if birthday:
        return birthday, birthday.year, birthday.month
    return None, birth_year, birth_month




# def pet_birthday(birth_year, birth_month, birth_day):
#     """ setting exact or approximate birthday date """
#     try:
#         current_year = datetime.now().year
#
#         if isinstance(birth_year, int) and 1900 <= birth_year <= current_year:
#             if isinstance(birth_month, int) and 1 <= birth_month <= 12:
#                 if isinstance(birth_day, int):
#                     try:
#                         return date(birth_year, birth_month, birth_day), None, None
#                     except ValueError:
#                         return None, None, None
#                 return None, birth_year, birth_month
#             return None, birth_year, None
#         return None, None, None
#
#     except Exception as e:
#         print("Unexpected error in pet_birthday:", e)
#         return None, None, None