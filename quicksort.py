from Pyro4 import expose
import time
from datetime import timedelta


class Solver:
    def __init__(self, workers=None, input_file_name=None, output_file_name=None):
        self.input_file_name = input_file_name
        self.output_file_name = output_file_name
        self.workers = workers if workers else []
        print("Initialized Solver")

    def solve(self):
        print("Job Started: Parallel QuickSort")
        # print(f"Workers: {len(self.workers)}")

        array = self.read_input()

        start = time.time()
        sorted_data = self.parallel_sorting(array)
        duration = time.time() - start
        self.write_output(duration)

    def parallel_sorting(self, array):
        if len(array) <= 1:
            return array
        if len(array) < len(self.workers):
            return self.quicksort(array)

        step = len(array) // len(self.workers)
        mapped = []

        for i in range(len(self.workers)):
            start = i * step
            end = (i + 1) * step if i < len(self.workers) - 1 else len(array)
            sub_array = array[start:end]
            mapped.append(self.workers[i].quicksort(sub_array))

        print("Map phase completed.")

        reduced = Solver.myreduce(mapped)
        print("Reduce phase completed.")

        return reduced

    @staticmethod
    def myreduce(mapped):
        sorted_parts = [result.value for result in mapped]
        return sorted(sum(sorted_parts, []))

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
        with open(self.input_file_name, 'r') as f:
            return [int(line.strip()) for line in f]

    def write_output(self, execution_time):
        formatted_time = str(timedelta(seconds=execution_time))
        with open(self.output_file_name, 'w') as f:
            f.write("Number of workers: " + str(len(self.workers)) + "\n")
            f.write("Execution Time: " + formatted_time + "\n")
        print("Job Finished: Result written to output file.")