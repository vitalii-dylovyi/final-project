from typing import List, Tuple, Callable, Optional
from difflib import get_close_matches
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
            "remove-tag": self.remove_tag,
            "search-notes": self.search_notes,
            "search-tags": self.search_by_tags,
            "help": self.show_help,
            "hello": lambda _: "How can I help you?",
        }

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
