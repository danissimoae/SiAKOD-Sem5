import random
from prettytable import PrettyTable

# Хеш-функция, использующая последние две цифры квадрата ключа
def hash_function(key):
    return (key ** 2) % 100

# Првоерка на уникальность чисел
def are_elements_unique(lst):
    return len(lst) == len(set(lst))

# Вставка с линейным и квадратичным пробированием
def insert_with_quadr_probing(hash_table, key, table_size, linear_limit=20):
    hash_value = hash_function(key)  # хеш для ключа
    steps = 0                        # счетчик шагов
    prob_index = 0                   # индекс для пробирования

    if find_element(hash_table, key, table_size) is not None:
        return -2

    # Линейное пробирование
    while steps < linear_limit:
        index = (hash_value + prob_index) % table_size
        if hash_table[index] in (None, -1):
            hash_table[index] = key
            return steps + 1  # возвращаем количество шагов, добавляя 1 за текущий шаг
        prob_index += 1
        steps += 1


    # Переход к квадратичному пробированию после достижения предела
    prob_index = 0
    while steps < table_size:
        index = (hash_value + prob_index * prob_index) % table_size
        if hash_table[index] in (None, -1):
            hash_table[index] = key
            return steps + 1  # возвращаем количество шагов, добавляя 1 за текущий шаг
        prob_index += 1
        steps += 1

    return -1  # возвращаем -1 при переполнении


def find_element(hash_table, key, table_size, linear_limit=20):
    hash_value = hash_function(key)
    steps = 0
    prob_index = 0
    while steps < linear_limit:
        index = (hash_value + prob_index) % table_size
        if hash_table[index] is None or hash_table[index] == -1:
            return None
        if hash_table[index] == key:
            return index
        prob_index += 1
        steps += 1

    prob_index = 0
    while steps < table_size:
        index = (hash_value + prob_index * prob_index) % table_size
        if hash_table[index] is None or hash_table[index] == -1:
            return None
        if hash_table[index] == key:
            return index
        prob_index += 1
        steps += 1
    return None


def delete_element(hash_table, key, table_size, linear_limit=20):
    index = find_element(hash_table, key, table_size, linear_limit)
    if index is None:
        return f"Элемента {key} в таблице нет."
    hash_table[index] = -1
    return f"Элемент {key} успешно удален с индекса {index}."


def replace_element(hash_table, table_size, linear_limit=20):
    # Ввод удаляемого элемента
    key_to_remove = int(input("Введите значение удаляемого элемента: "))
    index = find_element(hash_table, key_to_remove, table_size, linear_limit)

    if index is None:
        print(f"Элемента {key_to_remove} в таблице нет.")
        return

    print(delete_element(hash_table, key_to_remove, table_size, linear_limit))

    key_to_add = int(input("Введите значение нового элемента: "))
    if find_element(hash_table, key_to_add, table_size, linear_limit) is not None:
        print(f"Элемент {key_to_add} уже существует в таблице.")
        return

    if insert_with_quadr_probing(hash_table, key_to_add, table_size, linear_limit) == -1:
        print(f"Таблица переполнена, элемент не удалось добавить.")
    else:
        print(f"Элмент {key_to_add} успешно добавлен.")

#####################################################################
#####################################################################
#####################################################################
#####################################################################
def display_hash_table(hash_table, table_size):
    table = PrettyTable()
    columns = 8
    headers = []
    for i in range(columns):
        headers.append(f"Index_{i}")
        headers.append(f"Data_{i}")
    table.field_names = headers

    for row_start in range(0, table_size, columns):
        row = []
        for i in range(columns):
            index = row_start + i
            if index < table_size:
                row.append(index)
                row.append(hash_table[index] if hash_table[index] != None else "-")
            else:
                row.append("-")
                row.append("-")
        table.add_row(row)

    print(table)

# Основной цикл программы
def main():
    unique_numbers = random.sample(range(10, 100), 50)
    print("Сгенерированные элементы:")
    for i in range(0, len(unique_numbers), 20):
        print(*unique_numbers[i:i + 20])
    table_size = int(len(unique_numbers) * 1.5)
    hash_table = [None] * table_size

    for num in unique_numbers:
        insert_with_quadr_probing(hash_table, num, table_size)

    display_hash_table(hash_table, table_size)

    while True:
        print("\nВыберите нужный вариант:")
        print("1 - Найти элемент               2 - Удалить элемент")
        print("3 - Добавить новый элемент      4 - Заменить элемент      0 - Выход")

        choice = input("Введите номер варианта: ")
        if choice == "0":
            break

        elif choice == "1":
            key = int(input("Введите элемент для поиска: "))
            result = find_element(hash_table, key, table_size)
            if result is not None:
                print(f"Элемент {key} найден под индексом {result}.")
            else:
                print(f"Элемента {key} в таблице нет.")

        elif choice == "2":
            key = int(input("Введите элемент для удаления: "))
            print(delete_element(hash_table, key, table_size))
            display_hash_table(hash_table, table_size)

        elif choice == "3":
            key = int(input("Введите новый элемент для добавления: "))
            result = insert_with_quadr_probing(hash_table, key, table_size)
            if result == -1:
                print("Таблица переполнена, элемент не удалось добавить.")
            elif result == -2:
                print(f"Элемент {key} уже есть в таблице.")
            else:
                print(f"Элемент {key} добавлен.")
            display_hash_table(hash_table, table_size)

        elif choice == "4":
            replace_element(hash_table, table_size)
            display_hash_table(hash_table, table_size)

        else:
            print("Некорректный ввод, попробуйте снова.")

if __name__ == "__main__":
    main()