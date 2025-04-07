import time

from bb.lib.large_language_model import LLMMistral


def main():
    # Test LLMMistral
    llm = LLMMistral()
    print(llm.generate_text("What is the best French cheese?"))

    # Test LLMMistral speed
    times = []
    for i in range(10):
        start_time = time.time()
        llm.generate_text("What is the best French cheese?")
        end_time = time.time()
        time_of_execution = end_time - start_time
        print(f"Time taken: {time_of_execution} seconds")
        times.append(time_of_execution)
    print(f"LLM Mistral: Average time taken is {sum(times) / len(times)} seconds.")


if __name__ == "__main__":
    main()
