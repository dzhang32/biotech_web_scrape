#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Sep  7 00:53:49 2021

@author: david_zhang
"""

import utils
from selenium import webdriver
from bs4 import BeautifulSoup
import time
import pandas as pd
import datetime as dt

class Company:
    
    def __init__(self, name, soup):
        
        section_content = soup.find("div", class_ = "section-content")
        
        self.name = name
        self.soup = soup
        self.section_content = section_content
    
    def get_desc(self):
    
        desc = self.section_content.find("span", class_ = "description").text
    
        return desc
    
    def get_location(self):
    
        location = self.section_content.find_all("field-formatter", class_ = "ng-star-inserted")[0]
        location = location.text.strip()

        return location

    def get_size(self):

        size = self.section_content.find_all("field-formatter", class_ = "ng-star-inserted")[1]
        size = size.text.strip()

        return size

    def get_url(self):

        url = self.section_content.find_all("field-formatter", class_ = "ng-star-inserted")[4]
        url = url.find("a")["href"]

        return url

    def get_domains(self):

        domains = self.soup.find("chips-container", class_ = "ng-star-inserted")
        domains = domains.find_all("a", class_ = "ng-star-inserted")

        domains = [d.text for d in domains]
        domains = ",".join(domains)

        return domains
    
def scrape_company_info(driver, site, company_name):

    source = get_page_source(driver, site, company_name)

    soup = BeautifulSoup(source, "html.parser")

    company_curr = Company(company_name, soup)

    desc = company_curr.get_desc()
    location = company_curr.get_location()
    size = company_curr.get_size()
    url = company_curr.get_url()
    domain = company_curr.get_domains()
            
    return desc, location, size, url, domain

def get_page_source(driver, site, company_name):
        
    driver.get(site)

    driver.implicitly_wait(5)
        
    search_box = driver.find_element_by_id('mat-input-0')
    search_box.click()
        
    search_box.send_keys(company_name)
        
    time.sleep(3)
        
    comp_box = driver.find_elements_by_class_name("row-anchor.cb-padding-medium-horizontal.flex.layout-row.layout-align-start-center.cb-text-color-medium.ng-star-inserted")
    comp_box[0].click()
    
    time.sleep(1)
        
    page_source = driver.page_source
        
    return page_source

def convert_to_df(descs, locations, sizes, urls, domains):
    
    companies_info = pd.DataFrame({"description": descs, 
                                      "location": locations, 
                                      "sizes": sizes,
                                      "url": urls, 
                                      "domain": domains})
    
    return companies_info

