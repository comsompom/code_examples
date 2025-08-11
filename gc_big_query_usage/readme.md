# BigQuery Stock Prices Table

A comprehensive solution for creating, populating, and analyzing BigQuery tables designed for storing stock prices time-series data with optimized partitioning and clustering for financial analysis.

## Features

- **OHLCV data structure** (Open, High, Low, Close, Volume) for stock prices
- **Time-series optimized table design** with partitioning by date
- **Clustering** for improved query performance on stock symbols and exchanges
- **Comprehensive schema** supporting various financial data sources
- **Synthetic data generation** for testing and development with realistic market patterns
- **Advanced anomaly detection** using multiple statistical methods
- **Robust error handling** and data validation
- **BigQuery best practices** implementation
- **Clean, professional code** without emojis
- **Ready for immediate use** with stock data from any OHLCV source

## Table Schema

| Field | Type | Mode | Description |
|-------|------|------|-------------|
| `timestamp` | TIMESTAMP | REQUIRED | Timestamp of the price data |
| `symbol` | STRING | REQUIRED | Stock symbol/ticker (e.g., AAPL, GOOGL) |
| `exchange` | STRING | REQUIRED | Stock exchange (e.g., NASDAQ, NYSE) |
| `open` | FLOAT64 | REQUIRED | Opening price |
| `high` | FLOAT64 | REQUIRED | Highest price during the period |
| `low` | FLOAT64 | REQUIRED | Lowest price during the period |
| `close` | FLOAT64 | REQUIRED | Closing price |
| `volume` | INT64 | REQUIRED | Trading volume |
| `adjusted_close` | FLOAT64 | NULLABLE | Adjusted closing price (for splits/dividends) |
| `dividend_amount` | FLOAT64 | NULLABLE | Dividend amount if any |
| `split_coefficient` | FLOAT64 | NULLABLE | Split coefficient if any |
| `currency` | STRING | NULLABLE | Currency of the prices (e.g., USD, EUR) |
| `data_source` | STRING | NULLABLE | Source of the data (e.g., Yahoo Finance, Alpha Vantage) |
| `interval` | STRING | REQUIRED | Time interval (1m, 5m, 15m, 1h, 1d, 1wk, 1mo) |
| `created_at` | TIMESTAMP | REQUIRED | Timestamp when the record was created |
| `updated_at` | TIMESTAMP | REQUIRED | Timestamp when the record was last updated |

## Performance Optimizations

- **Partitioning**: Daily partitioning on the `timestamp` field
- **Clustering**: Clustered by `symbol`, `exchange`, and `interval`
- **Data expiration**: 60-day retention policy for partitions (sandbox mode)

## Prerequisites

1. **Google Cloud Project** with BigQuery enabled
2. **Authentication** set up (Application Default Credentials or service account)
3. **Python dependencies** installed

## Installation

1. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

2. **Authentication Setup**:
   ```bash
   # Set up Google Cloud authentication
   gcloud auth application-default login
   
   # Or use service account (optional)
   export GOOGLE_APPLICATION_CREDENTIALS="path/to/service-account-key.json"
   ```

3. **Environment Variables** (automatically set by scripts):
   - `GOOGLE_CLOUD_PROJECT`: Your Google Cloud project ID
   - `BIGQUERY_DATASET_ID`: BigQuery dataset ID (default: "stock_prices_data")

## Usage

### 1. Create the BigQuery Table

Run the script to create the BigQuery table:

```bash
python create_bigquery_timeseries_table.py
```

This will:
- Create a dataset named `stock_prices_data`
- Create a table named `stock_prices` with the optimized schema
- Set up partitioning and clustering for performance

### 2. Generate Synthetic Data

Generate synthetic stock prices data for testing:

```bash
python populate_stock_data.py
```

This will:
- Generate 500,000 realistic stock price data points using geometric Brownian motion
- Create CSV files for manual upload to BigQuery
- Include 10 stocks across 3 time intervals (1d, 1h, 15m)
- Apply market hours logic for intraday data
- Ensure OHLC relationship validation
- Clean and validate data before saving

### 3. Upload Data to BigQuery

Upload the generated data directly to BigQuery:

```bash
python upload_csv_to_bigquery.py
```

This will:
- Upload free tier records available
- Apply realistic price movements with mean reversion
- Upload data directly to BigQuery using load_table_from_dataframe
- Validate data before upload
- Verify the upload was successful

### 4. Detect Anomalies

Identify outliers and anomalies in the stock price data:

```bash
python anomaly_detection.py
```

This will:
- Fetch data from BigQuery for the last 30 days using parameterized queries
- Apply multiple anomaly detection methods:
  - Z-score method (beyond 3 standard deviations with proper statistical validation)
  - IQR method (Interquartile Range with robust outlier detection)
  - Extreme price changes (>10% for market event detection)
  - OHLC relationship violations (data quality checks)
  - Volume anomalies (extreme trading volume detection)
- Calculate price changes, returns, and moving averages
- Generate a comprehensive anomaly report with detailed analysis
- Save anomalies to a CSV file for further analysis

## Example Queries

### Get Latest Stock Prices
```sql
SELECT 
    symbol,
    exchange,
    close,
    volume,
    timestamp,
    currency
FROM `your-project.stock_prices_data.stock_prices`
WHERE timestamp = (
    SELECT MAX(timestamp) 
    FROM `your-project.stock_prices_data.stock_prices` t2 
    WHERE t2.symbol = `your-project.stock_prices_data.stock_prices`.symbol 
    AND t2.exchange = `your-project.stock_prices_data.stock_prices`.exchange
    AND t2.interval = `your-project.stock_prices_data.stock_prices`.interval
)
ORDER BY symbol
```

### Daily Price Summary
```sql
SELECT 
    symbol,
    exchange,
    DATE(timestamp) as date,
    MIN(open) as open_price,
    MAX(high) as day_high,
    MIN(low) as day_low,
    MAX(close) as close_price,
    SUM(volume) as total_volume,
    AVG(close) as avg_price,
    STDDEV(close) as price_volatility
FROM `your-project.stock_prices_data.stock_prices`
WHERE interval = '1d'
  AND symbol = 'AAPL'
  AND DATE(timestamp) >= DATE_SUB(CURRENT_DATE(), INTERVAL 30 DAY)
GROUP BY symbol, exchange, date
ORDER BY date DESC
```

### Price Changes Analysis
```sql
SELECT 
    symbol,
    timestamp,
    close,
    LAG(close) OVER (PARTITION BY symbol, exchange, interval ORDER BY timestamp) as prev_close,
    (close - LAG(close) OVER (PARTITION BY symbol, exchange, interval ORDER BY timestamp)) / 
    LAG(close) OVER (PARTITION BY symbol, exchange, interval ORDER BY timestamp) * 100 as price_change_pct,
    volume
FROM `your-project.stock_prices_data.stock_prices`
WHERE symbol = 'AAPL'
  AND interval = '1d'
  AND DATE(timestamp) >= DATE_SUB(CURRENT_DATE(), INTERVAL 30 DAY)
ORDER BY timestamp DESC
```

### Stock Performance Summary
```sql
SELECT 
    symbol,
    exchange,
    interval,
    COUNT(*) as total_records,
    MIN(close) as min_price,
    MAX(close) as max_price,
    AVG(close) as avg_price,
    STDDEV(close) as price_volatility,
    SUM(volume) as total_volume,
    AVG(volume) as avg_volume
FROM `your-project.stock_prices_data.stock_prices`
WHERE interval = '1d'
GROUP BY symbol, exchange, interval
ORDER BY total_volume DESC
```

### Moving Averages
```sql
SELECT 
    symbol,
    timestamp,
    close,
    AVG(close) OVER (
        PARTITION BY symbol 
        ORDER BY timestamp 
        ROWS BETWEEN 19 PRECEDING AND CURRENT ROW
    ) as ma_20,
    AVG(close) OVER (
        PARTITION BY symbol 
        ORDER BY timestamp 
        ROWS BETWEEN 49 PRECEDING AND CURRENT ROW
    ) as ma_50
FROM `your-project.stock_prices_data.stock_prices`
WHERE symbol = 'AAPL'
  AND interval = '1d'
  AND timestamp >= TIMESTAMP_SUB(CURRENT_TIMESTAMP(), INTERVAL 60 DAY)
ORDER BY timestamp DESC
```

## Anomaly Detection Methods

The anomaly detection script uses multiple statistical methods to identify outliers with mathematical soundness:

### 1. Z-Score Method
- Calculates z-scores for price, volume, and returns
- Flags data points beyond ±3 standard deviations from the mean (99.7% confidence)
- Handles division by zero and validates minimum data points
- Effective for normally distributed data

### 2. IQR Method (Interquartile Range)
- Uses Q1, Q3, and IQR to define outlier bounds
- More robust to non-normal distributions
- Bounds: [Q1 - 1.5×IQR, Q3 + 1.5×IQR]
- Validates IQR > 0 to avoid division by zero

### 3. Extreme Price Changes
- Identifies price changes exceeding 10% in a single period
- Useful for detecting market events and data errors
- Calculates percentage changes with proper validation

### 4. OHLC Relationship Violations
- Checks for logical inconsistencies in OHLC data
- Ensures: High ≥ Open, Close and Low ≤ Open, Close
- Detects data quality issues and invalid price relationships
- Validates positive prices and volumes

### 5. Volume Anomalies
- Identifies unusually high or low trading volumes
- Uses z-score method with threshold of ±5 standard deviations
- Requires minimum data points for statistical validity

## Working with the Table

### Using BigQuery Console
1. Go to [BigQuery Console](https://console.cloud.google.com/bigquery)
2. Navigate to your project and dataset
3. Click on the `stock_prices` table
4. Use the "Query" tab to run SQL queries
5. Create views and scheduled queries as needed

### Using Python
```python
from google.cloud import bigquery

client = bigquery.Client(project='your-project-id')

# Insert data with proper validation
table_ref = 'your-project.stock_prices_data.stock_prices'
rows_to_insert = [
    {
        'timestamp': '2024-01-15 16:00:00',
        'symbol': 'AAPL',
        'exchange': 'NASDAQ',
        'open': 150.00,
        'high': 152.50,
        'low': 149.75,
        'close': 151.25,
        'volume': 1000000,
        'interval': '1d',
        'created_at': '2024-01-15 16:00:00',
        'updated_at': '2024-01-15 16:00:00'
    }
]

# Note: Streaming inserts are not available in BigQuery free tier
# Use load_table_from_dataframe for batch uploads
```

### Best Practices
- Use `load_table_from_dataframe` for batch uploads (free tier compatible)
- Implement proper error handling and validation
- Use parameterized queries to prevent SQL injection
- Validate OHLC relationships before upload
- Handle BigQuery free tier limitations appropriately

## Customization

To customize the table schema, edit the `define_table_schema()` method in the script:

```python
def define_table_schema(self):
    schema = [
        bigquery.SchemaField("timestamp", "TIMESTAMP", mode="REQUIRED"),
        bigquery.SchemaField("symbol", "STRING", mode="REQUIRED"),
        # Add your custom fields here
        bigquery.SchemaField("market_cap", "FLOAT64", mode="NULLABLE"),
        bigquery.SchemaField("pe_ratio", "FLOAT64", mode="NULLABLE"),
        # ... more fields
    ]
    return schema
```

## Data Sources

This table is designed to work with various stock data sources:

- **Yahoo Finance**: Historical OHLCV data
- **Alpha Vantage**: Real-time and historical data
- **IEX Cloud**: Financial data API
- **Polygon.io**: Market data
- **Custom data feeds**: Any OHLCV format data

## Recent Improvements

### Code Quality Enhancements
- **Enhanced mathematical soundness** with proper division by zero handling
- **Improved statistical validation** with minimum data point requirements
- **Added comprehensive error handling** throughout all scripts
- **Implemented BigQuery best practices** including parameterized queries

### Data Generation Improvements
- **Realistic market patterns** using geometric Brownian motion
- **Market hours logic** for intraday data volume adjustment
- **Mean reversion effects** for more realistic price movements
- **OHLC relationship validation** to ensure data quality
- **Robust data cleaning** with proper CSV formatting

### Anomaly Detection Enhancements
- **Multiple detection methods** with statistical rigor
- **Proper handling of edge cases** (zero values, insufficient data)
- **Comprehensive reporting** with detailed analysis
- **Parameterized BigQuery queries** for security
- **Statistical validation** for all calculations

## Authentication

Ensure you have proper Google Cloud authentication set up:

- **Application Default Credentials**: `gcloud auth application-default login`
- **Service Account**: Set `GOOGLE_APPLICATION_CREDENTIALS` environment variable
- **User Account**: `gcloud auth login`

## Troubleshooting

### Common Issues

1. **Authentication Errors**:
   - Ensure `gcloud auth application-default login` is completed
   - Check that your project ID is correct
   - Verify BigQuery API is enabled

2. **BigQuery Free Tier Limitations**:
   - Streaming inserts are not available (use `load_table_from_dataframe`)
   - Partition expiration is limited to 60 days
   - Maximum 10,000 partitions per table

3. **Data Quality Issues**:
   - Run anomaly detection to identify data problems
   - Use the data cleaning functions in the scripts
   - Validate OHLC relationships before upload

4. **Performance Issues**:
   - Ensure proper partitioning and clustering are set up
   - Use appropriate time ranges in queries
   - Consider data expiration policies

## License

This project is provided as-is for educational and demonstration purposes.
