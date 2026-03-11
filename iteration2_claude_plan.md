# RiskPulse Iteration 2 Execution Checklist

## 1. Requirements Reconciliation & Mapping

### 1.1 Create Requirements Matrix
**File**: `docs/requirements-matrix.md`
```markdown
| Requirement | Status | Implementation | Tests | Notes |
|-------------|--------|----------------|-------|-------|
| R1: Portfolio risk calculation | ✓ | risk_calculator.py | test_risk_calculator.py | Complete |
| R2: Multi-timeframe analysis | ✓ | config.yaml windows | test_timeframes.py | Complete |
| R3: Data validation | ⚠ | basic validation | test_validation.py | Needs boundary cases |
| R4: Error handling | ⚠ | basic try/catch | test_errors.py | Needs edge cases |
| R5: Configurable parameters | ✓ | config.yaml | test_config.py | Complete |
| R6: Output reports | ⚠ | basic JSON/CSV | test_outputs.py | Needs examples |
```

**Acceptance Criteria**: 
- [ ] All 15+ requirements from original prompt mapped
- [ ] Each requirement links to specific file/function
- [ ] Status is Done/Partial/Missing with action plan

## 2. Documentation Completion

### 2.1 Enhanced Setup Guide
**File**: `README.md` (replace sections)
```markdown
## Quick Start (5 minutes)
1. Clone: `git clone <repo>`
2. Install: `pip install -r requirements.txt`
3. Configure: `cp config/config.example.yaml config/config.yaml`
4. Test: `python -m pytest tests/test_integration.py::test_happy_path`
5. Run: `python main.py --portfolio=examples/sample_portfolio.json`

Expected output: `outputs/risk_report_YYYY-MM-DD.json` (~2MB)
```

### 2.2 Architecture Documentation
**File**: `docs/architecture.md` (create new)
```markdown
## Data Flow
Input → Validation → Data Fetch → Risk Calc → Output Generation
- **Input**: Portfolio JSON + Config YAML
- **Validation**: Schema + business rules (fail fast)
- **Data Fetch**: yfinance API with retry/cache
- **Risk Calc**: VaR, volatility, correlation matrix
- **Output**: JSON report + CSV summary + plots

## Module Responsibilities
- `main.py`: CLI entry, orchestration
- `portfolio_loader.py`: Input validation, parsing
- `data_fetcher.py`: Market data retrieval, caching
- `risk_calculator.py`: Core risk calculations
- `report_generator.py`: Output formatting, visualization
```

### 2.3 Configuration Reference
**File**: `docs/configuration.md` (create new)
```markdown
## Required Settings
```yaml
portfolio_file: "portfolio.json"  # Path to portfolio
time_windows: [30, 90, 252]       # Days for analysis
confidence_levels: [0.95, 0.99]   # VaR confidence
```

## Default Behaviors
- Missing data: Skip asset with warning
- API failure: Retry 3x, then fail
- Insufficient history: Use available data if >20 days
```

**Acceptance Criteria**:
- [ ] New engineer can run system in <10 minutes using docs only
- [ ] All config options documented with defaults and valid ranges
- [ ] Failure modes and recovery documented

## 3. Validation Coverage Enhancement

### 3.1 Input Validation Strengthening
**File**: `src/portfolio_loader.py` (add functions)
```python
def validate_portfolio_bounds(portfolio_data):
    """Validate business rules and boundaries"""
    for asset in portfolio_data['assets']:
        # Weight bounds
        if not 0 <= asset['weight'] <= 1:
            raise ValueError(f"Asset weight {asset['weight']} outside [0,1]")
        
        # Symbol format
        if not re.match(r'^[A-Z]{1,5}$', asset['symbol']):
            raise ValueError(f"Invalid symbol format: {asset['symbol']}")
    
    # Total weight validation
    total_weight = sum(asset['weight'] for asset in portfolio_data['assets'])
    if abs(total_weight - 1.0) > 0.01:
        raise ValueError(f"Portfolio weights sum to {total_weight}, expected 1.0")

def validate_config_ranges(config):
    """Validate config parameter ranges"""
    if config['time_windows']:
        if any(w < 5 or w > 1000 for w in config['time_windows']):
            raise ValueError("Time windows must be between 5-1000 days")
    
    if config['confidence_levels']:
        if any(c <= 0 or c >= 1 for c in config['confidence_levels']):
            raise ValueError("Confidence levels must be between 0 and 1")
```

### 3.2 Output Validation
**File**: `src/report_generator.py` (add function)
```python
def validate_output_integrity(report_data):
    """Ensure output data consistency"""
    required_fields = ['portfolio_summary', 'risk_metrics', 'timestamp']
    missing = [f for f in required_fields if f not in report_data]
    if missing:
        raise ValueError(f"Output missing required fields: {missing}")
    
    # Validate numeric ranges
    var_values = report_data['risk_metrics']['var_values']
    if any(v < 0 for v in var_values.values()):
        raise ValueError("VaR values cannot be negative")
```

### 3.3 Enhanced Test Coverage
**File**: `tests/test_validation.py` (add tests)
```python
def test_portfolio_weight_bounds():
    invalid_portfolio = {
        "assets": [{"symbol": "AAPL", "weight": 1.5}]  # Invalid weight
    }
    with pytest.raises(ValueError, match="weight.*outside"):
        validate_portfolio_bounds(invalid_portfolio)

def test_empty_portfolio():
    with pytest.raises(ValueError, match="empty portfolio"):
        validate_portfolio_bounds({"assets": []})

def test_malformed_symbols():
    invalid_portfolio = {
        "assets": [{"symbol": "123INVALID", "weight": 1.0}]
    }
    with pytest.raises(ValueError, match="Invalid symbol format"):
        validate_portfolio_bounds(invalid_portfolio)
```

**Acceptance Criteria**:
- [ ] Invalid inputs fail within 1 second with specific error messages
- [ ] Test coverage >90% for validation functions
- [ ] Boundary values (0, 1, empty, max) explicitly tested

## 4. Edge Case Handling

### 4.1 Edge Case Matrix Implementation
**File**: `src/edge_case_handler.py` (create new)
```python
class EdgeCaseHandler:
    def handle_insufficient_data(self, symbol, available_days, required_days):
        if available_days < 20:
            raise InsufficientDataError(f"{symbol}: only {available_days} days available")
        elif available_days < required_days:
            logger.warning(f"{symbol}: using {available_days} days instead of {required_days}")
            return available_days
        return required_days
    
    def handle_api