import requests

def main():
    r = requests.get("https://hospital.blood.co.uk/business-continuity/blood-stocks/")
    print(r.text)