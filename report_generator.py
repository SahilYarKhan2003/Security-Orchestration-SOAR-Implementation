# ============================================================
# MINI SOAR - INCIDENT REPORT GENERATOR
# ============================================================
# This module exports all security incidents stored in the
# SQLite database into a CSV report.
#
# OUTPUT:
#
# reports/incident_report.csv
#
# ============================================================


# Import CSV library for creating CSV files
import csv

# Import OS library for folder operations
import os

# Import function used to retrieve incidents from SQLite
from database import get_all_incidents


# Location of the generated report
REPORT_FILE = "reports/incident_report.csv"


# ============================================================
# FUNCTION: generate_incident_report()
# ============================================================

def generate_incident_report():

    try:

        # Create reports folder if it does not exist
        os.makedirs("reports", exist_ok=True)


        # Retrieve all incidents from SQLite database
        incidents = get_all_incidents()


        # Stop report generation if database is empty
        if not incidents:

            print("[!] No incidents available for report generation.")

            return False


        # Open CSV report file
        #
        # newline="" prevents empty lines from appearing
        # between CSV rows on Windows.
        #
        # encoding="utf-8" provides standard text encoding.

        with open(
            REPORT_FILE,
            "w",
            newline="",
            encoding="utf-8"
        ) as report_file:


            # Create CSV writer object
            writer = csv.writer(report_file)


            # ------------------------------------------------
            # WRITE REPORT HEADER
            # ------------------------------------------------

            writer.writerow(
                [
                    "Incident ID",
                    "Alert Name",
                    "Priority",
                    "Severity",
                    "Timestamp",
                    "Source IP",
                    "Destination IP",
                    "Automated Response",
                    "Status"
                ]
            )


            # ------------------------------------------------
            # WRITE INCIDENT DATA
            # ------------------------------------------------

            for incident in incidents:

                writer.writerow(
                    [
                        incident[0],
                        incident[1],
                        incident[2],
                        incident[3],
                        incident[4],
                        incident[5],
                        incident[6],
                        incident[7],
                        incident[8]
                    ]
                )


        # Display success message
        print("=" * 60)

        print("MINI SOAR - INCIDENT REPORT GENERATOR")

        print("=" * 60)

        print(f"\n[+] Total Incidents Exported: {len(incidents)}")

        print(f"[+] Report Generated: {REPORT_FILE}")

        print("\nINCIDENT REPORT GENERATED SUCCESSFULLY")

        print("=" * 60)


        return True


    except PermissionError:

        print(
            "[ERROR] Cannot create the report. "
            "Close incident_report.csv if it is open in Excel."
        )

        return False


    except Exception as error:

        print("[ERROR] Failed to generate incident report:", error)

        return False


# ============================================================
# STARTING POINT
# ============================================================

if __name__ == "__main__":

    generate_incident_report()