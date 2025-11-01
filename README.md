# Currency Converter — Flask API

A lightweight Flask-based **Currency Conversion API** that fetches live exchange rates using the **Frankfurter API**. This README replaces the earlier CLI-focused documentation and documents the current Flask API, its endpoints, setup, and usage examples.

---

## Table of Contents

- [Overview](#overview)
- [Features](#features)
- [Requirements](#requirements)
- [Installation & Setup](#installation--setup)
- [Configuration](#configuration)
- [Running the API](#running-the-api)
- [API Endpoints](#api-endpoints)
- [Examples (curl & Python)](#examples-curl--python)
- [Error handling](#error-handling)
- [Testing](#testing)
- [Deployment notes (optional)](#deployment-notes-optional)
- [Future enhancements](#future-enhancements)

---

## Overview

This project provides a RESTful API to fetch **live** and **historical** currency exchange rates and to perform conversions. The API acts as a thin wrapper around the Frankfurter API (https://www.frankfurter.app/) and adds a few convenience endpoints and consistent JSON responses.

## Features

- `GET` live exchange rates (single pair or multiple targets)
- `GET` convert an amount between currencies
- `GET` supported currencies list
- `GET` historical rates for a date or range
- Simple, consistent JSON responses and HTTP status codes
- Basic error handling for invalid input & upstream API failures

## Requirements

- Python 3.8+
- `pip`

Python dependencies are in `requirements.txt`. The key dependencies are:

- Flask
- requests
- python-dotenv (optional — recommended for managing environment variables)

Example `requirements.txt` (project ships with this file):

```
Flask>=2.0
requests>=2.25
python-dotenv>=0.15
```

> If your project uses a virtual environment, activate it first (`python -m venv .venv && source .venv/bin/activate` on UNIX-like systems).

## Installation & Setup

1. Clone the repository:

```bash
git clone <your-repo-url>
cd currency_converter
```

2. Create and activate a virtual environment (recommended):

```bash
python -m venv .venv
# macOS / Linux
source .venv/bin/activate
# Windows (PowerShell)
.\.venv\Scripts\Activate.ps1
```

3. Install dependencies:

```bash
pip install -r requirements.txt
```

4. (Optional) Create a `.env` file in the project root to set environment variables used by the app (see [Configuration](#configuration)).

## Configuration

The application reads configuration from environment variables. The following are available:

- `FLASK_ENV` — standard Flask environment (`development` / `production`). Optional.
- `FRANKFURTER_BASE_URL` — (optional) override the default Frankfurter API base URL (default: `https://api.frankfurter.app`). Useful for testing/mirroring.
- `HOST` — host to bind to (default: `127.0.0.1`).
- `PORT` — port to bind to (default: `5000`).

Example `.env` file:

```
FLASK_ENV=development
FRANKFURTER_BASE_URL=https://api.frankfurter.app
HOST=0.0.0.0
PORT=5000
```

> The code uses sensible defaults if env vars are not provided.

## Running the API

There are two common ways to run the app during development:

### 1) Using Flask built-in server (development):

```bash
export FLASK_APP=app.py         # or the entrypoint module used in your repo
export FLASK_ENV=development
flask run --host=0.0.0.0 --port=5000
```

Or using `python` directly if `app.py` contains the `if __name__ == '__main__'` runner:

```bash
python app.py
```

### 2) Production (suggested):

Use a WSGI server like `gunicorn`:

```bash
pip install gunicorn
gunicorn -w 4 -b 0.0.0.0:8000 app:app
```

(Replace `app:app` with the proper module and Flask `app` variable if different.)

## API Endpoints

All endpoints return JSON and use the following content type: `application/json`.

Base path: `/api` (adjust if your implementation uses a different base path).

### `GET /api/supported`

Returns a list of supported currency codes and their full names (if available).

**Query parameters:** none

**Response (200)**

```json
{
  "success": true,
  "supported": ["USD", "EUR", "INR", "GBP", "JPY", ...]
}
```

### `GET /api/rate`

Fetches the latest exchange rate for a currency pair.

**Query parameters (required):**

- `from` — base currency (ISO code, e.g. `USD`)
- `to` — target currency (ISO code, e.g. `INR`)

**Example:** `/api/rate?from=USD&to=INR`

**Response (200)**

```json
{
  "success": true,
  "base": "USD",
  "target": "INR",
  "rate": 83.12,
  "date": "2025-11-01"
}
```

If multiple `to` currencies are supported in your implementation, a comma-separated list is accepted: `to=INR,EUR`

### `GET /api/convert`

Converts an amount from a base to a target currency using the latest rate.

**Query parameters:**

- `from` — base currency (required)
- `to` — target currency (required)
- `amount` — numeric amount to convert (optional, defaults to `1`)

**Example:** `/api/convert?from=EUR&to=USD&amount=50`

**Response (200)**

```json
{
  "success": true,
  "base": "EUR",
  "target": "USD",
  "amount": 50,
  "rate": 1.08,
  "converted": 54.0,
  "date": "2025-11-01"
}
```

### `GET /api/historical`

Fetch historical exchange rates. Your implementation may support either a single `date` or a `start`/`end` range.

**Query parameters (one of the following):**

- `date` — `YYYY-MM-DD` (returns rate on that date)
- `start` and `end` — date range `YYYY-MM-DD` (returns timeseries)
- `from` — base currency (required)
- `to` — target currency (required)

**Examples:**

- `/api/historical?from=USD&to=EUR&date=2025-01-01`
- `/api/historical?from=GBP&to=JPY&start=2025-09-01&end=2025-09-07`

**Response (200)** (single-date example):

```json
{
  "success": true,
  "base": "USD",
  "target": "EUR",
  "date": "2025-01-01",
  "rate": 0.92
}
```

**Response (200)** (range example):

```json
{
  "success": true,
  "base": "GBP",
  "target": "JPY",
  "rates": {
    "2025-09-01": 191.5,
    "2025-09-02": 190.9,
    "2025-09-03": 192.3
  }
}
```

### Error responses

The API returns consistent error shapes. Examples:

**400 Bad Request** (missing/invalid parameters):

```json
{
  "success": false,
  "error": "Missing required query parameter: from"
}
```

**502 Upstream error** (Frankfurter failure):

```json
{
  "success": false,
  "error": "Failed to fetch data from Frankfurter API"
}
```

**404 Not found** (unsupported currency):

```json
{
  "success": false,
  "error": "Unsupported currency code: XYZ"
}
```

## Examples (curl & Python)

### curl — get latest rate

```bash
curl "http://127.0.0.1:5000/api/rate?from=USD&to=INR"
```

### curl — convert amount

```bash
curl "http://127.0.0.1:5000/api/convert?from=EUR&to=USD&amount=100"
```

### Python (requests)

```python
import requests

resp = requests.get('http://127.0.0.1:5000/api/convert', params={'from':'EUR','to':'USD','amount':100})
print(resp.json())
```

## Error handling

- The API validates required query parameters and returns `400` for missing or invalid values.
- When the Frankfurter API is unavailable, the service returns a `502` with a helpful message.
- If your app includes caching layers, document them here (e.g., use a short TTL to avoid stale rates).

## Testing

If unit tests are included in the repo, run them with `pytest` (install in `requirements-dev.txt` or similar):

```bash
pip install pytest
pytest
```

Add endpoints tests for: supported list, rate, convert, historical, and error conditions.

## Deployment notes (optional)

- For production use, run behind a WSGI server (gunicorn) and a reverse proxy (NGINX).
- Consider HTTPS termination at the proxy.
- Add caching (Redis) if you expect high traffic.

## Future enhancements

- Add request rate-limiting and API key support.
- Add simple Swagger / OpenAPI docs (e.g., `flasgger` or `apispec`).
- Add response caching and a TTL setting.
- Add integration tests that mock the Frankfurter API.

---

## Contact / Contributing

If you have changes or spot inaccuracies in this README, open a PR or an issue in the repository. Include a brief summary of your change and any required code updates.

---

*End of README — updated to reflect the Flask API implementation.*
