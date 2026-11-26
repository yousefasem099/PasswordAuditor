
import time
import tracemalloc
from pathlib import Path

# Generate a temporary test wordlist
test_file = Path("data/performance_wordlist.txt")
total_words = 100_000

print("Generating test wordlist...")

with test_file.open("w", encoding="utf-8") as file:
    for i in range(total_words):
        file.write(f"TestPassword_{i:06d}\n")

print(f"Generated {total_words:,} test passwords.")

# Measure loading time and memory usage
tracemalloc.start()
start_time = time.perf_counter()

passwords = {
    line.strip().casefold()
    for line in test_file.open("r", encoding="utf-8")
}

load_time = time.perf_counter() - start_time
current_memory, peak_memory = tracemalloc.get_traced_memory()
tracemalloc.stop()

# Measure lookup time
target = "TestPassword_099999".casefold()

start_time = time.perf_counter()
found = target in passwords
lookup_time = time.perf_counter() - start_time

print("\n=== PERFORMANCE RESULTS ===")
print(f"Total entries: {len(passwords):,}")
print(f"Load time: {load_time:.4f} seconds")
print(f"Lookup time: {lookup_time:.8f} seconds")
print(f"Current memory: {current_memory / 1024 / 1024:.2f} MB")
print(f"Peak memory: {peak_memory / 1024 / 1024:.2f} MB")
print(f"Test password found: {found}")

test_file.unlink()
print("\nTemporary test file deleted.")
