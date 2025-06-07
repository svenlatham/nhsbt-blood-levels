import requests
import re
from bs4 import BeautifulSoup
import pandas
import os
import datetime

def main():
    r = requests.get("https://hospital.blood.co.uk/business-continuity/blood-stocks/")
    #print(r.text)
    soup = BeautifulSoup(r.text, features='html.parser')
    texts = soup.select("div.grid-text")
    texts = [x for x in texts if 'text version' in x.text]
    
    # texts[0] contains blood; texts[1] contains platelets
    # we need to check this in future to be sure!
    blood = texts[0]
    platelets = texts[1]
    now = datetime.datetime.now()
    current_date = now.strftime("%Y-%m-%d")

    def find_group(input, csv_file):
        vals = {}
        lines = input.split("\n")
        for line in lines:
            # We use the word 'day' as a crude measure to find the right line:
            if 'day' in line:
                line = line.replace("\xa0", " ") # This has caused me so many issues...
                matches = re.findall(r'([ABO\+\-]+) ([0-9\.]+)', line)
                print(str(matches))
                for k,v in matches:
                    print("Found %s = %s" % (k, v))
                    vals[k] = v
        vals['date'] = current_date
        row = pandas.DataFrame(vals, index=[0])
        if os.path.exists(csv_file):
            df = pandas.read_csv(csv_file)
            df = pandas.concat([df, row], ignore_index=True)
            # If we already have an entry for this date replace it to avoid
            # duplicated rows which can skew the charts.
            df = df.drop_duplicates(subset=["date"], keep="last")
        else:
            df = row
        df.to_csv(csv_file, index=False)
        return df
        

    print("Searching for blood data")
    df = find_group(blood.text, "blood.csv")
    

    print("Searching for platelet data")
    df = find_group(platelets.text, "platelets.csv")

