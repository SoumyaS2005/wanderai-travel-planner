
import os
from concurrent.futures import ThreadPoolExecutor, TimeoutError

from google import genai
from tool import search_travel_info


MODEL_NAME = "gemini-3.6-flash"
SEARCH_TIMEOUT = 20
GEMINI_TIMEOUT = 60


def get_api_key():
    """Get the Gemini API key from the environment or Streamlit secrets."""
    api_key = os.environ.get("GEMINI_API_KEY")

    if not api_key:
        try:
            import streamlit as st
            api_key = st.secrets.get("GEMINI_API_KEY")
        except Exception:
            api_key = None

    if not api_key:
        raise RuntimeError(
            "Gemini API key is missing. Set GEMINI_API_KEY "
            "in your environment or Streamlit secrets."
        )

    return api_key


def plan_trip(destination, days, budget, interests):
    """Search for travel information and generate a personalized itinerary."""

    destination = destination.strip()
    interests = interests.strip() or "General sightseeing and local food"

    if not destination:
        raise ValueError("Please enter a destination.")

    if not 1 <= int(days) <= 60:
        raise ValueError("Trip duration must be between 1 and 60 days.")

    if float(budget) <= 0:
        raise ValueError("Budget must be greater than zero.")

    print("Searching the web for travel information...", flush=True)

    query = (
        f"Travel guide tourist attractions local food transportation "
        f"budget tips for {destination}"
    )

    # Run web search with a time limit.
    search_executor = ThreadPoolExecutor(max_workers=1)

    try:
        search_future = search_executor.submit(
            search_travel_info, query, 5
        )
        try:
            search_results = search_future.result(
                timeout=SEARCH_TIMEOUT
            )
        except TimeoutError:
            search_future.cancel()
            search_results = (
                "Web search took too long. Use general travel knowledge "
                "and clearly identify information that needs verification."
            )
    finally:
        search_executor.shutdown(wait=False, cancel_futures=True)

    print("Preparing your personalized travel plan...", flush=True)

    prompt = f"""
You are WanderAI, a helpful AI travel-planning assistant.

Create a practical, personalized travel itinerary using the information below.

DESTINATION: {destination}
TRIP DURATION: {days} days
TOTAL USER BUDGET: {budget}
USER INTERESTS: {interests}

WEB SEARCH RESULTS:
{search_results}

INSTRUCTIONS:
1. Create a day-by-day itinerary for exactly {days} days.
2. Consider the user's interests and total budget.
3. Include suggested attractions and activities for each day.
4. Suggest local food and practical transportation options.
5. Organize the plan using clear headings and bullet points.
6. Provide an approximate budget breakdown where reasonable.
7. Do not invent exact hotel prices, opening hours, or availability.
8. Clearly label estimates as approximate.
9. If search information is unavailable, use general knowledge and say
   that details should be verified.
10. Mention that travel prices and schedules may change.
11. Keep the itinerary useful, realistic, and easy to understand.

Return the itinerary in a readable format with a short introduction,
daily plans, approximate budget, practical tips, and a final checklist.
"""

    client = genai.Client(
        api_key=get_api_key(),
        http_options={"timeout": GEMINI_TIMEOUT * 1000}
    )

    try:
        with ThreadPoolExecutor(max_workers=1) as executor:
            future = executor.submit(
                client.models.generate_content,
                model=MODEL_NAME,
                contents=prompt
            )
            response = future.result(timeout=GEMINI_TIMEOUT)

    except TimeoutError:
        raise RuntimeError(
            "Gemini took too long to respond. Please try again."
        ) from None

    except Exception as error:
        raise RuntimeError(
            f"Gemini could not generate the itinerary: {error}"
        ) from error

    if not response.text:
        raise RuntimeError(
            "Gemini returned an empty response. Please try again."
        )

    return response.text


def get_travel_details():
    """Collect and validate travel details through the terminal."""

    destination = input("Enter destination: ").strip()

    if not destination:
        raise ValueError("Destination cannot be empty.")

    try:
        days = int(input("Enter trip duration in days: "))
        budget = float(input("Enter your total budget: "))
    except ValueError:
        raise ValueError(
            "Please enter a valid number of days and budget."
        ) from None

    interests = input(
        "Enter your interests (e.g. beaches, food, nature): "
    ).strip()

    if not 1 <= days <= 60:
        raise ValueError("Trip duration must be between 1 and 60 days.")

    if budget <= 0:
        raise ValueError("Budget must be greater than zero.")

    return destination, days, budget, interests


def main():
    print("\n" + "=" * 45)
    print("          WANDERAI TRAVEL PLANNER")
    print("=" * 45)

    try:
        destination, days, budget, interests = get_travel_details()
        itinerary = plan_trip(destination, days, budget, interests)

        print("\nYOUR PERSONALIZED TRAVEL PLAN\n")
        print(itinerary)

    except KeyboardInterrupt:
        print("\nTravel planning cancelled.")

    except Exception as error:
        print(f"\nUnable to create your travel plan: {error}")


if __name__ == "__main__":
    main()
