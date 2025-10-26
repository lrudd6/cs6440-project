# FHIR (R4) JSON dictionaries.
# Keep small to better understand

from datetime import datetime

# Make Patient setting resourceType and an id.
def make_patient(patient_id="patient-001"):
    patient = {
        "resourceType": "Patient",
        "id": patient_id
    }
    return patient

# Make Condition for "Cancer" linked to patient.
def make_condition_cancer(patient_id="patient-001", condition_id="cond-cancer-001"):
    condition = {
        "resourceType": "Condition",
        "id": condition_id,
        "subject": {"reference": f"Patient/{patient_id}"},
        # Status
        "clinicalStatus": {
            "coding": [{
                "system": "http://terminology.hl7.org/CodeSystem/condition-clinical",
                "code": "active"
            }]
        },
        "verificationStatus": {
            "coding": [{
                "system": "http://terminology.hl7.org/CodeSystem/condition-ver-status",
                "code": "confirmed"
            }]
        },
        # Label cancer
        "code": {
            "text": "Cancer"
        }
    }
    return condition

# Make sleep observation:
# total sleep hours: valueQuantity
# SampledData inside component
def make_sleep_observation(sleep_dict, patient_id="patient-001",
                           condition_id="cond-cancer-001", obs_id=None):
    # Read values from the sleep_dict from sleep_gen.py
    date_str = sleep_dict.get("date")
    interval_minutes = sleep_dict.get("interval_minutes", 1)
    total_hours = float(sleep_dict.get("total_sleep_hours", 0.0))
    series = sleep_dict.get("sleep_data", [])

    # Make id based on the date if none exists
    if obs_id is None:
        obs_id = f"obs-sleep-{date_str}"

    # One pace seperated string for FHIR SampledData
    series_str = " ".join(str(x) for x in series)

    # Set FHIR R4 SampledData.period to milliseconds
    period_ms = float(interval_minutes) * 60.0 * 1000.0

    observation = {
        "resourceType": "Observation",
        "id": obs_id,
        "status": "final",
        "category": [{
            "coding": [{
                "system": "http://terminology.hl7.org/CodeSystem/observation-category",
                "code": "activity",
                "display": "Activity"
            }],
            "text": "Sleep"
        }],
        "code": {
            "text": "Sleep duration and binary signal"
        },
        "subject": {"reference": f"Patient/{patient_id}"},
        # Use the date as the effective time (midnight Z)
        "effectiveDateTime": f"{date_str}T00:00:00Z",
        # Total sleep hours
        "valueQuantity": {
            "value": total_hours,
            "unit": "hours"
        },
        #Sampled time series is raw 1/0 data
        "component": [
            {
                "code": {"text": "Sleep binary signal (1=asleep, 0=awake)"},
                "valueSampledData": {
                    "origin": {"value": 0, "unit": "binary"},
                    "period": period_ms,
                    "dimensions": 1,
                    "data": series_str
                }
            }
        ],
        # Link to the cancer Condition
        "hasMember": [
            {"reference": f"Condition/{condition_id}"}
        ]
    }

    return observation

# Make bundle with Patient + Condition + Observation together.
def make_bundle_with_sleep(patient, condition, observation):
    bundle = {
        "resourceType": "Bundle",
        "type": "collection",
        "entry": [
            {"resource": patient},
            {"resource": condition},
            {"resource": observation}
        ]
    }
    return bundle