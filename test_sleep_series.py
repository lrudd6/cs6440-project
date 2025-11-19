# Test sleep_series function
from app.sleep_gen import generate_sleep_series

if __name__ == "__main__":
    # Make 5 nights starting from today.
    nights = generate_sleep_series(num_nights=5)

    print("Number of nights:", len(nights))
    print()

    # Print a short summary for each night.
    for night in nights:
        print(
            "Date:", night["date"],
            "| Hours:", night["total_sleep_hours"],
            "| Quality:", night["sleep_quality"]
        )