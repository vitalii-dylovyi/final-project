from typing import List, Tuple, Callable
from .services.storage import AddressBook
from .services.notebook import NoteBook
from .services.record import Record
from .models.base import ValidationError


def input_error(func: Callable):
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except ValidationError as e:
            return f"Validation error: {str(e)}"
        except IndexError:
            return "Please provide all required arguments"
        except KeyError as e:
            return f"Not found: {str(e)}"
        except Exception as e:
            return f"An error occurred: {str(e)}"

    return wrapper


class Bot:
    def __init__(self):
        self.book = AddressBook()
        self.notebook = NoteBook()
        self.book.load_from_file()
        self.notebook.load_from_file()
        self._setup_commands()

    def _setup_commands(self):
        self.commands = {
            "add": self.add_contact,
            "change": self.change_contact,
            "phone": self.show_phone,
            "all": self.show_all,
            "find": self.find_contacts,
            "delete-contact": self.delete_contact,
            "add-birthday": self.add_birthday,
            "show-birthday": self.show_birthday,
            "birthdays": self.birthdays,
            "add-email": self.add_email,
            "add-address": self.add_address,
            "add-note": self.add_note,
            "show-note": self.show_note,
            "all-notes": self.show_all_notes,
            "delete-note": self.delete_note,
            "edit-note": self.edit_note,
            "add-tag": self.add_tag,
            "search-notes": self.search_notes,
            "search-tags": self.search_by_tags,
            "help": self.show_help,
            "hello": lambda _: "How can I help you?",
        }

    def save_data(self):
        self.book.save_to_file()

    def parse_input(self, user_input: str) -> Tuple[str, List[str]]:
        parts = user_input.strip().split()
        return (parts[0].lower(), parts[1:]) if parts else ("", [])

    @input_error
    def add_contact(self, args: List[str]) -> str:
        if len(args) < 2:
            raise IndexError
        name, phone = args[0], args[1]
        record = self.book.find(name)
        if record is None:
            record = Record(name)
            self.book.add_record(record)
            message = "Contact added."
        else:
            message = "Contact updated."
        record.add_phone(phone)
        self.save_data()
        return message

    @input_error
    def change_contact(self, args: List[str]) -> str:
        if len(args) < 3:
            raise IndexError
        name, old_phone, new_phone = args[0], args[1], args[2]
        record = self.book.find(name)
        if not record:
            raise KeyError(name)
        record.edit_phone(old_phone, new_phone)
        self.save_data()
        return "Phone number updated."

    @input_error
    def show_phone(self, args: List[str]) -> str:
        if not args:
            raise IndexError
        record = self.book.find(args[0])
        if not record:
            raise KeyError(args[0])
        return str(record)

    @input_error
    def show_all(self, _: List[str]) -> str:
        if not self.book.data:
            return "No contacts saved."
        return "\n".join(str(record) for record in self.book.data.values())

    @input_error
    def find_contacts(self, args: List[str]) -> str:
        if not args:
            raise IndexError
        query = args[0].lower()
        matches = []
        for record in self.book.data.values():
            if (
                query in record.name.value.lower()
                or any(query in phone.value for phone in record.phones)
                or (record.email and query in record.email.value.lower())
                or (record.address and query in record.address.value.lower())
            ):
                matches.append(str(record))
        return "\n".join(matches) if matches else "No matching contacts found."

    @input_error
    def delete_contact(self, args: List[str]) -> str:
        if not args:
            raise IndexError
        name = args[0]
        self.book.delete(name)
        self.save_data()
        return f"Contact {name} deleted."

    @input_error
    def add_birthday(self, args: List[str]) -> str:
        if len(args) < 2:
            raise IndexError
        name, birthday = args[0], args[1]
        record = self.book.find(name)
        if not record:
            raise KeyError(name)
        record.add_birthday(birthday)
        self.save_data()
        return "Birthday added."

    @input_error
    def show_birthday(self, args: List[str]) -> str:
        if not args:
            raise IndexError
        record = self.book.find(args[0])
        if not record:
            raise KeyError(args[0])
        if not record.birthday:
            return f"{args[0]} has no birthday set."
        return f"{args[0]}'s birthday: {record.birthday}"

    @input_error
    def birthdays(self, args: List[str]) -> str:
        days = int(args[0]) if args else 7
        upcoming = self.book.get_upcoming_birthdays(days)
        if not upcoming:
            return "No upcoming birthdays."
        return "\n".join(
            f"{b['name']}: {b['birthday']} (celebrate on {b['congratulation_date']})"
            for b in upcoming
        )

    @input_error
    def add_email(self, args: List[str]) -> str:
        if len(args) < 2:
            raise IndexError
        name, email = args[0], args[1]
        record = self.book.find(name)
        if not record:
            raise KeyError(name)
        record.add_email(email)
        self.save_data()
        return "Email added."

    @input_error
    def add_address(self, args: List[str]) -> str:
        if len(args) < 2:
            raise IndexError
        name = args[0]
        address = " ".join(args[1:])
        record = self.book.find(name)
        if not record:
            raise KeyError(name)
        record.add_address(address)
        self.save_data()
        return "Address added."

    def show_help(self, _: List[str]) -> str:
        return """Available commands:
    Contact Management:
    - add [name] [phone] - Add a new contact or phone
    - change [name] [old phone] [new phone] - Change existing phone
    - phone [name] - Show contact's phones
    - all - Show all contacts
    - find [query] - Search contacts
    - delete-contact [name] - Delete a contact
    - add-birthday [name] [DD.MM.YYYY] - Add birthday
    - show-birthday [name] - Show contact's birthday
    - birthdays [days] - Show upcoming birthdays
    - add-email [name] [email] - Add email
    - add-address [name] [address] - Add address

    Other Commands:
    - hello - Get a greeting
    - help - Show this help
    - exit/close - Exit the program"""

    def run(self) -> None:
        print("Welcome to the personal assistant! Type 'help' for commands.")
        while True:
            user_input = input("Enter a command: ").strip()
            command, args = self.parse_input(user_input)

            if command in ["close", "exit"]:
                self.save_data()
                print("Good bye!")
                break

            handler = self.commands.get(command)
            if handler:
                print(handler(args))
            else:
                print("Invalid command. Type 'help' for available commands.")
