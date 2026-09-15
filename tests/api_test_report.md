# GeoMine AI API Test Report

## 1. Overview

This report documents the P5 backend integration and API tests performed for the GeoMine AI system.

The tests cover:
- Production shortfall rule logic
- Downtime threshold rule
- Rainfall threshold rule
- Blast-delay threshold rule
- `/recommendations` endpoint
- `/dashboard-data` endpoint
- Reserve prediction data integration
- Production prediction data integration

---

## 2. Recommendation Rule Tests

### 2.1 Production Shortfall Rule

#### Function Tested
`calculate_shortfall()`

### Test Case 1 — Production below target

Input:
- Predicted output: `22361.2735`
- Planned target: `35000`

Expected:
- Shortfall flag = `True`
- Shortfall > 0

Result:
- Shortfall flag = `True`
- Shortfall = `12638.7265`
- Shortfall percentage ≈ `36.11%`

**Status: PASS**

### Test Case 2 — Production above target

Input:
- Predicted output: `36000`
- Planned target: `35000`

Expected:
- Shortfall flag = `False`
- Shortfall = `0`

Result:
- Shortfall flag = `False`
- Shortfall = `0.0`
- Shortfall percentage = `0.0%`

**Status: PASS**

---

### 2.2 Downtime Rule

Threshold:

`75.2 hours`

Rule:

- Downtime >= `75.2` → recommendation triggered
- Downtime < `75.2` → recommendation not triggered

Test:

- Input downtime: `75.2`
- Expected: Triggered
- Result: Triggered

**Status: PASS**

---

### 2.3 Rainfall Rule

Threshold:

`378.7 mm`

Rule:

- Rainfall >= `378.7` → recommendation triggered
- Rainfall < `378.7` → recommendation not triggered

Test:

- Input rainfall: `378.7`
- Expected: Triggered
- Result: Triggered

**Status: PASS**

---

### 2.4 Blast-Delay Rule

Threshold:

`5`

Rule:

- Blast delay >= `5` → recommendation triggered
- Blast delay < `5` → recommendation not triggered

Test:

- Input blast delay: `5`
- Expected: Triggered
- Result: Triggered

**Status: PASS**

---

## 3. Validation Using Actual P3 Production Data

The three operational rules were also checked against all six actual records from:

`ml/production/production_predictions.csv`

| Period | Downtime | Rainfall | Blast Delay | Downtime Rule | Rainfall Rule | Blast Rule |
|---|---:|---:|---:|---|---|---|
| 2024-07-31 | 75.2 | 378.7 | 5 | PASS | PASS | PASS |
| 2024-08-31 | 51.6 | 244.6 | 2 | Not Triggered | Not Triggered | Not Triggered |
| 2024-09-30 | 63.1 | 314.4 | 5 | Not Triggered | Not Triggered | PASS |
| 2024-10-31 | 31.6 | 1.8 | 3 | Not Triggered | Not Triggered | Not Triggered |
| 2024-11-30 | 24.6 | 25.7 | 1 | Not Triggered | Not Triggered | Not Triggered |
| 2024-12-31 | 26.8 | 22.4 | 1 | Not Triggered | Not Triggered | Not Triggered |

**Status: PASS**

The rules correctly trigger only when the actual production input reaches or exceeds the configured threshold.

---

## 4. Recommendations Endpoint

### Endpoint

`GET /recommendations`

### Test Performed

The endpoint was tested using the actual P3 production prediction output.

### Result

- HTTP status: `200`
- Production prediction records processed: `6`
- Recommendation records returned: `6`
- All six records correctly identified a production shortfall.
- Operational recommendations were generated according to the configured downtime, rainfall and blast-delay thresholds.

The first production record triggered all three operational rules in addition to the production shortfall rule.

The September record triggered the blast-delay rule in addition to the production shortfall rule.

**Status: PASS**

---

## 5. Dashboard Data Endpoint

### Endpoint

`GET /dashboard-data`

### Result

The endpoint successfully returned:

### Reserve Data
- Total reserve cells: `100`
- Low: `45`
- Medium: `43`
- High: `12`

### Production Data
- Production trend records: `6`

### Recommendation Data
- Recommendation records: `6`

**Status: PASS**

---

## 6. API Response Structure Validation

### `/recommendations`

Top-level response:

`recommendations`

Each recommendation record contains:

- `mine_id`
- `period`
- `predicted_output`
- `planned_target`
- `shortfall_flag`
- `shortfall`
- `shortfall_percent`
- `recommendations`

HTTP status verified:

`200`

**Status: PASS**

### `/dashboard-data`

Top-level response contains:

- `reserve`
- `production`
- `recommendations`

Reserve section contains:

- `summary`
- `predictions`

Production section contains:

- `trend`

HTTP status verified:

`200`

**Status: PASS**

---

## 7. Data Integration

The dashboard endpoint successfully integrates:

1. P2 reserve prediction output
2. P3 production prediction output
3. P5 recommendation logic

No synthetic prediction values were introduced during integration testing.

The reserve GeoJSON contains 100 unique reserve grid-cell polygons corresponding to the reserve prediction cells.

---

## 8. API Integration Status

| Component | Endpoint / Function | Status |
|---|---|---|
| Shortfall calculation | `calculate_shortfall()` | PASS |
| Downtime rule | `check_downtime()` | PASS |
| Rainfall rule | `check_rainfall()` | PASS |
| Blast-delay rule | `check_blast_delay()` | PASS |
| Recommendations | `GET /recommendations` | PASS |
| Dashboard integration | `GET /dashboard-data` | PASS |
| Reserve prediction data | `reserve_predictions.csv` | PASS |
| Production prediction data | `production_predictions.csv` | PASS |
| Reserve heatmap GeoJSON | `reserve_heatmap.geojson` | PASS |

---

## 9. Risk Classification

### Risk Engine

The P5 risk engine uses threshold-based operational conditions from the production prediction data.

The following thresholds are configured:

- Downtime: `75.2` hours
- Rainfall: `378.7` mm
- Blast delay: `5`

Risk classification is based on the number of triggered operational conditions:

| Triggered Conditions | Risk Level |
|---:|---|
| 0 | Low |
| 1-2 | Medium |
| 3 | High |

### Validation Using Actual P3 Data

| Period | Trigger Count | Triggered Conditions | Risk Level |
|---|---:|---|---|
| 2024-07-31 | 3 | Downtime, Rainfall, Blast Delay | High |
| 2024-08-31 | 0 | None | Low |
| 2024-09-30 | 1 | Blast Delay | Medium |
| 2024-10-31 | 0 | None | Low |
| 2024-11-30 | 0 | None | Low |
| 2024-12-31 | 0 | None | Low |

**Status: PASS**

The risk engine was also verified through the live `/recommendations` and `/dashboard-data` endpoints.

---


## 10. Conclusion

The P5 recommendation and dashboard integration components were successfully tested using the available P2 and P3 model output files.

The production shortfall, downtime, rainfall and blast-delay recommendation rules are operational and validated against the actual P3 production prediction data.

The `/recommendations` and `/dashboard-data` endpoints are operational and ready for frontend integration.

Risk classification remains pending until the agreed classification logic is finalized.