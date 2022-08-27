import requests
import re
from bs4 import BeautifulSoup

def main():
    r = requests.get("https://hospital.blood.co.uk/business-continuity/blood-stocks/")
    #print(r.text)
    soup = BeautifulSoup(r.text)
    texts = soup.select("div.grid-text")
    texts = [x for x in texts if 'Text version for accessibility' in x.text]
    f = open("nhsbt.txt","a")
    for entry in texts:
        matches = re.findall('([OAB\+\-]+) ([0-9\.]+)', entry.text, re.DOTALL)
        for match in matches:
            # Presented as a tuple, so we can split that right up
            str = ("%s,%s " % (match[0], match[1]))
            f.write(str)
    f.close()