import requests, sys, csv
import concurrent.futures
import logging

requestURLbase = "https://pubchem.ncbi.nlm.nih.gov/rest/pug/compound/name/"
requestURLparam = "/cids/JSON"
# https://pubchem.ncbi.nlm.nih.gov/rest/pug/compound/name/glucose/cids/JSON
# https://pubchem.ncbi.nlm.nih.gov/rest/pug/substance/name/Sarilumab/sids/JSON

def entry_retrieval(accessions):
    compounds = {}

    for acc in accessions:
        print("Processing " + acc)
        requestURL = requestURLbase + acc + requestURLparam
        r = requests.get(requestURL)

        if not r.ok:
            compounds[acc] = ["no CID found"]


            # r.raise_for_status()
            # sys.exit()

        else:
            json = r.json()

            if "IdentifierList" in json and "CID" in json["IdentifierList"]:
                cids = json["IdentifierList"]["CID"]
                compounds[acc] = cids

    return compounds

if __name__ == "__main__":
    path_to_file = "input_files/chemicals.tsv"

    accessions = []

    with open(path_to_file) as tsvfile:
        reader = csv.reader(tsvfile, delimiter='\t')
        for row in reader:
            accessions.append(row[0])

    pubchem_ids = entry_retrieval(accessions)


    with open('output_files/pubchem_entities.tsv', 'w') as entities_out_file:
        entities_writer = csv.writer(entities_out_file, delimiter='\t')

        for comp in pubchem_ids.keys():
            for id in pubchem_ids[comp]:
                entities_writer.writerow([comp, id])

