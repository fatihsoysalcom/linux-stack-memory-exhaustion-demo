import multiprocessing
import time
import os
import sys

# --- Configuration ---
# Memory to allocate per simulated "service" process (in MB)
# Adjust this value based on your system's RAM. A value too high might crash your system,
# too low might not show a significant impact. Aim for a total (MEMORY_PER_PROCESS_MB * NUM_PROCESSES)
# that is a noticeable fraction of your system's RAM (e.g., 25-50%).
MEMORY_PER_PROCESS_MB = 250 # Each process tries to allocate 250MB
NUM_PROCESSES = 6           # Number of "services" in our "great stack"
                            # Total simulated memory footprint: 250MB * 6 = 1.5GB

# --- Worker Process Function ---
def heavy_service_worker(process_id, memory_mb):
    """
    Simulates a 'heavy service' that allocates a significant amount of memory
    and performs some dummy CPU-bound work.
    """
    pid = os.getpid()
    print(f"[{pid}] Service {process_id}: Starting. Attempting to allocate {memory_mb}MB...")
    
    # Simulate memory allocation by creating a large bytearray.
    # This directly consumes RAM and can trigger swapping if physical memory is scarce.
    try:
        # 1 MB = 1024 * 1024 bytes
        memory_chunk = bytearray(memory_mb * 1024 * 1024)
        # Access an element to ensure the memory is 'touched' and not lazily allocated away
        _ = memory_chunk[0]
        print(f"[{pid}] Service {process_id}: {memory_mb}MB allocated successfully.")
    except MemoryError:
        print(f"[{pid}] Service {process_id}: Failed to allocate {memory_mb}MB. System might be low on RAM.")
        return

    # Simulate some CPU-bound work (e.g., a complex calculation)
    # This adds to the system load, competing for CPU cycles.
    start_cpu_work = time.time()
    dummy_sum = 0
    for i in range(10_000_000): # A large loop to consume CPU
        dummy_sum += i * 2
    end_cpu_work = time.time()
    print(f"[{pid}] Service {process_id}: Dummy CPU work finished in {end_cpu_work - start_cpu_work:.2f} seconds. (Sum: {dummy_sum}) ")

    # Keep the process alive for a bit to simulate a running service
    # This is crucial for demonstrating the sustained impact on other tasks.
    print(f"[{pid}] Service {process_id}: Holding resources for 10 seconds to simulate active state...")
    time.sleep(10) # Hold resources for 10 seconds
    
    print(f"[{pid}] Service {process_id}: Exiting.")

# --- Main Application Logic ---
def main():
    print("--- Simulating a 'Great Stack' on Linux ---")
    print(f"Config: {NUM_PROCESSES} services, each attempting to allocate ~{MEMORY_PER_PROCESS_MB}MB.")
    print(f"Total simulated memory footprint: ~{NUM_PROCESSES * MEMORY_PER_PROCESS_MB}MB.")
    print("\nThis example demonstrates how cumulative resource consumption (memory, CPU) by")
    print("multiple 'services' in a complex application stack can lead to system slowdowns")
    print("and unresponsiveness, even without a 'kernel panic'.")
    print("Watch your system's memory and CPU usage (e.g., with `htop` or `top`) while running this.")

    # --- Phase 1: Baseline Performance Measurement (System under low load) ---
    print("\n--- Phase 1: Baseline Performance (System under low load) ---")
    start_time_baseline = time.time()
    # A simple, CPU-bound task to measure system responsiveness.
    _ = [x * x for x in range(5_000_000)] 
    end_time_baseline = time.time()
    baseline_duration = end_time_baseline - start_time_baseline
    print(f"Simple task completed in {baseline_duration:.4f} seconds.")

    # --- Phase 2: Launching "Heavy Services" ---
    print("\n--- Phase 2: Launching 'Heavy Services' (Simulating a 'Great Stack') ---")
    processes = []
    for i in range(NUM_PROCESSES):
        p = multiprocessing.Process(target=heavy_service_worker, args=(i + 1, MEMORY_PER_PROCESS_MB))
        processes.append(p)
        p.start()
        # Give a small delay to allow processes to start allocating memory and avoid a burst
        time.sleep(0.5) 

    # --- Phase 3: Performance Measurement under Load (While services are active) ---
    # This is where the 'engineer panic' scenario is demonstrated: other applications
    # on the system become slow or unresponsive due to resource contention.
    print("\n--- Phase 3: Performance Under Load (While services are active) ---")
    print("Attempting the same simple task while 'services' are running and consuming resources...")
    start_time_under_load = time.time()
    _ = [x * x for x in range(5_000_000)] # The same simple task
    end_time_under_load = time.time()
    under_load_duration = end_time_under_load - start_time_under_load
    print(f"Simple task completed under load in {under_load_duration:.4f} seconds.")

    # --- Phase 4: Waiting for all services to finish ---
    print("\n--- Phase 4: Waiting for Services to Complete ---")
    for p in processes:
        p.join()
    
    # --- Phase 5: Post-Load Performance Measurement ---
    print("\n--- Phase 5: Post-Load Performance Measurement ---")
    print("Attempting the same simple task after services have exited...")
    start_time_post_load = time.time()
    _ = [x * x for x in range(5_000_000)] # The same simple task
    end_time_post_load = time.time()
    post_load_duration = end_time_post_load - start_time_post_load
    print(f"Simple task completed post-load in {post_load_duration:.4f} seconds.")

    # --- Summary ---
    print("\n--- Summary of Performance Impact ---")
    print(f"Baseline task duration: {baseline_duration:.4f} seconds")
    print(f"Task duration under load: {under_load_duration:.4f} seconds")
    print(f"Task duration post-load: {post_load_duration:.4f} seconds")

    if under_load_duration > baseline_duration * 1.5: # Arbitrary threshold for "significant slowdown"
        print("\nObservation: The simple task took significantly longer to complete when the")
        print("simulated 'great stack' services were active and consuming resources.")
        print("This demonstrates how cumulative resource pressure (memory, CPU) can make")
        print("a Linux system's applications slow down and become 'unworkable' without a crash.")
        print("This is often an 'Engineer Panic' scenario.")
    else:
        print("\nObservation: The impact on the simple task was not very significant.")
        print("You might need to increase MEMORY_PER_PROCESS_MB or NUM_PROCESSES,")
        print("or run on a system with less available RAM to observe a stronger effect.")
    
    print("\n--- Simulation Complete ---")

if __name__ == "__main__":
    # Required for multiprocessing to work correctly on some OSes (e.g., Windows)
    multiprocessing.freeze_support() 
    main()
