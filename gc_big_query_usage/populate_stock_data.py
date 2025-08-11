"""
Stock Prices Data Population Script

This script generates synthetic stock prices data and saves it to CSV files.
It creates realistic OHLCV data for multiple stocks with approximately normal distribution.
Due to BigQuery free tier limitations, data is saved to CSV files for manual upload.
"""

import os
import random
import numpy as np
import pandas as pd
from datetime import datetime, timedelta
from google.cloud import bigquery
from google.cloud.exceptions import NotFound
import logging

# Set environment variables directly
os.environ['GOOGLE_CLOUD_PROJECT'] = 'bq-example-468708'
os.environ['BIGQUERY_DATASET_ID'] = 'stock_prices_data'

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class StockDataGenerator:
    def __init__(self):
        """Initialize the stock data generator."""
        self.project_id = os.getenv('GOOGLE_CLOUD_PROJECT')
        self.dataset_id = os.getenv('BIGQUERY_DATASET_ID', 'stock_prices_data')
        self.table_ref = f"{self.project_id}.{self.dataset_id}.stock_prices"
        
        # Initialize BigQuery client
        self.client = bigquery.Client(project=self.project_id)
        
        # Stock configuration
        self.stocks = [
            {'symbol': 'AAPL', 'exchange': 'NASDAQ', 'base_price': 150.0, 'volatility': 0.02},
            {'symbol': 'GOOGL', 'exchange': 'NASDAQ', 'base_price': 2800.0, 'volatility': 0.025},
            {'symbol': 'MSFT', 'exchange': 'NASDAQ', 'base_price': 300.0, 'volatility': 0.018},
            {'symbol': 'AMZN', 'exchange': 'NASDAQ', 'base_price': 3200.0, 'volatility': 0.03},
            {'symbol': 'TSLA', 'exchange': 'NASDAQ', 'base_price': 800.0, 'volatility': 0.04},
            {'symbol': 'META', 'exchange': 'NASDAQ', 'base_price': 350.0, 'volatility': 0.022},
            {'symbol': 'NVDA', 'exchange': 'NASDAQ', 'base_price': 500.0, 'volatility': 0.035},
            {'symbol': 'JPM', 'exchange': 'NYSE', 'base_price': 150.0, 'volatility': 0.015},
            {'symbol': 'JNJ', 'exchange': 'NYSE', 'base_price': 170.0, 'volatility': 0.012},
            {'symbol': 'PG', 'exchange': 'NYSE', 'base_price': 140.0, 'volatility': 0.01}
        ]
        
        # Time intervals
        self.intervals = ['1d', '1h', '15m']
        
    def generate_price_series(self, base_price, volatility, num_points, start_date):
        """Generate realistic stock price series using geometric Brownian motion."""
        # Set random seed for reproducibility
        np.random.seed(int(start_date.timestamp()) % 2**32)
        
        # Generate random returns with normal distribution
        returns = np.random.normal(0, volatility, num_points)
        
        # Add some trend and mean reversion (more realistic)
        trend = np.linspace(0, 0.0001, num_points)  # Slight upward trend
        mean_reversion = -0.0001 * np.arange(num_points)  # Mean reversion effect
        returns += trend + mean_reversion
        
        # Generate price series
        prices = [base_price]
        for i in range(1, num_points):
            new_price = prices[-1] * (1 + returns[i-1])
            # Ensure prices stay positive
            new_price = max(new_price, base_price * 0.1)
            prices.append(new_price)
        
        return np.array(prices)
    
    def generate_ohlcv_data(self, symbol, exchange, base_price, volatility, num_points, start_date, interval):
        """Generate OHLCV data for a stock."""
        # Generate base price series
        prices = self.generate_price_series(base_price, volatility, num_points, start_date)
        
        # Generate timestamps
        if interval == '1d':
            timestamps = [start_date + timedelta(days=i) for i in range(num_points)]
        elif interval == '1h':
            timestamps = [start_date + timedelta(hours=i) for i in range(num_points)]
        elif interval == '15m':
            timestamps = [start_date + timedelta(minutes=15*i) for i in range(num_points)]
        
        data = []
        for i, (price, timestamp) in enumerate(zip(prices, timestamps)):
            # Generate OHLC from base price with some variation
            price_variation = price * 0.01  # 1% variation
            
            open_price = price + random.uniform(-price_variation, price_variation)
            high_price = max(open_price, price + random.uniform(0, price_variation * 2))
            low_price = min(open_price, price - random.uniform(0, price_variation * 2))
            close_price = price + random.uniform(-price_variation, price_variation)
            
            # Ensure OHLC relationship is maintained
            high_price = max(open_price, close_price, high_price)
            low_price = min(open_price, close_price, low_price)
            
            # Generate volume (correlated with price movement and volatility)
            base_volume = 1000000  # Base volume
            price_change = abs(close_price - open_price) / open_price if open_price > 0 else 0
            volatility_factor = 1 + price_change * 5  # Volume increases with price volatility
            time_factor = 1.0  # Base time factor
            
            # Adjust volume based on market hours for intraday data
            if interval != '1d':
                hour = timestamp.hour
                if 9 <= hour <= 16:  # Market hours
                    time_factor = 1.0
                else:  # Outside market hours
                    time_factor = 0.1
            
            volume = int(base_volume * volatility_factor * time_factor * random.uniform(0.5, 2.0))
            
            # Generate additional fields
            adjusted_close = close_price
            dividend_amount = 0.0 if random.random() > 0.95 else random.uniform(0.5, 2.0)
            split_coefficient = 1.0
            currency = 'USD'
            data_source = 'SYNTHETIC'
            
            # Market hours logic is now handled in volume calculation above
            
            data.append({
                'timestamp': timestamp.strftime('%Y-%m-%d %H:%M:%S'),
                'symbol': symbol,
                'exchange': exchange,
                'open': round(open_price, 2),
                'high': round(high_price, 2),
                'low': round(low_price, 2),
                'close': round(close_price, 2),
                'volume': volume,
                'adjusted_close': round(adjusted_close, 2),
                'dividend_amount': round(dividend_amount, 2),
                'split_coefficient': split_coefficient,
                'currency': currency,
                'data_source': data_source,
                'interval': interval,
                'created_at': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
                'updated_at': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            })
        
        return data
    
    def generate_dataset(self, total_points=500000):
        """Generate the complete dataset with specified number of points."""
        logger.info(f"Generating {total_points:,} data points...")
        
        # Calculate points per stock and interval
        num_stocks = len(self.stocks)
        num_intervals = len(self.intervals)
        points_per_combination = total_points // (num_stocks * num_intervals)
        
        logger.info(f"Points per stock/interval combination: {points_per_combination:,}")
        
        all_data = []
        start_date = datetime(2023, 1, 1, 9, 30)  # Market open
        
        for stock in self.stocks:
            for interval in self.intervals:
                logger.info(f"Generating data for {stock['symbol']} ({interval})...")
                
                data = self.generate_ohlcv_data(
                    symbol=stock['symbol'],
                    exchange=stock['exchange'],
                    base_price=stock['base_price'],
                    volatility=stock['volatility'],
                    num_points=points_per_combination,
                    start_date=start_date,
                    interval=interval
                )
                
                all_data.extend(data)
        
        logger.info(f"Generated {len(all_data):,} data points")
        return all_data
    
    def save_to_csv(self, data, filename='stock_prices_data.csv'):
        """Save data to CSV file."""
        logger.info(f"Saving {len(data):,} records to {filename}...")
        
        # Convert to DataFrame
        df = pd.DataFrame(data)
        
        # Clean the data before saving
        df = self.clean_dataframe(df)
        
        # Save to CSV with proper encoding and no line breaks in data
        df.to_csv(filename, index=False, encoding='utf-8', quoting=1)  # quoting=1 for QUOTE_ALL
        
        logger.info(f"Data saved to {filename}")
        logger.info(f"File size: {os.path.getsize(filename) / (1024*1024):.2f} MB")
        
        return filename
    
    def save_to_multiple_csvs(self, data, records_per_file=50000):
        """Save data to multiple CSV files for easier upload."""
        logger.info(f"Saving {len(data):,} records to multiple CSV files...")
        
        # Convert to DataFrame and clean
        df = pd.DataFrame(data)
        df = self.clean_dataframe(df)
        
        total_files = (len(df) + records_per_file - 1) // records_per_file
        filenames = []
        
        for i in range(0, len(df), records_per_file):
            batch = df[i:i + records_per_file]
            filename = f'stock_prices_data_part_{i//records_per_file + 1:03d}.csv'
            
            # Save with proper encoding and quoting
            batch.to_csv(filename, index=False, encoding='utf-8', quoting=1)
            
            filenames.append(filename)
            logger.info(f"Saved {len(batch):,} records to {filename}")
        
        logger.info(f"Created {len(filenames)} CSV files")
        return filenames
    
    def clean_dataframe(self, df):
        """Clean and validate the DataFrame."""
        logger.info("Cleaning DataFrame...")
        
        # Validate input DataFrame
        if df.empty:
            logger.warning("Empty DataFrame provided for cleaning")
            return df
        
        # Remove any rows with NaN values in required fields
        required_fields = ['timestamp', 'symbol', 'exchange', 'open', 'high', 'low', 'close', 'volume', 'interval']
        initial_count = len(df)
        df = df.dropna(subset=required_fields)
        if len(df) < initial_count:
            logger.warning(f"Removed {initial_count - len(df)} rows with missing required fields")
        
        # Ensure numeric fields are properly formatted
        numeric_fields = ['open', 'high', 'low', 'close', 'volume', 'adjusted_close', 'dividend_amount', 'split_coefficient']
        for field in numeric_fields:
            if field in df.columns:
                df[field] = pd.to_numeric(df[field], errors='coerce')
        
        # Ensure string fields are properly formatted and clean
        string_fields = ['symbol', 'exchange', 'currency', 'data_source', 'interval']
        for field in string_fields:
            if field in df.columns:
                df[field] = df[field].astype(str).str.strip()
        
        # Ensure OHLC relationships are maintained (High >= Open, Close and Low <= Open, Close)
        df['high'] = df[['open', 'high', 'close']].max(axis=1)
        df['low'] = df[['open', 'low', 'close']].min(axis=1)
        
        # Validate OHLC relationships
        ohlc_violations = df[
            (df['high'] < df['open']) | 
            (df['high'] < df['close']) |
            (df['low'] > df['open']) | 
            (df['low'] > df['close']) |
            (df['high'] < df['low'])
        ]
        if not ohlc_violations.empty:
            logger.warning(f"Found {len(ohlc_violations)} OHLC relationship violations - corrected")
        
        # Ensure volume is positive
        df['volume'] = df['volume'].abs()
        
        # Round numeric fields to 2 decimal places
        for field in ['open', 'high', 'low', 'close', 'adjusted_close', 'dividend_amount']:
            if field in df.columns:
                df[field] = df[field].round(2)
        
        # Round split_coefficient to 1 decimal place
        if 'split_coefficient' in df.columns:
            df['split_coefficient'] = df['split_coefficient'].round(1)
        
        # Convert timestamp columns to datetime and format properly
        df['timestamp'] = pd.to_datetime(df['timestamp'])
        df['created_at'] = pd.to_datetime(df['created_at'])
        df['updated_at'] = pd.to_datetime(df['updated_at'])
        
        # Format timestamps as strings without line breaks
        df['timestamp'] = df['timestamp'].dt.strftime('%Y-%m-%d %H:%M:%S')
        df['created_at'] = df['created_at'].dt.strftime('%Y-%m-%d %H:%M:%S')
        df['updated_at'] = df['updated_at'].dt.strftime('%Y-%m-%d %H:%M:%S')
        
        logger.info(f"Cleaned DataFrame: {len(df)} records")
        return df
    
    def verify_table_exists(self):
        """Verify that the BigQuery table exists."""
        try:
            self.client.get_table(self.table_ref)
            logger.info(f"Table {self.table_ref} exists")
            return True
        except NotFound:
            logger.error(f"Table {self.table_ref} does not exist")
            logger.error("Please run create_bigquery_timeseries_table.py first")
            return False
    
    def run_population(self, total_points=500000, split_files=True):
        """Run the complete data population process."""
        logger.info("Starting stock prices data generation...")
        
        # Verify table exists
        if not self.verify_table_exists():
            return False
        
        # Generate data
        data = self.generate_dataset(total_points)
        
        # Save data to CSV files
        if split_files:
            filenames = self.save_to_multiple_csvs(data)
            logger.info(f"Data saved to {len(filenames)} CSV files")
        else:
            filename = self.save_to_csv(data)
            logger.info(f"Data saved to {filename}")
        
        logger.info("Data generation completed!")
        logger.info(f"Total records generated: {len(data):,}")
        
        return True

def main():
    """Main function to run the data population."""
    try:
        generator = StockDataGenerator()
        success = generator.run_population(500000, split_files=True)
        
        if success:
            print("\n" + "="*60)
            print("STOCK PRICES DATA GENERATION COMPLETED")
            print("="*60)
            print("Successfully generated 500,000 data points")
            print("Data includes 10 stocks across 3 time intervals")
            print("Realistic OHLCV data with normal distribution")
            print("Data saved to CSV files for manual upload")
            print("\nNext steps:")
            print("1. Go to BigQuery Console")
            print("2. Navigate to your table")
            print("3. Click 'Create table' > 'Upload'")
            print("4. Upload the CSV files")
            print("5. Or use the 'bq load' command")
        else:
            print("Data generation failed")
            
    except Exception as e:
        logger.error(f"Data generation failed: {e}")
        raise

if __name__ == "__main__":
    main()
