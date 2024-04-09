import socket
import datetime as dt
import sys

from manage import *


def main():
    host = 'localhost'
    port = 5050
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind((host, port))
    server_socket.listen()

    manager = Manager()
    manager.fill_structures()

    while True:
        connection, client_address = server_socket.accept()
        try:
            data = connection.recv(1024).decode('utf-8').split(";")  # Получение данных
            command = data[0]
            match command:
                case "quit":
                    sys.exit()

                case "addGuest":
                    response = ';'.join(
                        [str(i) for i in manager.add_to_table(*data[1:], to_bd=True)])
                case "deleteGuest":
                    response = ';'.join([str(i) for i in manager.delete_from_table(*data[1:])])
                case "findGuestById":
                    response = ';'.join([str(i) for i in manager.find_by_id_in_table(*data[1:])])
                case "findGuestByFio":
                    response = ';'.join([str(i) for i in manager.find_by_fullname(*data[1:])])
                case "findAllGuests":
                    response = ';'.join([str(i) for i in manager.view_table()])
                case "clearGuests":
                    response = ';'.join([str(i) for i in manager.clear_table()])

                case "addRoom":
                    response = ';'.join([str(i) for i in manager.add_to_tree(data[1], int(data[2]), int(data[3]),
                                                                             bool(int(data[4]) - 1), data[5],
                                                                             to_bd=True)])
                case "deleteRoom":
                    response = ';'.join([str(i) for i in manager.delete_from_tree(*data[1:])])
                case "findRoomById":
                    response = ';'.join([str(i) for i in manager.find_by_id_in_tree(*data[1:])])
                case "findRoomByEquipment":
                    response = ';'.join([str(i) for i in manager.find_by_equipment(*data[1:])])
                case "findAllRooms":
                    response = ';'.join([str(i) for i in manager.view_tree()])
                case "clearRooms":
                    response = ';'.join([str(i) for i in manager.clear_tree()])

                case "moveIn":
                    date1 = dt.datetime(*reversed([int(i) for i in data[3].split(".")])).date()
                    date2 = dt.datetime(*reversed([int(i) for i in data[4].split(".")])).date()
                    response = ';'.join([str(i) for i in manager.move_in(data[1], data[2], date1, date2, to_bd=True)])
                case "depart":
                    date1 = dt.datetime(*reversed([int(i) for i in data[3].split(".")])).date()
                    date2 = dt.datetime(*reversed([int(i) for i in data[4].split(".")])).date()
                    response = ';'.join([str(i) for i in manager.depart(data[1], data[2], date1, date2, to_bd=True)])

                case "getRegistrations":
                    response = ';'.join([str(i) for i in manager.get_registrations()])

                case _:
                    response = ["False", "Ошибка"]

            connection.sendall(response.encode('utf-8'))  # Отправление ответа
        finally:
            connection.close()


if __name__ == "__main__":
    main()
