def apply_updates(record, data_dict, empty_string_fields=None):
    empty_string_fields = empty_string_fields or set()

    for field, value in data_dict.items():
        if value is None and field in empty_string_fields:
            setattr(record, field, "")
        else:
            setattr(record, field, value)