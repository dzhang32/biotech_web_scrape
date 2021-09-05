#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Sep  5 20:24:38 2021

@author: david_zhang
"""

import utils
import pandas as pd
import re
import datetime as dt

def main(df_path, rel_results_dir):
    
    results_dir = utils.get_rel_dir(__file__, rel_results_dir)
    
    df = pd.read_csv(df_path)
    df = tidy_name(df)
    df = tidy_location(df)
    df = df.sort_values(by = "name").reset_index(drop = True)
    
    df.to_csv(results_dir + "/" + "biotech_company_info_tidy_" + 
              dt.date.today().strftime("%d_%m_%Y") + 
              ".csv", 
              index = False)
    
    
def tidy_name(df):
    
    name_list = df["name"].tolist()

    df["name"] = [re.sub("^.*/", "", n) for n in name_list]
    
    return df
    
def tidy_location(df):
    
    location_list = df["location"].tolist()

    location_list = [re.sub("^.* ", "", l) for l in location_list]

    location_list = ["UK" if l == "-" else l for l in location_list]

    df["location"] = location_list
    
    return df

if __name__ == "__main__":
    
    main(df_path = "/Users/david_zhang/dz_home/work/data_sci/biotech_web_scrape/results/01a-get_biotech_companies/biotech_company_info_05_09_2021.csv", 
         rel_results_dir = "../results/01b-tidy_biotech_companies")