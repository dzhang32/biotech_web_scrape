# Web scraping biotech company information

As a final year bioinformatics PhD student, I decided to try and make the job hunt a little more enjoyable by automating and standardising the process of finding companies that I would be interested in working for. Here, I use [Beautiful Soup](https://beautiful-soup-4.readthedocs.io/en/latest/) and [Selenium](https://selenium-python.readthedocs.io) to find details of all UK companies within the field of Biotechnnology. 

# Disclaimer

I do not recommend web scraping data in any way. If you do web scrape, please respect the Terms of Service and [robots.txt](https://www.promptcloud.com/blog/how-to-read-and-respect-robots-file/) of the site you scrape. For more information on the legality of web scraping, you may find this [blog](https://benbernardblog.com/web-scraping-and-crawling-are-perfectly-legal-right/) useful.

# Contents

It's worth mentioning that due to the ever-updating nature of many websites, it's unlikely that these scripts will remain re-runnable out-of-the-box.

| Script | Description |
| --- | --- |
| [01a-get_biotech_companies.py](scripts/01a-get_biotech_companies.py) | Web scrape names of all UK biotech companies. |
| [01b-tidy_biotech_companies.py](scripts/01b-tidy_biotech_companies.py) | Tidy data from previous step. |
| [02a-scrape_company_info.py](script/02a-scrape_company_info.py) | Use selenium to navigate, search and scrape description, size, location, url and domains/tags of companies. |
| [02b-merge_tidy_company_info.py](script/02b-merge_tidy_company_info.py) | Tidying. Find the exceptions that were not scraped successfully. |
| [02c-scrape_company_info_2nd_pass.py](script/02c-scrape_company_info_2nd_pass.py) | 2nd pass, re-run scraping on the exceptions. |
| [02d-merge_exceptions_2nd_pass.py](script/02d-merge_exceptions_2nd_pass.py) | Merge together all company info. |
| [utils.py](scripts/utils.py) | Utility function to keep project self-contained. |

# Acknowledgements

This project was inspired by this [blog post](https://towardsdatascience.com/automating-my-job-search-with-python-ee2b465c6a8f) and accompanying [youtube video](https://www.youtube.com/watch?v=nK9LzpjeGKc) by Chris Lovejoy. 
