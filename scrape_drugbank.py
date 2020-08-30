from bs4 import BeautifulSoup
from pprint import pprint
import requests

# This is a farily simple scraping process that assumes much of the 
# expected data is available. I did have to implement some exception
# handling for the targets and actions, as different drugs have varying
# degrees of information here, including some with none at all.

# To imporve this process at larger scale, every query of the document
# structure (find, find_all, next_sibling, text, etc.) should be wrapped
# in a try/except block that addresses what to do if a given expected
# element is not found, even if to just record a blank or skip that part
# of the process. This way the process can continue for further iterations.

# To be able to tell which iterations (drugs, or drug-targets, in this case)
# finished successfully or not, the process should also log any missing
# expected document elements, either by warning if the single incident does not 
# compromise the extraction, or by error if it does.
def scrape(drug_identifiers):

    # Base URL to Drugbank's drug listings
    base_url = 'https://www.drugbank.ca/drugs/'

    # Start the list of drugs with the Drugbank identifiers
    drugs = []
    for identifier in drug_identifiers:
        drugs.append({'drug_bank_id': identifier})

    # Loop through all the drugs in the list
    for drug in drugs:
        
        # Build the URL for the current drug and get its document
        url = base_url + drug['drug_bank_id']
        response = requests.get(url)

        # Parse document; using html5lib to ensure tags such as dl, dt, and dd
        # are parsed correctly
        soup = BeautifulSoup(response.text, 'html5lib')

        # SMILES - located in the text of the tag after the tag with id 'smiles'
        try:
            smiles = soup.find(id='smiles').next_sibling.text
            drug['smiles'] = smiles
            
        except AttributeError:
            print(f"{drug['drug_bank_id']}: SMILES not found")

        # TARGETS - located in a list of cards wrapped by a tag with id 'targets'
        # Some drugs do not have any targets, and some targets do not have actions
        # or gene names; using try/except blocks to skip and keep scraping when
        # that happens
        try:
            targets = soup.find(id='targets')
            bond_list = targets.find('div', class_='bond-list')
            bond_cards = bond_list.find_all('div', class_='bond card')
            drug['targets'] = []

            # Iterate through all the cards in the list found here
            for bond_card in bond_cards:
                target = {}
                
                target_name = bond_card.find(class_='card-header').find('strong').find('a').text

                # ACTIONS - located within the bond-card in a list of elements in the 
                # tag following a tag with id 'actions'
                try:
                    actions = bond_card.find(id='actions').next_sibling.find_all()
                    target['actions'] = []
                    for action in actions:
                        target['actions'].append(action.text)
                except AttributeError:
                    print(f"{drug['drug_bank_id']}: {target_name}: no actions found")

                # GENE NAME - located within the bond-card in the text of the tag
                # following a tag with id 'gene-name'
                try:
                    gene_name = bond_card.find(id='gene-name').next_sibling.text
                    target['gene_name'] = gene_name
                except AttributeError:
                    print(f"{drug['drug_bank_id']}: {target_name}: gene name not found")

                if len(target) > 0: 
                    drug['targets'].append(target)

        except AttributeError:
            print(f"{drug['drug_bank_id']}: No targets found")

        # ALTERNATIVE IDENTIFIERS - located within a list in the tag following a
        # tag with id 'external-links'. The list is contained within a 'dl' tag
        # that has a series of alternating 'dt' and 'dd' tags that contain each
        # external link's name and value, respectively
        try:
            alt_ids = soup.find(id='external-links').next_sibling
            dts = alt_ids.find('dl').find_all('dt')
            drug['alternative_identifiers'] = {}

            for dt in dts:
                try:
                    drug['alternative_identifiers'][dt.text] = dt.next_sibling.text
                    
                except AttributeError:
                    print(f"{drug['drug_bank_id']}: error scraping alternative identifier")
        
        except AttributeError:
            print(f"{drug['drug_bank_id']}: no alternative identifiers found")

    return drugs