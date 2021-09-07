#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Sep  5 15:38:15 2021

@author: david_zhang
"""

import utils
from urllib.request import urlopen
from bs4 import BeautifulSoup
import pandas as pd
import datetime as dt

def main(url, rel_results_dir):
    
    results_dir = utils.get_rel_dir(__file__, rel_results_dir)
    
    soup = soup_url(url)
    
    company_info = get_company_info(soup)
    
    company_info.to_csv(results_dir + "/" + "biotech_company_info_" + 
                        dt.date.today().strftime("%d_%m_%Y") + 
                        ".csv", 
                        index = False)
    
def soup_url(url):
    
    page = urlopen(url)
    html = page.read().decode("utf-8")
    soup = BeautifulSoup(html, "html.parser")
    
    return soup

def get_company_info(soup):
    """Extracts company name, url, location and description. 
    
    @type soup: bs4.BeautifulSoup
    @param iso: Soup object containing website date
    @rtype: DataFrame
    @returns: a DataFrame containing company info.
    """
    
    companies = soup.find("table").find_all("tr")
    
    names = []
    urls = []
    locations = []
    descriptions = []

    for company in companies:

        company_class = company["class"][0]
        name_url = company.find("td", class_ = "company")
        
        # depending on class of the entry, info is structured differently
        if company_class == "inter":
        
            continue
        
        elif company_class == "sponsor":
            
            name = name_url.find("img")["alt"]
            url = name_url.find("a")["href"]
        
        else:
            
            name = name_url.find("a")["href"]
            url = name_url.find_all("a")[1]["href"]
        
        location = company.find("td", class_ = "location").text.strip()
        description = company.find("td", class_ = "description").text.strip()
        
        names.append(name)
        urls.append(url)
        locations.append(location)
        descriptions.append(description)
        
    company_info = pd.DataFrame({"name": names, 
                                 "url": urls, 
                                 "location": locations, 
                                 "desc": descriptions})
    
    return company_info

if __name__ == "__main__":
    
    main(url = "", 
         rel_results_dir = "../results/01a-get_biotech_companies")