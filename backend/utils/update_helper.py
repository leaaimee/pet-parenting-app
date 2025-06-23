from pydantic import BaseModel
from typing import Any, Union

def apply_updates(
    obj: Any,
    update_data: Union[BaseModel, dict],
    empty_string_fields: set[str] = None,
    skip_fields: list[str] = None
):
    empty_string_fields = empty_string_fields or set()
    skip_fields = skip_fields or []

    # Convert BaseModel to dict if needed
    if isinstance(update_data, BaseModel):
        update_data = update_data.dict(exclude_unset=True)

    for field, value in update_data.items():
        if field in skip_fields:
            continue
        if value is None and field in empty_string_fields:
            setattr(obj, field, "")
        else:
            setattr(obj, field, value)
