#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import utils
import pandas as pd
import datetime as dt

def main(rel_complete_path, rel_exceptions_path, rel_exceptions_2nd_pass_path, rel_results_dir):

    complete_path = utils.get_rel_dir(__file__, rel_complete_path)
    exceptions_path = utils.get_rel_dir(__file__, rel_exceptions_path)
    exceptions_2nd_pass_path = utils.get_rel_dir(__file__, rel_exceptions_2nd_pass_path)
    results_dir = utils.get_rel_dir(__file__, rel_results_dir)

    complete = pd.read_csv(complete_path)
    exceptions = pd.read_csv(exceptions_path)
    exceptions_2nd = pd.read_csv(exceptions_2nd_pass_path)

    exceptions = repair_exceptions(exceptions, exceptions_2nd)

    print(exceptions)

    complete = pd.concat([complete, exceptions]).reset_index(drop = True)

    complete.to_csv(results_dir + "/" + "biotech_company_info_complete_" +
                      dt.date.today().strftime("%d_%m_%Y") + ".csv",
                      index = False)

def repair_exceptions(exceptions, exceptions_2nd):

    exceptions = exceptions.drop(columns = ["name", "description", "location", "sizes", "url", "domain"])
    exceptions = pd.concat([exceptions, exceptions_2nd], axis = 1)

    return exceptions

if __name__ == "__main__":

    main("../results/02b-merge_tidy_company_info/biotech_company_info_complete_07_09_2021.csv",
         "../results/02b-merge_tidy_company_info/biotech_company_info_exceptions_07_09_2021.csv",
         "../results/02c-scrape_company_info_2nd_pass/biotech_company_info_exceptions_2nd_pass_07_09_2021.csv",
         "../results/02d-merge_exceptions_2nd_pass")