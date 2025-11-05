# Emergency Department Demand Forecasting - Big Data Analytics Dashboard

A comprehensive Streamlit-based big data analytics dashboard for Emergency Department (ED) demand forecasting and real-time monitoring.

## 🎯 Features

- **Real-Time Analytics**: Monitor patient arrivals, capacity, and demand patterns in real-time
- **Advanced Forecasting**: Multiple forecasting models (Time Series and Moving Average)
- **Interactive Visualizations**: Dynamic charts and graphs using Plotly
- **Demographics Analysis**: Patient triage distribution, chief complaints, hourly patterns
- **Capacity Monitoring**: Track bed occupancy and waiting times
- **Data Simulation**: Generate synthetic patient data for testing and demonstration

## 📋 Requirements

- Python 3.8+
- Streamlit
- See `requirements.txt` for all dependencies

## 🚀 Quick Start

1. **Install Dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

2. **Run the Dashboard**:
   
   Option 1: Using the quick start script:
   ```bash
   python run_dashboard.py
   ```
   
   Option 2: Direct Streamlit command:
   ```bash
   streamlit run app.py --server.port 9548
   ```

3. **Access the Dashboard**:
   - The dashboard will open automatically in your browser
   - URL: `http://localhost:9548`

## 📊 Dashboard Features

### Real-Time Metrics
- Total patient count
- Recent arrivals (last hour)
- Available beds
- Waiting patients

### Visualizations
1. **Patient Arrivals Over Time**: Time series chart showing patient arrivals in 15-minute intervals
2. **Demand Forecast**: Predictive forecast with confidence intervals
3. **Triage Level Distribution**: Pie chart showing patient severity distribution
4. **Chief Complaints**: Bar chart of top 10 complaints
5. **Hourly Arrival Pattern**: Hourly distribution of patient arrivals
6. **Capacity Monitoring**: Bed occupancy rate over time with warning thresholds

### Controls
- **Auto-refresh**: Enable automatic data refresh
- **Patient Generation**: Generate new patient arrivals on demand
- **Forecast Settings**: Configure forecast horizon and model selection
- **Sample Data**: Generate sample dataset for testing

## 🏗️ Project Structure

```
test_final/
├── app.py                 # Main Streamlit application
├── requirements.txt       # Python dependencies
└── README.md             # This file
```

## 🔧 Configuration

### Adjusting Arrival Rate
Use the sidebar slider to control the patient arrival rate (patients per minute).

### Forecast Settings
- **Forecast Horizon**: Number of 15-minute windows to forecast (4-24)
- **Model Selection**: Choose between Time Series (Advanced) or Simple Moving Average

### Data Management
- **Clear All Data**: Reset all collected data
- **Generate Sample Data**: Create 100 sample patient records for testing

## 📈 Use Cases

1. **Hospital Operations**: Monitor ED capacity and optimize staffing
2. **Resource Planning**: Forecast demand to allocate resources effectively
3. **Performance Analysis**: Analyze patient arrival patterns and triage distribution
4. **Research**: Study ED demand patterns and trends

## 🎨 Customization

The dashboard can be customized by:
- Modifying chart colors and styles in `app.py`
- Adjusting forecasting models in the forecasting module
- Adding new metrics and visualizations
- Integrating with real data sources

## 📝 Notes

- The dashboard uses simulated data by default
- For production use, integrate with real hospital data systems
- Forecast accuracy depends on data quality and volume
- Auto-refresh rate can be adjusted based on requirements

## 🤝 Contributing

Feel free to extend this dashboard with:
- Additional forecasting models
- More visualization types
- Export functionality
- Historical data analysis
- Alert system for capacity thresholds

## 📄 License

This project is part of the Emergency Department Demand Forecasting system.

---

**Built with Streamlit** 🚀

