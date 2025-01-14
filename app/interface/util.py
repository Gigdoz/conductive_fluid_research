class Event():
    def __init__(self, state):
        self.state = state
    
    def get_state(self):
        return self.state
    
    def change_state(self):
        self.state = not self.state

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