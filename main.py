import requests

def get_live_rate(base, target):
    url = f"https://api.frankfurter.app/latest?from={base}&to={target}"
    data = requests.get(url).json()
    return data['rates'][target]

base = input("Enter base currency ")
target = input("Enter target currency ")
rate = get_live_rate(base, target)
print(f"1 {base} = {rate} {target}")
