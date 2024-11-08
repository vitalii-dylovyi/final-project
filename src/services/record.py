from typing import Optional
from ..models.contact import (
    Name,
    Phone,
    Email,
    Address,
    Birthday,
    PhoneList,
    ValidationError,
)


class Record:
    def __init__(self, name: str):
        self.name = Name(name)
        self.phones = PhoneList()
        self.birthday: Optional[Birthday] = None
        self.email: Optional[Email] = None
        self.address: Optional[Address] = None

    def add_phone(self, phone: str) -> None:
        if self.find_phone(phone):
            raise ValidationError(f"Phone number {phone} already exists")
        self.phones.append(Phone(phone))

    def remove_phone(self, phone: str) -> None:
        normalized = Phone.normalize_phone(phone)
        original_length = len(self.phones)
        self.phones = PhoneList([p for p in self.phones if p.value != normalized])
        if len(self.phones) == original_length:
            raise ValidationError(f"Phone number {phone} not found")

    def edit_phone(self, old_phone: str, new_phone: str) -> None:
        old_normalized = Phone.normalize_phone(old_phone)
        for p in self.phones:
            if p.value == old_normalized:
                p.value = new_phone
                return
        raise ValidationError(f"Phone number {old_phone} not found")

    def find_phone(self, phone: str) -> Optional[Phone]:
        normalized = Phone.normalize_phone(phone)
        return next((p for p in self.phones if p.value == normalized), None)

    def add_birthday(self, birthday: str) -> None:
        self.birthday = Birthday(birthday)

    def add_email(self, email: str) -> None:
        self.email = Email(email)

    def add_address(self, address: str) -> None:
        self.address = Address(address)

    def __str__(self) -> str:
        parts = [f"Contact name: {self.name.value}"]
        if self.phones:
            parts.append(f"phones: {self.phones}")
        if self.email:
            parts.append(f"email: {self.email}")
        if self.address:
            parts.append(f"address: {self.address}")
        if self.birthday:
            parts.append(f"birthday: {self.birthday}")
        return ", ".join(parts)
