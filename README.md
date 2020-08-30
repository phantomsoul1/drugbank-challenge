# drugbank-challenge
Sample scraping of drug info for potential machine learning uses

For this exercise, we scraped a list of drugs from drugbank.ca:
* DB00619
* DB01048
* DB14093
* DB00173
* DB00734
* DB00218
* DB05196
* DB09095
* DB01053
* DB00274

For each of these drugs, we are interested in these values:
* DrugBank ID
* SMILES
* Gene Name and Actions of every Target
* All of the alternative identifiers (external links)

## Prequisites
* Create a PostGRE database called *drugbank_db*
* Execute the *DDL-Queries.sql* script in the *SQL* folder; this will create all the tables
* Python library dependencies
    * Beautiful Soup 4 (https://www.crummy.com/software/BeautifulSoup/)
    * SQLAlchemy (https://www.sqlalchemy.org)
    * html5lib (for Beautiful Soup 4) (pip install html5lib)
* Scripts were written and tested on Python version 3.7.6
* Provide values for the 4 attributes in the config.py file, as specified there, in order to connect to the PostGRESQL database

## Execution
Once the prerequisites are met, run the
*app.py* file. It will scrape the drugbank.ca webpages and write the results to the SQL database.

The *DML-Testing-Queries.sql* script, in the *SQL* folder, can then be used to observe the results.

## Reference Information
* A WIP (work in progress) folder has been included for some insight into the script development process. Jupyter Notebook is required to view those files.
* An ERD is provided in the *SQL* folder as a visual reference to the database structure

## Consideration
Much of this is described in comments within the scripts, but a summary is listed here for reference:

* The scraping makes a lot of assumptions about the shape of the webpage documents and existence of expected document elements. For the 10 drugs requested here, it is sufficient, but the code could make more robust use of try/except blocks and logging to ensure that a few unexpected document conditions don't halt an entire ETL execution.

* Storing this information in a relational database is cauing a double-extraction to take place. While we could solve it by scraping web data directly into data frames, it still does not alleviate the massive amount of joining that has to be done, at scale, to put drug information back together.

* Further, an RDBMS cannot show drugs with both their alternate names and target-actions in a single dataset without duplication of one or the other.

* A document-based data store, such as MongoDB can address many of these concerns. However, MongoDB is still an on-premise solution that needs a hardware team to manage its scale.

* Pipelines to online, cloud-based solutions, such as Snowflake or Redshift, can be much more scalable and have higher-availability than any kind of on-premise solution. 

