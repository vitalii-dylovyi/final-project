from decorators import input_error
from address_book import AddressBook
from record import Record

type Args = list[str]


def get_record(name: str, book: AddressBook) -> Record:
    record = book.find(name)

    if not record:
        raise KeyError("Contact not found")

    return record


@input_error
def add_contact(args: Args, book: AddressBook) -> str:
    name, phone = args

    record = book.find(name)

    message = "Contact updated."

    if not record:
        record = Record(name)
        book.add_record(record)
        message = "Contact added."

    record.add_phone(phone)

    return message


@input_error
def change_contact(args: Args, book: AddressBook) -> str:
    name, old_phone, new_phone = args

    record = get_record(name, book)

    record.edit_phone(old_phone, new_phone)

    return "Contact changed."


@input_error
def show_phone(args: Args, book: AddressBook) -> str:
    (name,) = args

    record = get_record(name, book)

    return ", ".join(phone.value for phone in record.phones)


def show_all(book: AddressBook) -> str:
    sep_line = f"\n{"-"*20}\n"
    return (
        "\n"
        + "All contacts:"
        + sep_line
        + sep_line.join(str(record) for record in book.values())
        + "\n"
    )


@input_error
def add_birthday(args: Args, book: AddressBook) -> str:
    name, birthday = args

    record = get_record(name, book)

    message = "Birthday updated" if record.birthday else "Birthday added"

    record.add_birthday(birthday)

    return message


@input_error
def show_birthday(args: Args, book: AddressBook) -> str:
    (name,) = args

    record = get_record(name, book)

    if record.birthday:
        return str(record.birthday)

    return "Birthday not added yet"


@input_error
def birthdays(book: AddressBook) -> str:
    birthdays = book.get_upcoming_birthdays()

    if not len(birthdays):
        return "No upcoming birthdays"

    sep_line = f"\n{"-"*20}\n"
    return (
        "\n"
        + "Upcoming birthdays:"
        + sep_line
        + "\n".join(
            f"{birthday['name']:<15}: {birthday['congratulation_date']}"
            for birthday in birthdays
        )
        + sep_line
    )