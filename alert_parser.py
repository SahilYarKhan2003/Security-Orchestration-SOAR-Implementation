# ============================================================
# MINI SOAR - SNORT ALERT PARSER
# ============================================================
# This program reads security alerts from a Snort alert file
# and extracts useful information from each alert.
#
# Information extracted:
# 1. Alert Name
# 2. Priority
# 3. Timestamp
# 4. Source IP Address
# 5. Destination IP Address
# ============================================================

# Import Regular Expression library.
# Regex helps us search and extract patterns from text.
import re


# Location of our sample Snort alert file.
ALERT_FILE = "alerts/snort_alerts.log"


# ============================================================
# FUNCTION: parse_snort_alerts()
# ============================================================

def parse_snort_alerts():

    # Empty list used to store all parsed security incidents.
    incidents = []

    try:

        # Open the Snort alert file.
        with open(ALERT_FILE, "r") as file:

            # Read the complete contents of the file.
            content = file.read()


        # Snort alerts in our sample file are separated
        # by one empty line.
        alert_blocks = content.strip().split("\n\n")


        # Process every Snort alert separately.
        for block in alert_blocks:

            # Split the alert into individual lines.
            lines = block.strip().splitlines()


            # Skip incomplete alert blocks.
            if len(lines) < 3:
                continue


            # ------------------------------------------------
            # EXTRACT ALERT NAME
            # ------------------------------------------------

            # Example:
            #
            # [**] [1:1000001:1] ICMP Ping Detected [**]
            #
            # Extract:
            #
            # ICMP Ping Detected

            alert_match = re.search(
                r"\]\s(.+?)\s\[\*\*\]",
                lines[0]
            )


            # ------------------------------------------------
            # EXTRACT PRIORITY
            # ------------------------------------------------

            # Example:
            #
            # [Priority: 3]
            #
            # Extract:
            #
            # 3

            priority_match = re.search(
                r"Priority:\s*(\d+)",
                lines[1]
            )


            # ------------------------------------------------
            # EXTRACT TIMESTAMP AND IP ADDRESSES
            # ------------------------------------------------

            # Example:
            #
            # 07/14-12:30:15.123456
            # 192.168.1.50 -> 192.168.1.10

            network_match = re.search(
                r"(\S+)\s+"
                r"(\d{1,3}(?:\.\d{1,3}){3})"
                r"\s+->\s+"
                r"(\d{1,3}(?:\.\d{1,3}){3})",
                lines[2]
            )


            # Continue only if all required information exists.
            if alert_match and priority_match and network_match:

                # Create a structured incident dictionary.
                incident = {

                    "alert_name": alert_match.group(1),

                    "priority": int(priority_match.group(1)),

                    "timestamp": network_match.group(1),

                    "source_ip": network_match.group(2),

                    "destination_ip": network_match.group(3)
                }


                # Add the incident to our incident list.
                incidents.append(incident)


        # Return all parsed incidents.
        return incidents


    # Handle the error if the Snort alert file is missing.
    except FileNotFoundError:

        print("[ERROR] Snort alert file was not found.")

        return []


    # Handle any unexpected errors.
    except Exception as error:

        print("[ERROR] Failed to parse Snort alerts:", error)

        return []


# ============================================================
# TEST THE ALERT PARSER
# ============================================================
# This section runs only when alert_parser.py is executed
# directly.
#
# Later, soar.py will import parse_snort_alerts() and use it.

if __name__ == "__main__":

    print("=" * 60)

    print("MINI SOAR - SNORT ALERT PARSER")

    print("=" * 60)


    # Call our parser function.
    parsed_incidents = parse_snort_alerts()


    # Display total number of alerts detected.
    print(f"\nTotal Alerts Parsed: {len(parsed_incidents)}")


    # Display every parsed incident.
    for incident_number, incident in enumerate(
        parsed_incidents,
        start=1
    ):

        print("\n" + "-" * 60)

        print(f"INCIDENT {incident_number}")

        print("-" * 60)

        print("Alert Name      :", incident["alert_name"])

        print("Priority        :", incident["priority"])

        print("Timestamp       :", incident["timestamp"])

        print("Source IP       :", incident["source_ip"])

        print("Destination IP  :", incident["destination_ip"])


    print("\n" + "=" * 60)

    print("ALERT PARSING COMPLETED")

    print("=" * 60)