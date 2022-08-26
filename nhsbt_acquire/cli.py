import requests
from bs4 import BeautifulSoup

def main():
    r = requests.get("https://hospital.blood.co.uk/business-continuity/blood-stocks/")
    #print(r.text)
    soup = BeautifulSoup(r.text)
    texts = soup.select("div.grid-text")
    for entry in texts:
        print(entry.text)