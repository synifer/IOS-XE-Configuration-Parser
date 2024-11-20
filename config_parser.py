import re
import json
import csv
import os

def parse_ios_xe_config(file_path):
    """
    Parses the IOS-XE configuration file to extract:
    - Hostname
    - Serial Number
    - Interface details (GigabitEthernet, Loopback, subinterfaces)
    """
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"The file {file_path} does not exist.")

    with open(file_path, 'r') as file:
        config = file.read()

    result = {
        "hostname": None,
        "serial_number": None,
        "interfaces": []
    }

    # Extract hostname from the configuration
    hostname_match = re.search(r"^hostname\s+(\S+)", config, re.MULTILINE)
    if hostname_match:
        result["hostname"] = hostname_match.group(1)
    else:
        result["hostname"] = "unknown"  # Default hostname if not found

    # Extract serial number from the configuration
    serial_match = re.search(r"^license\s+udi\s+pid\s+\S+\s+sn\s+(\S+)", config, re.MULTILINE)
    if serial_match:
        result["serial_number"] = serial_match.group(1)
    else:
        result["serial_number"] = "not available"

    # Extract interfaces and their details
    interface_pattern = re.compile(
        r"^interface\s+(GigabitEthernet[\d/.]+|Loopback\d+)(.*?)^(?=\S)", 
        re.MULTILINE | re.DOTALL
    )
    interfaces = interface_pattern.findall(config)

    for interface, body in interfaces:
        interface_data = {
            "name": interface,
            "description": None,
            "ip_address": None,
            "dot1q_vlan": None
        }

        # Extract description for the interface
        description_match = re.search(r"^\s+description\s+(.+)", body, re.MULTILINE)
        if description_match:
            interface_data["description"] = description_match.group(1)

        # Extract IP address and subnet mask
        ip_address_match = re.search(r"^\s+ip address\s+(\S+)\s+(\S+)", body, re.MULTILINE)
        if ip_address_match:
            interface_data["ip_address"] = f"{ip_address_match.group(1)} {ip_address_match.group(2)}"

        # Extract dot1Q VLAN ID for subinterfaces
        dot1q_match = re.search(r"^\s+encapsulation\s+dot1Q\s+(\d+)", body, re.MULTILINE)
        if dot1q_match:
            interface_data["dot1q_vlan"] = dot1q_match.group(1)

        result["interfaces"].append(interface_data)

    return result


def save_to_csv(data, csv_file_path):
    """
    Saves the parsed data into a CSV file with two columns: Variable and Value.
    """
    try:
        with open(csv_file_path, 'w', newline='', encoding='utf-8') as csvfile:
            writer = csv.writer(csvfile)
            writer.writerow(["Variable", "Value"])

            # Write hostname
            writer.writerow(["Hostname", data["hostname"]])

            # Write serial number
            writer.writerow(["Serial Number", data["serial_number"]])

            # Write interface details
            for interface in data["interfaces"]:
                writer.writerow(["Interface Name", interface["name"]])
                writer.writerow(["Description", interface.get("description", "N/A")])
                writer.writerow(["IP Address", interface.get("ip_address", "N/A")])
                writer.writerow(["Dot1Q VLAN", interface.get("dot1q_vlan", "N/A")])
    except Exception as e:
        raise IOError(f"Failed to write to CSV file {csv_file_path}: {e}")


if __name__ == "__main__":
    try:
        # Input configuration file
        config_file = r'C:\Users\username\devices\ios-device.cfg'

        # Parse the configuration file
        parsed_data = parse_ios_xe_config(config_file)

        # Get the directory and hostname from the parsed data
        input_directory = os.path.dirname(config_file)
        hostname = parsed_data["hostname"] or "unknown"

        # Create output file names based on hostname
        #json_output_file = os.path.join(input_directory, f"parsed_{hostname}_config.json")
        csv_output_file = os.path.join(input_directory, f"parsed_{hostname}_config.csv")

        # Save parsed data to JSON
        #try:
        #    with open(json_output_file, "w", encoding='utf-8') as json_file:
        #        json.dump(parsed_data, json_file, indent=4, ensure_ascii=False)
        #except Exception as e:
        #    raise IOError(f"Failed to write to JSON file {json_output_file}: {e}")

        # Save parsed data to CSV
        save_to_csv(parsed_data, csv_output_file)

        # Success message
        #print(f"Parsing completed. Files saved:\n- {json_output_file}\n- {csv_output_file}")

    except FileNotFoundError as e:
        print(f"Error: {e}")
    except IOError as e:
        print(f"File Error: {e}")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
