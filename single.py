from Pyro4 import expose, Daemon, locateNS
import time


class Solver:
    def __init__(self, workers=None, input_file_name=None, output_file_name=None):
        self.input_file_name = input_file_name
        self.output_file_name = output_file_name
        self.workers = workers if workers else [self]
        print("Initialized Solver")

    def solve(self):
        print("Job Started")
        arr = self.read_input()

        start_time = time.time()
        sorted_arr = self.quicksort(arr)
        elapsed_time = time.time() - start_time

        self.write_output(sorted_arr)
        print(f"Job Finished in {elapsed_time:.4f} seconds")

    @expose
    def quicksort(self, arr):
        if len(arr) <= 1:
            return arr
        pivot = arr[len(arr) // 2]
        left = [x for x in arr if x < pivot]
        middle = [x for x in arr if x == pivot]
        right = [x for x in arr if x > pivot]
        return self.workers[0].quicksort(left) + middle + self.workers[0].quicksort(right)

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



'''if __name__ == '__main__':
    daemon = Daemon()
    ns = locateNS()

    solver = SequentialSolver(input_file_name="input_100000.txt", output_file_name="output.txt")

    uri = daemon.register(solver)
    ns.register("SequentialSolver", uri)
    print("Ready")
    daemon.requestLoop()'''
