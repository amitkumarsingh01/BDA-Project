"""
Data Models for Emergency Department Patient Arrivals
"""
from datetime import datetime
from typing import Dict, Optional
import json

class PatientArrival:
    """Model representing a patient arrival at Emergency Department"""
    
    def __init__(
        self,
        patient_id: str,
        arrival_time: datetime,
        age: int,
        gender: str,
        triage_level: int,
        chief_complaint: str,
        temperature: Optional[float] = None,
        is_holiday: bool = False,
        day_of_week: int = None,
        hour_of_day: int = None
    ):
        self.patient_id = patient_id
        self.arrival_time = arrival_time
        self.age = age
        self.gender = gender
        self.triage_level = triage_level  # 1-5 (1 = most urgent)
        self.chief_complaint = chief_complaint
        self.temperature = temperature
        self.is_holiday = is_holiday
        self.day_of_week = day_of_week or arrival_time.weekday()
        self.hour_of_day = hour_of_day or arrival_time.hour
    
    def to_dict(self) -> Dict:
        """Convert to dictionary for JSON serialization"""
        return {
            'patient_id': self.patient_id,
            'arrival_time': self.arrival_time.isoformat(),
            'age': self.age,
            'gender': self.gender,
            'triage_level': self.triage_level,
            'chief_complaint': self.chief_complaint,
            'temperature': self.temperature,
            'is_holiday': self.is_holiday,
            'day_of_week': self.day_of_week,
            'hour_of_day': self.hour_of_day
        }
    
    def to_json(self) -> str:
        """Convert to JSON string"""
        return json.dumps(self.to_dict())
    
    @classmethod
    def from_json(cls, json_str: str) -> 'PatientArrival':
        """Create PatientArrival from JSON string"""
        data = json.loads(json_str)
        data['arrival_time'] = datetime.fromisoformat(data['arrival_time'])
        return cls(**data)

class DemandForecast:
    """Model representing forecasted demand"""
    
    def __init__(
        self,
        forecast_time: datetime,
        forecast_window_minutes: int,
        predicted_arrivals: int,
        confidence_interval_lower: float,
        confidence_interval_upper: float,
        model_type: str = 'time_series'
    ):
        self.forecast_time = forecast_time
        self.forecast_window_minutes = forecast_window_minutes
        self.predicted_arrivals = predicted_arrivals
        self.confidence_interval_lower = confidence_interval_lower
        self.confidence_interval_upper = confidence_interval_upper
        self.model_type = model_type
    
    def to_dict(self) -> Dict:
        """Convert to dictionary for JSON serialization"""
        return {
            'forecast_time': self.forecast_time.isoformat(),
            'forecast_window_minutes': self.forecast_window_minutes,
            'predicted_arrivals': self.predicted_arrivals,
            'confidence_interval_lower': self.confidence_interval_lower,
            'confidence_interval_upper': self.confidence_interval_upper,
            'model_type': self.model_type
        }
    
    def to_json(self) -> str:
        """Convert to JSON string"""
        return json.dumps(self.to_dict())

