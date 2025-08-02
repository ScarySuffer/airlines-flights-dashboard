# convert_csv_to_json.py
import pandas as pd
import json
import os

def parse_duration_to_minutes(duration_str):
    """Convert a duration like '2h 30m' or '45m' into total minutes."""
    if not isinstance(duration_str, str):
        return None  # Handle NaN or float types gracefully

    duration_str = duration_str.strip().lower()
    total_minutes = 0

    if 'h' in duration_str:
        parts = duration_str.split('h')
        try:
            hours = int(parts[0].strip())
            total_minutes += hours * 60
        except ValueError:
            pass
        if len(parts) > 1 and 'm' in parts[1]:
            minutes_part = parts[1].replace('m', '').strip()
            if minutes_part.isdigit():
                total_minutes += int(minutes_part)
    elif 'm' in duration_str:
        minutes_str = duration_str.replace('m', '').strip()
        if minutes_str.isdigit():
            total_minutes += int(minutes_str)

    return total_minutes


# --- File paths ---
csv_path = os.path.join('data', 'airlines_flights_data.csv')
json_output_path = os.path.join('dashboard', 'public', 'data', 'flights.json')

# --- Columns to keep ---
columns_to_keep = [
    'airline',
    'source_city',
    'destination_city',
    'departure_time',
    'arrival_time',
    'duration',
    'price'
]

try:
    df = pd.read_csv(csv_path)

    # Drop the index column if present
    if 'index' in df.columns:
        df = df.drop(columns=['index'])

    # Keep only relevant columns
    df = df[columns_to_keep]

    # Add parsed duration in minutes
    df['duration_minutes'] = df['duration'].apply(parse_duration_to_minutes)

    # Convert to JSON
    json_data = df.to_json(orient='records', indent=2)

    # Ensure output directory exists
    os.makedirs(os.path.dirname(json_output_path), exist_ok=True)

    # Save JSON
    with open(json_output_path, 'w') as f:
        f.write(json_data)

    print(f"✅ Successfully created JSON with duration_minutes at {json_output_path}")

except FileNotFoundError:
    print(f"❌ CSV not found at '{csv_path}' — check path.")
except KeyError as e:
    print(f"❌ Column error: {e}")
except Exception as e:
    print(f"❌ Unexpected error: {e}")
