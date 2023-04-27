import time
import run
import debug

def main():
    start_time = time.time()

    debug.debug_print()

    run.run()

    end_time = time.time()
    runtime = end_time - start_time

    print()
    print(f"Program runtime: {runtime} seconds")

if __name__ == '__main__':
    main()


