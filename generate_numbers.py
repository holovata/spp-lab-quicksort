import random


def generate_random_numbers(file_name, n, min_value=1, max_value=99999999999):
    numbers = [random.randint(min_value, max_value) for _ in range(n)]

    with open(file_name, 'w') as f:
        f.write(' '.join(map(str, numbers)))

    print(f"{n} случайных чисел записано в файл {file_name}.")


generate_random_numbers('input_5000000.txt', n=5000000)
