# dashboard/convert_csv_to_json.py (or whatever you name it inside dashboard/)

import pandas as pd
import json
import os

def parse_duration_to_minutes(duration_str):
    """
    Parses a duration string like "2h 30m" into total minutes.
    Handles various formats including just hours or just minutes.
    """
    total_minutes = 0
    if 'h' in duration_str:
        parts = duration_str.split('h')
        hours = int(parts[0].strip())
        total_minutes += hours * 60
        if parts[1].strip() and 'm' in parts[1]: # Check if minutes part exists and contains 'm'
            minutes_part = parts[1].strip()
            # Handle cases like "1h" or "1h 30m"
            if 'm' in minutes_part:
                minutes_val = minutes_part.replace('m', '').strip()
                if minutes_val: # Ensure there's a numeric value for minutes
                    minutes = int(minutes_val)
                    total_minutes += minutes
    elif 'm' in duration_str: # Handles cases like "45m"
        minutes = int(duration_str.strip('m ').strip())
        total_minutes += minutes
    return total_minutes

# Paths relative to the 'dashboard' directory
# The raw CSV is in 'airlines-flights-dashboard/data', so from 'dashboard' it's '../../data'
csv_path = os.path.join('..', '..', 'data', 'airlines_flights_data.csv')
json_output_path = os.path.join('public', 'data', 'flights.json') # This path remains correct from 'dashboard'

try:
    # Load CSV
    df = pd.read_csv(csv_path)

    # Drop index column if exists (as per your original update)
    if 'index' in df.columns:
        df = df.drop(columns=['index'])

    # --- NEW: Apply duration parsing ---
    df['duration_minutes'] = df['duration'].apply(parse_duration_to_minutes)
    # --- END NEW ---

    # Convert to JSON
    json_data = df.to_json(orient='records', indent=2)

    # Ensure output directory exists
    os.makedirs(os.path.dirname(json_output_path), exist_ok=True)

    # Save JSON
    with open(json_output_path, 'w') as f:
        f.write(json_data)

    print(f"✅ CSV converted to JSON with 'duration_minutes' and saved to {json_output_path}")

except FileNotFoundError:
    print(f"❌ Error: CSV file not found at '{csv_path}'. Please ensure the path is correct from the 'dashboard' directory.")
except Exception as e:
    print(f"❌ An error occurred: {e}")