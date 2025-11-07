# Flask app that returns fake sleep data as JSON
# Uses sleep_gen.py

import os

from flask import Flask, jsonify, request, render_template
from app.sleep_gen import generate_sleep_night

# Import functions from fhir_untils.py
from fhir_utils import make_patient, make_condition_cancer, make_sleep_observation, make_bundle_with_sleep

# Make app
app = Flask(__name__)

# Home page to check if running
@app.route("/")
def home():
    return """
    <h1>Sleep Tracker API</h1>
    <p>Sleep Tracker demo application.</p>
    <p>The following routes show the system:</p>
    <ul>
        <li><a href="/sleep">/sleep</a> – View a sample JSON of generated sleep data</li>
        <li><a href="/dashboard">/dashboard</a> – View a chart visualization of sleep data</li>
        <li><a href="/fhir/observation">/fhir/observation</a> – View FHIR Bundle JSON for the sample patient</li>
        <li><a href="Refresh page to see different data</li>
    </ul>
    <p>This app demonstrates how synthetic sleep data can be represented and shared in FHIR format.</p>
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