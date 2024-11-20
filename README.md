# IOS-XE-Configuration-Parser
This script is designed to parse a Cisco IOS-XE device configuration file, extract key details, and save them into two different file formats (JSON and CSV).
It is beginner-friendly and includes robust error handling, making it ideal for learning and understanding Python scripting in the context of network automation.

**What the Script Does**


**1. Parses the Configuration File:**

- Reads a Cisco IOS-XE configuration file stored locally (no connection to the device is required).
- Extracts important details:
  - Hostname: The name of the device.
  - Serial Number: The unique identifier of the device.
  - Interfaces: Details of physical and logical interfaces (GigabitEthernet, Loopback, and subinterfaces).
  - Description: Any description provided for the interface.
  - IP Address: The assigned IP address and subnet mask.
  - VLAN ID: For subinterfaces configured with dot1Q.
    
**2. Saves the Extracted Data:**

- JSON File: Outputs a structured JSON file named parsed_<hostname>_config.json, which can be used for automation or integration with other tools.
- CSV File: Outputs a readable CSV file named parsed_<hostname>_config.csv, listing details in two columns: Variable and Value.
  
**3. Error Handling:**

- Ensures the script doesn’t crash when encountering missing files, incorrect configurations, or permission errors.
- Provides clear messages for any issues encountered

  
