from collections import Counter
from time import time
import concurrent.futures
import random
import string
import os  # Added missing import


def generate_random_words(num_words):
    return [''.join(random.choices(string.ascii_lowercase, k=5)) for _ in range(num_words)]


def benchmark_counter_vs_dict(num_urls=1000, words_per_url=10000):
    # Simulate data from multiple URLs
    all_url_words = [generate_random_words(words_per_url) for _ in range(num_urls)]

    # Test Counter
    start = time()
    counter = Counter()
    for words in all_url_words:
        counter.update(words)
    counter_time = time() - start

    # Test Dictionary
    start = time()
    dictionary = {}
    for words in all_url_words:
        for word in words:
            dictionary[word] = dictionary.get(word, 0) + 1
    dict_time = time() - start

    return counter_time, dict_time


def parallel_counting_with_counter(args):
    url_words, worker_id = args
    count = Counter(url_words)
    print(f"Worker {worker_id} processed {len(url_words)} words")
    return count


def parallel_counting_with_dict(url_words):
    word_dict = {}
    for word in url_words:
        word_dict[word] = word_dict.get(word, 0) + 1
    return word_dict


def parallel_benchmark(num_urls=1000, words_per_url=10000):
    all_url_words = [generate_random_words(words_per_url) for _ in range(num_urls)]
    max_workers = min(num_urls, os.cpu_count() or 1)

    print(f"Number of CPU cores available: {os.cpu_count()}")
    print(f"Number of workers being used: {max_workers}")

    urls_per_worker = num_urls // max_workers
    print(f"Each worker will handle approximately {urls_per_worker} URLs\n")

    work_items = [(words, i) for i, words in enumerate(all_url_words)]

    # Test Counter with parallel processing
    start = time()
    with concurrent.futures.ProcessPoolExecutor(max_workers=max_workers) as executor:
        counters = list(executor.map(parallel_counting_with_counter, work_items))  # Added list() to consume iterator

        print(f"\nAll workers finished. Combining results...")
        final_counter = Counter()
        for i, counter in enumerate(counters):
            words_counted = sum(counter.values())
            print(f"Adding results from worker {i}: {len(counter)} unique words, {words_counted} total words")
            final_counter.update(counter)
    counter_time = time() - start

    # Test Dictionary with parallel processing
    start = time()
    with concurrent.futures.ProcessPoolExecutor(max_workers=max_workers) as executor:
        dicts = list(executor.map(parallel_counting_with_dict, all_url_words))  # Added list() to consume iterator
        final_dict = {}
        for d in dicts:
            for word, count in d.items():
                final_dict[word] = final_dict.get(word, 0) + count
    dict_time = time() - start

    return counter_time, dict_time


if __name__ == "__main__":  # Added proper main guard
    # Run benchmarks only once
    print("Running sequential benchmark...")
    counter_time, dict_time = benchmark_counter_vs_dict()
    print(f"Sequential processing times:")
    print(f"Counter: {counter_time:.2f} seconds")
    print(f"Dictionary: {dict_time:.2f} seconds")

    print("\nRunning parallel benchmark...")
    counter_time, dict_time = parallel_benchmark()
    print(f"Parallel processing times:")
    print(f"Counter: {counter_time:.2f} seconds")
    print(f"Dictionary: {dict_time:.2f} seconds")