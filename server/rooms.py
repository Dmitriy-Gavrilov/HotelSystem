class Node:
    def __init__(self, room_id, capacity, rooms, bathroom, equipment, left=None, right=None):
        if not self.check_room(room_id, capacity, rooms, bathroom):
            return
        self.key = int(room_id[1:])
        self.height = 0
        self.left = left
        self.right = right
        self.data = {
            "room_id": room_id,
            "capacity": capacity,
            "rooms": rooms,
            "bathroom": bathroom,
            "equipment": equipment
        }
        self.free_rooms = self.data["capacity"]
        self.guests = []

    def __str__(self):
        return f"""Номер комнаты: {self.data['room_id']}
Количество мест: {self.data['capacity']}
Количество свободных мест: {self.free_rooms}
Количество комнат: {self.data['rooms']}
Санузел: {'Есть' if self.data['bathroom'] else 'Нет'}
Оборудование: {self.data['equipment']}"""

    def update_height(self):
        self.height = max(-1 if not self.left else self.left.height, -1 if not self.right else self.right.height) + 1

    def calc_balance(self):
        return (-1 if not self.right else self.right.height) - (-1 if not self.left else self.left.height)

    @staticmethod
    def check_room(room_id, capacity, rooms, bathroom):
        if (len(room_id) != 4 or not room_id[0].isalpha() or
                any(not x.isdigit() for x in room_id[1:]) or room_id[-1] == "0" or room_id[0] not in "ЛПОМ"):
            return False
        if type(capacity) != int: return False
        if type(rooms) != int: return False
        if type(bathroom) != bool: return False
        if room_id[0] == "О" and capacity != 1: return False
        if room_id[0] == "М" and capacity < 2: return False
        return True


class Tree:
    def __init__(self):
        self.head = None
        self.stack = []

    def __str__(self):
        if not self.head:
            return "Нет номеров"
        s = []
        self.in_order(self.head, s)
        return "\n------\n".join(s)

    def __rotate_left(self, x, parent):
        f = False
        if self.head == x:
            f = True
        right_ch = x.right
        t = right_ch.left
        right_ch.left = x
        x.right = t
        if parent:
            if right_ch.key > parent.key:
                parent.right = right_ch
            else:
                parent.left = right_ch

        x.update_height()
        right_ch.update_height()

        if f:
            self.head = right_ch

    def __rotate_right(self, x, parent):
        f = False
        if self.head == x:
            f = True
        left_ch = x.left
        t = left_ch.right
        left_ch.right = x
        x.left = t
        if parent:
            if left_ch.key > parent.key:
                parent.right = left_ch
            else:
                parent.left = left_ch

        x.update_height()
        left_ch.update_height()

        if f:
            self.head = left_ch

    def __balance(self, node, par):
        bal = node.calc_balance()
        if bal == -2:
            bal1 = node.left.calc_balance() if node else 0
            if bal1 == 1:
                self.__rotate_left(node.left, node)
            self.__rotate_right(node, par)
        elif bal == 2:
            bal1 = node.right.calc_balance() if node else 0
            if bal1 == -1:
                self.__rotate_right(node.right, node)
            self.__rotate_left(node, par)

    def __add_elem(self, elem, par=None):
        if not par:
            if not self.head:
                self.head = elem
                self.head.update_height()
                return True
            else:
                return self.__add_elem(elem, self.head)
        else:
            if elem.key < par.key:
                if not par.left:
                    par.left = elem
                    par.update_height()
                    return True
                else:
                    return self.__add_elem(elem, par.left)
            elif elem.key > par.key:
                if not par.right:
                    par.right = elem
                    par.update_height()
                    return True
                else:
                    return self.__add_elem(elem, par.right)
            else:
                return False

    def __delete_elem(self, elem, node, par=None):
        if not node:
            return False
        elif elem == node.key:
            if node.guests:
                return False
            if self.stack:
                del self.stack[-1]
            if not node.left and not node.right:
                new_node = None
            elif node.left and node.right:
                min_right, parent = node.right, node
                if min_right.left:
                    while min_right.left:
                        parent = min_right
                        min_right = min_right.left
                    parent.left = None
                    min_right.right = node.right
                    min_right.left = node.left
                    self.stack.append([parent, min_right])
                else:
                    parent.right = None
                    min_right.left = node.left
                new_node = min_right
                self.stack.insert(0, [new_node, par])
            else:
                new_node = node.left if node.left else node.right
                self.stack.append([new_node, par])
            if par:
                if elem < par.key:
                    par.left = new_node
                else:
                    par.right = new_node
            else:
                self.head = new_node
        elif elem < node.key:
            self.stack.append([node.left, node])
            self.__delete_elem(elem, node.left, node)
        else:
            self.stack.append([node.right, node])
            self.__delete_elem(elem, node.right, node)

    def in_order(self, node, s, eq='', equipment_flag=False, find_substring=None):
        if node:
            self.in_order(node.left, s, eq, equipment_flag, find_substring)
            self.in_order(node.right, s, eq, equipment_flag, find_substring)
            if equipment_flag:
                if find_substring(node.data["equipment"], eq):
                    s.append(str(node))
            else:
                s.append(node.__str__())

    def find_by_id(self, elem, node=None):
        if node is None:
            node = self.head

        if elem == node.key:
            return [str(node), node.guests]
        elif elem < node.key:
            if node.left:
                return self.find_by_id(elem, node.left)
            else:
                return False
        else:
            if node.right:
                return self.find_by_id(elem, node.right)
            else:
                return False

    def find_by_equipment(self, find_substring, eq):
        s = []
        self.in_order(self.head, s, eq=eq, equipment_flag=True, find_substring=find_substring)
        return s

    def get_room_id(self, key, node=None):
        if node is None:
            node = self.head
        if key == node.key:
            return node.data["room_id"]
        elif key < node.key:
            if node.left:
                return self.get_room_id(key, node.left)
            else:
                return False
        else:
            if node.right:
                return self.get_room_id(key, node.right)
            else:
                return False

    def add(self, elem):
        f = self.__add_elem(elem)
        if f is not False:
            self.stack.reverse()
            self.stack.append([self.head, None])

            for i in self.stack:
                self.__balance(i[0], i[1])
                i[0].update_height()
            self.stack = []
            return True
        self.stack = []
        return False

    def delete(self, elem):
        f = self.__delete_elem(elem, self.head)
        if f is not False:
            self.stack.reverse()
            self.stack.append([self.head, None])

            for i in self.stack:
                if i[0] and i[0].key != elem and i[1] != elem:
                    self.__balance(i[0], i[1])
                    i[0].update_height()
            self.stack = []
            return True
        return False

    def update_guests(self, room_id, guest, is_add=False, node=None):
        if node is None:
            node = self.head

        if room_id == node.key:
            if is_add:
                if node.free_rooms:
                    node.guests.append(guest)
                    node.free_rooms -= 1
                else:
                    return False
            else:
                if guest in node.guests:
                    del node.guests[node.guests.index(guest)]
                    node.free_rooms += 1
                else:
                    return False
            return True
        elif room_id < node.key:
            if node.left:
                return self.update_guests(room_id, guest, is_add, node.left)
            else:
                return False
        else:
            if node.right:
                return self.update_guests(room_id, guest, is_add, node.right)
            else:
                return False

    def clear(self, table):
        self.__clear_tree(self.head, table)

    def __clear_tree(self, node, table):
        if node is None:
            return None
        self.__clear_tree(node.left, table)
        self.__clear_tree(node.right, table)

        if node.guests:
            for i in node.guests:
                table.update_room(i)
        if node == self.head:
            self.head = None
        return None
