import re
import json


def extract_data_from_file(file_path):
    data = []
    with open(file_path, 'r') as file:
        lines = file.readlines()
        record = {}
        for line in lines:
            line = line.strip()
            if line:
                key, value = re.split(r':\s*', line, maxsplit=1)
                record[key] = value
            else:
                data.append(record)
                record = {}
        if record:
            data.append(record)
    return data


def main():
    file_path = 'NOLAN\NOLAN_ocr_result.txt'  # Replace with your file path
    data = extract_data_from_file(file_path)
    with open('output.json', 'w') as json_file:
        json.dump(data, json_file, indent=2)


if __name__ == "__main__":
    main()
