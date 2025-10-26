# Test sleep_gen.py program.
# Run one example night of sleep data and prints the results.

from app.sleep_gen import generate_sleep_night

# Make up one night of fake sleep data
sleep_info = generate_sleep_night(
    date="2025-10-19",
    bedtime="23:00",
    waketime="07:00",
    interval=1,
    chance_asleep=0.85
)

# Print summary
print("Sleep date:", sleep_info["date"])
print("Interval (minutes):", sleep_info["interval_minutes"])
print("Total sleep hours:", sleep_info["total_sleep_hours"])

# Print first few data points so we can see what it looks like
print("Sample signal (first 20 points):", sleep_info["sleep_data"][:20])