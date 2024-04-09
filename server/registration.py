class Element:
    def __init__(self, person, room, date_check_in, date_depart, status):
        self.next = None
        self.key = int(room[1:])  # Первичный ключ

        self.person = person  # Номер паспорта
        self.room = room  # Номер комнаты
        self.date_check_in = date_check_in
        self.date_depart = date_depart
        self.status = status

    def __str__(self):
        return f"""{self.status}
Гость (паспорт): {self.person}
Номер: {self.room}
Дата заселения: {self.date_check_in}
Дата выселения: {self.date_depart}"""


class List:
    def __init__(self):
        self.head = None
        self.tail = None
        self.length = 0

    def __str__(self):
        if not self.head:
            return "Нет данных о вселении и выселении гостей"

        last_10 = []
        t = self.head
        while t.next != self.head:
            if len(last_10) < 10:
                last_10.insert(0, t)
            else:
                last_10.pop(0)
                last_10.insert(0, t)
            t = t.next

        if len(last_10) < 10:
            last_10.insert(0, t)
        else:
            last_10.pop(0)
            last_10.insert(0, t)

        s = ""
        for node in last_10:
            s += str(node) + "\n------\n"
        return s

    def add(self, elem):
        if not self.head:
            self.head = elem
            self.tail = elem
            elem.next = elem
        else:
            elem.next = self.head
            self.tail.next = elem
            self.tail = elem
        self.length += 1

    def find_element(self, key, person):
        if not self.head:
            return None

        res = None
        current = self.head
        while True:
            if current.key == key and current.person == person:
                res = current
            current = current.next
            if current == self.head:
                break

        return res

    def delete(self, ind):  # Переделать (сравнивать key элементов)
        i = 1
        if self.length >= ind > 0:
            t1 = t = self.head
            if ind == 1:
                self.head = t.next
                self.tail.next = t.next
            else:
                while i != ind:
                    t1 = t
                    t = t.next
                    i += 1
                t1.next = t.next
            self.length -= 1
            return True
        return False

    def clear(self):
        if self.head:
            cur = self.head
            while cur.next != self.head:
                t = cur.next
                cur.next = None
                cur = t
            self.head = None
            self.tail = None
            self.length = 0
