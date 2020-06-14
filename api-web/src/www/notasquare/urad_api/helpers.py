
def translate_constant_select(field_value, choices):
    for (id, label) in choices:
        if field_value == id:
            return label
    return ''
