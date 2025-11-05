# Emergency Department Demand Forecasting with Apache Kafka

## Project Overview

This project implements a real-time Emergency Department (ED) demand forecasting system using Apache Kafka for data streaming and processing. The system simulates ED patient arrivals, streams data through Kafka, and performs real-time demand forecasting using machine learning models.

## Architecture

```
ED Data Sources → Kafka Producer → Kafka Topics → Kafka Consumer → Forecasting Model → Dashboard/Analytics
```

## Components

1. **Kafka Producer**: Simulates ED patient arrival data and streams it to Kafka topics
2. **Kafka Consumer**: Consumes data from Kafka topics and performs demand forecasting
3. **Data Models**: Patient arrival data structure and forecasting models
4. **Forecasting Service**: ML-based forecasting using historical patterns

## Prerequisites

- Python 3.8+
- Apache Kafka 2.8+
- Docker and Docker Compose (optional, for easy setup)
- Required Python packages (see requirements.txt)

## Quick Start

1. Start Kafka using Docker Compose:
   ```bash
   docker-compose up -d
   ```

2. Install Python dependencies:
   ```bash
   pip install -r requirements.txt
   ```

3. Run the Kafka producer:
   ```bash
   python src/producer/ed_data_producer.py
   ```

4. Run the Kafka consumer:
   ```bash
   python src/consumer/ed_demand_consumer.py
   ```

## Project Structure

```
final_project/
├── src/
│   ├── producer/          # Kafka producer components
│   ├── consumer/          # Kafka consumer components
│   ├── models/            # Data models and schemas
│   ├── forecasting/       # ML forecasting models
│   └── utils/             # Utility functions
├── config/                # Configuration files
├── data/                  # Sample data and outputs
├── docker-compose.yml     # Docker setup for Kafka
├── requirements.txt       # Python dependencies
└── README.md             # This file
```

## Kafka Topics

- `ed-arrivals`: Raw patient arrival data
- `ed-forecasts`: Forecasted demand predictions
- `ed-statistics`: Real-time statistics and metrics

## Features

- Real-time data streaming with Apache Kafka
- Patient arrival simulation with realistic patterns
- Demand forecasting using time series analysis
- Scalable architecture for high-throughput scenarios
- Integration ready for big data analytics tools

## Big Data Analytics Integration

This project demonstrates key Big Data Analytics concepts:
- **Volume**: Handles large-scale patient data streams
- **Velocity**: Real-time processing and forecasting
- **Variety**: Multiple data sources and formats
- **Stream Processing**: Kafka Streams for continuous data processing

