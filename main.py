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