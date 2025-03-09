import concurrent.futures


def handle_futures(futures: list[concurrent.futures.Future]):
    for future in concurrent.futures.as_completed(futures):
        try:
            future.result()  # Ensures errors are caught
        except Exception as e:
            print(f"Error in processing {future}: {e}")
