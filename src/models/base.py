class ValidationError(Exception):
    pass


class Field:
    def __init__(self, value: str):
        self.validate(value)
        self._value = value

    @property
    def value(self):
        return self._value

    @value.setter
    def value(self, new_value: str):
        self.validate(new_value)
        self._value = new_value

    def validate(self, value: str):
        pass

    def __str__(self) -> str:
        return str(self._value)
