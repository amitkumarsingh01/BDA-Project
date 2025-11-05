"""
Kafka Producer for Emergency Department Patient Arrival Data
Simulates real-time patient arrivals and streams to Kafka
"""
import json
import time
import random
from datetime import datetime, timedelta
from kafka import KafkaProducer
from kafka.errors import KafkaError
import sys
import os

# Add project root to path
project_root = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.insert(0, project_root)

from config.kafka_config import KAFKA_BOOTSTRAP_SERVERS, TOPIC_ARRIVALS, PRODUCER_CONFIG
from src.models.patient_models import PatientArrival
from src.utils.data_utils import (
    generate_patient_id, get_triage_level_distribution,
    get_chief_complaint, simulate_temperature, is_holiday,
    get_arrival_rate_factor
)

class EDDataProducer:
    """Producer for streaming ED patient arrival data to Kafka"""
    
    def __init__(self, base_arrival_rate: float = 2.0):
        """
        Initialize Kafka producer
        
        Args:
            base_arrival_rate: Base patient arrivals per minute
        """
        self.producer = KafkaProducer(**PRODUCER_CONFIG)
        self.topic = TOPIC_ARRIVALS
        self.base_arrival_rate = base_arrival_rate
        self.running = False
        
        print(f"✓ Producer initialized, connecting to Kafka at {KAFKA_BOOTSTRAP_SERVERS}")
        print(f"✓ Topic: {self.topic}")
    
    def generate_patient_arrival(self, current_time: datetime) -> PatientArrival:
        """Generate a simulated patient arrival"""
        patient_id = generate_patient_id()
        age = random.randint(1, 90)
        gender = random.choice(['M', 'F'])
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
    
    def calculate_arrival_rate(self, current_time: datetime) -> float:
        """Calculate current arrival rate based on time patterns"""
        hour = current_time.hour
        day_of_week = current_time.weekday()
        holiday = is_holiday(current_time)
        
        factor = get_arrival_rate_factor(hour, day_of_week, holiday)
        return self.base_arrival_rate * factor
    
    def send_patient_arrival(self, patient: PatientArrival) -> bool:
        """Send patient arrival data to Kafka topic"""
        try:
            # Use patient_id as key for partitioning
            key = patient.patient_id.encode('utf-8')
            value = patient.to_json().encode('utf-8')
            
            future = self.producer.send(
                self.topic,
                key=key,
                value=value,
                timestamp_ms=int(patient.arrival_time.timestamp() * 1000)
            )
            
            # Optional: wait for acknowledgment
            record_metadata = future.get(timeout=10)
            
            return True
            
        except KafkaError as e:
            print(f"✗ Error sending message: {e}")
            return False
    
    def run(self, duration_minutes: int = 60, verbose: bool = True):
        """
        Run producer for specified duration
        
        Args:
            duration_minutes: How long to run the producer
            verbose: Print detailed logs
        """
        self.running = True
        start_time = datetime.now()
        end_time = start_time + timedelta(minutes=duration_minutes)
        
        print(f"\n🚀 Starting ED Data Producer")
        print(f"⏰ Duration: {duration_minutes} minutes")
        print(f"📊 Base arrival rate: {self.base_arrival_rate} patients/minute\n")
        
        total_sent = 0
        
        try:
            while self.running and datetime.now() < end_time:
                current_time = datetime.now()
                arrival_rate = self.calculate_arrival_rate(current_time)
                
                # Poisson process: probability of arrival in this second
                probability = arrival_rate / 60.0
                
                if random.random() < probability:
                    patient = self.generate_patient_arrival(current_time)
                    success = self.send_patient_arrival(patient)
                    
                    if success:
                        total_sent += 1
                        if verbose:
                            print(f"[{current_time.strftime('%Y-%m-%d %H:%M:%S')}] "
                                  f"Patient {patient.patient_id} arrived - "
                                  f"Triage: {patient.triage_level}, "
                                  f"Complaint: {patient.chief_complaint}")
                
                # Sleep for 1 second
                time.sleep(1)
                
        except KeyboardInterrupt:
            print("\n⚠️  Producer stopped by user")
        finally:
            self.stop()
            print(f"\n📈 Total patients sent: {total_sent}")
            print(f"📈 Average rate: {total_sent / duration_minutes:.2f} patients/minute")
    
    def stop(self):
        """Stop the producer"""
        self.running = False
        self.producer.flush()
        self.producer.close()
        print("✓ Producer stopped and closed")


def main():
    """Main function to run the producer"""
    import argparse
    
    parser = argparse.ArgumentParser(description='ED Data Producer')
    parser.add_argument('--duration', type=int, default=60,
                       help='Duration in minutes (default: 60)')
    parser.add_argument('--rate', type=float, default=2.0,
                       help='Base arrival rate per minute (default: 2.0)')
    parser.add_argument('--quiet', action='store_true',
                       help='Reduce output verbosity')
    
    args = parser.parse_args()
    
    producer = EDDataProducer(base_arrival_rate=args.rate)
    
    try:
        producer.run(duration_minutes=args.duration, verbose=not args.quiet)
    except Exception as e:
        print(f"✗ Fatal error: {e}")
        sys.exit(1)


if __name__ == '__main__':
    main()

