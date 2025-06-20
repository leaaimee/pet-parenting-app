from typing import Optional, Tuple
from datetime import date

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from backend.models.pets_models import Pets
from backend.domain.exceptions import NotFoundError



def pet_birthday(
    year: Optional[int] = None,
    month: Optional[int] = None,
    day: Optional[date] = None,
) -> Tuple[Optional[date], Optional[int], Optional[int]]:
    """
    Normalize the pet’s birthday information into:
      (birthday: date | None,
       birth_year: int    | None,
       birth_month: int   | None)

    - If `day` is provided (a full date), we extract year/month/day.
    - Else if only `year` + `month` are provided, we pick the 1st of that month.
    - Else if only `year` is provided, we default to January 1st of that year.
    - Otherwise, we return (None, None, None).
    """
    if day:
        # Full date given
        return day, day.year, day.month

    if year and month:
        # Year + month known, approximate to first day of month
        try:
            approx = date(year, month, 1)
            return approx, year, month
        except ValueError:
            # Bad month (e.g. month=13)? Fall back to January 1st
            approx = date(year, 1, 1)
            return approx, year, 1

    if year:
        # Only year known, approximate to January 1st
        approx = date(year, 1, 1)
        return approx, year, 1

    # Nothing known
    return None, None, None



async def verify_pet_access(pet_id: int, user_id: int, session: AsyncSession) -> Pets:
    result = await session.execute(
        select(Pets).where(Pets.id == pet_id, Pets.parent_id == user_id)
    )
    pet = result.scalar_one_or_none()
    if not pet:
        raise NotFoundError("Pet not found or access denied.")
    return pet








