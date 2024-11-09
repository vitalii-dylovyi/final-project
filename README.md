# Memok Personal Assistant

A comprehensive command-line personal assistant that helps you manage contacts and notes.

## Installation

```bash
pip install .
```

## Usage

After installation, you can run the assistant from anywhere using:

```bash
memok
```

## Features

### Contact Management

- Store and manage contacts with names, addresses, phone numbers, emails, and birthdays
- Search contacts by various criteria
- Edit and delete contacts
- View upcoming birthdays
- Validate phone numbers and email addresses

### Note Management

- Create and manage text notes
- Add tags to notes for better organization
- Search notes by content or tags
- Edit and delete notes

### Smart Command Recognition

- The assistant tries to guess what command you want to execute based on your input
- Suggests the closest matching command if an exact match is not found

## Available Commands

### Contact Management

- `add [name] [phone]` - Add a new contact or phone
- `change [name] [old phone] [new phone]` - Change existing phone
- `phone [name]` - Show contact's phones
- `all` - Show all contacts
- `find [query]` - Search contacts
- `delete-contact [name]` - Delete a contact
- `add-birthday [name] [DD.MM.YYYY]` - Add birthday
- `show-birthday [name]` - Show contact's birthday
- `birthdays [days]` - Show upcoming birthdays
- `add-email [name] [email]` - Add email
- `add-address [name] [address]` - Add address

### Note Management

- `add-note [title] [content]` - Add a new note
- `show-note [title]` - Show a specific note
- `all-notes` - Show all notes
- `delete-note [title]` - Delete a note
- `edit-note [title] [new content]` - Edit a note
- `add-tag [title] [tag]` - Add a tag to a note
- `remove-tag [title] [tag]` - Remove a tag from a note
- `search-notes [query]` - Search notes by text
- `search-tags [tag1] [tag2] ...` - Search notes by tags

### Other Commands

- `hello` - Get a greeting
- `help` - Show help
- `exit/close` - Exit the program
