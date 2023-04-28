import requests
import re
from bs4 import BeautifulSoup
import pandas
import os

def main():
    r = requests.get("https://hospital.blood.co.uk/business-continuity/blood-stocks/")
    #print(r.text)
    soup = BeautifulSoup(r.text, features='html.parser')
    texts = soup.select("div.grid-text")
    texts = [x for x in texts if 'Text version for accessibility' in x.text]
    print(repr(texts))
    
    # texts[0] contains blood; texts[1] contains platelets
    # we need to check this in future to be sure!
    blood = texts[0]
    platelets = texts[1]
    
    matches = re.findall('([OAB\+\-]+) ([0-9\.]+)', blood.text, re.DOTALL)
    vals = []
    cols = []
    for k,v in matches:
        cols.append(k)
        vals.append(v)

    df = pandas.DataFrame([vals], columns=cols)
    df.to_csv("blood.csv",mode='a', header=not os.path.exists('blood.csv'))

    matches = re.findall('([OAB\+\-]+) ([0-9\.]+)', platelets.text, re.DOTALL)
    vals = []
    cols = []
    for k,v in matches:
        cols.append(k)
        vals.append(v)

    df = pandas.DataFrame([vals], columns=cols)
    df.to_csv("platelets.csv",mode='a', header=not os.path.exists('platelets.csv'))

