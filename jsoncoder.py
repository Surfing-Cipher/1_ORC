import re
import json


def extract_data_from_file(file_path):
    data = {
        "records": [],
        "file_name": "",
    }
    with open(file_path, 'r', encoding='utf-8') as file:
        record = {}
        for line in file:
            line = line.strip()
            if match := re.match(r'Text extracted from (.*):', line):
                data["file_name"] = match.group(1)
            elif match := re.match(r'^NO\.: (\d+)$', line):
                record["serial_number"] = match.group(1)
            elif match := re.match(r'^NAME: (.+)$', line):
                names = match.group(1).split()
                # Assigning names based on the split parts
                if len(names) == 3:
                    record["first_name"], record["middle_name"], record["last_name"] = names
                elif len(names) == 2:
                    record["first_name"], record["last_name"] = names
                    record["middle_name"] = ''
                else:
                    record["first_name"] = names[0] if names else ''
                    record["middle_name"] = ''
                    record["last_name"] = ' '.join(
                        names[1:]) if len(names) > 1 else ''
            # Extract other fields in a similar pattern
            elif match := re.match(r'^ALLEGED OFFENSE: (.+)$', line):
                record["offense"] = match.group(1)
            elif match := re.match(r'^DATE OF BIRTH: (.+)$', line):
                record["date_of_birth"] = match.group(1)
            # Add more fields and handle cases similarly

            elif not line and record:
                # Filter out empty values from the record
                filtered_record = {k: v for k, v in record.items() if v}
                data["records"].append(filtered_record)
                record = {}

    # Append the last record if not empty and no blank line follows the last data
    if record:
        filtered_record = {k: v for k, v in record.items() if v}
        data["records"].append(filtered_record)

    return data


def main():
    file_path = 'DENTON/DENTON_ocr_result.txt'  # Replace with your file path
    data = extract_data_from_file(file_path)
    output_file_name = file_path.split('.')[0] + '.json'
    with open(output_file_name, 'w') as json_file:
        json.dump(data, json_file, indent=2)


if __name__ == "__main__":
    main()
