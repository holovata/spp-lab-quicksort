from Pyro4 import expose
import time


class Solver:
    def __init__(self, workers=None, input_file_name=None, output_file_name=None):
        self.input_file_name = input_file_name
        self.output_file_name = output_file_name
        self.workers = workers
        print("Inited")

    def solve(self):
        print("Job Started")
        print("Workers %d" % len(self.workers))

        array = self.read_input()

        start_time = time.time()
        sorted_array = Solver.quicksort(array)
        elapsed_time = time.time() - start_time

        print("Sorted the array in " + str(elapsed_time) + " seconds.")

        if Solver.is_sorted(sorted_array):
            print("Array is correctly sorted.")
        else:
            print("ERROR: Array is NOT sorted correctly!")

        self.write_output("ready")

        print("Job Finished")

    @staticmethod
    def is_sorted(arr):
        return all(arr[i] <= arr[i + 1] for i in range(len(arr) - 1))

    @staticmethod
    @expose
    def quicksort(arr):
        if len(arr) <= 1:
            return arr
        pivot = arr[len(arr) // 2]
        left = [x for x in arr if x < pivot]
        middle = [x for x in arr if x == pivot]
        right = [x for x in arr if x > pivot]
        return Solver.quicksort(left) + middle + Solver.quicksort(right)

    def read_input(self):
        f = open(self.input_file_name, 'r')  # Открытие файла
        array = list(map(int, f.readline().strip().split()))  # Чтение и обработка данных
        f.close()  # Закрытие файла, даже если возникнет ошибка
        return array

    def write_output(self, output):
        f = open(self.output_file_name, 'w')
        f.write(str(output))
        f.write('\n')
        f.close()