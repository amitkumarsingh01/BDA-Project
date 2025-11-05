"""
Example script demonstrating how to use the ED Demand Forecasting system
"""
import time
import subprocess
import sys
import os

def print_header(text):
    """Print formatted header"""
    print("\n" + "="*60)
    print(f"  {text}")
    print("="*60 + "\n")

def check_kafka_running():
    """Check if Kafka is running"""
    try:
        from kafka import KafkaProducer
        producer = KafkaProducer(bootstrap_servers=['localhost:9092'])
        producer.close()
        return True
    except:
        return False

def main():
    print_header("Emergency Department Demand Forecasting - Quick Start")
    
    print("This script demonstrates the Kafka-based ED demand forecasting system.")
    print("\nPrerequisites:")
    print("1. Kafka should be running (use docker-compose up -d)")
    print("2. Python dependencies installed (pip install -r requirements.txt)")
    
    if not check_kafka_running():
        print("\n⚠️  WARNING: Kafka is not running!")
        print("Please start Kafka first:")
        print("  docker-compose up -d")
        print("\nWaiting 10 seconds for you to start Kafka...")
        time.sleep(10)
        
        if not check_kafka_running():
            print("✗ Kafka is still not running. Exiting.")
            sys.exit(1)
    
    print("\n✓ Kafka is running!")
    
    print("\nStarting the system:")
    print("1. Starting Kafka Consumer (in background)...")
    print("2. Starting Kafka Producer (will run for 10 minutes)...")
    
    # Start consumer in background
    print("\n[1/2] Starting Consumer...")
    consumer_process = subprocess.Popen(
        [sys.executable, "src/consumer/ed_demand_consumer.py", "--forecast-interval", "5"],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE
    )
    
    time.sleep(3)  # Give consumer time to start
    
    # Start producer
    print("[2/2] Starting Producer...")
    print("\n📊 Producer will simulate patient arrivals for 10 minutes")
    print("📈 Consumer will generate forecasts every 5 minutes\n")
    
    try:
        producer_process = subprocess.Popen(
            [sys.executable, "src/producer/ed_data_producer.py", "--duration", "10", "--rate", "2.0"],
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            universal_newlines=True
        )
        
        # Print producer output
        for line in producer_process.stdout:
            print(line, end='')
        
        producer_process.wait()
        
    except KeyboardInterrupt:
        print("\n\n⚠️  Stopping producer...")
        producer_process.terminate()
    
    finally:
        print("\n\n⚠️  Stopping consumer...")
        consumer_process.terminate()
        consumer_process.wait()
        
        print_header("System Stopped")
        print("Check Kafka topics to see the data:")
        print("  docker exec -it kafka kafka-console-consumer --bootstrap-server localhost:9092 --topic ed-arrivals")
        print("  docker exec -it kafka kafka-console-consumer --bootstrap-server localhost:9092 --topic ed-forecasts")

if __name__ == '__main__':
    main()

