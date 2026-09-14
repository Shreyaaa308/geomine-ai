# GeoMine AI Backend API

## Base URL

Local development:

http://127.0.0.1:8000

---

## Health Check

### GET /health

Checks whether the backend is running.

### Response

```json
{
  "status": "healthy",
  "service": "GeoMine AI Backend"
}
---

## Common Status Codes

| Code | Meaning |
|---|---|
| 200 | Request successful |
| 422 | Invalid or missing input |
| 500 | Internal server error |

---

## Interactive API Documentation

FastAPI automatically provides interactive Swagger documentation at:

http://127.0.0.1:8000/docs

## POST /predict-production

Predicts the expected manganese production output based on operational and environmental inputs.

### Request

```json
{
  "downtime": 38.5,
  "rainfall": -0.4,
  "blast_delay": 3,
  "previous_period_output": 28584.4,
  "month": 1
}