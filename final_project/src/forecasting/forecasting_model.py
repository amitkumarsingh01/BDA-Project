"""
Time Series Forecasting Model for ED Demand
"""
import numpy as np
import pandas as pd
from typing import Tuple, List
from datetime import datetime, timedelta
from sklearn.linear_model import LinearRegression
from sklearn.preprocessing import StandardScaler


class TimeSeriesForecaster:
    """Simple time series forecasting model for ED demand"""
    
    def __init__(self, window_size: int = 96):
        """
        Initialize forecaster
        
        Args:
            window_size: Number of historical data points to use
        """
        self.window_size = window_size
        self.model = LinearRegression()
        self.scaler = StandardScaler()
        self.is_fitted = False
        self.historical_data = []
    
    def add_data_point(self, timestamp: datetime, count: int):
        """Add a new data point to historical data"""
        self.historical_data.append({
            'timestamp': timestamp,
            'count': count
        })
        
        # Keep only recent data
        if len(self.historical_data) > self.window_size:
            self.historical_data = self.historical_data[-self.window_size:]
    
    def prepare_features(self, df: pd.DataFrame) -> pd.DataFrame:
        """Prepare features for forecasting"""
        df = df.copy()
        df['timestamp'] = pd.to_datetime(df['timestamp'])
        df = df.sort_values('timestamp')
        
        # Time features
        df['hour'] = df['timestamp'].dt.hour
        df['day_of_week'] = df['timestamp'].dt.dayofweek
        df['is_weekend'] = (df['day_of_week'] >= 5).astype(int)
        
        # Cyclical encoding for hour
        df['hour_sin'] = np.sin(2 * np.pi * df['hour'] / 24)
        df['hour_cos'] = np.cos(2 * np.pi * df['hour'] / 24)
        
        # Lag features
        df['lag_1'] = df['count'].shift(1)
        df['lag_4'] = df['count'].shift(4)  # 1 hour ago (4 * 15 min)
        df['lag_24'] = df['count'].shift(24)  # 6 hours ago
        
        # Moving averages
        df['ma_4'] = df['count'].rolling(window=4, min_periods=1).mean()
        df['ma_24'] = df['count'].rolling(window=24, min_periods=1).mean()
        
        # Fill NaN values
        df = df.bfill().fillna(0)
        
        return df
    
    def fit(self, df: pd.DataFrame):
        """Fit the forecasting model"""
        if len(df) < 10:
            return  # Need minimum data points
        
        df_features = self.prepare_features(df)
        
        # Select features
        feature_cols = ['hour_sin', 'hour_cos', 'is_weekend', 
                       'lag_1', 'lag_4', 'lag_24', 'ma_4', 'ma_24']
        
        X = df_features[feature_cols].values
        y = df_features['count'].values
        
        # Scale features
        X_scaled = self.scaler.fit_transform(X)
        
        # Fit model
        self.model.fit(X_scaled, y)
        self.is_fitted = True
    
    def predict(self, forecast_horizon: int = 4) -> Tuple[List[float], List[float], List[float]]:
        """
        Predict future demand
        
        Args:
            forecast_horizon: Number of 15-minute windows to forecast
        
        Returns:
            Tuple of (predictions, lower_bound, upper_bound)
        """
        if not self.is_fitted or len(self.historical_data) < 10:
            # Return simple average if not enough data
            if self.historical_data:
                avg = np.mean([d['count'] for d in self.historical_data[-24:]])
                predictions = [avg] * forecast_horizon
            else:
                predictions = [0.0] * forecast_horizon
            
            return predictions, predictions, predictions
        
        # Create DataFrame from historical data
        df = pd.DataFrame(self.historical_data)
        df = df.sort_values('timestamp')
        
        # Get last timestamp
        last_timestamp = df['timestamp'].iloc[-1]
        
        # Prepare features for last data point
        df_features = self.prepare_features(df)
        last_features = df_features[['hour_sin', 'hour_cos', 'is_weekend',
                                     'lag_1', 'lag_4', 'lag_24', 'ma_4', 'ma_24']].iloc[-1:].values
        
        # Generate predictions
        predictions = []
        lower_bounds = []
        upper_bounds = []
        
        current_df = df.copy()
        
        for i in range(forecast_horizon):
            # Prepare features
            features = self.prepare_features(current_df)
            features_vector = features[['hour_sin', 'hour_cos', 'is_weekend',
                                       'lag_1', 'lag_4', 'lag_24', 'ma_4', 'ma_24']].iloc[-1:].values
            
            # Scale and predict
            features_scaled = self.scaler.transform(features_vector)
            pred = self.model.predict(features_scaled)[0]
            pred = max(0, pred)  # Ensure non-negative
            
            predictions.append(pred)
            
            # Simple confidence interval (can be improved)
            std_dev = np.std(df['count'].values[-24:]) if len(df) >= 24 else 1.0
            lower_bounds.append(max(0, pred - 1.96 * std_dev))
            upper_bounds.append(pred + 1.96 * std_dev)
            
            # Update current_df with prediction for next iteration
            next_timestamp = last_timestamp + timedelta(minutes=15 * (i + 1))
            new_row = pd.DataFrame({
                'timestamp': [next_timestamp],
                'count': [pred]
            })
            current_df = pd.concat([current_df, new_row], ignore_index=True)
        
        return predictions, lower_bounds, upper_bounds


class SimpleMovingAverageForecaster:
    """Simple moving average based forecaster"""
    
    def __init__(self, window_size: int = 24):
        self.window_size = window_size
        self.historical_data = []
    
    def add_data_point(self, timestamp: datetime, count: int):
        """Add a new data point"""
        self.historical_data.append({
            'timestamp': timestamp,
            'count': count
        })
        
        if len(self.historical_data) > self.window_size * 2:
            self.historical_data = self.historical_data[-self.window_size * 2:]
    
    def predict(self, forecast_horizon: int = 4) -> Tuple[List[float], List[float], List[float]]:
        """Predict using moving average"""
        if len(self.historical_data) < 4:
            return [0.0] * forecast_horizon, [0.0] * forecast_horizon, [0.0] * forecast_horizon
        
        counts = [d['count'] for d in self.historical_data[-self.window_size:]]
        avg = np.mean(counts)
        std = np.std(counts) if len(counts) > 1 else 1.0
        
        predictions = [avg] * forecast_horizon
        lower_bounds = [max(0, avg - 1.96 * std)] * forecast_horizon
        upper_bounds = [avg + 1.96 * std] * forecast_horizon
        
        return predictions, lower_bounds, upper_bounds

