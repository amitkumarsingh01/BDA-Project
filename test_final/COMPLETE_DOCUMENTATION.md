# Emergency Department Demand Forecasting Dashboard - Complete Documentation

## Table of Contents
1. [Overview](#overview)
2. [Medical Terminology Explained](#medical-terminology-explained)
3. [Dashboard Components](#dashboard-components)
4. [Real-Time Metrics](#real-time-metrics)
5. [Charts and Visualizations](#charts-and-visualizations)
6. [Forecasting Models](#forecasting-models)
7. [Control Panel Features](#control-panel-features)
8. [Data Interpretation Guide](#data-interpretation-guide)
9. [Use Cases](#use-cases)

---

## Overview

### What is Emergency Department Demand Forecasting?

Emergency Department (ED) Demand Forecasting is a predictive analytics system designed to help hospitals and emergency departments anticipate patient arrivals and optimize resource allocation. By analyzing historical patterns, time-based trends, and real-time data, the system predicts how many patients will arrive in future time periods.

**Why is this important?**
- **Resource Planning**: Helps hospitals prepare adequate staff, beds, and equipment
- **Capacity Management**: Prevents overcrowding by anticipating peak times
- **Cost Optimization**: Reduces unnecessary staffing during low-demand periods
- **Patient Care**: Ensures timely care by having resources ready when needed

### Dashboard Purpose

This Streamlit-based dashboard provides a comprehensive, real-time view of:
- Current patient arrivals and ED capacity
- Historical arrival patterns
- Predictive forecasts for future demand
- Visual analytics for decision-making

---

## Medical Terminology Explained

### 🎯 Triage Level

**What is Triage?**
Triage is a medical priority classification system used in emergency departments to determine the order and priority of patient treatment based on the severity of their condition.

**Triage Levels (1-5):**

| Level | Name | Description | Typical Response Time | Examples |
|-------|------|-------------|---------------------|----------|
| **1** | **Critical** | Life-threatening, immediate treatment required | Immediate (< 1 min) | Cardiac arrest, severe trauma, unconscious |
| **2** | **Urgent** | Serious condition, requires prompt attention | < 15 minutes | Chest pain, severe breathing difficulty, stroke symptoms |
| **3** | **Standard** | Moderate condition, can wait | < 30 minutes | Abdominal pain, moderate injuries, high fever |
| **4** | **Low Priority** | Minor condition, non-urgent | < 60 minutes | Minor cuts, sprains, mild symptoms |
| **5** | **Non-Urgent** | Very minor, can wait | < 120 minutes | Minor complaints, prescription refills |

**Distribution in System:**
- Level 1 (Critical): 5% of patients
- Level 2 (Urgent): 15% of patients
- Level 3 (Standard): 40% of patients (most common)
- Level 4 (Low Priority): 30% of patients
- Level 5 (Non-Urgent): 10% of patients

### 🏥 Chief Complaint

**Definition**: The primary reason why a patient seeks medical attention. It's the main symptom or problem described by the patient upon arrival.

**Common Chief Complaints in the Dashboard:**
1. **Chest Pain** - Can indicate heart attack, angina, or other cardiac issues
2. **Shortness of Breath** - Respiratory problems, asthma, heart failure
3. **Abdominal Pain** - Digestive issues, appendicitis, infections
4. **Fever** - Infections, inflammatory conditions
5. **Headache** - Migraines, tension headaches, serious conditions
6. **Trauma** - Injuries from accidents, falls, violence
7. **Back Pain** - Musculoskeletal issues, disc problems
8. **Dizziness** - Inner ear problems, low blood pressure, neurological issues
9. **Nausea/Vomiting** - Digestive disorders, infections, pregnancy
10. **Cough** - Respiratory infections, allergies, chronic conditions
11. **Weakness** - Fatigue, neurological conditions, metabolic issues
12. **Seizure** - Epilepsy, brain conditions, metabolic disorders
13. **Unconscious** - Severe medical emergencies
14. **Allergic Reaction** - Hives, anaphylaxis, reactions to medications

### 📊 Patient Arrival Data Fields

Each patient record contains:

- **Patient ID**: Unique identifier (e.g., PAT123456)
- **Arrival Time**: Timestamp when patient arrived at ED
- **Age**: Patient's age (1-90 years)
- **Gender**: M (Male) or F (Female)
- **Triage Level**: Urgency classification (1-5)
- **Chief Complaint**: Primary symptom/reason for visit
- **Temperature**: Body temperature in Celsius
  - Normal: 36.5-37.5°C
  - Fever: >38°C (indicates infection or inflammation)
- **Day of Week**: 0 (Monday) to 6 (Sunday)
- **Hour of Day**: 0-23 (24-hour format)

### 🏥 Capacity Metrics

- **Total Beds**: Maximum number of beds available in ED
- **Occupied Beds**: Number of beds currently in use
- **Available Beds**: Total - Occupied (beds ready for new patients)
- **Waiting Patients**: Number of patients waiting for bed assignment
- **Occupancy Rate**: Percentage of beds occupied (Occupied/Total × 100)

---

## Dashboard Components

### Layout Structure

The dashboard is organized into several sections:

1. **Header**: Title and branding
2. **Sidebar**: Control panel with all settings
3. **Main Area**: 
   - Real-time metrics (top row)
   - Visualizations (charts)
   - Data tables (bottom)

---

## Real-Time Metrics

### 📊 Real-Time Metrics Section

Four key metrics displayed at the top of the dashboard:

#### 1. Total Patients
- **What it shows**: Total number of patients that have arrived since data collection started
- **Use**: Track overall volume and workload
- **Interpretation**: Higher numbers indicate busier periods

#### 2. Recent Arrivals (1hr)
- **What it shows**: Number of patients who arrived in the last hour
- **Use**: Monitor current activity level
- **Interpretation**: 
  - High numbers (>10/hr): Very busy period
  - Medium numbers (5-10/hr): Normal activity
  - Low numbers (<5/hr): Quiet period

#### 3. Available Beds
- **What it shows**: Number of beds currently available for new patients
- **Use**: Capacity planning and resource allocation
- **Interpretation**:
  - >10 beds: Good capacity
  - 5-10 beds: Moderate capacity
  - <5 beds: Low capacity, may need to prepare for overflow

#### 4. Waiting Patients
- **What it shows**: Number of patients waiting for bed assignment
- **Use**: Monitor patient flow and bottlenecks
- **Interpretation**:
  - 0-5: Normal flow
  - 6-10: Moderate delay
  - >10: Potential bottleneck, may need additional resources

---

## Charts and Visualizations

### 📈 Patient Arrivals Over Time

**Chart Type**: Line Chart with Markers

**What it shows**:
- Historical patient arrivals aggregated into 15-minute time windows
- Trend of patient arrivals over time

**X-axis**: Time (timestamps)
**Y-axis**: Number of patients per 15-minute interval

**How to read**:
- **Rising line**: Increasing patient arrivals (busier period)
- **Falling line**: Decreasing arrivals (quieter period)
- **Peaks**: High-demand periods
- **Valleys**: Low-demand periods

**Use cases**:
- Identify peak hours
- Understand daily patterns
- Compare current period to historical trends

**Example interpretation**:
```
If you see:
- Peak at 2 PM: Afternoon rush
- Peak at 8 PM: Evening rush
- Low at 3 AM: Night shift quiet period
```

---

### 🔮 Demand Forecast

**Chart Type**: Combined Line Chart with Confidence Intervals

**What it shows**:
- Historical data (blue line)
- Predicted future demand (orange dashed line)
- Confidence intervals (shaded area)

**Components**:

1. **Historical Data (Blue Line)**
   - Actual patient arrivals up to current time
   - Solid line with markers

2. **Forecast (Orange Dashed Line)**
   - Predicted patient arrivals for future periods
   - Based on selected forecasting model

3. **Confidence Interval (Shaded Area)**
   - Upper bound: Maximum likely demand
   - Lower bound: Minimum likely demand
   - Represents uncertainty (95% confidence)

**How to read**:
- **Forecast line above historical**: Expected increase in demand
- **Forecast line below historical**: Expected decrease in demand
- **Wide confidence interval**: Higher uncertainty in prediction
- **Narrow confidence interval**: More confident prediction

**Decision-making**:
- If forecast exceeds capacity → Prepare additional resources
- If forecast is low → Normal operations sufficient
- If confidence interval is very wide → Exercise caution, monitor closely

**Example**:
```
Historical shows 5 patients/15min average
Forecast shows 8 patients/15min for next hour
Confidence interval: 6-10 patients/15min

Action: Prepare for 30-40% increase in demand
```

---

### 🎯 Triage Level Distribution

**Chart Type**: Pie Chart

**What it shows**:
- Proportion of patients by triage level
- Visual breakdown of patient urgency

**Colors**: Red tones (darker = more urgent)

**How to read**:
- **Large Critical segment (Level 1)**: High-acuity period, requires trauma team
- **Large Standard segment (Level 3)**: Normal operations
- **Large Non-Urgent segment (Level 5)**: Mostly minor cases

**Use cases**:
- Staff planning based on acuity mix
- Identify periods with high critical cases
- Resource allocation (critical care vs. general care)

**Example interpretation**:
```
If Critical (Level 1) = 15%:
- Normal: 5%
- Current: 15% (3x normal)
- Action: Alert trauma team, prepare ICU resources
```

---

### 🏥 Chief Complaints

**Chart Type**: Horizontal Bar Chart

**What it shows**:
- Top 10 most common chief complaints
- Frequency of each complaint type

**X-axis**: Number of patients
**Y-axis**: Complaint types

**How to read**:
- **Taller bars**: More common complaints
- **Shorter bars**: Less common complaints
- **Color intensity**: Darker = more frequent

**Use cases**:
- Identify common conditions (may need specialized staff)
- Seasonal patterns (e.g., flu season → more fever complaints)
- Resource preparation (e.g., many trauma cases → prepare trauma bay)

**Example interpretation**:
```
Top complaints:
1. Chest Pain (20 patients)
2. Abdominal Pain (15 patients)
3. Fever (12 patients)

Analysis: High cardiac cases → ensure cardiologist available
```

---

### ⏰ Hourly Arrival Pattern

**Chart Type**: Bar Chart

**What it shows**:
- Distribution of patient arrivals across 24 hours
- Hourly pattern of ED demand

**X-axis**: Hour of day (0-23)
**Y-axis**: Number of patients

**How to read**:
- **High bars**: Peak hours (busier periods)
- **Low bars**: Quiet hours
- **Color gradient**: Visual indication of volume

**Typical patterns**:
- **Morning peak (8-10 AM)**: After-hours clinic overflow
- **Afternoon peak (2-4 PM)**: Post-lunch period
- **Evening peak (6-10 PM)**: Highest demand period
- **Night (12-6 AM)**: Lowest demand

**Use cases**:
- Shift planning
- Staff scheduling
- Resource allocation by time of day

**Example interpretation**:
```
Peak hours:
- 8 PM: 25 patients
- 2 PM: 18 patients
- 4 AM: 3 patients

Action: Schedule more staff during 6-10 PM shift
```

---

### 🏥 Capacity Monitoring

**Chart Type**: Area Chart with Threshold Lines

**What it shows**:
- Bed occupancy rate over time
- Percentage of beds occupied

**Y-axis**: Occupancy rate (0-100%)
**X-axis**: Time

**Threshold Lines**:
- **Orange dashed line (80%)**: Warning threshold
- **Red dashed line (95%)**: Critical threshold

**How to read**:
- **Below 80%**: Comfortable capacity
- **80-95%**: Warning zone, monitor closely
- **Above 95%**: Critical, immediate action needed

**Use cases**:
- Real-time capacity monitoring
- Alert triggers for overflow protocols
- Resource allocation decisions

**Example interpretation**:
```
Current occupancy: 85%
Trend: Increasing (was 75% an hour ago)

Action: 
- Prepare overflow area
- Consider diverting low-acuity patients
- Alert additional staff
```

---

### 📋 Recent Patient Arrivals Table

**Table Type**: Data Table

**What it shows**:
- Last 20 patient arrivals with detailed information
- Individual patient records

**Columns**:
- Patient ID
- Arrival Time
- Age
- Gender
- Triage Level
- Chief Complaint
- Temperature

**Use cases**:
- Review recent arrivals
- Identify patterns in current patients
- Detailed patient-level analysis

**Sorting**: Click column headers to sort

---

## Forecasting Models

### Overview

The dashboard offers two forecasting models to predict future patient demand:

### 1. Simple Moving Average

**How it works**:
- Calculates average of recent historical data
- Uses same average for all future periods
- Simple statistical method

**Formula**:
```
Forecast = Average of last N periods
```

**Pros**:
- Fast computation
- Easy to understand
- Works with minimal data

**Cons**:
- Doesn't account for time patterns
- Same prediction for all periods
- Less accurate for complex patterns

**Best for**:
- Quick estimates
- Baseline comparisons
- Limited historical data

**Example**:
```
Last 24 periods average: 5 patients/15min
Forecast: 5 patients/15min for all future periods
```

---

### 2. Time Series (Advanced)

**How it works**:
- Machine learning model (Linear Regression)
- Uses 8 features:
  1. Hour of day (cyclical encoding)
  2. Day of week
  3. Weekend indicator
  4. Recent lag values (1, 4, 24 periods ago)
  5. Moving averages (1-hour, 6-hour)

**Pros**:
- Accounts for time patterns
- Adapts to daily/weekly cycles
- More accurate predictions
- Considers trends

**Cons**:
- Requires more data (10+ points)
- Slightly slower computation
- More complex

**Best for**:
- Operational planning
- Accurate demand forecasting
- Complex pattern recognition

**Example**:
```
Time: 6 PM, Weekday
Features: Evening hour, Recent high demand, Upward trend
Forecast: 8 patients/15min (higher than average due to evening pattern)
```

---

## Control Panel Features

### Sidebar Controls

Located on the left side of the dashboard, the control panel provides:

#### Simulation Section

**Auto-refresh data**
- **Function**: Automatically refreshes dashboard data
- **When to use**: Real-time monitoring
- **Caution**: Uses more resources

**Refresh interval (seconds)**
- **Range**: 1-10 seconds
- **Default**: 2 seconds
- **Impact**: Lower = more frequent updates, higher resource usage

**Patient arrival rate (per minute)**
- **Range**: 0.5-5.0 patients/minute
- **Default**: 2.0 patients/minute
- **Use**: Adjust simulation speed

**Generate New Patients Button**
- **Function**: Creates new patient arrivals
- **Options**: Select number of patients (1-50)
- **Use**: Simulate patient arrivals for testing

---

#### Forecast Settings Section

**Forecast horizon (15-min windows)**
- **Range**: 4-24 windows
- **Default**: 8 windows (2 hours)
- **Meaning**: How far into future to forecast
- **Example**: 8 windows = 2 hours ahead

**Forecasting Model**
- **Options**:
  - Time Series (Advanced)
  - Simple Moving Average
- **Use**: Select based on data availability and accuracy needs

---

#### Data Management Section

**Clear All Data Button**
- **Function**: Removes all collected data
- **Use**: Reset dashboard for fresh start
- **Warning**: Cannot undo

**Generate Sample Data Button**
- **Function**: Creates 100 sample patients
- **Use**: Quickly populate dashboard for demonstration
- **Data**: Spreads across last 6 hours with realistic patterns

---

## Data Interpretation Guide

### Understanding Patterns

#### Daily Patterns
- **Morning (6-10 AM)**: Moderate activity, often after-hours overflow
- **Afternoon (12-4 PM)**: Steady activity
- **Evening (6-10 PM)**: Peak hours, highest demand
- **Night (10 PM-6 AM)**: Lowest activity

#### Weekly Patterns
- **Weekdays**: Higher activity
- **Weekends**: 30% lower activity typically
- **Holidays**: 40% lower activity (except trauma cases)

#### Seasonal Patterns
- **Winter**: More respiratory complaints, flu
- **Summer**: More trauma, heat-related issues
- **Spring/Fall**: Moderate activity

### Decision-Making Framework

#### When to Act

**Green Zone (Normal Operations)**:
- Occupancy < 80%
- Forecast within normal range
- Standard triage distribution

**Yellow Zone (Monitor Closely)**:
- Occupancy 80-95%
- Forecast above average
- Increased critical cases

**Red Zone (Take Action)**:
- Occupancy > 95%
- Forecast significantly exceeds capacity
- High proportion of critical cases

**Action Items**:
1. **Staffing**: Call additional staff if forecast exceeds capacity
2. **Resources**: Prepare equipment and supplies
3. **Beds**: Prepare overflow areas
4. **Divert**: Consider diverting low-acuity patients if overwhelmed

---

## Use Cases

### 1. Hospital Operations Management

**Scenario**: ED manager needs to plan next shift staffing

**Dashboard Use**:
1. Check hourly arrival pattern
2. Review forecast for next 4 hours
3. Analyze current capacity
4. Make staffing decisions

**Example**:
```
Forecast shows 8 patients/15min for next 2 hours
Current capacity: 85%
Action: Schedule 2 additional nurses for evening shift
```

---

### 2. Resource Planning

**Scenario**: Need to prepare for peak period

**Dashboard Use**:
1. Identify peak hours from hourly pattern
2. Check forecast for peak period
3. Review chief complaints to prepare equipment
4. Monitor capacity trends

**Example**:
```
Peak hour: 8 PM
Forecast: 10 patients/15min
Top complaint: Chest Pain
Action: Ensure cardiologist available, prepare cardiac monitoring equipment
```

---

### 3. Capacity Management

**Scenario**: Monitor real-time capacity

**Dashboard Use**:
1. Watch capacity monitoring chart
2. Check available beds metric
3. Monitor waiting patients
4. Review forecast to anticipate future demand

**Example**:
```
Current occupancy: 90%
Forecast: Increasing trend
Available beds: 5
Action: Prepare overflow area, alert transport team
```

---

### 4. Quality Analysis

**Scenario**: Analyze patient patterns

**Dashboard Use**:
1. Review triage distribution
2. Analyze chief complaints
3. Examine hourly patterns
4. Compare periods

**Example**:
```
Triage analysis shows:
- Critical cases: 10% (normal: 5%)
- Standard cases: 35% (normal: 40%)

Analysis: Higher acuity period, may need specialized care
```

---

### 5. Training and Demonstration

**Scenario**: Training new staff on ED operations

**Dashboard Use**:
1. Generate sample data
2. Explain each visualization
3. Show decision-making process
4. Demonstrate forecasting concepts

---

## Tips for Best Use

1. **Start with Sample Data**: Use "Generate Sample Data" to explore features
2. **Enable Auto-refresh**: For real-time monitoring
3. **Adjust Forecast Horizon**: Based on planning needs (short-term vs. long-term)
4. **Compare Models**: Try both forecasting models to see differences
5. **Monitor Trends**: Watch for patterns in charts
6. **Set Thresholds**: Use capacity thresholds for alerts
7. **Regular Review**: Check dashboard regularly for early warnings

---

## Technical Notes

### Data Aggregation
- Patient arrivals are aggregated into 15-minute windows
- This provides balance between detail and clarity

### Forecasting Accuracy
- Accuracy improves with more historical data
- Time Series model requires 10+ data points for best results
- Confidence intervals show prediction uncertainty

### Performance
- Dashboard updates in real-time
- Auto-refresh can be adjusted based on needs
- Data is stored in session (cleared on refresh)

---

## Glossary

- **ED**: Emergency Department
- **Triage**: Priority classification system
- **Chief Complaint**: Primary reason for visit
- **Occupancy Rate**: Percentage of beds in use
- **Forecast Horizon**: Future time period for predictions
- **Lag Feature**: Previous period's value used in prediction
- **Confidence Interval**: Range of likely values (95% confidence)
- **Moving Average**: Average of recent values
- **Aggregation**: Combining data into time windows

---

## Conclusion

This dashboard provides comprehensive tools for Emergency Department demand forecasting and management. By understanding each component, visualization, and metric, users can make informed decisions about resource allocation, staffing, and capacity management.

For questions or issues, refer to the QUICK_START.md guide or check the technical documentation.

---

**Last Updated**: Dashboard v1.0  
**Maintained by**: ED Demand Forecasting Team

