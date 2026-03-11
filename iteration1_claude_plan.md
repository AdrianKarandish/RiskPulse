# RiskPulse - Implementation-Ready Plan

## Final File Tree
```
riskpulse/
├── pyproject.toml
├── requirements.txt
├── README.md
├── src/
│   └── riskpulse/
│       ├── __init__.py
│       ├── main.py
│       ├── cli/
│       │   ├── __init__.py
│       │   ├── parser.py
│       │   └── validators.py
│       ├── domain/
│       │   ├── __init__.py
│       │   └── models.py
│       ├── data/
│       │   ├── __init__.py
│       │   ├── market_data.py
│       │   ├── fundamentals.py
│       │   └── preprocess.py
│       ├── analytics/
│       │   ├── __init__.py
│       │   ├── returns.py
│       │   ├── risk_metrics.py
│       │   ├── beta.py
│       │   ├── fundamentals.py
│       │   └── summary.py
│       ├── reporting/
│       │   ├── __init__.py
│       │   ├── csv_exporter.py
│       │   ├── charts.py
│       │   └── filenames.py
│       ├── services/
│       │   ├── __init__.py
│       │   └── analysis_service.py
│       └── utils/
│           ├── __init__.py
│           ├── dates.py
│           ├── logging.py
│           └── math_utils.py
├── tests/
│   ├── __init__.py
│   ├── conftest.py
│   ├── fixtures/
│   │   ├── __init__.py
│   │   └── sample_data.py
│   ├── unit/
│   │   ├── __init__.py
│   │   ├── test_cli.py
│   │   ├── test_data.py
│   │   ├── test_analytics.py
│   │   ├── test_reporting.py
│   │   └── test_utils.py
│   └── integration/
│       ├── __init__.py
│       └── test_full_pipeline.py
└── outputs/
```

## Module Responsibilities

### CLI Layer (`cli/`)
- **parser.py**: Argument parsing, help text, command structure
- **validators.py**: Input validation (ticker format, date ranges, rolling window bounds)

### Domain Layer (`domain/`)
- **models.py**: Data classes for AnalysisRequest, MarketData, RiskMetrics, AnalysisResult

### Data Layer (`data/`)
- **market_data.py**: yfinance fetching, caching, error handling
- **fundamentals.py**: Financial statement data extraction for Piotroski
- **preprocess.py**: Data alignment, missing value handling, return calculations

### Analytics Layer (`analytics/`)
- **returns.py**: Period returns, cumulative returns, benchmark comparison
- **risk_metrics.py**: VaR, CVaR, volatility, max drawdown, Sortino ratio
- **beta.py**: Beta and downside beta calculations
- **fundamentals.py**: Piotroski F-score implementation
- **summary.py**: Aggregate all metrics into final result

### Reporting Layer (`reporting/`)
- **csv_exporter.py**: CSV generation with defined schemas
- **charts.py**: Matplotlib chart generation
- **filenames.py**: Consistent output file naming

### Services Layer (`services/`)
- **analysis_service.py**: Main orchestration, error aggregation, workflow coordination

### Utils Layer (`utils/`)
- **dates.py**: Date parsing, business day calculations, period extensions
- **logging.py**: Structured logging setup
- **math_utils.py**: Statistical helper functions

## Exact Build Steps with Acceptance Criteria

### Step 1: Project Scaffold
**Duration**: 30 minutes
```bash
# Create project structure
mkdir -p riskpulse/src/riskpulse/{cli,domain,data,analytics,reporting,services,utils}
mkdir -p riskpulse/tests/{unit,integration,fixtures}
mkdir -p riskpulse/outputs
touch riskpulse/src/riskpulse/**/__init__.py
touch riskpulse/tests/**/__init__.py
```

**Files to create**:
- `pyproject.toml` - Python packaging configuration
- `requirements.txt` - Dependencies
- `README.md` - Usage instructions

**Acceptance Criteria**:
- [ ] `pip install -e .` succeeds
- [ ] `python -m riskpulse --help` shows help text
- [ ] All directories created with proper `__init__.py` files

### Step 2: CLI Foundation
**Duration**: 45 minutes

**`cli/parser.py`**:
- Argument groups: ticker (required), period (rolling OR start/end dates)
- Output directory option
- Verbosity levels

**`cli/validators.py`**:
- Ticker format validation (1-5 chars, alphanumeric + dots/dashes)
- Date format validation (YYYY-MM-DD)
- Rolling window bounds (5-252 business days)
- Start date < end date validation

**Acceptance Criteria**:
- [ ] Valid inputs parse correctly
- [ ] Invalid tickers rejected with clear error
- [ ] Date validation prevents future dates
- [ ] Cannot specify both rolling and custom dates
- [ ] Help text is comprehensive

### Step 3: Date Utilities
**Duration**: 30 minutes

**`utils/dates.py`**:
```python
def parse_period_input(rolling_days: int = None, start_date: str = None, end_date: str = None) -> PeriodSpec
def calculate_extended_lookback(selected_period: PeriodSpec, metric_requirements: dict) -> datetime
def align_to_business_days(date: datetime) -> datetime
```

**Acceptance Criteria**:
- [ ] Rolling window correctly calculates business days
- [ ] Custom date ranges validated and parsed
- [ ] Extended lookback adds minimum 252 days for 1Y metrics
- [ ] Weekend dates adjusted to previous business day

### Step 4: Domain Models
**Duration**: 30 minutes

**`domain/models.py`**:
```python
@dataclass
class AnalysisRequest:
    ticker: str
    selected_period: PeriodSpec
    extended_period: PeriodSpec
    output_dir: Path

@dataclass
class MarketData:
    stock_prices: pd.Series
    benchmark_prices: pd.Series
    stock_returns: pd.Series
    benchmark_returns: pd.Series
    fundamentals: dict

@dataclass
class RiskMetrics:
    max_drawdown_1y: float
    worst_day_return: float
    worst_5day_return: float
    var_95_parametric: float
    var_95_historical: float
    cvar_95: float
    annualized_volatility: float
    sortino_ratio: float
    beta: float
    downside_beta: float

@dataclass
class AnalysisResult:
    request: AnalysisRequest
    market_data: MarketData
    risk_metrics: RiskMetrics
    period_returns: dict
    piotroski_score: float
    warnings: List[str]
```

**Acceptance Criteria**:
- [ ] All models have proper type hints
- [ ] Models serialize/deserialize correctly
- [ ] Optional fields handle None values properly

### Step 5: Market Data Fetcher
**Duration**: 60 minutes

**`data/market_data.py`**:
```python
class MarketDataFetcher:
    def fetch_stock_data(self, ticker: str, start: datetime, end: datetime) -> pd.DataFrame
    def fetch_benchmark_data(self, start: datetime, end: datetime) -> pd.DataFrame
    def validate_data_sufficiency(self, data: pd.DataFrame, min_points: int) -> bool
```

**Acceptance Criteria**:
- [ ] Fetches OHLCV data with proper error handling
- [ ] Handles yfinance API failures gracefully
- [ ] Returns standardized DataFrame format
- [ ] Validates minimum data points available
- [ ] Caches data within session to avoid repeated API calls

### Step 6: Data Preprocessing
**Duration**: 45 minutes

**`data/preprocess.py`**:
```python
def align_price_series(stock_df: pd.DataFrame, benchmark_df: pd.DataFrame) -> Tuple[pd.Series, pd.Series]
def calculate_returns(prices: pd.Series, method: str = 'simple') -> pd.Series
def handle_missing_data(data: pd.Series, max_gap_days: int = 5) -> pd.Series
```

**Acceptance Criteria**:
- [ ] Stock