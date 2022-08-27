import requests
import re
from bs4 import BeautifulSoup
import pandas
import json

def main():
    r = requests.get("https://hospital.blood.co.uk/business-continuity/blood-stocks/")
    #print(r.text)
    soup = BeautifulSoup(r.text)
    texts = soup.select("div.grid-text")
    texts = [x for x in texts if 'Text version for accessibility' in x.text]
    debug = json.dumps(texts)
    print(debug)
    
    # texts[0] contains blood; texts[1] contains platelets
    # we need to check this in future to be sure!
    blood = texts[0]
    platelets = texts[1]
    
    for entry in blood:
        matches = re.findall('([OAB\+\-]+) ([0-9\.]+)', entry.text, re.DOTALL)
        df = pandas.DataFrame.from_items(matches)
        df.to_csv("blood.csv",mode='a', header=not os.path.exists('blood.csv'))
    
    for entry in platelets:
        matches = re.findall('([OAB\+\-]+) ([0-9\.]+)', entry.text, re.DOTALL)
        df = pandas.DataFrame.from_items(matches)
        df.to_csv("platelets.csv",mode='a', header=not os.path.exists('platelets.csv'))

