class Item:
    def __init__(self, key, full_name, year_of_birth, address, reason):
        if not self.check_guest(key, full_name, year_of_birth, address):
            return

        self.key = key
        self.value = {
            "passport_id": key,
            "full_name": full_name,
            "year_of_birth": year_of_birth,
            "address": address,
            "reason": reason
        }
        self.room = 0

    def __str__(self):
        return f"""ФИО: {self.value['full_name']}
Год рождения: {self.value['year_of_birth']}
Номер паспорта: {self.value['passport_id']}
Адрес: {self.value['address']}
Цель прибытия: {self.value['reason']}
Гостиничный номер: {self.room if self.room else 'Не проживает в гостинице'}"""

    @staticmethod
    def check_key(key):
        return len(list(filter(lambda x: x.isdigit(), list(key[:4] + key[5:])))) == 10

    def check_guest(self, key, full_name, year_of_birth, address):
        if not self.check_key(key):
            return False
        if any(x.isdigit() for x in full_name) or not full_name:
            return False
        if not all(x.isdigit() for x in year_of_birth) or not year_of_birth:
            return False
        if any(x.isdigit() for x in address) or not address:
            return False
        return True


class HashTable:
    def __init__(self, size=0):
        self.size = size
        self.table_arr = [0] * size
        self.length = 0

    def __str__(self):
        if not self.length:
            return "Гостей нет"
        s = ""
        for i in range(self.size):
            if self.table_arr[i] not in (0, "del"):
                s += (str(self.table_arr[i]) + "\n------\n")
        return s

    def add(self, item):
        if self.find_by_id(item.key):
            return False
        index = self.hash_func(item.key, self.size)
        current = self.table_arr[index]
        k = 1
        while current and current != "del":
            index = (index + k ** 2) % self.size
            k += 1
        self.table_arr[index] = item
        self.length += 1
        return True

    def find_by_id(self, id):
        ind = self.hash_func(id, self.size)
        j = 1
        while True:
            current = self.table_arr[ind]
            if not current:
                return False
            elif current != "del" and current.key == id:
                return [str(current), current.room]
            ind = (ind + j ** 2) % self.size
            j += 1

    def find_by_full_name(self, find_substring, fullname):
        ans = []
        for i in self.table_arr:
            if i != 0 and i != "del":
                if find_substring(i.value["full_name"], fullname):
                    ans.append([f"Паспорт: {i.value['passport_id']}", f"ФИО: {i.value['full_name']}"])
        return ans

    def get_info_by_id(self, key):
        ind = self.hash_func(key, self.size)
        j = 1
        while True:
            current = self.table_arr[ind]
            if not current:
                return False
            elif current != "del" and current.key == key:
                return [f"Паспорт: {key}", f"Имя: {current.value['full_name']}"]
            ind = (ind + j ** 2) % self.size
            j += 1

    def update_room(self, key, room_id, is_add=False):
        ind = self.hash_func(key, self.size)
        j = 1
        while True:
            current = self.table_arr[ind]
            if not current:
                return False
            elif current != "del" and current.key == key:
                if is_add:
                    if not current.room:
                        current.room = room_id
                    else:
                        return False
                else:
                    if current.room:
                        current.room = 0
                    else:
                        return False
                return True
            ind = (ind + j ** 2) % self.size
            j += 1

    def delete(self, key):
        ind = self.hash_func(key, self.size)
        k = 1
        while True:
            current = self.table_arr[ind]
            if not current:
                return False
            elif current != "del" and current.key == key:
                if current.room:
                    return False
                self.table_arr[ind] = "del"
                self.length -= 1
                return True
            ind = (ind + k ** 2) % self.size
            k += 1

    def clear(self, tree):
        for i in range(self.size):
            current = self.table_arr[i]
            if current not in (0, "del"):
                if current.room:
                    tree.update_guests(current.room, current.key, is_add=False)
                self.table_arr[i] = 0
                self.length -= 1

    @staticmethod
    def hash_func(string, max_len):
        n = 0
        for i in range(len(string)):
            n += (ord(string[i]) + i) ** 2 - i

        return n % max_len
