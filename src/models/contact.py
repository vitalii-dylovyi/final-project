from collections import UserList
from datetime import datetime
import re
from .base import Field, ValidationError


class Name(Field):
    def validate(self, value: str):
        if not value or not value.strip():
            raise ValidationError("Name cannot be empty")
        if not all(char.isalnum() or char.isspace() for char in value):
            raise ValidationError("Name can only contain letters, numbers, and spaces")


class Email(Field):
    def validate(self, value: str):
        pattern = r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$"
        if not re.match(pattern, value):
            raise ValidationError("Invalid email format")


class Address(Field):
    def validate(self, value: str):
        if not value or not value.strip():
            raise ValidationError("Address cannot be empty")


class PhoneList(UserList):
    def __str__(self) -> str:
        return f"{'; '.join(p.value for p in self.data)}"


class Phone(Field):
    def validate(self, value: str):
        digits = "".join(filter(str.isdigit, value))
        if len(digits) != 10:
            raise ValidationError("Phone number must contain exactly 10 digits")
        self._value = digits

    @staticmethod
    def normalize_phone(phone: str) -> str:
        return "".join(filter(str.isdigit, phone))


class Birthday(Field):
    def __init__(self, value: str):
        self.validate(value)
        self._value = datetime.strptime(value, "%d.%m.%Y").date()

    def validate(self, value: str):
        try:
            date = datetime.strptime(value, "%d.%m.%Y").date()
            if date > datetime.now().date():
                raise ValidationError("Birthday cannot be in the future")
            self._value = date
        except ValueError:
            raise ValidationError("Invalid date format. Use DD.MM.YYYY")

    def __str__(self) -> str:
        return self._value.strftime("%d.%m.%Y")
