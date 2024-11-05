from fields.field import Field
from datetime import datetime


class Birthday(Field[datetime]):
    DATE_FORMAT = "%d.%m.%Y"

    def __init__(self, birthday_str: str):
        try:
            birth_date = datetime.strptime(birthday_str, Birthday.DATE_FORMAT)
            super().__init__(birth_date)
        except ValueError:
            raise ValueError("Invalid date format. Use DD.MM.YYYY")

    def __str__(self):
        if self.value:
            return self.value.strftime(Birthday.DATE_FORMAT)

        return ""