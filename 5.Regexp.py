import csv
import re
from pprint import pprint
from collections import defaultdict

# # читаем адресную книгу в формате CSV в список contacts_list
with open("phonebook_raw.csv", encoding="utf-8") as f:
  rows = csv.reader(f, delimiter=",")
  contacts_list = list(rows)
pprint(contacts_list)
def split_full_name(contact):
    full_name = " ".join(contact[:3]).split()
    return full_name + [""] * (3 - len(full_name))
def normalize_phone(phone):
    pattern = r"(\+7|8)?\s*\(?(\d{3})\)?[\s-]*(\d{3})[\s-]*(\d{2})[\s-]*(\d{2})(\s*\(?(доб\.)\s*(\d+)\)?)?"
    subst = r"+7(\2)\3-\4-\5\6\7\8"
    return re.sub(pattern, subst, phone)

normalized_contacts = []
for contact in contacts_list:
    # Обрабатываем ФИО
    lastname, firstname, surname = split_full_name(contact)
    organization, position, phone, email = contact[3:7]
    phone = normalize_phone(phone)
    normalized_contacts.append([lastname, firstname, surname, organization, position, phone, email])

contacts_dict = defaultdict(lambda: ["", "", "", "", "", "", ""])

for contact in normalized_contacts:
    key = (contact[0], contact[1])  # Фамилия и Имя как ключ
    for i in range(2, 7):  # Индексы от 2 до 6 (всего 7 элементов)
        if not contacts_dict[key][i] and contact[i]:
            contacts_dict[key][i] = contact[i]


result_contacts = [list(key) + values for key, values in contacts_dict.items()]

# код для записи файла в формате CSV
with open("phonebook.csv", "w", encoding="utf-8") as f:
    datawriter = csv.writer(f, delimiter=',')
    datawriter.writerows([contacts_list[0]] + result_contacts)
