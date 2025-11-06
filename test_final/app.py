import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime, timedelta
import time
from collections import deque
import sys
import os
import random

# Add parent directory to path to import modules
USE_EXTERNAL_MODULES = False
try:
    sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'final_project'))
    
    from src.models.patient_models import PatientArrival
    from src.utils.data_utils import (
        generate_patient_id, get_triage_level_distribution,
        get_chief_complaint, simulate_temperature, is_holiday,
        get_arrival_rate_factor, aggregate_arrivals_by_time_window,
        calculate_statistics
    )
    from src.forecasting.forecasting_model import TimeSeriesForecaster, SimpleMovingAverageForecaster
    
    USE_EXTERNAL_MODULES = True
except ImportError as e:
    USE_EXTERNAL_MODULES = False

# Fallback implementations (used if external modules not available)
if not USE_EXTERNAL_MODULES:
    
    class PatientArrival:
        def __init__(self, patient_id, arrival_time, age, gender, triage_level, 
                     chief_complaint, temperature=None, is_holiday=False, 
                     day_of_week=None, hour_of_day=None):
            self.patient_id = patient_id
            self.arrival_time = arrival_time
            self.age = age
            self.gender = gender
            self.triage_level = triage_level
            self.chief_complaint = chief_complaint
            self.temperature = temperature
            self.is_holiday = is_holiday
            self.day_of_week = day_of_week or arrival_time.weekday()
            self.hour_of_day = hour_of_day or arrival_time.hour
        
        def to_dict(self):
            return {
                'patient_id': self.patient_id,
                'arrival_time': self.arrival_time.isoformat() if isinstance(self.arrival_time, datetime) else str(self.arrival_time),
                'age': self.age,
                'gender': self.gender,
                'triage_level': self.triage_level,
                'chief_complaint': self.chief_complaint,
                'temperature': self.temperature,
                'is_holiday': self.is_holiday,
                'day_of_week': self.day_of_week,
                'hour_of_day': self.hour_of_day
            }
    
    def generate_patient_id():
        return f"PAT{random.randint(100000, 999999)}"
    
    def get_triage_level_distribution():
        weights = [0.05, 0.15, 0.40, 0.30, 0.10]
        return random.choices(range(1, 6), weights=weights)[0]
    
    CHIEF_COMPLAINTS = [
        'Chest Pain', 'Shortness of Breath', 'Abdominal Pain', 'Fever',
        'Headache', 'Trauma', 'Back Pain', 'Dizziness', 'Nausea/Vomiting',
        'Cough', 'Weakness', 'Seizure', 'Unconscious', 'Allergic Reaction'
    ]
    
    def get_chief_complaint():
        return random.choice(CHIEF_COMPLAINTS)
    
    def simulate_temperature():
        if random.random() < 0.3:
            return round(random.uniform(38.0, 40.0), 1)
        return round(random.uniform(36.5, 37.5), 1)
    
    def is_holiday(date):
        holidays = [(1, 1), (12, 25), (7, 4)]
        return (date.month, date.day) in holidays
    
    def get_arrival_rate_factor(hour, day_of_week, is_holiday):
        hour_factor = 0.3 + 0.7 * np.sin((hour - 6) * np.pi / 12) if hour >= 6 else 0.3
        day_factor = 0.7 if day_of_week >= 5 else 1.0
        holiday_factor = 0.6 if is_holiday else 1.0
        return hour_factor * day_factor * holiday_factor
    
    def aggregate_arrivals_by_time_window(arrivals, window_minutes=15):
        if not arrivals:
            return pd.DataFrame(columns=['timestamp', 'count'])
        
        df = pd.DataFrame(arrivals)
        df['arrival_time'] = pd.to_datetime(df['arrival_time'])
        df['window'] = df['arrival_time'].dt.floor(f'{window_minutes}T')
        aggregated = df.groupby('window').size().reset_index(name='count')
        aggregated.columns = ['timestamp', 'count']
        return aggregated
    
    def calculate_statistics(arrivals):
        if not arrivals:
            return {'total_arrivals': 0, 'avg_triage_level': 0, 'common_complaints': {}}
        df = pd.DataFrame(arrivals)
        return {
            'total_arrivals': len(arrivals),
            'avg_triage_level': df['triage_level'].mean() if 'triage_level' in df.columns else 0,
            'common_complaints': df['chief_complaint'].value_counts().head(5).to_dict() if 'chief_complaint' in df.columns else {}
        }
    
    # Simplified forecasters
    class TimeSeriesForecaster:
        def __init__(self, window_size=96):
            self.window_size = window_size
            self.historical_data = []
        
        def fit(self, df):
            if len(df) > 0:
                self.historical_data = df.to_dict('records')
        
        def predict(self, forecast_horizon=4):
            if len(self.historical_data) < 4:
                return [0.0] * forecast_horizon, [0.0] * forecast_horizon, [0.0] * forecast_horizon
            
            counts = [d['count'] for d in self.historical_data[-self.window_size:]]
            avg = np.mean(counts)
            std = np.std(counts) if len(counts) > 1 else 1.0
            predictions = [avg] * forecast_horizon
            lower_bounds = [max(0, avg - 1.96 * std)] * forecast_horizon
            upper_bounds = [avg + 1.96 * std] * forecast_horizon
            return predictions, lower_bounds, upper_bounds
    
    class SimpleMovingAverageForecaster:
        def __init__(self, window_size=24):
            self.window_size = window_size
            self.historical_data = []
        
        def add_data_point(self, timestamp, count):
            self.historical_data.append({'timestamp': timestamp, 'count': count})
            if len(self.historical_data) > self.window_size * 2:
                self.historical_data = self.historical_data[-self.window_size * 2:]
        
        def predict(self, forecast_horizon=4):
            if len(self.historical_data) < 4:
                return [0.0] * forecast_horizon, [0.0] * forecast_horizon, [0.0] * forecast_horizon
            
            counts = [d['count'] for d in self.historical_data[-self.window_size:]]
            avg = np.mean(counts)
            std = np.std(counts) if len(counts) > 1 else 1.0
            predictions = [avg] * forecast_horizon
            lower_bounds = [max(0, avg - 1.96 * std)] * forecast_horizon
            upper_bounds = [avg + 1.96 * std] * forecast_horizon
            return predictions, lower_bounds, upper_bounds

# Page configuration
st.set_page_config(
    page_title="ED Demand Forecasting Analytics",
    page_icon="🏥",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Show warning if using fallback modules
if not USE_EXTERNAL_MODULES:
    st.warning("Welcome!!")

# Custom CSS for better styling
st.markdown("""
    <style>
    .main-header {
        font-size: 3rem;
        font-weight: bold;
        color: #1f77b4;
        text-align: center;
        padding: 1rem;
    }
    .metric-card {
        background-color: #f0f2f6;
        padding: 1rem;
        border-radius: 0.5rem;
        margin: 0.5rem;
    }
    .stAlert {
        margin-top: 1rem;
    }
    </style>
""", unsafe_allow_html=True)

# Initialize session state
if 'patient_arrivals' not in st.session_state:
    st.session_state.patient_arrivals = deque(maxlen=1000)
if 'forecaster' not in st.session_state:
    st.session_state.forecaster = TimeSeriesForecaster(window_size=96)
if 'simple_forecaster' not in st.session_state:
    st.session_state.simple_forecaster = SimpleMovingAverageForecaster(window_size=24)
if 'aggregated_data' not in st.session_state:
    st.session_state.aggregated_data = deque(maxlen=200)
if 'is_running' not in st.session_state:
    st.session_state.is_running = False
if 'capacity_data' not in st.session_state:
    st.session_state.capacity_data = deque(maxlen=100)
if 'start_time' not in st.session_state:
    st.session_state.start_time = datetime.now()

# Utility functions
def generate_patient_arrival():
    """Generate a simulated patient arrival"""
    current_time = datetime.now()
    patient_id = generate_patient_id()
    age = np.random.randint(1, 90)
    gender = np.random.choice(['M', 'F'])
    triage_level = get_triage_level_distribution()
    chief_complaint = get_chief_complaint()
    temperature = simulate_temperature()
    holiday = is_holiday(current_time)
    
    return PatientArrival(
        patient_id=patient_id,
        arrival_time=current_time,
        age=age,
        gender=gender,
        triage_level=triage_level,
        chief_complaint=chief_complaint,
        temperature=temperature,
        is_holiday=holiday,
        day_of_week=current_time.weekday(),
        hour_of_day=current_time.hour
    )

def generate_capacity_update():
    """Generate hospital capacity information"""
    total_beds = 50
    occupied = np.random.randint(25, 45)
    waiting = np.random.randint(3, 15)
    
    return {
        'timestamp': datetime.now(),
        'total_beds': total_beds,
        'occupied_beds': occupied,
        'available_beds': total_beds - occupied,
        'waiting_patients': waiting,
        'occupancy_rate': (occupied / total_beds) * 100
    }

def update_forecasters():
    """Update forecasting models with latest aggregated data"""
    if len(st.session_state.aggregated_data) < 4:
        return
    
    # Convert to DataFrame
    df = pd.DataFrame(list(st.session_state.aggregated_data))
    df = df.sort_values('timestamp')
    
    # Update TimeSeriesForecaster
    st.session_state.forecaster.fit(df)
    
    # Update SimpleMovingAverageForecaster (add data points)
    for _, row in df.iterrows():
        st.session_state.simple_forecaster.add_data_point(
            row['timestamp'], 
            int(row['count'])
        )

# Main dashboard
def main():
    # Header
    st.markdown('<h1 class="main-header">🏥 Emergency Department Demand Forecasting Analytics</h1>', 
                unsafe_allow_html=True)
    st.markdown("---")
    
    # Sidebar controls
    with st.sidebar:
        st.header("⚙️ Control Panel")
        
        # Simulation controls
        st.subheader("Simulation")
        auto_refresh = st.checkbox("Auto-refresh data", value=False)
        refresh_interval = st.slider("Refresh interval (seconds)", 1, 10, 2)
        
        # Data generation rate
        arrival_rate = st.slider("Patient arrival rate (per minute)", 0.5, 5.0, 2.0, 0.1)
        
        # Generate data button
        if st.button("🔄 Generate New Patients", use_container_width=True):
            num_patients = st.slider("Number of patients", 1, 50, 10)
            for _ in range(num_patients):
                patient = generate_patient_arrival()
                st.session_state.patient_arrivals.append(patient.to_dict())
                
                # Update aggregated data
                if len(st.session_state.patient_arrivals) > 0:
                    arrivals_list = list(st.session_state.patient_arrivals)
                    aggregated = aggregate_arrivals_by_time_window(
                        arrivals_list, window_minutes=15
                    )
                    if not aggregated.empty:
                        for _, row in aggregated.iterrows():
                            st.session_state.aggregated_data.append({
                                'timestamp': row['timestamp'],
                                'count': row['count']
                            })
                
                # Update capacity
                capacity = generate_capacity_update()
                st.session_state.capacity_data.append(capacity)
            
            st.success(f"Generated {num_patients} new patient arrivals!")
        
        st.markdown("---")
        
        # Forecast settings
        st.subheader("Forecast Settings")
        forecast_horizon = st.slider("Forecast horizon (15-min windows)", 4, 24, 8)
        forecast_model = st.selectbox(
            "Forecasting Model",
            ["Time Series (Advanced)", "Simple Moving Average"]
        )
        
        st.markdown("---")
        
        # Data management
        st.subheader("Data Management")
        if st.button("🗑️ Clear All Data", use_container_width=True):
            st.session_state.patient_arrivals.clear()
            st.session_state.aggregated_data.clear()
            st.session_state.capacity_data.clear()
            st.success("Data cleared!")
        
        if st.button("📊 Generate Sample Data", use_container_width=True):
            # Generate 100 sample patients
            base_time = datetime.now() - timedelta(hours=6)
            for i in range(100):
                patient_time = base_time + timedelta(minutes=i*5)
                patient = PatientArrival(
                    patient_id=generate_patient_id(),
                    arrival_time=patient_time,
                    age=np.random.randint(1, 90),
                    gender=np.random.choice(['M', 'F']),
                    triage_level=get_triage_level_distribution(),
                    chief_complaint=get_chief_complaint(),
                    temperature=simulate_temperature(),
                    is_holiday=is_holiday(patient_time),
                    day_of_week=patient_time.weekday(),
                    hour_of_day=patient_time.hour
                )
                st.session_state.patient_arrivals.append(patient.to_dict())
            
            # Aggregate data
            arrivals_list = list(st.session_state.patient_arrivals)
            aggregated = aggregate_arrivals_by_time_window(arrivals_list, window_minutes=15)
            for _, row in aggregated.iterrows():
                st.session_state.aggregated_data.append({
                    'timestamp': row['timestamp'],
                    'count': row['count']
                })
            
            st.success("Generated 100 sample patients!")
        
        st.markdown("---")
        
        # Information
        st.info("💡 **Tip**: Use auto-refresh for real-time monitoring")
    
    # Main content area
    if len(st.session_state.patient_arrivals) == 0:
        st.warning("⚠️ No data available. Please generate sample data or start simulation.")
        return
    
    # Key Metrics Row
    st.header("📊 Real-Time Metrics")
    col1, col2, col3, col4 = st.columns(4)
    
    total_patients = len(st.session_state.patient_arrivals)
    arrivals_df = pd.DataFrame(list(st.session_state.patient_arrivals))
    
    # Calculate metrics
    avg_triage = arrivals_df['triage_level'].mean() if 'triage_level' in arrivals_df.columns else 0
    recent_arrivals = len([p for p in st.session_state.patient_arrivals 
                          if (datetime.now() - datetime.fromisoformat(p['arrival_time'])).seconds < 3600])
    
    if st.session_state.capacity_data:
        latest_capacity = list(st.session_state.capacity_data)[-1]
        available_beds = latest_capacity['available_beds']
        waiting_patients = latest_capacity['waiting_patients']
    else:
        available_beds = 50
        waiting_patients = 0
    
    with col1:
        st.metric("Total Patients", total_patients, delta=None)
    with col2:
        st.metric("Recent Arrivals (1hr)", recent_arrivals, delta=None)
    with col3:
        st.metric("Available Beds", available_beds, delta=None)
    with col4:
        st.metric("Waiting Patients", waiting_patients, delta=None)
    
    st.markdown("---")
    
    # Charts Row 1: Time Series and Forecasts
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("📈 Patient Arrivals Over Time")
        
        if len(st.session_state.aggregated_data) > 0:
            df_agg = pd.DataFrame(list(st.session_state.aggregated_data))
            df_agg['timestamp'] = pd.to_datetime(df_agg['timestamp'])
            df_agg = df_agg.sort_values('timestamp')
            
            fig = px.line(
                df_agg,
                x='timestamp',
                y='count',
                title='Patient Arrivals (15-min intervals)',
                labels={'count': 'Number of Patients', 'timestamp': 'Time'},
                markers=True
            )
            fig.update_traces(line_color='#1f77b4', line_width=2)
            fig.update_layout(height=400, showlegend=False)
            st.plotly_chart(fig, use_container_width=True)
        else:
            st.info("No aggregated data available")
    
    with col2:
        st.subheader("🔮 Demand Forecast")
        
        if len(st.session_state.aggregated_data) >= 4:
            update_forecasters()
            
            if forecast_model == "Time Series (Advanced)":
                forecaster = st.session_state.forecaster
            else:
                forecaster = st.session_state.simple_forecaster
            
            predictions, lower_bounds, upper_bounds = forecaster.predict(forecast_horizon)
            
            # Create forecast timeline
            if len(st.session_state.aggregated_data) > 0:
                last_time = pd.to_datetime(list(st.session_state.aggregated_data)[-1]['timestamp'])
            else:
                last_time = datetime.now()
            
            forecast_times = [last_time + timedelta(minutes=15*(i+1)) for i in range(len(predictions))]
            
            # Historical data
            df_agg = pd.DataFrame(list(st.session_state.aggregated_data))
            df_agg['timestamp'] = pd.to_datetime(df_agg['timestamp'])
            df_agg = df_agg.sort_values('timestamp')
            
            # Forecast data
            forecast_df = pd.DataFrame({
                'timestamp': forecast_times,
                'predicted': predictions,
                'lower': lower_bounds,
                'upper': upper_bounds
            })
            
            fig = go.Figure()
            
            # Historical data
            fig.add_trace(go.Scatter(
                x=df_agg['timestamp'],
                y=df_agg['count'],
                mode='lines+markers',
                name='Historical',
                line=dict(color='#1f77b4', width=2)
            ))
            
            # Forecast
            fig.add_trace(go.Scatter(
                x=forecast_df['timestamp'],
                y=forecast_df['predicted'],
                mode='lines+markers',
                name='Forecast',
                line=dict(color='#ff7f0e', width=2, dash='dash')
            ))
            
            # Confidence interval
            fig.add_trace(go.Scatter(
                x=forecast_df['timestamp'].tolist() + forecast_df['timestamp'].tolist()[::-1],
                y=forecast_df['upper'].tolist() + forecast_df['lower'].tolist()[::-1],
                fill='toself',
                fillcolor='rgba(255, 127, 14, 0.2)',
                line=dict(color='rgba(255,255,255,0)'),
                name='Confidence Interval'
            ))
            
            fig.update_layout(
                title='Demand Forecast with Confidence Intervals',
                xaxis_title='Time',
                yaxis_title='Number of Patients',
                height=400,
                hovermode='x unified'
            )
            st.plotly_chart(fig, use_container_width=True)
        else:
            st.info("Need at least 4 data points for forecasting")
    
    st.markdown("---")
    
    # Charts Row 2: Demographics and Patterns
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("🎯 Triage Level Distribution")
        
        if 'triage_level' in arrivals_df.columns:
            triage_counts = arrivals_df['triage_level'].value_counts().sort_index()
            triage_labels = {1: 'Critical', 2: 'Urgent', 3: 'Standard', 4: 'Low Priority', 5: 'Non-Urgent'}
            
            fig = px.pie(
                values=triage_counts.values,
                names=[triage_labels.get(i, f'Level {i}') for i in triage_counts.index],
                title='Patient Triage Distribution',
                color_discrete_sequence=px.colors.sequential.Reds_r
            )
            fig.update_layout(height=400)
            st.plotly_chart(fig, use_container_width=True)
        else:
            st.info("No triage data available")
    
    with col2:
        st.subheader("🏥 Chief Complaints")
        
        if 'chief_complaint' in arrivals_df.columns:
            complaint_counts = arrivals_df['chief_complaint'].value_counts().head(10)
            
            fig = px.bar(
                x=complaint_counts.values,
                y=complaint_counts.index,
                orientation='h',
                title='Top 10 Chief Complaints',
                labels={'x': 'Count', 'y': 'Complaint'},
                color=complaint_counts.values,
                color_continuous_scale='Blues'
            )
            fig.update_layout(height=400, showlegend=False)
            st.plotly_chart(fig, use_container_width=True)
        else:
            st.info("No complaint data available")
    
    st.markdown("---")
    
    # Charts Row 3: Hourly Patterns and Capacity
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("⏰ Hourly Arrival Pattern")
        
        if 'hour_of_day' in arrivals_df.columns:
            arrivals_df['hour'] = arrivals_df['hour_of_day']
            hourly_counts = arrivals_df['hour'].value_counts().sort_index()
            
            fig = px.bar(
                x=hourly_counts.index,
                y=hourly_counts.values,
                title='Patient Arrivals by Hour of Day',
                labels={'x': 'Hour of Day', 'y': 'Number of Patients'},
                color=hourly_counts.values,
                color_continuous_scale='Viridis'
            )
            fig.update_layout(height=400, showlegend=False)
            st.plotly_chart(fig, use_container_width=True)
        else:
            st.info("No hourly data available")
    
    with col2:
        st.subheader("🏥 Capacity Monitoring")
        
        if len(st.session_state.capacity_data) > 0:
            capacity_df = pd.DataFrame(list(st.session_state.capacity_data))
            capacity_df['timestamp'] = pd.to_datetime(capacity_df['timestamp'])
            capacity_df = capacity_df.sort_values('timestamp')
            
            fig = go.Figure()
            
            fig.add_trace(go.Scatter(
                x=capacity_df['timestamp'],
                y=capacity_df['occupancy_rate'],
                mode='lines+markers',
                name='Occupancy Rate (%)',
                line=dict(color='#d62728', width=2),
                fill='tonexty'
            ))
            
            fig.add_hline(y=80, line_dash="dash", line_color="orange", 
                         annotation_text="Warning Threshold (80%)")
            fig.add_hline(y=95, line_dash="dash", line_color="red", 
                         annotation_text="Critical Threshold (95%)")
            
            fig.update_layout(
                title='Bed Occupancy Rate Over Time',
                xaxis_title='Time',
                yaxis_title='Occupancy Rate (%)',
                height=400,
                yaxis_range=[0, 100]
            )
            st.plotly_chart(fig, use_container_width=True)
        else:
            st.info("No capacity data available")
    
    st.markdown("---")
    
    # Detailed Data Table
    st.subheader("📋 Recent Patient Arrivals")
    
    # Show last 20 arrivals
    recent_arrivals = list(st.session_state.patient_arrivals)[-20:]
    if recent_arrivals:
        df_recent = pd.DataFrame(recent_arrivals)
        df_recent['arrival_time'] = pd.to_datetime(df_recent['arrival_time'])
        
        # Select columns to display
        display_cols = ['patient_id', 'arrival_time', 'age', 'gender', 
                       'triage_level', 'chief_complaint', 'temperature']
        available_cols = [col for col in display_cols if col in df_recent.columns]
        
        df_display = df_recent[available_cols].copy()
        df_display['arrival_time'] = df_display['arrival_time'].dt.strftime('%Y-%m-%d %H:%M:%S')
        
        st.dataframe(df_display, use_container_width=True, height=300)
    
    # Auto-refresh logic
    if auto_refresh:
        time.sleep(refresh_interval)
        st.rerun()

if __name__ == "__main__":
    main()

