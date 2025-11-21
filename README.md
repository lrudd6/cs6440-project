# CS6440 Project - Sleep Tracking for Cancer patients (with FHIR Integration)
This project simulates nightly sleep data for a synthetic cancer patient and exposes it through a small Flask application. The system includes multiple API endpoints, a dashboard for visualizing sleep patterns, and a FHIR-compliant Observation bundle for interoperability demonstration. All data is fully simulated.

The application provides:
- A binary sleep signal generator (asleep = 1, awake = 0)
- Nightly summaries: total hours slept and a randomized sleep-quality label
- Multi-night sleep series generation
- A FHIR Patient, Condition, and Observation Bundle
- A dashboard that displays sleep data over time using Chart.js
- A dedicated FHIR view page for visualizing the bundle in a formatted way

Live Deployment (Render)
The project is deployed through Render:
https://cs6440-project-1.onrender.com/
Recommended pages:
/dashboard — main sleep visualization dashboard
/sleep — single-night sleep data (JSON)
/sleep/series?nights=5 — multi-night sleep series
/fhir/observation — FHIR Bundle (raw JSON)
/fhir/view — formatted display of the FHIR Bundle

Note: Render may take up a minute or two to wake after inactivity

Repository Structure
app/
    sleep_gen.py        # Sleep generator module
templates/
    dashboard.html      # Dashboard with Chart.js
    fhir_view.html      # Human-readable FHIR page
static/
server.py               # Flask application
fhir_utils.py           # Patient/Condition/Observation builder
test_sleep_gen.py       # Basic tests for single-night generator
test_sleep_series.py    # Basic tests for multi-night generator
requirements.txt        # Python dependencies
Procfile                # Render deployment command
docs/
    Architecture_Diagram.jpeg   # Architecture diagram from Sprint #2
    Mockup.jpeg             # Mockup diagram from Sprint #2
README.md 

Installation (Local Run Instructions)
1. Clone the repository
git clone https://github.gatech.edu/Lael-Rudd/cs6440-project.git
cd cs6440-project

2. Create and activate a virtual environment
python -m venv .venv
source .venv/bin/activate      # macOS / Linux
.venv\Scripts\activate         # Windows

3. Install required packages
pip install -r requirements.txt

4. Run the Flask app
python server.py

5. Open your browser
Go to:

http://127.0.0.1:5000/dashboard


API Endpoints
/ – Home Page

Lists available routes with short descriptions.

/sleep – One Night of Sleep Data
Returns JSON with:
    start/end times
    binary sleep array
    sleep quality
    total hours

/sleep/series?nights=5 – Multiple Nights
Generates several nights of data at once.

/dashboard – Main Visualization Page
Displays:
    Line chart of total hours slept
    Night-by-night summary
    Sidebar with API links
    Patient info box

/fhir/observation – FHIR Bundle (Raw JSON)
    Returns a FHIR Bundle containing:
    Patient (ID: patient-001)
    Condition (Cancer)
    Observation (sleep duration + sampled data)

/fhir/view – Human-Readable FHIR Page
Formatted page showing:
    Patient summary
    Condition summary
    Observation summary
    Full JSON FHIR bundle (pretty-printed)

