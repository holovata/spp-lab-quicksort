import random


def generate_random_numbers(file_name, n, min_value=1, max_value=99999999999):
    with open(file_name, 'w') as f:
        for _ in range(n):
            f.write(f"{random.randint(min_value, max_value)}\n")


generate_random_numbers('input_100000.txt', n=100000)
