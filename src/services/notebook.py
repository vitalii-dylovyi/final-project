from typing import Dict, List, Optional
import pickle
from ..models.base import Note


class NoteBook:
    def __init__(self):
        self.notes: Dict[str, Note] = {}

    def add_note(
        self, title: str, content: str, tags: Optional[List[str]] = None
    ) -> None:
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

    def add_tag(self, title: str, tag: str) -> None:
        if title not in self.notes:
            raise KeyError(f"Note '{title}' not found")
        self.notes[title].add_tag(tag)

    def remove_tag(self, title: str, tag: str) -> None:
        if title not in self.notes:
            raise KeyError(f"Note '{title}' not found")
        self.notes[title].remove_tag(tag)

    def search_by_tags(self, tags: List[str]) -> List[Note]:
        search_tags = set(tag.lower() for tag in tags)
        return [
            note for note in self.notes.values() if search_tags.intersection(note.tags)
        ]

    def search_by_text(self, query: str) -> List[Note]:
        query = query.lower()
        return [
            note
            for note in self.notes.values()
            if query in note.title.lower() or query in note.content.lower()
        ]

    def save_to_file(self, filename: str = "notebook.pkl") -> None:
        with open(filename, "wb") as f:
            pickle.dump(self.notes, f)

    def load_from_file(self, filename: str = "notebook.pkl") -> None:
        try:
            with open(filename, "rb") as f:
                self.notes = pickle.load(f)
        except FileNotFoundError:
            self.notes = {}
