from address_book import AddressBook
from persist import load_data, save_data
import handlers


def parse_input(user_input: str):
    try:
        cmd, *args = user_input.split()
        cmd = cmd.strip().lower()
    except:
        cmd = ""
        args = []

    return cmd, args


def process_command(command: str, args: list[str], book: AddressBook) -> str:
    match command:
        case "hello":
            return "How can I help you?"

        case "add":
            return handlers.add_contact(args, book)

        case "change":
            return handlers.change_contact(args, book)

        case "phone":
            return handlers.show_phone(args, book)

        case "all":
            return handlers.show_all(book)

        case "add-birthday":
            return handlers.add_birthday(args, book)

        case "show-birthday":
            return handlers.show_birthday(args, book)

        case "birthdays":
            return handlers.birthdays(book)

        case _:
            return "Invalid command."


def main():
    book = load_data()
    print("Welcome to the assistant bot!")

    while True:
        user_input = input("Enter a command: ")
        command, args = parse_input(user_input)

        if command in ["close", "exit"]:
            print("Good bye!")
            break

        message = process_command(command, args, book)
        print(message)

    save_data(book)


if __name__ == "__main__":
    main()