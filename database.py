# ============================================================
# MINI SOAR - INCIDENT DATABASE
# ============================================================
# This module manages the SQLite database used by Mini SOAR.
#
# FEATURES:
# 1. Create the incident database.
# 2. Store security incidents.
# 3. Prevent duplicate incidents.
# 4. Retrieve stored incidents.
# 5. Update incident status.
# ============================================================


# Import SQLite library.
# SQLite is built into Python.
import sqlite3


# Name of the SQLite database file.
DATABASE_FILE = "soar_incidents.db"


# ============================================================
# FUNCTION: create_database()
# ============================================================
# Creates the SQLite database and incidents table.
#
# If the database already exists, it will NOT be deleted.
# If the incidents table already exists, it will NOT be
# created again.
# ============================================================

def create_database():

    try:

        # Connect to SQLite database.
        # SQLite automatically creates the database file
        # if it does not already exist.
        connection = sqlite3.connect(DATABASE_FILE)

        # Create a cursor for executing SQL commands.
        cursor = connection.cursor()


        # Create the incidents table.
        cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS incidents (

                id INTEGER PRIMARY KEY AUTOINCREMENT,

                alert_name TEXT NOT NULL,

                priority INTEGER NOT NULL,

                severity TEXT NOT NULL,

                timestamp TEXT NOT NULL,

                source_ip TEXT NOT NULL,

                destination_ip TEXT NOT NULL,

                response_action TEXT NOT NULL,

                status TEXT DEFAULT 'OPEN'

            )
            """
        )


        # Save database changes.
        connection.commit()

        # Close database connection.
        connection.close()


        print("[+] Incident database initialized successfully.")


        return True


    except sqlite3.Error as error:

        print("[ERROR] Failed to create database:", error)

        return False


# ============================================================
# FUNCTION: save_incident()
# ============================================================
# Saves a security incident into SQLite.
#
# Before inserting the incident, the function checks whether
# the same alert already exists.
#
# Duplicate identification uses:
#
# Alert Name
# Timestamp
# Source IP
# Destination IP
#
# RETURN VALUES:
#
# True  = New incident successfully stored.
#
# False = Duplicate incident or database error.
# ============================================================

def save_incident(incident, playbook_result):

    try:

        # Connect to SQLite database.
        connection = sqlite3.connect(DATABASE_FILE)

        cursor = connection.cursor()


        # ----------------------------------------------------
        # CHECK FOR DUPLICATE INCIDENT
        # ----------------------------------------------------

        cursor.execute(
            """
            SELECT id

            FROM incidents

            WHERE alert_name = ?

            AND timestamp = ?

            AND source_ip = ?

            AND destination_ip = ?
            """,

            (
                incident["alert_name"],

                incident["timestamp"],

                incident["source_ip"],

                incident["destination_ip"]
            )
        )


        # Retrieve matching incident.
        existing_incident = cursor.fetchone()


        # If the incident already exists, skip insertion.
        if existing_incident:

            print(
                f"[!] Duplicate incident skipped: "
                f"{incident['alert_name']}"
            )

            connection.close()

            return False


        # ----------------------------------------------------
        # INSERT NEW INCIDENT
        # ----------------------------------------------------

        cursor.execute(
            """
            INSERT INTO incidents (

                alert_name,

                priority,

                severity,

                timestamp,

                source_ip,

                destination_ip,

                response_action,

                status

            )

            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
            """,

            (
                incident["alert_name"],

                incident["priority"],

                playbook_result["severity"],

                incident["timestamp"],

                incident["source_ip"],

                incident["destination_ip"],

                playbook_result["response_action"],

                "OPEN"
            )
        )


        # Save database changes.
        connection.commit()

        # Close database connection.
        connection.close()


        print(
            f"[+] New incident stored: "
            f"{incident['alert_name']}"
        )


        return True


    except sqlite3.Error as error:

        print("[ERROR] Failed to store incident:", error)

        return False


# ============================================================
# FUNCTION: get_all_incidents()
# ============================================================
# Retrieves all security incidents from SQLite.
#
# Incidents are returned with the newest incident first.
# ============================================================

def get_all_incidents():

    try:

        # Connect to SQLite database.
        connection = sqlite3.connect(DATABASE_FILE)

        cursor = connection.cursor()


        # Retrieve all incidents.
        cursor.execute(
            """
            SELECT *

            FROM incidents

            ORDER BY id DESC
            """
        )


        # Store database records.
        incidents = cursor.fetchall()


        # Close database connection.
        connection.close()


        return incidents


    except sqlite3.Error as error:

        print("[ERROR] Failed to retrieve incidents:", error)

        return []


# ============================================================
# FUNCTION: update_incident_status()
# ============================================================
# Changes the lifecycle status of a security incident.
#
# Allowed Status:
#
# OPEN
# INVESTIGATING
# RESOLVED
#
# RETURN VALUES:
#
# True  = Status successfully updated.
#
# False = Invalid status, incident not found, or database error.
# ============================================================

def update_incident_status(incident_id, new_status):

    # Allowed incident status values.
    allowed_statuses = [

        "OPEN",

        "INVESTIGATING",

        "RESOLVED"

    ]


    # --------------------------------------------------------
    # VALIDATE STATUS
    # --------------------------------------------------------

    if new_status not in allowed_statuses:

        print("[ERROR] Invalid incident status.")

        return False


    try:

        # Connect to SQLite database.
        connection = sqlite3.connect(DATABASE_FILE)

        cursor = connection.cursor()


        # ----------------------------------------------------
        # UPDATE INCIDENT STATUS
        # ----------------------------------------------------

        cursor.execute(
            """
            UPDATE incidents

            SET status = ?

            WHERE id = ?
            """,

            (
                new_status,

                incident_id
            )
        )


        # Check if the incident exists.
        if cursor.rowcount == 0:

            connection.close()

            print(
                f"[ERROR] Incident {incident_id} not found."
            )

            return False


        # Save database changes.
        connection.commit()

        # Close database connection.
        connection.close()


        print(
            f"[+] Incident {incident_id} status updated "
            f"to {new_status}."
        )


        return True


    except sqlite3.Error as error:

        print(
            "[ERROR] Failed to update incident status:",
            error
        )

        return False


# ============================================================
# DATABASE TEST SECTION
# ============================================================
# This section runs ONLY when database.py is directly executed.
#
# It DOES NOT insert any sample incidents.
#
# Command:
#
# python database.py
# ============================================================

if __name__ == "__main__":

    print("=" * 60)

    print("MINI SOAR - DATABASE TEST")

    print("=" * 60)


    # Initialize database.
    create_database()


    # Retrieve stored incidents.
    incidents = get_all_incidents()


    print(
        "\nTotal Stored Incidents:",
        len(incidents)
    )


    # Display stored incidents.
    for incident in incidents:

        print("\n" + "-" * 60)

        print("Incident ID      :", incident[0])

        print("Alert Name       :", incident[1])

        print("Priority         :", incident[2])

        print("Severity         :", incident[3])

        print("Timestamp        :", incident[4])

        print("Source IP        :", incident[5])

        print("Destination IP   :", incident[6])

        print("Response Action  :", incident[7])

        print("Status           :", incident[8])


    print("\n" + "=" * 60)

    print("DATABASE TEST COMPLETED")

    print("=" * 60)