from fields.field import Field
import re


class Phone(Field[str]):
    def __init__(self, phone_number: str):
        if not re.match(r"^\d{10}$", phone_number):
            raise ValueError(f"Phone {phone_number} is not valid")

        super().__init__(phone_number)