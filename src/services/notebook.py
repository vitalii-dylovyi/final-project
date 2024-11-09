from typing import Dict, List, Optional
import pickle
from ..models.base import Note

class NoteBook:
    def __init__(self):
        self.notes: Dict[str, Note] = {}

    def add_note(self, title: str, content: str, tags: Optional[List[str]] = None) -> None:
        if title in self.notes:
            raise KeyError(f"Note with title '{title}' already exists")
        self.notes[title] = Note(title, content, set(tags) if tags else set())

    def find_note(self, title: str) -> Optional[Note]:
        return self.notes.get(title)

    def update_note(self, title: str, content: str) -> None:
        if title not in self.notes:
            raise KeyError(f"Note '{title}' not found")
        self.notes[title].update_content(content)

    def delete_note(self, title: str) -> None:
        if title not in self.notes:
            raise KeyError(f"Note '{title}' not found")
        del self.notes[title]


    def get_all_notes(self) -> List[Note]:
        return list(self.notes.values())


  