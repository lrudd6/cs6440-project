import random
from datetime import datetime, timedelta

# Pick simple "sleep quality" and map it to a chance of being asleep.
def pick_sleep_quality():
    quality = random.choice(["great", "good", "bad"])
    if quality == "great":
        return quality, 0.95
    elif quality == "good":
        return quality, 0.85
    else:
        return quality, 0.65

# Make up fake sleep data for one night
# Use 1 for "asleep" and 0 for "awake" at given time intervals (Currently every minute)
def generate_sleep_night(date=None, bedtime="23:00", waketime="07:00", interval=1, chance_asleep=None):

    # If no date is given, use today's date as default
    if date is None:
        date = datetime.now().strftime("%Y-%m-%d")

    # If no chance_asleep is given, pick quality level for the night
    if chance_asleep is None:
        quality, chance_asleep = pick_sleep_quality()
    else:
        # If user passes enters value, label it "custom"
        quality = "custom"

    # Turn date and times into real datetime values
    start_time = datetime.strptime(f"{date} {bedtime}", "%Y-%m-%d %H:%M")
    end_time = datetime.strptime(f"{date} {waketime}", "%Y-%m-%d %H:%M")

    # If wake time is after midnight, add a day
    if end_time < start_time:
        end_time += timedelta(days=1)

    # Determine number of intervals (Currently every minute)
    total_minutes = int((end_time - start_time).total_seconds() / 60)
    data_points = total_minutes // interval

    # Make list of 1s and 0s for asleep and awake
    sleep_data = []
    for _ in range(data_points):
        if random.random() < chance_asleep:
            sleep_data.append(1)
        else:
            sleep_data.append(0)

    # Add total time was asleep
    asleep_minutes = sum(sleep_data) * interval
    total_sleep_hours = round(asleep_minutes / 60, 2)

    # Put everything into a dictionary to use later
    result = {
        "date": date,
        "bedtime": bedtime,
        "waketime": waketime,
        "interval_minutes": interval,
        "sleep_quality": quality,
        "chance_asleep": round(chance_asleep, 2),
        "total_sleep_hours": total_sleep_hours,
        "sleep_data": sleep_data
    }

    return result