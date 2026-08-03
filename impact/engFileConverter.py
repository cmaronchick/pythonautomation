import json
import os

import chardet

def convert_eng_to_json(input_file, output_file):
    if not os.path.exists(input_file):
        print(f"Error: {input_file} not found.")
        return

    data = {}
    
    # Using utf-8-sig handles files with a BOM (common in Windows-created files)

    with open(input_file, 'rb') as file:
        raw_data = file.read()
        result = chardet.detect(raw_data)
        encoding = result['encoding']
        print('encoding: ', encoding)

    with open(input_file, 'r', encoding=encoding) as f:
        for line in f:
            line = line.strip()
            
            # Skip empty lines or the header
            if not line or line.startswith('['):
                continue
            
            if '=' in line:
                # Split only on the first '=' in case the text contains an '='
                key, value = line.split('=', 1)
                
                # Clean up whitespace and quotes
                key = key.strip()
                value = value.strip().strip('"')
                
                data[key] = value
                print(f"Captured: {key} = {value}")

    if not data:
        print("Warning: No data was captured. Printing file content for debug:")
        with open(input_file, 'r') as f:
            print(f.read())
        return

    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=4)
        print(f"Success! Saved to {output_file}")

if __name__ == "__main__":
    convert_eng_to_json('UI.eng', 'UI.json')