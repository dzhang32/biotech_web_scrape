#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import utils
import pandas as pd
import datetime as dt

def main(rel_results_dir):

    results_dir = utils.get_rel_dir(__file__, rel_results_dir)

    rel_df_paths = ["../results/02a-scrape_company_info/biotech_company_scraped_info_0-150_07_09_2021.csv",
                    "../results/02a-scrape_company_info/biotech_company_scraped_info_151-250_07_09_2021.csv",
                    "../results/02a-scrape_company_info/biotech_company_scraped_info_251-700_07_09_2021.csv",
                    "../results/02a-scrape_company_info/biotech_company_scraped_info_701-731_07_09_2021.csv"]

    rel_biotech_comp_path = "../results/01b-tidy_biotech_companies/biotech_company_info_tidy_05_09_2021.csv"
    biotech_comp_path = utils.get_rel_dir(__file__, rel_biotech_comp_path)
    biotech_comp = pd.read_csv(biotech_comp_path)

    biotech_comp = rename_cols(biotech_comp)
    company_info = load_company_info(rel_df_paths)
    df_tidy = tidy_biotech_info(biotech_comp, company_info)

    complete, exceptions = split_exceptions(df_tidy)

    complete.to_csv(results_dir + "/" + "biotech_company_info_complete_" +
                    dt.date.today().strftime("%d_%m_%Y") + ".csv",
                    index = False)

    exceptions.to_csv(results_dir + "/" + "biotech_company_info_exceptions_" +
                      dt.date.today().strftime("%d_%m_%Y") + ".csv",
                      index = False)

def load_company_info(rel_df_paths):

    company_info = []

    for path in rel_df_paths:

        df_path = utils.get_rel_dir(__file__, path)

        df = pd.read_csv(df_path)
        company_info.append(df)

    company_info = pd.concat(company_info).reset_index(drop = True)

    return company_info

def rename_cols(biotech_comp):

    colnames = list(biotech_comp.columns)
    colnames_w_orig = [c + "_orig" for c in colnames]
    colnames_dict = zip(colnames, colnames_w_orig)
    colnames_dict = {key: value for key, value in colnames_dict}
    biotech_comp.rename(colnames_dict, axis = 1, inplace=True)

    return biotech_comp

def tidy_biotech_info(biotech_comp, company_info):

    df_tidy = pd.concat([biotech_comp, company_info], axis=1)
    df_tidy = df_tidy.reset_index(drop = True)

    # remove duplicate original
    # realised that there were a number of companies
    # that were duplicated in the orginal list
    df_tidy = df_tidy.drop_duplicates(subset = ["name_orig"], keep="last").reset_index(drop = True)
    df_tidy = df_tidy.reset_index(drop=True)

    return df_tidy

def split_exceptions(df_tidy):

    # obtain entries with no issues
    complete = df_tidy[(df_tidy["name"].notna()) & (df_tidy["name"] != "Clever")]

    # obtain entries that failed
    # either all values were missing (when name is NA)
    # or name was "Clever", Clever is the company
    # that is the default company in the search engine
    # i.e. the actual company was not searched
    exceptions = df_tidy[(df_tidy["name"].isna()) | (df_tidy["name"] == "Clever")]
    exceptions = exceptions.reset_index(drop = True)

    return complete, exceptions

if __name__ == "__main__":

    main(rel_results_dir = "../results/02b-merge_tidy_company_info")