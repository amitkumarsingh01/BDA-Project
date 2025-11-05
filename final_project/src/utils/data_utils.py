"""
Utility Functions for ED Demand Forecasting
"""
from datetime import datetime, timedelta
import random
from typing import List, Dict
import pandas as pd
import numpy as np

# Common chief complaints in Emergency Departments
CHIEF_COMPLAINTS = [
    'Chest Pain', 'Shortness of Breath', 'Abdominal Pain', 'Fever',
    'Headache', 'Trauma', 'Back Pain', 'Dizziness', 'Nausea/Vomiting',
    'Cough', 'Weakness', 'Seizure', 'Unconscious', 'Allergic Reaction'
]

# Gender distribution
GENDERS = ['M', 'F']

def generate_patient_id() -> str:
    """Generate a unique patient ID"""
    return f"PAT{random.randint(100000, 999999)}"

def get_triage_level_distribution() -> int:
    """Generate triage level based on realistic distribution"""
    # Level 1: 5%, Level 2: 15%, Level 3: 40%, Level 4: 30%, Level 5: 10%
    weights = [0.05, 0.15, 0.40, 0.30, 0.10]
    return random.choices(range(1, 6), weights=weights)[0]

def get_chief_complaint() -> str:
    """Randomly select a chief complaint"""
    return random.choice(CHIEF_COMPLAINTS)

def simulate_temperature() -> float:
    """Simulate body temperature (normal: 36.5-37.5°C, fever: >38°C)"""
    if random.random() < 0.3:  # 30% chance of fever
        return round(random.uniform(38.0, 40.0), 1)
    return round(random.uniform(36.5, 37.5), 1)

def is_holiday(date: datetime) -> bool:
    """Check if date is a holiday (simplified)"""
    # Simple check for major holidays
    holidays = [
        (1, 1),   # New Year
        (12, 25), # Christmas
        (7, 4),   # Independence Day (US example)
    ]
    return (date.month, date.day) in holidays

def get_arrival_rate_factor(hour: int, day_of_week: int, is_holiday: bool) -> float:
    """
    Calculate arrival rate multiplier based on time patterns
    Returns a factor that multiplies base arrival rate
    """
    # Hourly pattern: peak during day, lower at night
    hour_factor = 0.3 + 0.7 * np.sin((hour - 6) * np.pi / 12) if hour >= 6 else 0.3
    
    # Weekly pattern: lower on weekends
    day_factor = 0.7 if day_of_week >= 5 else 1.0
    
    # Holiday factor: typically lower except for trauma
    holiday_factor = 0.6 if is_holiday else 1.0
    
    return hour_factor * day_factor * holiday_factor

def aggregate_arrivals_by_time_window(
    arrivals: List[Dict],
    window_minutes: int = 15
) -> pd.DataFrame:
    """
    Aggregate patient arrivals into time windows
    Returns DataFrame with columns: timestamp, count
    """
    if not arrivals:
        return pd.DataFrame(columns=['timestamp', 'count'])
    
    df = pd.DataFrame(arrivals)
    df['arrival_time'] = pd.to_datetime(df['arrival_time'])
    df['window'] = df['arrival_time'].dt.floor(f'{window_minutes}T')
    
    aggregated = df.groupby('window').size().reset_index(name='count')
    aggregated.columns = ['timestamp', 'count']
    
    return aggregated

def create_time_features(df: pd.DataFrame) -> pd.DataFrame:
    """Create time-based features for forecasting"""
    if 'timestamp' not in df.columns:
        return df
    
    df['hour'] = pd.to_datetime(df['timestamp']).dt.hour
    df['day_of_week'] = pd.to_datetime(df['timestamp']).dt.dayofweek
    df['month'] = pd.to_datetime(df['timestamp']).dt.month
    df['is_weekend'] = (df['day_of_week'] >= 5).astype(int)
    df['is_night'] = ((df['hour'] >= 22) | (df['hour'] < 6)).astype(int)
    df['is_day'] = ((df['hour'] >= 8) & (df['hour'] < 18)).astype(int)
    
    return df

def calculate_statistics(arrivals: List[Dict]) -> Dict:
    """Calculate real-time statistics from arrivals"""
    if not arrivals:
        return {
            'total_arrivals': 0,
            'avg_triage_level': 0,
            'common_complaints': {}
        }
    
    df = pd.DataFrame(arrivals)
    
    return {
        'total_arrivals': len(arrivals),
        'avg_triage_level': df['triage_level'].mean() if 'triage_level' in df.columns else 0,
        'common_complaints': df['chief_complaint'].value_counts().head(5).to_dict() if 'chief_complaint' in df.columns else {},
        'timestamp': datetime.now().isoformat()
    }

