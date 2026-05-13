from collections import UserDict


class Field:
    def __init__(self, value):
        self.value = value

    def __str__(self):
        return str(self.value)

# Клас для зберігання імені контакту. Обов'язкове поле
class Name(Field):
    def __init__(self, value):
        if not value:
            raise ValueError('Name is required') # Помилка якщо імʼя не додане
        super().__init__(value)

# Клас для зберігання номера телефону
class Phone(Field):
    def __init__(self, value):
        # Валідація номера телефону - повинен складатися з цифр і мати довжину 10 знаків
        if not value.isdigit() or len(value) != 10:
            raise ValueError(f'Phone number: "{value}" is incorrect')
        super().__init__(value)

# Клас для зберігання інформації про контакт, включаючи ім'я та список телефонів
class Record:
    def __init__(self, name):
        self.name = Name(name)
        self.phones = []

    # Метод який додає телефон відповідного формату у список контактів
    def add_phone(self, phone):
        self.phones.append(Phone(phone))

    # Метод видалення телефону зі списку контактів
    def remove_phone(self, phone):
        p = self.find_phone(phone)
        if p:
            self.phones.remove(p)

    # Метод заміни старого номеру телефону на новий
    def edit_phone(self, old_phone, new_phone):
        if old_phone == new_phone: # Перевірка, щоб номери не були однаковими
            raise ValueError('Cannot edit same phone')
        if not self.find_phone(old_phone): # Перевірка існування старого номера телефону
            raise ValueError(f'The phone not found')
        self.add_phone(new_phone)
        self.remove_phone(old_phone)

    # Метод для пошуку номера телефона в списку контактів, якщо не знайдено, то повертає None
    def find_phone(self, phone):
        return next((p for p in self.phones if p.value == phone), None)

    def __str__(self):
        return f"Contact name: {self.name.value}, phones: {'; '.join(p.value for p in self.phones)}"

# Клас для зберігання та управління записами
class AddressBook(UserDict):
    def add_record(self, record: Record):
        self.data[record.name.value] = record

    # Метод який знаходить запис за ім'ям. Якщо імʼя не знайдено, то повертає None
    def find(self, name):
        return self.data.get(name, None)

    # Метод який видаляє запис за ім'ям
    def delete(self, name):
        if name in self.data:
            del self.data[name]
        else:
            raise ValueError(f'The name: {name} does not exist') # Якщо імʼя не знайдено - виведе помилку

    def __str__(self):
        return '\n'.join(str(record) for record in self.data.values())


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

print(book)

# Знаходження та редагування телефону для John
john = book.find("John")
john.edit_phone("1234567890", "1112223333")

print(john)  # Виведення: Contact name: John, phones: 1112223333; 5555555555

# Пошук конкретного телефону у записі John
found_phone = john.find_phone("5555555555")
print(f"{john.name}: {found_phone}")  # Виведення: John: 5555555555

# Видалення запису Jane
book.delete("Jane")

