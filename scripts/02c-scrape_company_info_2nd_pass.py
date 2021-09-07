#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import utils
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
import time
import pandas as pd
import datetime as dt

# bad practice, used as can't have special chrs
# in module name, will change script name formats in future
# https://stackoverflow.com/questions/761519/is-it-ok-to-use-dashes-in-python-files-when-trying-to-import-them
scraper = __import__("02a-scrape_company_info")

def main(site, rel_results_dir):

    results_dir = utils.get_rel_dir(__file__, rel_results_dir)

    biotech_comp = utils.get_rel_dir(__file__,
                                     "../results/02b-merge_tidy_company_info/" +
                                     "biotech_company_info_exceptions_07_09_2021.csv")

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

        print(str(i) + " - " + biotech_comp["name_orig"][i])

        # attempt to catch error when website changes, doesn't always work
        # NoSuchElementException is the type of exception thrown when
        # selenium cannot find an element
        try:

            name, desc, location, size, url, domain = scraper.scrape_company_info(driver, site, biotech_comp["name_orig"][i])

        except (AttributeError, IndexError, NoSuchElementException):

            time.sleep(5)
            driver.implicitly_wait(5)

            name, desc, location, size, url, domain = scraper.scrape_company_info(driver, site, biotech_comp["name_orig"][i])

        names.append(name)

        descs.append(desc)
        locations.append(location)
        sizes.append(size)
        urls.append(url)
        domains.append(domain)

        # batch saves, every 50 companies, avoid redoing everything every time
        # there's an error
        save_at = list(range(0, len(biotech_comp), 50))
        save_at.append(len(biotech_comp) - 1)
        save_at.remove(0)

        if i in save_at:
            print("Saving data on the", indexes[0], "-", i, "companies...")

            companies_info = scraper.convert_to_df(names, descs, locations, sizes, urls, domains)

            companies_info.to_csv(results_dir + "/" + "biotech_company_info_exceptions_2nd_pass_" +
                                  dt.date.today().strftime("%d_%m_%Y") + ".csv",
                                  index = False)

if __name__ == "__main__":

    main(site = "",
         rel_results_dir = "../results/02c-scrape_company_info_2nd_pass")