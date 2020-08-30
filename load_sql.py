from config import username, password, hostname, port
from pprint import pprint
from sqlalchemy import create_engine
import json
import pandas as pd

# While loading the scraped drug data into SQL tables may seem like the 
# natural thing to do, it does result in a double-extraction, in which the 
# information is first scraped from a web page, and then re-extracted from the 
# resulting json dictionary.

# One way to improve this would be to plan for the table schema in the scraping
# code, in which we could add information scraped from the web pages directly
# into the data frames, however it still does not address the amount of 
# joining that has to be done in order to put all the drug information 
# back together. Also, its very difficult to show both targets/actions and 
# alternate identifiers in a single data set, as the join would duplicate one 
# for each value of the other.

# A more practical solution might be a document-based storage model, such as
# MongoDB. This can be especially useful if the ML processes
# typically access individual drugs as a whole (with all or at least most of 
# their related data).

# MongoDB, however is still an on-premise solution, meaning we would need our
# own network engineers to help scale it out - more nodes in the cluster, more
# storage for each node, associated performance concerns, etc.

# Creating a pipeline to an online, cloud-based service such as Snowflake or 
# Red Shift can help address such scalability issues without needing to acquire
# a dedicated hardware engineering team to manage on-premise servers.

def load_sql(drugs):

    # Initialize data frames to go with SQL Tables
    action_df = pd.DataFrame(columns=['target_id', 'action'])
    alt_id_df = pd.DataFrame(columns=['drug_id', 'location', 'name'])
    drug_df = pd.DataFrame(columns=['drug_id', 'smiles'])
    target_df = pd.DataFrame(columns=['drug_id', 'gene_name'])

    # Loop through all the drugs and extract relevant data at 
    # tabular levels into the data frames created above
    for drug in drugs:
    
        # Extract top-level scalar drug information
        drug_df = drug_df.append({
            'drug_id': drug['drug_bank_id'], 
            'smiles': drug['smiles']
        }, ignore_index=True)

        # Extract alternate identifier information into its data frame
        # use try/except block in case a particular drug doesn't have 
        # any alternative identifiers
        try:
            alt_ids = drug['alternative_identifiers']
            for key, value in alt_ids.items():
                alt_id_df = alt_id_df.append({
                    'drug_id': drug['drug_bank_id'], 
                    'location': key, 
                    'name': value
                }, ignore_index=True)
        except KeyError:
            print(f"{drug['drug_bank_id']}: alt identifiers not found")

        # Extract target information into its data frame
        # use try/except block in case a particular drug does not 
        # have any targets
        try:
            targets = drug['targets']
            for target in targets:

                # Extract scalar target information
                target_df = target_df.append({
                    'drug_id': drug['drug_bank_id'], 
                    'gene_name': target['gene_name']
                }, ignore_index=True)
                
                # Extract target actions
                # use try/except block in case a particular drug-target
                # has no actions listed
                try:
                    for action in target['actions']:

                        # Extract scalar action information
                        action_df = action_df.append({
                            'target_id': target_df.last_valid_index(), 
                            'action': action
                        }, ignore_index=True)
                except KeyError:
                    print(f"{drug['drug_bank_id']}: actions not found")
                    
        except KeyError:
            print(f"{drug['drug_bank_id']}: targets not found")

    # We could probably improve the efficency of the stored data by
    # adding some validation here, including removing duplicates; the 
    # sample set does not require this

    # Write the resulting data frames to the SQL database
    # (be sure to provide the 4 values in the config.py file)
    engine = create_engine(f"postgres://{username}:{password}@{hostname}:{port}/drugbank_db")
    with engine.connect() as connection:
        drug_df.to_sql('drug', con=connection, if_exists='append', index=False)
        alt_id_df.to_sql('alt_identifier', con=connection, if_exists='append', index_label='alt_identifier_id')
        target_df.to_sql('target', con=connection, if_exists='append', index_label='target_id')
        action_df.to_sql('action', con=connection, if_exists='append', index_label='action_id')

def reset_tables():
    
    #clear sql tables to avoid duplicated information with multiple executions
    print(username)
    engine = create_engine(f"postgres://{username}:{password}@{hostname}:{port}/drugbank_db")
    with engine.connect() as connection:
        connection.execute("DELETE FROM alt_identifier")
        connection.execute("DELETE FROM action")
        connection.execute("DELETE FROM target")
        connection.execute("DELETE FROM drug")

if __name__ == '__main__':
    reset_tables()