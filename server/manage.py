import psycopg2

from guests import HashTable, Item
from rooms import Tree, Node
from registration import List, Element


class Manager:
    def __init__(self):
        self.tree = Tree()
        self.table = HashTable(200)
        self.linked_list = List()

        self.connection = psycopg2.connect(user="postgres",
                                           password="1111",
                                           host="127.0.0.1",
                                           port="5432",
                                           database="hoteldb")
        self.cursor = self.connection.cursor()

    # Передавать данные с qt

    def fill_structures(self):
        # Заполнение гостей
        self.cursor.execute("select * from guests")
        guests = self.cursor.fetchall()
        for guest in guests:
            self.add_to_table(guest[0], guest[1], str(guest[2]), str(guest[3]), guest[4])

        # Заполнение комнат
        self.cursor.execute("select * from rooms")
        rooms = self.cursor.fetchall()
        for room in rooms:
            self.add_to_tree(*room)

        # Заполнение регистраций
        self.cursor.execute("select * from registrations")
        regs = self.cursor.fetchall()
        for reg in regs:
            if reg[-1] == "Заселение":
                self.move_in(*reg[:-1])
            else:
                self.depart(*reg[:-1])

    def add_to_table(self, key, full_name, year_of_birth, address, reason, to_bd=False):
        item = Item(key, full_name, year_of_birth, address, reason)
        try:
            msg = (True, "Гость успешно добавлен", "addGuestform") if self.table.add(item) else \
                (False, "Гость с таким паспортом уже существует", "addGuestform")
        except AttributeError:
            msg = (False, "Некорректные данные гостя", "addGuestform")

        if to_bd and msg[0]:
            self.cursor.execute(
                "insert into guests (passport_id, fullname, year_of_birth, address, reason) values (%s, %s, %s, %s, %s)",
                (key, full_name, int(year_of_birth), address, reason))
            self.connection.commit()

        return msg

    def add_to_tree(self, room_id, capacity, rooms, bathroom, equipment, to_bd=False):
        node = Node(room_id, capacity, rooms, bathroom, equipment)
        try:
            msg = (True, "Комната успешно добавлена", "addRoomForm") if self.tree.add(node) else \
                (False, "Комната с таким номером уже существует", "addRoomForm")
        except AttributeError:
            msg = False, "Некорректные данные комнаты", "addRoomForm"

        if to_bd and msg[0]:
            self.cursor.execute(
                "insert into rooms (room_id, capacity, rooms_count, bathroom, equipment) values (%s, %s, %s, %s, %s)",
                (room_id, capacity, rooms, bathroom, equipment))
            self.connection.commit()

        return msg

    def delete_from_table(self, key):
        item = self.table.find_by_id(key)
        if not item:
            return False, "Нет гостя с такими данными", "deleteGuestForm"
        elif item[1]:
            return False, "Невозможно удалить гостя, заселенного в комнату", "deleteGuestForm"

        self.table.delete(key)

        self.cursor.execute("delete from guests where passport_id = %s", (key,))
        self.connection.commit()

        return True, "Данные о госте успешно удалены", "deleteGuestForm"

    def delete_from_tree(self, room_id):
        if not (room_id and room_id[0].isalpha() and all(i.isdigit() for i in room_id[1:])):
            return False, "Некорректный номер комнаты", "deleteRoomForm"
        node = self.tree.find_by_id(int(room_id[1:]))
        if not node:
            return False, "Нет комнаты с таким номером", "deleteRoomForm"
        elif node[1]:
            return False, "Невозможно удалить непустую комнату", "deleteRoomForm"
        self.tree.delete(int(room_id[1:]))

        self.cursor.execute("delete from rooms where room_id = %s", (room_id,))
        self.connection.commit()

        return True, "Данные о комнате успешно удалены", "deleteRoomForm"

    def find_by_id_in_table(self, key):
        data = self.table.find_by_id(key)
        if data:
            if data[1]:
                res = data[0].split("\n")
                res[-1] = f"Гостиничный номер: {self.tree.get_room_id(data[1])}"
                data = '\n'.join(res)
            else:
                data = data[0]
            return True, "Гость найден", "findGuestByIdForm", "findGuest", data
        return False, "Нет такого гостя", "findGuestByIdForm"

    def find_by_id_in_tree(self, room_id):
        if not (room_id and room_id[0].isalpha() and all(i.isdigit() for i in room_id[1:])):
            return False, "Некорректный номер комнаты", "findRoomByIdForm"

        data = self.tree.find_by_id(int(room_id[1:]))
        if data:
            result = '\n\t'.join([', '.join(self.table.get_info_by_id(i)) for i in data[1]])
            data = data[0].split("\n")
            data.append(f"Гости:\t {result}" if result else "Гостей нет")

            return True, "Комната найдена", "findRoomByIdForm", "findRoom", '\n'.join(data)
        return False, "Нет такой комнаты", "findRoomByIdForm"

    def find_by_fullname(self, fullname):
        if not fullname or fullname.isspace():
            return False, "Пустая строка", "findGuestByFioForm"
        arr = self.table.find_by_full_name(self.__find_substring, fullname)
        if arr:
            return True, "Гости найдены", "findGuestByFioForm", "findGuest", '\n------\n'.join(['\n'.join(i) for i in arr])
        return False, "Нет гостей с таким ФИО", "findGuestByFioForm"

    def find_by_equipment(self, equipment):
        if not equipment or equipment.isspace():
            return False, "Пустая строка", "findRoomByEquipmentForm"
        arr = self.tree.find_by_equipment(self.__find_substring, equipment)
        if arr:
            return True, "Комнаты найдены", "findRoomByEquipmentForm", "findRoom", '\n------\n'.join(arr)
        return False, "Нет комнат с таким оборудованием", "findRoomByEquipmentForm"

    def clear_table(self):
        self.table.clear(self.tree)
        self.linked_list.clear()

        self.cursor.execute("delete from guests")
        self.cursor.execute("delete from registrations")
        self.connection.commit()

        return True, "Данные о гостях удалены", "clearGuests"

    def clear_tree(self):
        self.tree.clear(self.table)
        self.linked_list.clear()

        self.cursor.execute("delete from rooms")
        self.cursor.execute("delete from registrations")
        self.connection.commit()

        return True, "Данные о комнатах удалены", "clearRooms"

    def view_table(self):
        return True, "Найдены все гости", "findAllGuests", "findGuest", str(self.table)

    def view_tree(self):
        return True, "Найдены все комнаты", "findAllRooms", "findRoom", str(self.tree)

    def move_in(self, room, person, date_check_in, date_depart, to_bd=False):
        if not (room and room[0].isalpha() and all(i.isdigit() for i in room[1:])):
            return False, "Некорректный номер комнаты", "moveInForm"

        status = "Заселение"
        room_id = int(room[1:])
        is_success, msg = self.__check_registration(person, room, date_check_in, date_depart, status)

        if not is_success:
            return False, msg, "moveInForm"

        element = Element(person, room, date_check_in, date_depart, status)
        if not self.table.update_room(person, room_id, is_add=True):
            return False, "Гость уже заселен в другую комнату", "moveInForm"
        if not self.tree.update_guests(room_id, person, is_add=True):
            return False, "Комната переполнена", "moveInForm"

        if to_bd:
            self.cursor.execute("""insert into registrations (room_key, guest, date_check_in, date_depart, status) 
                                            values (%s, %s, %s, %s, %s)""",
                                (room, person, date_check_in, date_depart, status))
            self.connection.commit()

        self.linked_list.add(element)

        return True, "Гость успешно заселен", "moveInForm", "findRegistrations", str(self.linked_list)

    def depart(self, room, person, date_check_in, date_depart, to_bd=False):
        if not (room and room[0].isalpha() and all(i.isdigit() for i in room[1:])):
            return False, "Некорректный номер комнаты", "departForm"

        status = "Выселение"
        room_id = int(room[1:])
        is_success, msg = self.__check_registration(person, room, date_check_in, date_depart, status)

        if not is_success:
            return False, msg, "departForm"

        move_in_element = self.linked_list.find_element(room_id, person)
        if move_in_element:
            if move_in_element.date_check_in != date_check_in or move_in_element.date_depart != date_depart:
                return False, "Даты не соответствуют заселению", "departForm"

        if (not self.table.update_room(person, room_id, is_add=False) or
                not self.tree.update_guests(room_id, person, is_add=False)):
            return False, "Гость не заселен в этот номер", "departForm"

        element = Element(person, room, date_check_in, date_depart, status)

        if to_bd:
            self.cursor.execute("""insert into registrations (room_key, guest, date_check_in, date_depart, status) 
                                                        values (%s, %s, %s, %s, %s)""",
                                (room, person, date_check_in, date_depart, status))
            self.connection.commit()

        self.linked_list.add(element)

        return True, "Гость успешно выселен", "departForm", "findRegistrations", str(self.linked_list)

    def get_registrations(self):
        return True, "Данные о регистрацих найдены", "", "findRegistrations", str(self.linked_list), ""

    def __check_registration(self, person, room, date_check_in, date_depart, status):
        if status != "Заселение" and status != "Выселение":
            return False, "Неверный статус"
        if not self.find_by_id_in_table(person)[0]:
            return False, "Не существует гостя с таким паспортом"
        if not self.find_by_id_in_tree(room)[0]:
            return False, "Не существует комнаты с таким номером"
        if date_check_in > date_depart:  # Доделать сравнение
            return False, "Дата вселения больше даты выселения"
        return True, ""

    @staticmethod
    def __find_substring(string, substr):
        n, m = len(string), len(substr)

        if n < m:
            return False

        t = {}
        for i in range(m):
            t[substr[i]] = i

        i, j = m - 1, m - 1
        while i < n:
            if string[i].lower() == substr[j].lower():
                if j == 0:
                    return True
                else:
                    i -= 1
                    j -= 1
            else:
                if string[i] not in t:
                    i += m
                else:
                    k = t[string[i]]
                    i += max(1, j - k)
                    j = m - 1

        return False

    @staticmethod
    def sort_list(lst):
        if not lst.head:
            return

        max_key = lst.head.key
        cur = lst.head.next
        while cur != lst.head:
            if cur.key > max_key:
                max_key = cur.key
            cur = cur.next

        count = [0] * (max_key + 1)

        cur = lst.head
        while cur != lst.tail:
            count[cur.key] += 1
            cur = cur.next

        for i in range(1, max_key + 1):
            count[i] += count[i - 1]

        temp_list = [None] * lst.length

        cur = lst.head
        while cur != lst.tail:
            temp_list[count[cur.key] - 1] = cur
            count[cur.key] -= 1
            cur = cur.next

        lst.head = temp_list[0]
        lst.tail = temp_list[-1]

        for i in range(lst.length - 1):
            temp_list[i].next = temp_list[i + 1]

        temp_list[-1].next = lst.head

