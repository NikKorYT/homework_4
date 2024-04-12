from collections import UserDict


class Field:
    def __init__(self, value):
        self.value = value

    # return the value of the field as a string
    def __str__(self):
        return str(self.value)


class Name(Field):
    # реалізація класу
    pass


class Phone(Field):
    # реалізація класу
    pass


class Record:
    def __init__(self, name):
        self.name = Name(name)
        self.phones = []

    # реалізація класу

    def __str__(self):
        return f"Contact name: {self.name.value}, phones: {'; '.join(p.value for p in self.phones)}"


class AddressBook(UserDict):
    
    def add_record(self, record):
        self.data[record.name.value] = record
        
    def find(self, name):
        return self.data[name]
    
    def delete(self, name):
        del self.data[name]


def input_error(func):
    def inner(*args, **kwargs):

        try:
            return func(*args, **kwargs)

        except ValueError:
            return "Please try again and add all nessesary arguments, or delete extra arguments."

        except KeyError:
            return "Invalid contact name. Please try again."

        except IndexError:
            return "Contact not found."

    return inner


@input_error
def main():
    """
    The function is controlling the cycle of command processing.
    """
    print("Welcome to the assistant bot!")
    contacts = {}
    while True:
        # Getting the input from the user
        user_input = input("\nEnter a command: ")
        command, *args = parse_input(user_input)

        # Checking the command and calling the appropriate function
        if command in ["close", "exit"]:
            print("Good bye!")
            break

        elif command == "hello":
            print("How can I help you?")

        elif command == "add":
            print(add_contact(args, contacts))

        elif command == "change":
            print(change_contact(args, contacts))

        elif command == "phone":
            print(get_phone(args, contacts))

        elif command == "all":
            print(print_all_contacts(contacts))

        # if the command is not recognized - print an error message
        else:
            print("Invalid command.")


@input_error
def parse_input(user_input) -> tuple:
    """Function is finding a command in the input and returns it"""
    # Splitting the input into words, first word is a command, other words are arguments
    cmd, *args = user_input.split()
    # Converting the command to lower case and deleting extra spaces
    cmd = cmd.strip().lower()
    return cmd, *args


@input_error
def add_contact(args, contacts) -> str:
    """Function is adding a contact to the contacts dictionary. Returns a message about the result."""
    # Getting the name and phone from the args
    name, phone = args
    contacts[name] = phone
    return "Contact added."


@input_error
def change_contact(args, contacts) -> str:
    """Function is changing the phone number for the contact in the contacts dictionary. Returns a message about the result."""
    name, phone = args
    # Try to access the contact in the dictionary
    _ = contacts[
        name  # This line will raise a KeyError if the name is not in the dictionary
    ]
    contacts[name] = phone
    return "Contact changed."


@input_error
def get_phone(args, contacts) -> str:
    """Function is getting the phone number for the contact from the contacts dictionary. Returns a message about the result."""
    name = args[0]
    if name in contacts:
        return f"The {name} phone number is: {contacts[name]}"
    else:
        return "Contact not found."


@input_error
def print_all_contacts(contacts) -> str:
    """Function is printing all contacts from the contacts dictionary. Returns a message about the result."""
    if contacts:
        for name, phone in contacts.items():
            print(f"{name}: {phone}")

        return "All contacts printed"
    else:
        return "No contacts found."


# decorator for handling input errors


if __name__ == "__main__":
    main()
