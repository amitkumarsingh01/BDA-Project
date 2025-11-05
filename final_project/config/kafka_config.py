"""
Kafka Configuration for ED Demand Forecasting
"""
import os

# Kafka Configuration
KAFKA_BOOTSTRAP_SERVERS = os.getenv('KAFKA_BOOTSTRAP_SERVERS', 'localhost:9092')
KAFKA_ZOOKEEPER_CONNECT = os.getenv('KAFKA_ZOOKEEPER_CONNECT', 'localhost:2181')

# Topic Names
TOPIC_ARRIVALS = 'ed-arrivals'
TOPIC_FORECASTS = 'ed-forecasts'
TOPIC_STATISTICS = 'ed-statistics'

# Producer Configuration
PRODUCER_CONFIG = {
    'bootstrap_servers': KAFKA_BOOTSTRAP_SERVERS,
    'value_serializer': lambda v: v.encode('utf-8') if isinstance(v, str) else v,
    'key_serializer': lambda k: str(k).encode('utf-8') if k else None,
    'acks': 'all',  # Wait for all replicas
    'retries': 3,
    'max_in_flight_requests_per_connection': 1,
    'enable_idempotence': True,
}

# Consumer Configuration
CONSUMER_CONFIG = {
    'bootstrap_servers': KAFKA_BOOTSTRAP_SERVERS,
    'auto_offset_reset': 'earliest',  # Start from beginning if no offset
    'enable_auto_commit': True,
    'auto_commit_interval_ms': 1000,
    'group_id': 'ed-demand-forecasting-group',
    'value_deserializer': lambda m: m.decode('utf-8') if m else None,
    'consumer_timeout_ms': 1000,
}

# Forecasting Configuration
FORECAST_WINDOW_MINUTES = 60  # Forecast for next 60 minutes
AGGREGATION_INTERVAL_MINUTES = 15  # Aggregate data in 15-minute windows
HISTORICAL_DATA_POINTS = 96  # Use last 24 hours (96 * 15 minutes)

