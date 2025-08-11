"""
Anomaly Detection Script for Stock Prices Data

This script identifies anomalies (outliers) in the stored time-series stock prices data.
It uses multiple statistical methods to detect outliers:
1. Z-score method (beyond 3 standard deviations from mean)
2. IQR method (Interquartile Range)
3. Price change anomalies
4. Volume anomalies
5. OHLC relationship violations

The script queries data from BigQuery and outputs detected anomalies with detailed analysis.
"""

import os
import numpy as np
import pandas as pd
from datetime import datetime
from google.cloud import bigquery
import logging
from typing import Dict

# Set environment variables directly
os.environ['GOOGLE_CLOUD_PROJECT'] = 'bq-example-468708'
os.environ['BIGQUERY_DATASET_ID'] = 'stock_prices_data'

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class AnomalyDetector:
    def __init__(self):
        """Initialize the anomaly detector."""
        self.project_id = os.getenv('GOOGLE_CLOUD_PROJECT')
        self.dataset_id = os.getenv('BIGQUERY_DATASET_ID', 'stock_prices_data')
        self.table_ref = f"{self.project_id}.{self.dataset_id}.stock_prices"
        
        # Initialize BigQuery client
        self.client = bigquery.Client(project=self.project_id)
        
        # Anomaly detection parameters
        self.z_score_threshold = 3.0  # Standard deviations for z-score method (99.7% confidence)
        self.iqr_multiplier = 1.5     # Multiplier for IQR method (standard for outlier detection)
        self.price_change_threshold = 0.1  # 10% price change threshold (market event detection)
        self.volume_threshold = 5.0   # Volume z-score threshold (extreme volume detection)
        self.min_data_points = 10     # Minimum data points required for statistical analysis
        
    def fetch_data_from_bigquery(self, symbol: str = None, days: int = 30) -> pd.DataFrame:
        """Fetch stock prices data from BigQuery."""
        logger.info(f"Fetching data from BigQuery table: {self.table_ref}")
        
        # Build query with parameterized inputs to prevent SQL injection
        if symbol:
            query = f"""
            SELECT *
            FROM `{self.table_ref}`
            WHERE symbol = @symbol
            AND timestamp >= TIMESTAMP_SUB(CURRENT_TIMESTAMP(), INTERVAL @days DAY)
            ORDER BY timestamp ASC
            """
            query_params = [
                bigquery.ScalarQueryParameter("symbol", "STRING", symbol),
                bigquery.ScalarQueryParameter("days", "INT64", days)
            ]
        else:
            query = f"""
            SELECT *
            FROM `{self.table_ref}`
            WHERE timestamp >= TIMESTAMP_SUB(CURRENT_TIMESTAMP(), INTERVAL @days DAY)
            ORDER BY symbol, timestamp ASC
            """
            query_params = [
                bigquery.ScalarQueryParameter("days", "INT64", days)
            ]
        
        try:
            # Execute query with parameters
            job_config = bigquery.QueryJobConfig(query_parameters=query_params)
            query_job = self.client.query(query, job_config=job_config)
            results = query_job.result()
            
            # Convert to DataFrame
            df = pd.DataFrame([dict(row) for row in results])
            
            if df.empty:
                logger.warning("No data found in BigQuery table")
                return df
            
            # Convert timestamp to datetime
            df['timestamp'] = pd.to_datetime(df['timestamp'])
            
            logger.info(f"Fetched {len(df)} records from BigQuery")
            return df
            
        except Exception as e:
            logger.error(f"Error fetching data from BigQuery: {e}")
            return pd.DataFrame()
    
    def calculate_price_changes(self, df: pd.DataFrame) -> pd.DataFrame:
        """Calculate price changes and returns for anomaly detection."""
        df = df.copy()
        
        # Sort by symbol and timestamp
        df = df.sort_values(['symbol', 'timestamp'])
        
        # Calculate price changes
        df['price_change'] = df.groupby('symbol')['close'].pct_change()
        df['price_change_abs'] = df['price_change'].abs()
        
        # Calculate returns (log returns for better statistical properties)
        # Handle division by zero and negative values properly
        df['log_return'] = df.groupby('symbol')['close'].transform(
            lambda x: np.where(
                (x.shift(1) > 0) & (x > 0),
                np.log(x / x.shift(1)),
                np.nan
            )
        )
        
        # Calculate moving averages for comparison
        df['ma_5'] = df.groupby('symbol')['close'].rolling(window=5, min_periods=1).mean().reset_index(0, drop=True)
        df['ma_20'] = df.groupby('symbol')['close'].rolling(window=20, min_periods=1).mean().reset_index(0, drop=True)
        
        # Calculate deviation from moving average (handle division by zero)
        df['deviation_from_ma'] = np.where(
            df['ma_20'] > 0,
            (df['close'] - df['ma_20']) / df['ma_20'],
            np.nan
        )
        
        return df
    
    def detect_z_score_anomalies(self, df: pd.DataFrame, column: str) -> pd.DataFrame:
        """Detect anomalies using z-score method."""
        anomalies = []
        
        for symbol in df['symbol'].unique():
            symbol_data = df[df['symbol'] == symbol]
            
            if len(symbol_data) < self.min_data_points:  # Need minimum data points for statistical validity
                continue
                
            # Calculate z-score
            mean_val = symbol_data[column].mean()
            std_val = symbol_data[column].std()
            
            if std_val == 0:  # Avoid division by zero
                continue
                
            z_scores = (symbol_data[column] - mean_val) / std_val
            
            # Find anomalies
            anomaly_mask = abs(z_scores) > self.z_score_threshold
            anomaly_data = symbol_data[anomaly_mask].copy()
            
            if not anomaly_data.empty:
                anomaly_data['z_score'] = z_scores[anomaly_mask]
                anomaly_data['anomaly_type'] = f'z_score_{column}'
                anomaly_data['anomaly_reason'] = f'Z-score: {z_scores[anomaly_mask].round(2).tolist()}'
                anomalies.append(anomaly_data)
        
        if anomalies:
            return pd.concat(anomalies, ignore_index=True)
        else:
            return pd.DataFrame()
    
    def detect_iqr_anomalies(self, df: pd.DataFrame, column: str) -> pd.DataFrame:
        """Detect anomalies using IQR method."""
        anomalies = []
        
        for symbol in df['symbol'].unique():
            symbol_data = df[df['symbol'] == symbol]
            
            if len(symbol_data) < self.min_data_points:  # Need minimum data points for statistical validity
                continue
                
            # Calculate quartiles
            Q1 = symbol_data[column].quantile(0.25)
            Q3 = symbol_data[column].quantile(0.75)
            IQR = Q3 - Q1
            
            if IQR == 0:  # Avoid division by zero
                continue
                
            # Define bounds
            lower_bound = Q1 - self.iqr_multiplier * IQR
            upper_bound = Q3 + self.iqr_multiplier * IQR
            
            # Find anomalies
            anomaly_mask = (symbol_data[column] < lower_bound) | (symbol_data[column] > upper_bound)
            anomaly_data = symbol_data[anomaly_mask].copy()
            
            if not anomaly_data.empty:
                anomaly_data['iqr_lower'] = lower_bound
                anomaly_data['iqr_upper'] = upper_bound
                anomaly_data['anomaly_type'] = f'iqr_{column}'
                anomaly_data['anomaly_reason'] = f'IQR bounds: [{lower_bound:.2f}, {upper_bound:.2f}]'
                anomalies.append(anomaly_data)
        
        if anomalies:
            return pd.concat(anomalies, ignore_index=True)
        else:
            return pd.DataFrame()
    
    def detect_price_change_anomalies(self, df: pd.DataFrame) -> pd.DataFrame:
        """Detect anomalies based on extreme price changes."""
        anomalies = []
        
        for symbol in df['symbol'].unique():
            symbol_data = df[df['symbol'] == symbol]
            
            # Find extreme price changes
            extreme_changes = symbol_data[symbol_data['price_change_abs'] > self.price_change_threshold].copy()
            
            if not extreme_changes.empty:
                extreme_changes['anomaly_type'] = 'extreme_price_change'
                extreme_changes['anomaly_reason'] = f'Price change: {extreme_changes["price_change"].round(3).tolist()}'
                anomalies.append(extreme_changes)
        
        if anomalies:
            return pd.concat(anomalies, ignore_index=True)
        else:
            return pd.DataFrame()
    
    def detect_ohlc_violations(self, df: pd.DataFrame) -> pd.DataFrame:
        """Detect OHLC relationship violations."""
        violations = []
        
        # Check OHLC relationships
        ohlc_violations = df[
            (df['high'] < df['open']) | 
            (df['high'] < df['close']) |
            (df['low'] > df['open']) | 
            (df['low'] > df['close']) |
            (df['high'] < df['low'])
        ].copy()
        
        if not ohlc_violations.empty:
            ohlc_violations['anomaly_type'] = 'ohlc_violation'
            ohlc_violations['anomaly_reason'] = 'OHLC relationship violation'
            violations.append(ohlc_violations)
        
        # Check for zero or negative prices
        price_violations = df[
            (df['open'] <= 0) | 
            (df['high'] <= 0) | 
            (df['low'] <= 0) | 
            (df['close'] <= 0) |
            (df['volume'] <= 0)
        ].copy()
        
        if not price_violations.empty:
            price_violations['anomaly_type'] = 'invalid_price_volume'
            price_violations['anomaly_reason'] = 'Zero or negative price/volume'
            violations.append(price_violations)
        
        if violations:
            return pd.concat(violations, ignore_index=True)
        else:
            return pd.DataFrame()
    
    def detect_volume_anomalies(self, df: pd.DataFrame) -> pd.DataFrame:
        """Detect volume anomalies."""
        anomalies = []
        
        for symbol in df['symbol'].unique():
            symbol_data = df[df['symbol'] == symbol]
            
            if len(symbol_data) < self.min_data_points:  # Need minimum data points for statistical validity
                continue
                
            # Calculate volume z-score
            mean_volume = symbol_data['volume'].mean()
            std_volume = symbol_data['volume'].std()
            
            if std_volume == 0:
                continue
                
            volume_z_scores = (symbol_data['volume'] - mean_volume) / std_volume
            
            # Find extreme volumes
            extreme_volumes = symbol_data[abs(volume_z_scores) > self.volume_threshold].copy()
            
            if not extreme_volumes.empty:
                extreme_volumes['volume_z_score'] = volume_z_scores[abs(volume_z_scores) > self.volume_threshold]
                extreme_volumes['anomaly_type'] = 'extreme_volume'
                extreme_volumes['anomaly_reason'] = f'Volume z-score: {extreme_volumes["volume_z_score"].round(2).tolist()}'
                anomalies.append(extreme_volumes)
        
        if anomalies:
            return pd.concat(anomalies, ignore_index=True)
        else:
            return pd.DataFrame()
    
    def run_anomaly_detection(self, symbol: str = None, days: int = 30) -> Dict:
        """Run comprehensive anomaly detection on stock prices data."""
        logger.info("Starting anomaly detection...")
        
        # Fetch data from BigQuery
        df = self.fetch_data_from_bigquery(symbol, days)
        
        if df.empty:
            logger.error("No data available for anomaly detection")
            return {}
        
        # Calculate price changes and additional metrics
        df = self.calculate_price_changes(df)
        
        # Initialize results
        all_anomalies = []
        detection_results = {}
        
        # 1. Z-score anomalies for different metrics
        logger.info("Detecting z-score anomalies...")
        for column in ['close', 'volume', 'price_change_abs', 'log_return']:
            if column in df.columns:
                anomalies = self.detect_z_score_anomalies(df, column)
                if not anomalies.empty:
                    all_anomalies.append(anomalies)
                    detection_results[f'z_score_{column}'] = len(anomalies)
        
        # 2. IQR anomalies
        logger.info("Detecting IQR anomalies...")
        for column in ['close', 'volume', 'price_change_abs']:
            if column in df.columns:
                anomalies = self.detect_iqr_anomalies(df, column)
                if not anomalies.empty:
                    all_anomalies.append(anomalies)
                    detection_results[f'iqr_{column}'] = len(anomalies)
        
        # 3. Price change anomalies
        logger.info("Detecting extreme price changes...")
        price_anomalies = self.detect_price_change_anomalies(df)
        if not price_anomalies.empty:
            all_anomalies.append(price_anomalies)
            detection_results['extreme_price_change'] = len(price_anomalies)
        
        # 4. OHLC violations
        logger.info("Detecting OHLC violations...")
        ohlc_anomalies = self.detect_ohlc_violations(df)
        if not ohlc_anomalies.empty:
            all_anomalies.append(ohlc_anomalies)
            detection_results['ohlc_violations'] = len(ohlc_anomalies)
        
        # 5. Volume anomalies
        logger.info("Detecting volume anomalies...")
        volume_anomalies = self.detect_volume_anomalies(df)
        if not volume_anomalies.empty:
            all_anomalies.append(volume_anomalies)
            detection_results['extreme_volume'] = len(volume_anomalies)
        
        # Combine all anomalies
        if all_anomalies:
            combined_anomalies = pd.concat(all_anomalies, ignore_index=True)
            # Remove duplicates based on timestamp and symbol
            combined_anomalies = combined_anomalies.drop_duplicates(subset=['timestamp', 'symbol'])
        else:
            combined_anomalies = pd.DataFrame()
        
        # Prepare results
        results = {
            'total_records': len(df),
            'total_anomalies': len(combined_anomalies),
            'detection_results': detection_results,
            'anomalies': combined_anomalies,
            'data_summary': {
                'symbols': df['symbol'].nunique(),
                'date_range': f"{df['timestamp'].min()} to {df['timestamp'].max()}",
                'total_records': len(df)
            }
        }
        
        logger.info(f"Anomaly detection completed. Found {len(combined_anomalies)} anomalies out of {len(df)} records")
        return results
    
    def print_anomaly_report(self, results: Dict):
        """Print a comprehensive anomaly detection report."""
        print("\n" + "="*80)
        print("ANOMALY DETECTION REPORT")
        print("="*80)
        
        # Summary statistics
        print(f"Data Summary:")
        print(f"  Total Records: {results['total_records']:,}")
        print(f"  Total Anomalies: {results['total_anomalies']:,}")
        print(f"  Anomaly Rate: {(results['total_anomalies'] / results['total_records'] * 100):.2f}%")
        print(f"  Symbols Analyzed: {results['data_summary']['symbols']}")
        print(f"  Date Range: {results['data_summary']['date_range']}")
        
        # Detection method breakdown
        print(f"\nDetection Method Breakdown:")
        for method, count in results['detection_results'].items():
            print(f"  {method}: {count} anomalies")
        
        # Detailed anomalies
        if not results['anomalies'].empty:
            print(f"\nDetailed Anomalies:")
            print("-" * 80)
            
            # Group by symbol
            for symbol in results['anomalies']['symbol'].unique():
                symbol_anomalies = results['anomalies'][results['anomalies']['symbol'] == symbol]
                print(f"\nSymbol: {symbol} ({len(symbol_anomalies)} anomalies)")
                
                for _, anomaly in symbol_anomalies.iterrows():
                    print(f"  {anomaly['timestamp'].strftime('%Y-%m-%d %H:%M:%S')} - {anomaly['anomaly_type']}")
                    print(f"    Reason: {anomaly['anomaly_reason']}")
                    print(f"    OHLC: O:{anomaly['open']:.2f} H:{anomaly['high']:.2f} L:{anomaly['low']:.2f} C:{anomaly['close']:.2f}")
                    print(f"    Volume: {anomaly['volume']:,}")
        else:
            print(f"\nNo anomalies detected in the data.")
        
        print("\n" + "="*80)

def main():
    """Main function to run anomaly detection."""
    try:
        detector = AnomalyDetector()
        
        # Run anomaly detection for all symbols
        print("Running anomaly detection for all symbols...")
        results = detector.run_anomaly_detection(days=30)
        
        if results:
            detector.print_anomaly_report(results)
            
            # Save anomalies to CSV for further analysis
            if not results['anomalies'].empty:
                filename = f"anomalies_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv"
                results['anomalies'].to_csv(filename, index=False)
                print(f"\nAnomalies saved to: {filename}")
        else:
            print("No data available for anomaly detection")
            
    except Exception as e:
        logger.error(f"Anomaly detection failed: {e}")
        raise

if __name__ == "__main__":
    main()
