from Pyro4 import expose

class Solver:
    def __init__(self, workers=None, input_file_name=None, output_file_name=None):
        self.input_file_name = input_file_name
        self.output_file_name = output_file_name
        self.workers = workers if workers else []
        print(f"Initialized with {len(self.workers)} workers.")

    def solve(self):
        print("Job Started: Parallel QuickSort")
        print(f"Workers: {len(self.workers)}")

        array = self.read_input()
        step = len(array) // len(self.workers)
        mapped = []

        # map: отправляем части массива воркерам
        for i in range(len(self.workers)):
            start = i * step
            end = (i + 1) * step if i < len(self.workers) - 1 else len(array)
            sub_array = array[start:end]
            mapped.append(self.workers[i].quicksort(sub_array))

        print("Map phase completed.")

        # reduce: объединяем отсортированные подмассивы
        reduced = self.myreduce(mapped)
        print("Reduce phase completed.")

        self.write_output(reduced)
        print("Job Finished: Result written to output file.")

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

    @staticmethod
    def myreduce(mapped):
        sorted_parts = [result.value for result in mapped]
        return sorted(sum(sorted_parts, []))

    def read_input(self):
        f = open(self.input_file_name, 'r')
        array = list(map(int, f.readline().strip().split()))
        f.close()
        return array

    def write_output(self, output):
        f = open(self.output_file_name, 'w')
        f.write(str(output))
        f.write('\n')
        f.close()
