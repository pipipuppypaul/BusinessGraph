# Resources:
    # Task desc: https://gist.github.com/jvani/57200744e1567f33041130840326d488
    # networkX: https://networkx.org/documentation/stable/tutorial.html
    # data source website: https://firststop.sos.nd.gov/search/business
    

# requirements:
* Scrape data from [ND](https://firststop.sos.nd.gov/search/business)
  * target1: all active companies whose names start with the letter "X" (e.g., Xtreme Xteriors LLC)
  * target2: Commercial Registered Agent, Registered Agent, and/or Owners
  * **Q**: what if no Commercial Agent? No Owners found?
* Save data in some format (hyu: CSV.gz chosen)
* Read the data and plot Graph using NetworkX
  * graph content: companies, registered agents, and owners
* Deliverables: repo link of data and plot (hyu: code also) 
* Limit: 
  * As of 2019/08/21 there are 193 such companies (there may be fewer). Please do not spam the web app.
  * Together, using scrapy and NetworkX, your **crawling and graph** code should not go well beyond **100 lines** of PEP8 code.
* **Q**:
  * which date or date range should I use? (Now assuming current day)
  

# roadmap:
* Understand the website
  * filters: 'Starts with', 'active entities only'
  * **Q**: why does the website show business like 'AKITA DRILLING USA CORP' etc. even when I turned on 'Starts with X'?
* Use scrapy to scape data with filters described above.
  * get_data_from_web() -> company names; RA1; RA2; Owners; datadate
  * **Q**: Any NaN? Any dup?
* Save data with specific schema in csv.gz files:
  * schema: 
    * company names: Unique, NA not allowed
    * RA1: NA allowed
    * RA2: NA allowed
    * Owners: NA allowed
    * datadate: curdate(), NA not allowed
  * file name convention: nd_business_X_yyyymmdd.csv.gz
* Read data from file
* Plot with NetworkX