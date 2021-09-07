#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Sep  7 00:53:49 2021
@author: david_zhang
"""

import utils
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
from bs4 import BeautifulSoup
import time
import pandas as pd
import datetime as dt

class Company:
    """Obtain the relevant company details

    Company contains various methods to extract the name,
    description, location, size, and domains/tags from a
    BeautifulSoup object.
    """
    def __init__(self, soup):
        
        self.soup = soup
        
    def get_name(self):
        
        name = self.soup.find("h1", class_ = "profile-name")

        # required incase that particular company does not
        # have a specific parameter available
        # driver.find will return None
        if name is None: 
            
            return ""
        
        name = name.text.strip()
        
        return name
    
    def get_desc(self):
    
        desc = self.soup.find("span", class_ = "description")
        
        if desc is None: 
            
            return ""
        
        desc = desc.text.strip()
    
        return desc
    
    def get_location(self):
    
        location = self.soup.find_all("a", class_ = "link-accent ng-star-inserted")

        # required incase that particular company does not
        # have a specific parameter available
        # driver.find_all will return an empty list
        if len(location) == 0: 
            
            return ""
        
        location = ",".join([l.text.strip() for l in location])
        
        return location

    def get_size(self):

        size = self.soup.find("a", class_ = "component--field-formatter field-type-enum " + 
                              "link-accent ng-star-inserted")
        
        if size is None: 
            
            return ""
        
        size = size.text.strip()

        return size

    def get_url(self):
        
        url = self.soup.find("a", class_ = "component--field-formatter link-accent ng-star-inserted")
        
        if url is None: 
            
            return ""
        
        url = url.text.strip()

        return url

    def get_domains(self):

        domains = self.soup.find_all("div", class_ = "cb-overflow-ellipsis")
        
        if len(domains) == 0: 
            
            return ""

        domains = ",".join([d.text for d in domains])

        return domains

def main(site, rel_results_dir):

    results_dir = utils.get_rel_dir(__file__, rel_results_dir)

    biotech_comp = utils.get_rel_dir(__file__,
                                     "../results/01b-tidy_biotech_companies/" +
                                     "biotech_company_info_tidy_05_09_2021.csv")
    biotech_comp = pd.read_csv(biotech_comp)

    # driver need chromedriver executable
    # https://chromedriver.chromium.org/downloads
    chrom_path = utils.get_rel_dir(__file__, "../tools/chromedriver")
    driver = webdriver.Chrome(chrom_path)
    
    names = []
    descs = []
    locations = []
    sizes = []
    urls = []
    domains = []

    indexes = range(0, len(biotech_comp), 1)

    for i in indexes:

        print(str(i) + " - " + biotech_comp["name"][i])

        # attempt to catch error when website changes, doesn't always work
        # NoSuchElementException is the type of exception thrown when
        # selenium cannot find an element
        try: 
            
            name, desc, location, size, url, domain = scrape_company_info(driver, site, biotech_comp["name"][i])
            
        except (AttributeError, IndexError, NoSuchElementException):
            
            time.sleep(5)
            driver.implicitly_wait(5)
            
            name, desc, location, size, url, domain = scrape_company_info(driver, site, biotech_comp["name"][i])
        
        names.append(name)

        descs.append(desc)
        locations.append(location)
        sizes.append(size)
        urls.append(url)
        domains.append(domain)

        # batch saves, every 50 companies, avoid redoing everything every time
        # there's an error
        save_at = list(range(0, len(biotech_comp), 50))
        save_at.append(len(biotech_comp))
        save_at.remove(0)

        if i in save_at:

            print("Saving data on the", indexes[0], "-", i, "companies...")

            companies_info = convert_to_df(names, descs, locations, sizes, urls, domains)

            companies_info.to_csv(results_dir + "/" + "biotech_company_scraped_info_" +
                                  str(indexes[0]) + "-" + str(i) + "_" +
                                  dt.date.today().strftime("%d_%m_%Y") +
                                  ".csv",
                                  index = False)

def scrape_company_info(driver, site, company_name):
    """Scrapes website for info on a specific company

    @type driver: selenium.webdriver.Chrome
    @param driver: Initialised by selenium.webdriver.Chrome()
    @type company_name: site
    @param company_name: Site to be scraped.
    @type company_name: str
    @param company_name: Name of the company of interest.
    @rtype: str
    @returns: 6 str objects, each containing one aspect
    of the company
    """
    source = get_page_source(driver, site, company_name)

    soup = BeautifulSoup(source, "html.parser")

    company_curr = Company(soup)

    name = company_curr.get_name()
    desc = company_curr.get_desc()
    location = company_curr.get_location()
    size = company_curr.get_size()
    url = company_curr.get_url()
    domain = company_curr.get_domains()
    
    return name, desc, location, size, url, domain

def get_page_source(driver, site, company_name):
    """Searches company and navigates website to the url
    desribing that company

    @type driver: selenium.webdriver.Chrome
    @param driver: Initialised by selenium.webdriver.Chrome()
    @type company_name: site
    @param company_name: Site to be scraped.
    @type company_name: str
    @param company_name: Name of the company of interest.
    @rtype: bs4.BeautifulSoup
    @returns: Souped version of the company url.
    """

    driver.get(site)

    driver.implicitly_wait(5)

    search_box = driver.find_element_by_id('mat-input-0')
    search_box.click()

    search_box.send_keys(company_name)

    # after putting company in search box, need to
    # wait for site to dynamically pull up results
    time.sleep(3)

    comp_box = driver.find_elements_by_class_name("row-anchor.cb-padding-medium-horizontal.flex" +
                                                  ".layout-row.layout-align-start-center." +
                                                  "cb-text-color-medium.ng-star-inserted")
    comp_box[0].click()

    # sometimes loading can be slow
    time.sleep(1)

    page_source = driver.page_source

    return page_source

def convert_to_df(names, descs, locations, sizes, urls, domains):
    
    companies_info = pd.DataFrame({"name": names,
                                   "description": descs, 
                                   "location": locations, 
                                   "sizes": sizes,
                                   "url": urls, 
                                   "domain": domains})
    
    return companies_info

if __name__ == "__main__":

    main(site = "",
         rel_results_dir = "../results/02a-scrape_company_info")
