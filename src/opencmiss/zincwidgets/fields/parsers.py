from numbers import Number

STRING_FLOAT_FORMAT = '{:.5g}'


def parse_to_vector(text):
    """
    Return real vector from comma separated text.
    """
    try:
        values = [float(value) for value in text.split(',')]
    except ValueError:
        values = []
    return values


def display_vector(values, number_format=STRING_FLOAT_FORMAT):
    """
    Display real vector values in a widget. Also handle scalar
    """
    if isinstance(values, Number):
        new_text = STRING_FLOAT_FORMAT.format(values)
    else:
        new_text = ", ".join(number_format.format(value) for value in values)

    return new_text

