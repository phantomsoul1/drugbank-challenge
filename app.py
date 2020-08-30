from bs4 import BeautifulSoup
from config import username, password, hostname, port
from pprint import pprint
from sqlalchemy import create_engine
import json
import load_sql
import pandas as pd
import requests
import scrape_drugbank

def get_drug_identifiers():
    
    # Provided list of drugs to scrape
    return [
        'DB00619',
        'DB01048',
        'DB14093',
        'DB00173',
        'DB00734',
        'DB00218',
        'DB05196',
        'DB09095',
        'DB01053',
        'DB00274'
    ]

def main():

    # Scrape drug information from drugbank.ca
    print('Running scrape...')
    drugs = scrape_drugbank.scrape(get_drug_identifiers())
    print("Done.")

    # Delete any previous data in the SQL tables
    # (so we don't duplicate it on multiple executions)
    # (potential improvement: add an option for this for runtime)
    print("Resetting SQL tables...")
    load_sql.reset_tables()
    print("Done.")

    # Load results into PostGRESQL database
    # (See SQL folders for DB resources required)
    print('Loading into PostGRESQL...')
    load_sql.load_sql(drugs)
    print("Done.")

if __name__ == '__main__':
    main()