"""
Service layer for the Memok personal assistant.

Contains business logic for managing contacts and notes.
"""

from .storage import AddressBook
from .notebook import NoteBook
from .record import Record

__all__ = ["AddressBook", "NoteBook", "Record"]
