# 💱 Currency Converter (Flask API)

A simple **Python + Flask project** that fetches **live currency exchange rates** using the **Frankfurter API**.  
This API allows users to convert between any two supported world currencies in real-time through **HTTP requests**.

---

## 📖 Overview

This project upgrades the original **command-line currency converter** into a **Flask-based REST API**.  
It retrieves **live exchange rates**, handles invalid inputs gracefully, stores **conversion history in a CSV file**, and includes a **timestamp** for each conversion.

---

## 🚀 Features

* Fetches **real-time exchange rates** via Frankfurter API.  
* Provides a **RESTful API** built with Flask.  
* Adds **error handling** for invalid currency codes and connection issues.  
* Automatically adds a **timestamp** when conversion data is retrieved.  
* Stores **conversion history** in a CSV file for record-keeping.  
* Lightweight — requires only `Flask`, `requests`, and `pandas`.

---

## 🧩 Requirements

Make sure you have **Python 3.x** installed.  
Install dependencies using:

```bash
pip install -r requirements.txt
```

**Dependencies:**
- Flask  
- requests  
- pandas  

---

## 📂 Project Structure

```
currency_converter/
│
├── app.py                     # Main Flask API script
├── conversion_history.csv      # Stores conversion logs
├── requirements.txt
└── README.md
```

---

## ⚙️ Setup and Usage

1. Clone or download this repository.
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
3. Run the Flask server:
   ```bash
   python app.py
   ```
4. The API will start on:
   ```
   http://127.0.0.1:5000
   ```

---

## 🔗 API Endpoints

### **1️⃣ Get Live Exchange Rate**
**Endpoint:**
```
GET /api/rate?base=USD&target=INR
```

**Response:**
```json
{
  "base": "USD",
  "target": "INR",
  "rate": 83.12,
  "timestamp": "2025-11-01T10:45:23"
}
```

---

### **2️⃣ Convert Amount**
**Endpoint:**
```
GET /api/convert?base=USD&target=EUR&amount=100
```

**Response:**
```json
{
  "base": "USD",
  "target": "EUR",
  "amount": 100,
  "converted_amount": 92.4,
  "rate": 0.924,
  "timestamp": "2025-11-01T10:47:12"
}
```

---

### **3️⃣ View Conversion History**
**Endpoint:**
```
GET /api/history
```

**Response:**
```json
[
  {
    "base": "USD",
    "target": "INR",
    "amount": 1,
    "converted_amount": 83.12,
    "timestamp": "2025-11-01T10:45:23"
  }
]
```

---

## ⚠️ Error Handling

The API gracefully handles:
- Invalid currency codes  
- Missing parameters  
- API connection issues  

**Example Response:**
```json
{
  "error": "Invalid currency code or API error."
}
```

---

## 🧠 Implementation Notes

* Data fetched via `requests` from Frankfurter API.  
* Each conversion is saved in `conversion_history.csv`.  
* Flask handles routing for `/api/rate`, `/api/convert`, and `/api/history`.  
* Added timestamps for tracking when data was retrieved.  

---

## 🧪 Example Usage (Python)

```python
import requests

response = requests.get("http://127.0.0.1:5000/api/convert?base=USD&target=INR&amount=10")
print(response.json())
```

**Output:**
```
{
  "base": "USD",
  "target": "INR",
  "amount": 10,
  "converted_amount": 831.2,
  "rate": 83.12,
  "timestamp": "2025-11-01T10:45:23"
}
```

---

## 🏁 Future Enhancements

* Add **GUI dashboard** using Tkinter or React.  
* Include **historical rate charts**.  
* Implement **authentication** for API access.  
* Support **multiple currency conversions** in one request.  
