from typing import List, Tuple, Callable, Optional
from .services.storage import AddressBook
from .services.notebook import NoteBook
from .services.record import Record
from .models.base import ValidationError
from difflib import get_close_matches


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
            "remove-tag": self.remove_tag,
            "search-notes": self.search_notes,
            "search-tags": self.search_by_tags,
            "help": self.show_help,
            "hello": lambda _: "How can I help you?",
        }

    def find_closest_command(self, user_input: str) -> Optional[str]:
        words = user_input.lower().split()
        all_commands = list(self.commands.keys())
        for word in words:
            matches = get_close_matches(word, all_commands, n=1, cutoff=0.6)
            if matches:
                return matches[0]
        return None

    def save_data(self):
        self.book.save_to_file()
        self.notebook.save_to_file()

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

    @input_error
    def add_note(self, args: List[str]) -> str:
        if len(args) < 2:
            raise IndexError
        title = args[0]
        content = " ".join(args[1:])
        self.notebook.add_note(title, content)
        self.save_data()
        return "Note added."

    @input_error
    def show_note(self, args: List[str]) -> str:
        if not args:
            raise IndexError
        note = self.notebook.find_note(args[0])
        if not note:
            raise KeyError(args[0])
        return str(note)

    @input_error
    def show_all_notes(self, _: List[str]) -> str:
        notes = self.notebook.get_all_notes()
        if not notes:
            return "No notes saved."
        return "\n\n".join(str(note) for note in notes)

    @input_error
    def delete_note(self, args: List[str]) -> str:
        if not args:
            raise IndexError
        self.notebook.delete_note(args[0])
        self.save_data()
        return "Note deleted."

    @input_error
    def edit_note(self, args: List[str]) -> str:
        if len(args) < 2:
            raise IndexError
        title = args[0]
        content = " ".join(args[1:])
        self.notebook.update_note(title, content)
        self.save_data()
        return "Note updated."

    @input_error
    def add_tag(self, args: List[str]) -> str:
        if len(args) < 2:
            raise IndexError
        title, tag = args[0], args[1]
        self.notebook.add_tag(title, tag)
        self.save_data()
        return "Tag added."

    @input_error
    def remove_tag(self, args: List[str]) -> str:
        if len(args) < 2:
            raise IndexError
        title, tag = args[0], args[1]
        self.notebook.remove_tag(title, tag)
        self.save_data()
        return "Tag removed."

    @input_error
    def search_notes(self, args: List[str]) -> str:
        if not args:
            raise IndexError
        query = " ".join(args)
        notes = self.notebook.search_by_text(query)
        if not notes:
            return "No matching notes found."
        return "\n\n".join(str(note) for note in notes)

    @input_error
    def search_by_tags(self, args: List[str]) -> str:
        if not args:
            raise IndexError
        notes = self.notebook.search_by_tags(args)
        if not notes:
            return "No notes found with specified tags."
        return "\n\n".join(str(note) for note in notes)

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

    Note Management:
    - add-note [title] [content] - Add a new note
    - show-note [title] - Show a specific note
    - all-notes - Show all notes
    - delete-note [title] - Delete a note
    - edit-note [title] [new content] - Edit a note
    - add-tag [title] [tag] - Add a tag to a note
    - remove-tag [title] [tag] - Remove a tag from a note
    - search-notes [query] - Search notes by text
    - search-tags [tag1] [tag2] ... - Search notes by tags


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
                closest = self.find_closest_command(user_input)
                if closest:
                    print(f"Command not found. Did you mean '{closest}'?")
                else:
                    print("Invalid command. Type 'help' for available commands.")
