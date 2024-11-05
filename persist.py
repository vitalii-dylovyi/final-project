import pickle
from address_book import AddressBook
from pathlib import Path

FILENAME = str(Path(__file__).parent / "addressbook.pkl")


def save_data(book: AddressBook, filename=FILENAME):
    with open(filename, "wb") as f:
        pickle.dump(book, f)


def load_data(filename=FILENAME) -> AddressBook:
    try:
        with open(filename, "rb") as f:
            return pickle.load(f)
    except FileNotFoundError:
        return AddressBook()  # Повернення нової адресної книги, якщо файл не знайдено