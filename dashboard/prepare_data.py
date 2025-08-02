# prepare_data.py (Place this file directly in the dashboard/ folder)

import pandas as pd
import json
import os
import numpy as np # Import numpy for np.nan

def parse_duration_to_minutes(duration_str):
    """
    Parses a duration string like "2h 30m" into total minutes.
    Returns None if the input is not a valid string or cannot be parsed.
    """
    if pd.isna(duration_str): # Check if it's NaN (Not a Number) from pandas
        return None
    if not isinstance(duration_str, str): # Check if it's not a string type at all
        return None # Or raise an error if you want to be strict

    total_minutes = 0
    # Lowercase and remove extra spaces to make parsing more robust
    duration_str = duration_str.lower().strip()

    try:
        if 'h' in duration_str:
            parts = duration_str.split('h')
            hours_str = parts[0].strip()
            if hours_str: # Ensure hours_str is not empty
                total_minutes += int(hours_str) * 60
            
            # Check for minutes part after 'h'
            if len(parts) > 1 and parts[1].strip():
                minutes_part = parts[1].strip()
                if 'm' in minutes_part:
                    minutes_str = minutes_part.replace('m', '').strip()
                    if minutes_str: # Ensure minutes_str is not empty
                        total_minutes += int(minutes_str)
        elif 'm' in duration_str: # Handles cases like "45m"
            minutes_str = duration_str.replace('m', '').strip()
            if minutes_str: # Ensure minutes_str is not empty
                total_minutes += int(minutes_str)
        else:
            # If neither 'h' nor 'm' are found, and it's a string,
            # it's an unexpected format. Return None.
            return None
    except ValueError:
        # Catch errors if int() conversion fails (e.g., "abc h")
        return None
    except Exception as e:
        # Catch any other unexpected errors during parsing
        print(f"Warning: Could not parse duration '{duration_str}'. Error: {e}")
        return None
        
    return total_minutes

# Paths relative to the 'dashboard' directory, where this script is located
csv_path = os.path.join('..', 'data', 'airlines_flights_data.csv')
json_output_path = os.path.join('public', 'data', 'flights.json')

try:
    df = pd.read_csv(csv_path)

    if 'index' in df.columns:
        df = df.drop(columns=['index'])

    # Apply the parsing function. Missing/unparseable values will become None.
    df['duration_minutes'] = df['duration'].apply(parse_duration_to_minutes)

    # Convert DataFrame to a list of dictionaries (JSON format)
    # df.to_json(orient='records') will convert Python None to JSON null, which is desirable.
    json_data = df.to_json(orient='records', indent=2)

    # Ensure output directory exists
    os.makedirs(os.path.dirname(json_output_path), exist_ok=True)

    # Save JSON
    with open(json_output_path, 'w') as f:
        f.write(json_data)

    print(f"✅ CSV converted to JSON with 'duration_minutes' (handling missing values) and saved to {json_output_path}")

except FileNotFoundError:
    print(f"❌ Error: CSV file not found at '{csv_path}'. Please ensure the path is correct from the 'dashboard' directory.")
except Exception as e:
    print(f"❌ An error occurred: {e}")