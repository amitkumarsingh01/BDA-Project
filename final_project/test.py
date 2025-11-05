"""
Emergency Department Demand Forecasting
SIMPLE VERSION - No Kafka, No Docker, No Installation!
Just run: python ed_forecasting_simple.py
"""

import time
import random
from datetime import datetime, timedelta
from collections import deque, defaultdict
import json

# ============================================
# DATA GENERATORS (Like Kafka Producers)
# ============================================

def generate_patient_arrival():
    """Generate a patient arrival event"""
    severities = ['Low', 'Medium', 'High', 'Critical']
    complaints = ['Chest Pain', 'Respiratory Issues', 'Trauma', 
                  'Abdominal Pain', 'Neurological', 'Pediatric Emergency']
    
    hour = datetime.now().hour
    # More arrivals in evening/night
    if 18 <= hour <= 23:
        severity_weights = [0.3, 0.35, 0.25, 0.1]
    else:
        severity_weights = [0.4, 0.35, 0.2, 0.05]
    
    return {
        'timestamp': datetime.now().isoformat(),
        'patient_id': f"P-{random.randint(10000, 99999)}",
        'severity': random.choices(severities, weights=severity_weights)[0],
        'complaint': random.choice(complaints),
        'hour': hour
    }

def generate_ambulance():
    """Generate ambulance dispatch"""
    if random.random() < 0.1:  # 10% chance
        return {
            'timestamp': datetime.now().isoformat(),
            'ambulance_id': f"AMB-{random.randint(100, 999)}",
            'eta_minutes': random.randint(5, 30),
            'severity': random.choice(['High', 'Critical']),
            'patient_count': random.randint(1, 3)
        }
    return None

def generate_capacity():
    """Generate hospital capacity info"""
    total_beds = 50
    occupied = random.randint(25, 45)
    return {
        'timestamp': datetime.now().isoformat(),
        'total_beds': total_beds,
        'occupied_beds': occupied,
        'available_beds': total_beds - occupied,
        'waiting_patients': random.randint(3, 15)
    }

# ============================================
# FORECASTING ENGINE (Like Kafka Consumer)
# ============================================

class SimpleForecastingEngine:
    def __init__(self):
        self.arrivals = deque(maxlen=100)  # Last 100 arrivals
        self.ambulances = deque(maxlen=20)
        self.capacity_history = deque(maxlen=20)
        self.severity_counts = defaultdict(int)
        
    def add_arrival(self, arrival):
        """Process new patient arrival"""
        self.arrivals.append(arrival)
        self.severity_counts[arrival['severity']] += 1
    
    def add_ambulance(self, ambulance):
        """Process ambulance dispatch"""
        if ambulance:
            self.ambulances.append(ambulance)
    
    def add_capacity(self, capacity):
        """Process capacity update"""
        self.capacity_history.append(capacity)
    
    def get_arrival_rate(self, minutes=60):
        """Calculate arrivals per hour in last X minutes"""
        if not self.arrivals:
            return 0
        
        cutoff = datetime.now() - timedelta(minutes=minutes)
        recent = [a for a in self.arrivals 
                 if datetime.fromisoformat(a['timestamp']) > cutoff]
        
        return len(recent) / (minutes / 60)  # Convert to per hour
    
    def forecast_next_hour(self):
        """Generate forecast for next hour"""
        current_rate = self.get_arrival_rate(60)
        
        if current_rate == 0:
            return None
        
        # Adjust based on time of day
        hour = datetime.now().hour
        if 18 <= hour <= 23:
            time_factor = 1.4  # Evening peak
        elif 0 <= hour <= 6:
            time_factor = 1.3  # Night
        else:
            time_factor = 1.0
        
        # Adjust for incoming ambulances
        ambulance_factor = 1.0 + (len(self.ambulances) * 0.05)
        
        # Calculate predictions
        predicted_rate = current_rate * time_factor * ambulance_factor
        
        forecasts = {
            '15min': int(predicted_rate * 0.25),
            '30min': int(predicted_rate * 0.5),
            '60min': int(predicted_rate),
            '120min': int(predicted_rate * 2)
        }
        
        return forecasts
    
    def get_recommendations(self):
        """Generate staffing recommendations"""
        if not self.capacity_history:
            return []
        
        latest_capacity = self.capacity_history[-1]
        available_beds = latest_capacity['available_beds']
        waiting = latest_capacity['waiting_patients']
        
        forecast = self.forecast_next_hour()
        if not forecast:
            return []
        
        next_hour = forecast['60min']
        recommendations = []
        
        if next_hour > 15:
            recommendations.append({
                'priority': '🔴 HIGH',
                'action': 'Call additional staff immediately',
                'reason': f'Expecting {next_hour} patients in next hour'
            })
        
        if available_beds < 10:
            recommendations.append({
                'priority': '🟡 MEDIUM',
                'action': 'Prepare for capacity issues',
                'reason': f'Only {available_beds} beds available'
            })
        
        if waiting > 10:
            recommendations.append({
                'priority': '🟡 MEDIUM',
                'action': 'Speed up triage process',
                'reason': f'{waiting} patients waiting'
            })
        
        critical_ratio = self.severity_counts.get('Critical', 0) / max(1, sum(self.severity_counts.values()))
        if critical_ratio > 0.15:
            recommendations.append({
                'priority': '🔴 HIGH',
                'action': 'Alert trauma team',
                'reason': 'High proportion of critical patients'
            })
        
        return recommendations
    
    def display_dashboard(self):
        """Display real-time dashboard"""
        print("\n" + "="*70)
        print("🏥 EMERGENCY DEPARTMENT - REAL-TIME DASHBOARD")
        print("="*70)
        print(f"⏰ Time: {datetime.now().strftime('%H:%M:%S')}")
        
        # Current metrics
        print("\n📊 CURRENT METRICS:")
        print(f"   Arrival Rate: {self.get_arrival_rate(60):.1f} patients/hour")
        print(f"   Total Arrivals Today: {len(self.arrivals)}")
        
        if self.capacity_history:
            latest = self.capacity_history[-1]
            print(f"   Available Beds: {latest['available_beds']}/{latest['total_beds']}")
            print(f"   Waiting Patients: {latest['waiting_patients']}")
        
        if self.ambulances:
            print(f"   Incoming Ambulances: {len(self.ambulances)}")
        
        # Severity breakdown
        print("\n🎯 SEVERITY BREAKDOWN:")
        total = sum(self.severity_counts.values())
        if total > 0:
            for severity, count in sorted(self.severity_counts.items()):
                percentage = (count / total) * 100
                bar = "█" * int(percentage / 5)
                print(f"   {severity:8s}: {bar} {count} ({percentage:.1f}%)")
        
        # Forecasts
        forecast = self.forecast_next_hour()
        if forecast:
            print("\n🔮 DEMAND FORECAST:")
            for period, count in forecast.items():
                print(f"   Next {period:6s}: {count:2d} patients expected")
        
        # Recommendations
        recommendations = self.get_recommendations()
        if recommendations:
            print("\n💡 RECOMMENDATIONS:")
            for rec in recommendations:
                print(f"   {rec['priority']} {rec['action']}")
                print(f"      → {rec['reason']}")
        
        # Recent arrivals
        if self.arrivals:
            print("\n📋 RECENT ARRIVALS (Last 5):")
            for arrival in list(self.arrivals)[-5:]:
                time_str = datetime.fromisoformat(arrival['timestamp']).strftime('%H:%M:%S')
                print(f"   {time_str} | {arrival['severity']:8s} | {arrival['complaint']}")
        
        print("="*70)

# ============================================
# MAIN SIMULATION
# ============================================

def run_simulation(duration_seconds=300):
    """
    Run the complete ED forecasting simulation
    duration_seconds: How long to run (default 5 minutes)
    """
    print("🚀 Starting Emergency Department Demand Forecasting Simulation")
    print(f"⏱️  Running for {duration_seconds} seconds ({duration_seconds//60} minutes)")
    print("Press Ctrl+C to stop anytime\n")
    time.sleep(2)
    
    engine = SimpleForecastingEngine()
    start_time = time.time()
    last_dashboard_update = 0
    last_capacity_update = 0
    
    try:
        while (time.time() - start_time) < duration_seconds:
            current_time = time.time()
            
            # Generate patient arrivals (30% chance each second)
            if random.random() < 0.3:
                arrival = generate_patient_arrival()
                engine.add_arrival(arrival)
                print(f"✅ Patient Arrival: {arrival['severity']} - {arrival['complaint']}")
            
            # Generate ambulance dispatches (occasional)
            ambulance = generate_ambulance()
            if ambulance:
                engine.add_ambulance(ambulance)
                print(f"🚑 Ambulance Dispatched: ETA {ambulance['eta_minutes']} min")
            
            # Update capacity every 30 seconds
            if current_time - last_capacity_update > 30:
                capacity = generate_capacity()
                engine.add_capacity(capacity)
                print(f"🏥 Capacity Update: {capacity['available_beds']} beds available")
                last_capacity_update = current_time
            
            # Display dashboard every 15 seconds
            if current_time - last_dashboard_update > 15:
                engine.display_dashboard()
                last_dashboard_update = current_time
            
            time.sleep(1)
    
    except KeyboardInterrupt:
        print("\n\n⏹️  Simulation stopped by user")
    
    # Final summary
    print("\n" + "="*70)
    print("📈 SIMULATION SUMMARY")
    print("="*70)
    print(f"Total Patients Processed: {len(engine.arrivals)}")
    print(f"Total Ambulances: {len(engine.ambulances)}")
    print(f"Average Arrival Rate: {engine.get_arrival_rate(duration_seconds//60):.1f} patients/hour")
    print("="*70)
    print("\n✨ Thank you for using ED Demand Forecasting!")

# ============================================
# RUN IT!
# ============================================

if __name__ == "__main__":
    # Run simulation for 5 minutes (300 seconds)
    # Change to any duration you want
    run_simulation(duration_seconds=180)  # 3 minutes for demo