
from ddgs import DDGS
from concurrent.futures import ThreadPoolExecutor, TimeoutError


def _perform_search(query, max_results):
    """Perform a web search and return the results."""
    with DDGS() as ddgs:
        return list(ddgs.text(query, max_results=max_results))


def search_travel_info(query, max_results=5):
    """Search for travel information with a time limit."""

    executor = ThreadPoolExecutor(max_workers=1)
    future = executor.submit(_perform_search, query, max_results)

    try:
        results = future.result(timeout=15)

        if not results:
            return "No search results found. Continue using general travel knowledge."

        output = []

        for number, result in enumerate(results, start=1):
            output.append(
                f"{number}. {result.get('title', 'No title')}\n"
                f"   Link: {result.get('href', '')}\n"
                f"   Details: {result.get('body', 'No description')}"
            )

        return "\n\n".join(output)

    except TimeoutError:
        future.cancel()
        return "Web search timed out. Continue using general travel knowledge."

    except Exception as error:
        return (
            "Web search is temporarily unavailable. "
            f"Error: {error}\n"
            "Continue using general travel knowledge."
        )

    finally:
        executor.shutdown(wait=False, cancel_futures=True)


if __name__ == "__main__":
    query = input("What travel information do you want to search for? ").strip()

    if query:
        print("\nSearching the web...\n")
        print(search_travel_info(query))
    else:
        print("Please enter a search query.")
