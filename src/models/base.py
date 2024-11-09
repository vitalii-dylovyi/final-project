from datetime import datetime
from typing import Optional, Set


class ValidationError(Exception):
    pass


class Field:
    def __init__(self, value: str):
        self.validate(value)
        self._value = value

    @property
    def value(self):
        return self._value

    @value.setter
    def value(self, new_value: str):
        self.validate(new_value)
        self._value = new_value

    def validate(self, value: str):
        pass

    def __str__(self) -> str:
        return str(self._value)
    

    
class Note:
    def __init__(self, title: str, content: str, tags: Set[str] = None):
        self.title = title
        self.content = content
        self.tags = tags or set()
        self.created_at = datetime.now()
        self.modified_at = self.created_at


    def update_content(self, content: str) -> None:
        self.content = content
        self.modified_at = datetime.now()

    def __str__(self) -> str:
        tags_str = ", ".join(sorted(self.tags)) if self.tags else "No tags"
        return (
            f"Title: {self.title}\n"
            f"Content: {self.content}\n"
            f"Tags: {tags_str}\n"
            f"Created: {self.created_at:%Y-%m-%d %H:%M:%S}\n"
            f"Modified: {self.modified_at:%Y-%m-%d %H:%M:%S}"
        )
   

