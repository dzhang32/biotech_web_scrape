# Web scraping biotech company information

As a final year bioinformatics PhD student, I decided to try and make the job hunt a little more enjoyable by automating and standardising the process of finding companies that I would be interested in working for. Here, I use [Beautiful Soup](https://beautiful-soup-4.readthedocs.io/en/latest/) and [Selenium](https://selenium-python.readthedocs.io) to find details of all UK companies within the field of Biotechnnology. 

# Contents

| Script | Description |
| --- | --- |
| [01a-get_biotech_companies.py](scripts/01a-get_biotech_companies.py) | Web scrape names of all UK biotech companies. |
| [01b-tidy_biotech_companies.py](scripts/01b-tidy_biotech_companies.py) | Tidy data from previous step. |
| [02a-scrape_company_info.py](script/02a-scrape_company_info.py) | Use selenium to navigate, search and scrape description, size, location, url and domains/tags of companies. |
| [02b-merge_tidy_company_info.py](script/02b-merge_tidy_company_info.py) | Tidying. Find the exceptions that were not scraped successfully. |
| [02c-scrape_company_info_2nd_pass.py](script/02c-scrape_company_info_2nd_pass.py) | 2nd pass, re-run scraping on the exceptions. |
| [02d-merge_exceptions_2nd_pass.py](script/02d-merge_exceptions_2nd_pass.py) | Merge together all company info. |
| [utils.py](scripts/utils.py) | Utility function to keep project self-contained. |
