import multiprocessing
import numpy as np
import matplotlib.pyplot as plt
import time

# Funkcja obliczająca wartość funkcji dla danego argumentu
def calculate_function_value(args):
    function, argument = args
    return function(argument)

# Funkcja do przetwarzania danych w sposób współbieżny
def process_data_parallel(function, data, num_processes):
    pool = multiprocessing.Pool(processes=num_processes)
    results = pool.map(calculate_function_value, [(function, argument) for argument in data], chunksize=1)
    pool.close()
    pool.join()
    return results

# Funkcje matematyczne
def square(x):
    return x**2

def sin(x):
    return np.sin(x)

def log(x):
    return np.log(x)
# dodać jeszcze jedną funcje matemtyczną, usunąć niepotrzebne komentarze, wytłumaczyć co robi w programie map pool

# Testowanie wydajności dla różnych funkcji i rozmiarów danych
def test_performance():
    functions = [square, sin, log]
    data_sizes = [10, 100, 1000, 10000]
    num_processes = [1, 2, 4, 8]

    for function in functions:
        function_name = function.__name__
        execution_times = []
        for size in data_sizes:
            data = np.random.random(size)  # Generowanie losowych danych
            times = []
            for num_procs in num_processes:
                start_time = time.time()
                process_data_parallel(function, data, num_procs)
                end_time = time.time()
                execution_time = end_time - start_time
                times.append(execution_time)
            execution_times.append(times)

        # Generowanie wykresu
        plt.figure()
        plt.title(f"Wydajność obliczeń dla funkcji {function_name}")
        plt.xlabel("Liczba procesów")
        plt.ylabel("Czas wykonania (s)")
        for i, size in enumerate(data_sizes):
            plt.plot(num_processes, execution_times[i], label=f"Rozmiar danych: {size}")
        plt.legend()
        plt.savefig(f"{function_name}_performance.png")
        plt.close()

if __name__ == '__main__':
    multiprocessing.freeze_support()  # Dodanie tej linii dla systemu Windows
    test_performance()
