# ============================================================
# MINI SOAR - SEVERITY CLASSIFICATION & RESPONSE PLAYBOOK
# ============================================================
# This module:
# 1. Converts Snort priority into severity.
# 2. Selects an automated response based on severity.
# 3. Returns the response details to the main SOAR program.
#
# IMPORTANT:
# This student version simulates response actions.
# It does not actually block IP addresses or modify the firewall.
# ============================================================


# Function to classify the severity of an incident
def classify_severity(priority):

    # In Snort, Priority 1 represents the most serious alerts
    if priority == 1:
        return "HIGH"

    # Priority 2 represents medium-level alerts
    elif priority == 2:
        return "MEDIUM"

    # Priority 3 and above are treated as low severity
    else:
        return "LOW"


# Function to execute the appropriate response playbook
def execute_playbook(incident):

    # Get the priority from the incident
    priority = incident["priority"]

    # Convert priority into a severity level
    severity = classify_severity(priority)

    # Get useful information from the incident
    source_ip = incident["source_ip"]
    alert_name = incident["alert_name"]


    # --------------------------------------------------------
    # HIGH SEVERITY PLAYBOOK
    # --------------------------------------------------------

    if severity == "HIGH":

        response_action = (
            f"Recommend blocking source IP {source_ip}, "
            f"create a high-priority incident, and notify the security analyst."
        )


    # --------------------------------------------------------
    # MEDIUM SEVERITY PLAYBOOK
    # --------------------------------------------------------

    elif severity == "MEDIUM":

        response_action = (
            f"Add source IP {source_ip} to the watchlist "
            f"and investigate additional activity."
        )


    # --------------------------------------------------------
    # LOW SEVERITY PLAYBOOK
    # --------------------------------------------------------

    else:

        response_action = (
            f"Record the alert for source IP {source_ip} "
            f"and continue monitoring."
        )


    # Return the result as a dictionary
    return {

        "alert_name": alert_name,

        "source_ip": source_ip,

        "severity": severity,

        "response_action": response_action
    }


# ============================================================
# TEST THE PLAYBOOK
# ============================================================

if __name__ == "__main__":

    # Create a sample incident for testing
    sample_incident = {

        "alert_name": "Suspicious SSH Connection",

        "priority": 1,

        "timestamp": "07/14-12:32:25.987654",

        "source_ip": "192.168.1.70",

        "destination_ip": "192.168.1.10"
    }


    print("=" * 60)

    print("MINI SOAR - AUTOMATED RESPONSE PLAYBOOK")

    print("=" * 60)


    # Execute the response playbook
    result = execute_playbook(sample_incident)


    print("\nAlert Name      :", result["alert_name"])

    print("Source IP       :", result["source_ip"])

    print("Severity        :", result["severity"])

    print("Response Action :", result["response_action"])


    print("\n" + "=" * 60)

    print("PLAYBOOK EXECUTION COMPLETED")

    print("=" * 60)