# ============================================================
# MINI SOAR - MAIN ORCHESTRATION ENGINE WITH AUDIT LOGGING
# ============================================================

import logging
import os

from alert_parser import parse_snort_alerts
from playbook import execute_playbook
from database import create_database, save_incident


# ============================================================
# LOGGING CONFIGURATION
# ============================================================

# Create logs folder if it does not exist
os.makedirs("logs", exist_ok=True)

# Configure the audit log file
logging.basicConfig(
    filename="logs/soar.log",
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S"
)

logger = logging.getLogger(__name__)


# ============================================================
# FUNCTION: run_soar()
# ============================================================

def run_soar():

    print("=" * 65)
    print("MINI SOAR - SECURITY ORCHESTRATION & AUTOMATED RESPONSE")
    print("=" * 65)

    logger.info("SOAR_EXECUTION_STARTED")


    # --------------------------------------------------------
    # STEP 1: INITIALIZE DATABASE
    # --------------------------------------------------------

    print("\n[1] INITIALIZING INCIDENT DATABASE")

    database_created = create_database()

    if not database_created:

        logger.error("DATABASE_INITIALIZATION_FAILED")

        print("[ERROR] Unable to initialize database.")

        return

    logger.info("DATABASE_INITIALIZED")


    # --------------------------------------------------------
    # STEP 2: READ SNORT ALERTS
    # --------------------------------------------------------

    print("\n[2] READING SNORT SECURITY ALERTS")

    incidents = parse_snort_alerts()

    print(f"[+] Total alerts detected: {len(incidents)}")

    logger.info(
        "ALERT_FILE_PARSED | ALERT_COUNT=%s",
        len(incidents)
    )


    # Stop if no alerts exist
    if not incidents:

        print("[!] No alerts available.")

        logger.info("NO_ALERTS_DETECTED")

        return


    # --------------------------------------------------------
    # STEP 3: PROCESS INCIDENTS
    # --------------------------------------------------------

    print("\n[3] PROCESSING SECURITY INCIDENTS")

    stored_count = 0


    for incident_number, incident in enumerate(
        incidents,
        start=1
    ):

        print("\n" + "-" * 65)

        print(f"PROCESSING INCIDENT {incident_number}")

        print("-" * 65)


        print("Alert Name      :", incident["alert_name"])
        print("Priority        :", incident["priority"])
        print("Timestamp       :", incident["timestamp"])
        print("Source IP       :", incident["source_ip"])
        print("Destination IP  :", incident["destination_ip"])


        # ----------------------------------------------------
        # RECORD ALERT PROCESSING EVENT
        # ----------------------------------------------------

        logger.info(
            "ALERT_PROCESSED | ALERT=%s | PRIORITY=%s | "
            "SOURCE=%s | DESTINATION=%s",
            incident["alert_name"],
            incident["priority"],
            incident["source_ip"],
            incident["destination_ip"]
        )


        # ----------------------------------------------------
        # EXECUTE RESPONSE PLAYBOOK
        # ----------------------------------------------------

        playbook_result = execute_playbook(incident)


        print("\n[+] Severity Classification")

        print(
            "Severity         :",
            playbook_result["severity"]
        )


        print("\n[+] Automated Response Playbook")

        print(
            "Response Action  :",
            playbook_result["response_action"]
        )


        # Record playbook execution
        logger.info(
            "PLAYBOOK_EXECUTED | ALERT=%s | "
            "SEVERITY=%s | ACTION=%s",
            incident["alert_name"],
            playbook_result["severity"],
            playbook_result["response_action"]
        )


        # ----------------------------------------------------
        # SAVE INCIDENT
        # ----------------------------------------------------

        was_stored = save_incident(
            incident,
            playbook_result
        )


        if was_stored:

            stored_count += 1

            logger.info(
                "INCIDENT_STORED | ALERT=%s | "
                "SOURCE=%s | SEVERITY=%s",
                incident["alert_name"],
                incident["source_ip"],
                playbook_result["severity"]
            )

        else:

            logger.warning(
                "INCIDENT_SKIPPED | DUPLICATE | "
                "ALERT=%s | SOURCE=%s",
                incident["alert_name"],
                incident["source_ip"]
            )


        print("[+] Incident processing completed.")


    # --------------------------------------------------------
    # EXECUTION SUMMARY
    # --------------------------------------------------------

    print("\n" + "=" * 65)

    print("MINI SOAR EXECUTION SUMMARY")

    print("=" * 65)

    print("Alerts Processed :", len(incidents))

    print("Playbooks Run    :", len(incidents))

    print("Incidents Stored :", stored_count)


    logger.info(
        "SOAR_EXECUTION_COMPLETED | "
        "ALERTS_PROCESSED=%s | NEW_INCIDENTS=%s",
        len(incidents),
        stored_count
    )


    print("\nMINI SOAR EXECUTION COMPLETED SUCCESSFULLY")

    print("=" * 65)


# ============================================================
# START APPLICATION
# ============================================================

if __name__ == "__main__":

    run_soar()