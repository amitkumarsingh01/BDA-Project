#!/usr/bin/env python3
"""
Setup script for ED Demand Forecasting Project
"""
import os
import sys
import subprocess

def run_command(command, description):
    """Run a command and print status"""
    print(f"\n{'='*60}")
    print(f"{description}")
    print(f"{'='*60}")
    print(f"Running: {command}\n")
    
    try:
        result = subprocess.run(command, shell=True, check=True, 
                              capture_output=True, text=True)
        print(result.stdout)
        if result.stderr:
            print(result.stderr)
        print(f"✓ {description} completed successfully")
        return True
    except subprocess.CalledProcessError as e:
        print(f"✗ Error: {e}")
        print(f"Error output: {e.stderr}")
        return False

def check_docker():
    """Check if Docker is installed"""
    try:
        subprocess.run(['docker', '--version'], 
                      capture_output=True, check=True)
        return True
    except:
        return False

def check_python():
    """Check Python version"""
    version = sys.version_info
    if version.major >= 3 and version.minor >= 8:
        return True
    return False

def main():
    print("\n" + "="*60)
    print("  Emergency Department Demand Forecasting - Setup")
    print("="*60)
    
    # Check prerequisites
    print("\n[1/4] Checking prerequisites...")
    
    if not check_python():
        print("✗ Python 3.8+ is required")
        print(f"  Current version: {sys.version}")
        sys.exit(1)
    print(f"✓ Python {sys.version.split()[0]} detected")
    
    if not check_docker():
        print("⚠️  Docker not found. You'll need Docker to run Kafka.")
        print("  Install Docker from: https://www.docker.com/get-started")
    else:
        print("✓ Docker detected")
    
    # Install Python dependencies
    print("\n[2/4] Installing Python dependencies...")
    if not run_command("pip install -r requirements.txt", 
                       "Installing requirements"):
        print("⚠️  Failed to install some dependencies. Continuing anyway...")
    
    # Create data directory
    print("\n[3/4] Creating directories...")
    os.makedirs('data', exist_ok=True)
    os.makedirs('data/raw', exist_ok=True)
    os.makedirs('data/processed', exist_ok=True)
    os.makedirs('data/forecasts', exist_ok=True)
    print("✓ Directories created")
    
    # Check Kafka
    print("\n[4/4] Checking Kafka setup...")
    print("\nTo start Kafka, run:")
    print("  docker-compose up -d")
    print("\nThis will start:")
    print("  - Zookeeper (port 2181)")
    print("  - Kafka broker (port 9092)")
    print("  - Kafka UI (http://localhost:8080)")
    
    print("\n" + "="*60)
    print("  Setup Complete!")
    print("="*60)
    print("\nNext steps:")
    print("1. Start Kafka: docker-compose up -d")
    print("2. Wait 30 seconds for Kafka to initialize")
    print("3. Start consumer: python src/consumer/ed_demand_consumer.py")
    print("4. Start producer: python src/producer/ed_data_producer.py")
    print("\nOr run the example: python run_example.py")
    print("\nFor more information, see README.md and KAFKA_GUIDE.md")

if __name__ == '__main__':
    main()

