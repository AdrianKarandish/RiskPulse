# RiskPulse Release Checklist

## Positioning
- Current state: **MVP-ready**
- Production-ready: **Not yet** (depends on external data reliability, richer monitoring, stronger runtime resiliency)

## Go / No-Go Criteria

### MVP Go Criteria
- [x] Inputs support ticker + rolling/custom ranges
- [x] Required metrics implemented
- [x] Return comparison implemented
- [x] Main + price-only CSV outputs generated
- [x] Cumulative + volatility charts generated
- [x] Modular architecture present
- [x] Test suite passing locally
- [x] Documentation includes run instructions and output locations

### Production No-Go Gaps
- [ ] Robust retry/backoff and circuit breaker around upstream data failures
- [ ] Deterministic fallback data-source strategy when Yahoo endpoints fail
- [ ] Runtime telemetry/alerts and structured logging for ops
- [ ] CI pipeline with test + lint + packaging checks
- [ ] Expanded statistical validation against trusted reference datasets

## Current Decision
- **Go for MVP/internal usage**
- **No-Go for production external promises** until Production No-Go Gaps are closed

## Sign-off Template
- Product owner: ________
- Engineering owner: ________
- Date: ________
- Decision: GO (MVP) / NO-GO (Production)
- Notes: ________
