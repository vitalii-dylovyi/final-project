from collections import UserDict
from record import Record
from datetime import date, datetime, timedelta
from fields import Birthday


class AddressBook(UserDict[str, Record]):
    def add_record(self, record: Record):
        self.data[record.name.value] = record

    def find(self, name: str) -> Record | None:
        if name in self.data:
            return self.data[name]

        return None

    def delete(self, name: str):
        if name in self.data:
            del self.data[name]

    def get_upcoming_birthdays(self) -> list[dict[str, str]]:
        today_date = datetime.today().date()
        upcoming_birthdays = []

        for record in self.data.values():
            if not record.birthday:
                continue

            birthday_date = record.birthday.value.date()
            congratulation_date = birthday_date.replace(year=today_date.year)

            if congratulation_date < today_date:
                # if the user already had birthday this year we set congratulation_date on the next year
                congratulation_date = congratulation_date.replace(
                    year=today_date.year + 1
                )

            days_before_birthday = (congratulation_date - today_date).days

            if days_before_birthday < 7:
                week_days_left = 7 - congratulation_date.weekday()

                if week_days_left <= 2:
                    # if congratulations date is weekend - shift it on monday
                    congratulation_date += timedelta(days=week_days_left)

                congratulation_date_str = date.strftime(
                    congratulation_date, Birthday.DATE_FORMAT
                )

                upcoming_birthdays.append(
                    {
                        "name": record.name.value,
                        "congratulation_date": congratulation_date_str,
                    }
                )

        return upcoming_birthdays