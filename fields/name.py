from fields.field import Field


class Name(Field[str]):
    def __init__(self, name: str):
        super().__init__(name)