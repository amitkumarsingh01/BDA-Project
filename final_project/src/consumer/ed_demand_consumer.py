"""
Kafka Consumer for Emergency Department Demand Forecasting
Consumes patient arrival data and generates demand forecasts
"""
import json
import time
from datetime import datetime, timedelta
from kafka import KafkaConsumer
from kafka.errors import KafkaError
import sys
import os

# Add project root to path
project_root = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.insert(0, project_root)

from config.kafka_config import (
    CONSUMER_CONFIG, TOPIC_ARRIVALS, TOPIC_FORECASTS, TOPIC_STATISTICS,
    FORECAST_WINDOW_MINUTES, AGGREGATION_INTERVAL_MINUTES
)
from src.models.patient_models import PatientArrival, DemandForecast
from src.utils.data_utils import aggregate_arrivals_by_time_window, calculate_statistics
from src.forecasting.forecasting_model import TimeSeriesForecaster, SimpleMovingAverageForecaster

class EDDemandConsumer:
    """Consumer for processing ED arrivals and generating forecasts"""
    
    def __init__(self, use_advanced_model: bool = True):
        """
        Initialize Kafka consumer
        
        Args:
            use_advanced_model: Use TimeSeriesForecaster if True, else SimpleMovingAverageForecaster
        """
        self.consumer = KafkaConsumer(
            TOPIC_ARRIVALS,
            **CONSUMER_CONFIG
        )
        
        # Producer for sending forecasts
        from kafka import KafkaProducer
        from config.kafka_config import PRODUCER_CONFIG
        self.forecast_producer = KafkaProducer(**PRODUCER_CONFIG)
        
        # Initialize forecasting model
        if use_advanced_model:
            self.forecaster = TimeSeriesForecaster(window_size=96)
        else:
            self.forecaster = SimpleMovingAverageForecaster(window_size=24)
        
        self.arrivals_buffer = []
        self.last_aggregation_time = None
        self.running = False
        
        print(f"✓ Consumer initialized, subscribing to topic: {TOPIC_ARRIVALS}")
        print(f"✓ Forecast producer initialized for topic: {TOPIC_FORECASTS}")
        print(f"✓ Using {'Advanced' if use_advanced_model else 'Simple'} forecasting model")
    
    def process_patient_arrival(self, message):
        """Process a single patient arrival message"""
        try:
            # Decode message
            value = message.value.decode('utf-8') if isinstance(message.value, bytes) else message.value
            patient_data = json.loads(value)
            
            # Parse timestamp
            patient_data['arrival_time'] = datetime.fromisoformat(patient_data['arrival_time'])
            
            # Create PatientArrival object
            patient = PatientArrival(**patient_data)
            
            # Add to buffer
            self.arrivals_buffer.append(patient.to_dict())
            
            return patient
            
        except Exception as e:
            print(f"✗ Error processing message: {e}")
            return None
    
    def aggregate_and_update_model(self):
        """Aggregate arrivals and update forecasting model"""
        if not self.arrivals_buffer:
            return
        
        # Aggregate arrivals into time windows
        aggregated = aggregate_arrivals_by_time_window(
            self.arrivals_buffer,
            window_minutes=AGGREGATION_INTERVAL_MINUTES
        )
        
        # Update forecasting model with new data points
        for _, row in aggregated.iterrows():
            timestamp = row['timestamp']
            count = int(row['count'])
            
            if isinstance(self.forecaster, TimeSeriesForecaster):
                self.forecaster.add_data_point(timestamp, count)
            else:
                self.forecaster.add_data_point(timestamp, count)
        
        # Fit model if using advanced forecaster
        if isinstance(self.forecaster, TimeSeriesForecaster) and len(aggregated) >= 10:
            self.forecaster.fit(aggregated)
        
        # Clear buffer
        self.arrivals_buffer = []
    
    def generate_forecast(self) -> DemandForecast:
        """Generate demand forecast"""
        forecast_horizon = FORECAST_WINDOW_MINUTES // AGGREGATION_INTERVAL_MINUTES
        
        predictions, lower_bounds, upper_bounds = self.forecaster.predict(forecast_horizon)
        
        # Use average prediction for simplicity
        avg_prediction = sum(predictions) / len(predictions) if predictions else 0
        avg_lower = sum(lower_bounds) / len(lower_bounds) if lower_bounds else 0
        avg_upper = sum(upper_bounds) / len(upper_bounds) if upper_bounds else 0
        
        forecast = DemandForecast(
            forecast_time=datetime.now(),
            forecast_window_minutes=FORECAST_WINDOW_MINUTES,
            predicted_arrivals=int(avg_prediction),
            confidence_interval_lower=round(avg_lower, 2),
            confidence_interval_upper=round(avg_upper, 2),
            model_type='time_series' if isinstance(self.forecaster, TimeSeriesForecaster) else 'moving_average'
        )
        
        return forecast
    
    def send_forecast(self, forecast: DemandForecast):
        """Send forecast to Kafka topic"""
        try:
            value = forecast.to_json().encode('utf-8')
            key = forecast.forecast_time.strftime('%Y%m%d%H%M').encode('utf-8')
            
            self.forecast_producer.send(
                TOPIC_FORECASTS,
                key=key,
                value=value
            )
            
            print(f"[{forecast.forecast_time.strftime('%Y-%m-%d %H:%M:%S')}] "
                  f"Forecast: {forecast.predicted_arrivals} arrivals "
                  f"(CI: {forecast.confidence_interval_lower:.1f}-{forecast.confidence_interval_upper:.1f})")
            
        except Exception as e:
            print(f"✗ Error sending forecast: {e}")
    
    def send_statistics(self, stats: dict):
        """Send statistics to Kafka topic"""
        try:
            value = json.dumps(stats).encode('utf-8')
            self.forecast_producer.send(TOPIC_STATISTICS, value=value)
        except Exception as e:
            print(f"✗ Error sending statistics: {e}")
    
    def run(self, forecast_interval_minutes: int = 15):
        """
        Run consumer and generate forecasts
        
        Args:
            forecast_interval_minutes: How often to generate forecasts
        """
        self.running = True
        last_forecast_time = datetime.now()
        
        print(f"\n🚀 Starting ED Demand Consumer")
        print(f"⏰ Forecast interval: {forecast_interval_minutes} minutes")
        print(f"📊 Aggregation window: {AGGREGATION_INTERVAL_MINUTES} minutes\n")
        
        try:
            for message in self.consumer:
                if not self.running:
                    break
                
                # Process patient arrival
                patient = self.process_patient_arrival(message)
                
                if patient:
                    print(f"[{patient.arrival_time.strftime('%Y-%m-%d %H:%M:%S')}] "
                          f"Patient {patient.patient_id} - Triage: {patient.triage_level}")
                
                # Aggregate and update model periodically
                current_time = datetime.now()
                if (self.last_aggregation_time is None or 
                    (current_time - self.last_aggregation_time).total_seconds() >= 
                    AGGREGATION_INTERVAL_MINUTES * 60):
                    
                    self.aggregate_and_update_model()
                    self.last_aggregation_time = current_time
                
                # Generate and send forecast periodically
                if (current_time - last_forecast_time).total_seconds() >= forecast_interval_minutes * 60:
                    forecast = self.generate_forecast()
                    self.send_forecast(forecast)
                    
                    # Send statistics
                    stats = calculate_statistics(self.arrivals_buffer)
                    self.send_statistics(stats)
                    
                    last_forecast_time = current_time
                
        except KeyboardInterrupt:
            print("\n⚠️  Consumer stopped by user")
        except Exception as e:
            print(f"✗ Fatal error: {e}")
        finally:
            self.stop()
    
    def stop(self):
        """Stop the consumer"""
        self.running = False
        self.consumer.close()
        self.forecast_producer.flush()
        self.forecast_producer.close()
        print("✓ Consumer stopped and closed")


def main():
    """Main function to run the consumer"""
    import argparse
    
    parser = argparse.ArgumentParser(description='ED Demand Consumer')
    parser.add_argument('--forecast-interval', type=int, default=15,
                       help='Forecast generation interval in minutes (default: 15)')
    parser.add_argument('--simple-model', action='store_true',
                       help='Use simple moving average model instead of advanced model')
    
    args = parser.parse_args()
    
    consumer = EDDemandConsumer(use_advanced_model=not args.simple_model)
    
    try:
        consumer.run(forecast_interval_minutes=args.forecast_interval)
    except Exception as e:
        print(f"✗ Fatal error: {e}")
        sys.exit(1)


if __name__ == '__main__':
    main()

