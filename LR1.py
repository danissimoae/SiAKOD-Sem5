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

    # Линейное пробирование
    while steps < linear_limit:
        index = (hash_value + prob_index) % table_size
        if hash_table[index] is None:
            hash_table[index] = key
            return steps + 1  # возвращаем количество шагов, добавляя 1 за текущий шаг
        prob_index += 1
        steps += 1


    # Переход к квадратичному пробированию после достижения предела
    prob_index = 0
    while steps < table_size:
        index = (hash_value + prob_index * prob_index) % table_size
        if hash_table[index] is None:
            hash_table[index] = key
            return steps + 1  # возвращаем количество шагов, добавляя 1 за текущий шаг
        prob_index += 1
        steps += 1

    return steps  # возвращаем количество шагов при переполнении

#####################################################################
#####################################################################

# Генерация уникальных случайных чисел
unique_numbers = random.sample(range(10, 100), 50)
for i in range(0, len(unique_numbers), 20):
    print(*unique_numbers[i:i+20])

# Параметры для хеш-таблицы
table_size = int(len(unique_numbers) * 1.5)
hash_table = [None] * table_size

# Заполнение хеш-таблицы
total_steps = 0
collisions = 0

for num in unique_numbers:
    steps = insert_with_quadr_probing(hash_table, num, table_size)
    total_steps += steps
    if steps > 1:
        collisions += 1

# Анализ хеш-таблицы
filled_cells = sum(1 for cell in hash_table if cell is not None)
coef = filled_cells / table_size
average_steps = total_steps / len(unique_numbers)
is_unique = are_elements_unique(unique_numbers)

#####################################################################
#####################################################################

# Вывод результатов в виде форматированной таблицы
print("\nХеш-таблица:")

# Настройки форматированной таблицы
columns = 8  # Количество столбцов
table = PrettyTable()

# Создаем заголовки для форматированной таблицы
header = []
for i in range(columns):
    header.append(f"Index_{i}")
    header.append(f"Data_{i}")
table.field_names = header

# Заполняем таблицу данными
for row_start in range(0, table_size, columns):
    row = []
    for i in range(columns):
        index = row_start + i
        if index < table_size:
            row.append(index)
            row.append(hash_table[index] if hash_table[index] is not None else "-")
        else:
            row.append("-")
            row.append("-")
    table.add_row(row)

print(table)
print("\n+---------+---------+---------+---------Анализ:---------+---------+---------+---------+")
print("Коэффициент заполнения (α):                   ", coef)
print("Среднее кол-во шагов для размещения ключа:    ", average_steps)
print("Всего шагов:                                  ", total_steps)
print("Коллизий:                                     ", collisions)
print("Уникальны ли элементы в списке:               ", is_unique)
