def unpack(value):
    value = value.get()
    if isinstance(value, int):
        if value:
            return True
        return False

    value = list(map(float, value.split()))
    if len(value) == 0:
        raise ValueError("Пустое поле")
    elif len(value) == 1:
        value = value[0]
    return value