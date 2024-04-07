import multiprocessing
import time

def factorize_single(num, output_queue):
    # Функція для знаходження множників числа num
    factors = [i for i in range(1, num + 1) if num % i == 0]
    output_queue.put((num, factors))

def factorize_parallel(*numbers):
    # Функція для паралельного розкладання чисел на множники
    output_queue = multiprocessing.Queue()
    processes = []
    
    for num in numbers:
        process = multiprocessing.Process(target=factorize_single, args=(num, output_queue))
        process.start()
        processes.append(process)
    
    for process in processes:
        process.join()

    # Отримуємо результати та зберігаємо їх разом із відповідними числами
    results = {}
    for _ in numbers:
        num, factors = output_queue.get()
        results[num] = factors
    return results

if __name__ == '__main__':
    # Виміряємо час виконання паралельної версії
    start_time = time.time()
    results = factorize_parallel(128, 255, 99999, 10651060)
    end_time = time.time()

    print("Parallel execution time:", end_time - start_time, "seconds")

    # Тест паралельної версії
    assert results[128] == [1, 2, 4, 8, 16, 32, 64, 128]
    assert results[255] == [1, 3, 5, 15, 17, 51, 85, 255]
    assert results[99999] == [1, 3, 9, 41, 123, 271, 369, 813, 2439, 11111, 33333, 99999]
    assert results[10651060] == [1, 2, 4, 5, 7, 10, 14, 20, 28, 35, 70, 140, 76079, 152158, 304316, 380395, 532553, 760790, 1065106, 1521580, 2130212, 2662765, 5325530, 10651060]

    print("All tests passed successfully.")