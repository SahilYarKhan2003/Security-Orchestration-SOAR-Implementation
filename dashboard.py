# ============================================================
# MINI SOAR - FLASK WEB DASHBOARD
# ============================================================
# FEATURES:
#
# 1. Display all security incidents.
# 2. Display incident statistics.
# 3. Update incident status.
# 4. Log analyst status changes.
# 5. Run Flask dashboard reliably without debug reloader.
# ============================================================


# Import required Python libraries
import logging
import os


# Import Flask components
from flask import Flask, render_template, redirect, url_for


# Import required database functions
from database import (
    create_database,
    get_all_incidents,
    update_incident_status
)


# ============================================================
# LOGGING CONFIGURATION
# ============================================================


# Create the logs folder if it does not exist
os.makedirs("logs", exist_ok=True)


# Configure audit logging
logging.basicConfig(

    filename="logs/soar.log",

    level=logging.INFO,

    format="%(asctime)s | %(levelname)s | %(message)s",

    datefmt="%Y-%m-%d %H:%M:%S"
)


# Create logger object
logger = logging.getLogger(__name__)


# ============================================================
# CREATE FLASK APPLICATION
# ============================================================


app = Flask(__name__)


# ============================================================
# ROUTE: MAIN DASHBOARD
# ============================================================


@app.route("/")
def dashboard():

    # Ensure database exists
    create_database()


    # Retrieve all security incidents
    incidents = get_all_incidents()


    # --------------------------------------------------------
    # CALCULATE INCIDENT STATISTICS
    # --------------------------------------------------------


    # Total number of incidents
    total_incidents = len(incidents)


    # Count HIGH severity incidents
    high_count = sum(

        1 for incident in incidents

        if incident[3] == "HIGH"
    )


    # Count MEDIUM severity incidents
    medium_count = sum(

        1 for incident in incidents

        if incident[3] == "MEDIUM"
    )


    # Count LOW severity incidents
    low_count = sum(

        1 for incident in incidents

        if incident[3] == "LOW"
    )


    # --------------------------------------------------------
    # DISPLAY DASHBOARD
    # --------------------------------------------------------


    return render_template(

        "dashboard.html",

        incidents=incidents,

        total_incidents=total_incidents,

        high_count=high_count,

        medium_count=medium_count,

        low_count=low_count
    )


# ============================================================
# ROUTE: UPDATE INCIDENT STATUS
# ============================================================


@app.route(
    "/update_status/<int:incident_id>/<new_status>",
    methods=["POST"]
)
def update_status(incident_id, new_status):


    # --------------------------------------------------------
    # GET INCIDENT INFORMATION BEFORE UPDATE
    # --------------------------------------------------------


    incidents = get_all_incidents()


    # Search for selected incident
    selected_incident = next(

        (

            incident

            for incident in incidents

            if incident[0] == incident_id

        ),

        None
    )


    # --------------------------------------------------------
    # GET OLD STATUS AND ALERT NAME
    # --------------------------------------------------------


    if selected_incident:

        old_status = selected_incident[8]

        alert_name = selected_incident[1]


    else:

        old_status = "UNKNOWN"

        alert_name = "UNKNOWN"


    # --------------------------------------------------------
    # UPDATE INCIDENT STATUS
    # --------------------------------------------------------


    was_updated = update_incident_status(

        incident_id,

        new_status
    )


    # --------------------------------------------------------
    # LOG SUCCESSFUL STATUS CHANGE
    # --------------------------------------------------------


    if was_updated:

        logger.info(

            "STATUS_CHANGED | INCIDENT_ID=%s | "
            "ALERT=%s | OLD_STATUS=%s | NEW_STATUS=%s",

            incident_id,

            alert_name,

            old_status,

            new_status
        )


    # --------------------------------------------------------
    # LOG FAILED STATUS CHANGE
    # --------------------------------------------------------


    else:

        logger.warning(

            "STATUS_CHANGE_FAILED | "
            "INCIDENT_ID=%s | REQUESTED_STATUS=%s",

            incident_id,

            new_status
        )


    # Return to dashboard
    return redirect(url_for("dashboard"))


# ============================================================
# START FLASK WEB SERVER
# ============================================================


if __name__ == "__main__":


    print("=" * 60)

    print("MINI SOAR - WEB DASHBOARD")

    print("=" * 60)


    print("\nStarting dashboard...")


    print("\nOpen this address in your browser:")

    print("http://127.0.0.1:5000")


    print("\nPress CTRL + C to stop the dashboard.\n")


    # Start Flask server.
    #
    # debug=False:
    # Disables Flask debugging mode.
    #
    # use_reloader=False:
    # Prevents Flask from automatically restarting
    # the Python process.
    #
    # threaded=True:
    # Allows Flask to handle browser requests normally.

    app.run(

        host="127.0.0.1",

        port=5000,

        debug=False,

        use_reloader=False,

        threaded=True
    )