import os
import ephem
import pandas as pd
from datetime import datetime, timedelta

def calculate_lunar_phases(start_date: datetime = None) -> pd.DataFrame:
    """Calculate lunar phases starting from the given date (or default to 5 years ago).

    Args:
        start_date (datetime, optional): Start date for calculating lunar phases. Defaults to 5 years ago.

    Returns:
        pd.DataFrame: A dataframe containing dates and their corresponding lunar phases.
    """
    end_date = datetime.now()
    if start_date is None:
        start_date = end_date - timedelta(days=5*365)
    directory = "src/moonedge/data"
    filename = f"{directory}/lunar_phases_{start_date.strftime('%Y-%m-%d')}_{end_date.strftime('%Y-%m-%d')}.csv"

    try:
        # Create directory if it doesn't exist
        if not os.path.exists(directory):
            os.makedirs(directory)

        # Check if data already exists on disk
        if os.path.exists(filename):
            return pd.read_csv(filename, index_col='date', parse_dates=True)

        phases = []
        current_date = start_date

        while current_date <= end_date:
            moon = ephem.Moon(current_date)
            phase_name = moon.phase
            phases.append({
                "date": current_date.strftime('%Y-%m-%d'),
                "phase": phase_name
            })
            current_date += timedelta(days=1)

        df = pd.DataFrame(phases)
        df.to_csv(filename, index=False)

        return df

    except Exception as e:
        raise RuntimeError(f"Error calculating lunar phases: {e}")