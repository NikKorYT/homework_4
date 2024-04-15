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
    def __init__(self, value: str):
        super().__init__(value)

        # check if the phone number contains 10 digits
        if not value.isdigit() or len(value) != 10:
            raise ValueError("Phone number must contain 10 digits.")


class Record:
    def __init__(self, name):
        self.name = name
        self.phones = []

    def add_phone(self, phone):
        Phone(phone)
        self.phones.append(phone)

    def remove_phone(self, phone):
        self.phones.remove(phone)

    def edit_phone(self, phone, new_phone):
        self.phones[self.phones.index(phone)] = new_phone

    def find_phone(self, phone):
        # return phone
        return self.phones[self.phones.index(phone)]

    def __str__(self) -> str:
        return f"Contact name: {self.name}, phones: {'; '.join(p for p in self.phones)}"


class AddressBook(UserDict):

    def add_record(self, record: Record):
        self.data[record.name] = record

    def find(self, name) -> Record:
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

if __name__ == "__main__":
    #     main()
    # Створення нової адресної книги
    # Створення нової адресної книги
    book = AddressBook()

    # Створення запису для John
    john_record = Record("John")
    john_record.add_phone("1234567890")
    john_record.add_phone("5555555555")

    # Додавання запису John до адресної книги
    book.add_record(john_record)

    # Створення та додавання нового запису для Jane
    jane_record = Record("Jane")
    jane_record.add_phone("9876543210")
    book.add_record(jane_record)

    # Виведення всіх записів у книзі
    for name, record in book.data.items():
        print(record)

    # Знаходження та редагування телефону для John
    john = book.find("John")
    john.edit_phone("1234567890", "1112223333")

    print(john)  # Виведення: Contact name: John, phones: 1112223333; 5555555555

    # Пошук конкретного телефону у записі John
    found_phone = john.find_phone("5555555555")
    print(f"{john.name}: {found_phone}")  # Виведення: 5555555555

    # Видалення запису Jane
    book.delete("Jane")