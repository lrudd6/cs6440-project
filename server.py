# Flask app that returns fake sleep data as JSON
# Uses sleep_gen.py

import os

from flask import Flask, jsonify, request, render_template
from app.sleep_gen import generate_sleep_night, generate_sleep_series

from datetime import datetime

# Import functions from fhir_untils.py
from fhir_utils import make_patient, make_condition_cancer, make_sleep_observation, make_bundle_with_sleep

# Make app
app = Flask(__name__)

# Home page to check if running
@app.route("/")
def home():
    return """
    <h2>Sleep Tracker Project</h2>
    <p>Here are the pages you can try:</p>

    <p>/sleep - this makes one night of sleep data</p>

    <p>/sleep/series?nights=5 - this makes several nights of sleep data</p>

    <p>/dashboard - this shows a simple chart</p>

    <p>/fhir/observation - this shows the sleep data as a FHIR Bundle</p>
    """

# Main route that gives back sleep data
@app.route("/sleep")
def get_sleep():
    # URL option
    date = request.args.get("date")
    bedtime = request.args.get("bedtime", "23:00")
    waketime = request.args.get("waketime", "07:00")
    interval = request.args.get("interval", default=1, type=int)
    chance_asleep = request.args.get("chance_asleep", type=float)

    # Make fake sleep data
    sleep_info = generate_sleep_night(
        date=date,
        bedtime=bedtime,
        waketime=waketime,
        interval=interval,
        chance_asleep=chance_asleep
    )

    # Send back as JSON
    return jsonify(sleep_info)

# Route for multiple nights of sleep
@app.route("/sleep/series")
def get_sleep_series():
    # Read "nights" from the URL, default 5
    nights = request.args.get("nights", default=5, type=int)

    # Use today as last night
    today_str = datetime.now().strftime("%Y-%m-%d")

    # Call helper that makes series
    series = generate_sleep_series(
        start_date=today_str,
        num_nights=nights,
        bedtime="23:00",
        waketime="07:00",
        interval=10
    )

    # Send back in JSON format
    return jsonify(series)

# Route made-up FHIR Bundle that links together fake patient, cancer condition, and sleep data.
@app.route("/fhir/observation")
def get_fhir_observation():
    # Make a night of sleep data using the same function as /sleep
    sleep_info = generate_sleep_night()

    # Make fake patient ID
    patient = make_patient(patient_id="patient-001")

    # Make a fake cancer "Condition"
    condition = make_condition_cancer(
        patient_id="patient-001",
        condition_id="cond-cancer-001"
    )

    # Use the sleep data to make FHIR Observation entry
    observation = make_sleep_observation(
        sleep_dict=sleep_info,
        patient_id="patient-001",
        condition_id="cond-cancer-001"
    )

    # Bundle patient, condition, and observation
    bundle = make_bundle_with_sleep(patient, condition, observation)

    # Send back in JSON format
    return jsonify(bundle)

@app.route("/fhir/view")
def fhir_view():
    """
    Small helper page to show the same FHIR bundle
    but in a more readable way for humans.
    """
    sleep_info = generate_sleep_night()
    patient = make_patient(patient_id="patient-001")
    condition = make_condition_cancer(
        patient_id="patient-001",
        condition_id="cond-cancer-001"
    )
    observation = make_sleep_observation(
        sleep_dict=sleep_info,
        patient_id="patient-001",
        condition_id="cond-cancer-001"
    )
    bundle = make_bundle_with_sleep(patient, condition, observation)

    # Pull out a few fields for the page
    total_hours = sleep_info.get("total_sleep_hours")
    quality = sleep_info.get("sleep_quality")
    date = sleep_info.get("date")

    return render_template(
        "fhir_view.html",
        bundle=bundle,
        total_hours=total_hours,
        quality=quality,
        date=date
    )

# Simple HTML dashboard page
@app.route("/dashboard")
def dashboard():
    # Renders templates/dashboard.html
    return render_template("dashboard.html")

# Run app locally or on Render (this portion has been modified since last version)
if __name__ == "__main__":
    # Render gives PORT number automatically. Use 5000 locally
    port = int(os.environ.get("PORT", 5000))
    # host="0.0.0.0" to listens on all network connections
    app.run(host="0.0.0.0", port=port, debug=True)