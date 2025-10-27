# Currency Converter

---

# 💱 Currency Converter

A simple Python project that fetches **live currency exchange rates** using the **Frankfurter API**.
This tool allows users to convert between any two supported world currencies in real-time.

---

## 📖 Overview

This project is a **command-line based currency converter** built with Python.
It uses the [Frankfurter API](https://www.frankfurter.app/) to retrieve **live exchange rates**, ensuring accurate and up-to-date results.

---

## 🚀 Features

* Fetches **real-time exchange rates**.
* Simple **command-line interface (CLI)** for user input.
* Handles **errors gracefully** (invalid inputs or connection issues).
* Lightweight — requires only the `requests` library.

---

## 🧩 Requirements

Make sure you have **Python 3.x** installed.
You’ll also need to install the **requests** module if not already available.

```bash
pip install requests
```

---

## 📂 Project Structure

```
currency_converter/
│
├── currency_converter.py     # Main Python script
└── README.md                 # Project documentation
```

---

## 💻 Usage

1. Clone or download this repository.
2. Open a terminal in the project directory.
3. Run the script using:

```bash
python currency_converter.py
```

4. Enter your desired currencies when prompted:

```
Enter base currency: USD
Enter target currency: INR
```

5. Output example:

```
1 USD = 83.12 INR
```

---

## ⚙️ Code Explanation

```python
import requests

def get_live_rate(base, target):
    try:
        url = f"https://api.frankfurter.app/latest?from={base}&to={target}"
        data = requests.get(url).json()
        return data['rates'][target]
    except Exception:
        print("Something went wrong. Please check your input or internet connection.")
        return None

base = input("Enter base currency: ").upper()
target = input("Enter target currency: ").upper()

rate = get_live_rate(base, target)
if rate:
    print(f"1 {base} = {rate} {target}")
```

### 🧠 Explanation:

* **requests.get(url).json()** — Fetches real-time currency data.
* **Exception handling** — Ensures smooth user experience even if the network fails.
* **Dynamic user input** — Accepts any valid currency code (e.g., USD, EUR, INR).

---

## 🧪 Demonstration

### Example 1

**Input:**

```
Enter base currency: EUR
Enter target currency: USD
```

**Output:**

```
1 EUR = 1.08 USD
```

### Example 2

**Input:**

```
Enter base currency: GBP
Enter target currency: JPY
```

**Output:**

```
1 GBP = 191.53 JPY
```

---

## ⚠️ Error Handling Example

If the user enters an invalid currency code:

**Input:**

```
Enter base currency: XYZ
Enter target currency: INR
```

**Output:**

```
Something went wrong. Please check your input or internet connection.
```

---

## 🌍 API Information

The project uses the **Frankfurter API**, which provides **free and reliable foreign exchange rate data**:

* API Endpoint: `https://api.frankfurter.app/latest`
* Example Request:

  ```
  https://api.frankfurter.app/latest?from=USD&to=INR
  ```


## 🏁 Future Enhancements

* Add currency **conversion amount feature**.
* Integrate a **GUI** using Tkinter or PyQt.
* Add **historical exchange rate** comparison.
* Implement **multi-currency conversion** support.

---

