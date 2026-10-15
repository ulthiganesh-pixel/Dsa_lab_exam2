import time
import random
import matplotlib.pyplot as plt
from solution import parse_file_and_build

# Your available input files
files = ["input.txt", "input2.txt", "input3.txt", "input4.txt"]
labels = ["Input 1", "Input 2", "Input 3", "Input 4"]

implementations = ['trie', 'bst', 'dict']
constr_times = {impl: [] for impl in implementations}
search_times = {impl: [] for impl in implementations}
print_times = {impl: [] for impl in implementations}

for filename in files:
    print(f"\nBenchmarking {filename}...")
    for impl in implementations:
        print(f"  -> Testing {impl.upper()}...")
        
        # 1. Construction Time
        start = time.time()
        index = parse_file_and_build(filename, impl)
        constr_times[impl].append(time.time() - start)

        # 2. Search Time (1,000 random word lookups)
        entries = index.get_lexicographic_order()
        all_words = [w for w, _ in entries] if entries else ["test"]
        queries = [random.choice(all_words) for _ in range(1000)]
        
        start = time.time()
        for w in queries:
            index.search(w)
        search_times[impl].append(time.time() - start)

        # 3. Printing / Sorting Time
        start = time.time()
        _ = index.get_lexicographic_order()
        print_times[impl].append(time.time() - start)

# Plotting using Matplotlib
plt.figure(figsize=(15, 5))

plt.subplot(1, 3, 1)
for impl in implementations:
    plt.plot(labels, constr_times[impl], marker='o', label=impl.upper())
plt.title("Index Construction Time")
plt.xlabel("Datasets")
plt.ylabel("Seconds")
plt.legend()
plt.grid(True)

plt.subplot(1, 3, 2)
for impl in implementations:
    plt.plot(labels, search_times[impl], marker='s', label=impl.upper())
plt.title("Search Time")
plt.xlabel("Datasets")
plt.ylabel("Seconds")
plt.legend()
plt.grid(True)

plt.subplot(1, 3, 3)
for impl in implementations:
    plt.plot(labels, print_times[impl], marker='^', label=impl.upper())
plt.title("Sorting & Print Time")
plt.xlabel("Datasets")
plt.ylabel("Seconds")
plt.legend()
plt.grid(True)

plt.tight_layout()
plt.savefig("performance_comparison.png")
print("\nBenchmark complete! 'performance_comparison.png' generated successfully.")