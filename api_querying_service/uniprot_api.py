import requests, sys, csv
import concurrent.futures
import logging


requestURLbase = "https://www.ebi.ac.uk/proteins/api/proteins/"



def entry_retrieval(accessions, max_id):

    entities = []
    preferred = []
    synonyms = []

    for acc in accessions:
        requestURL = requestURLbase + acc
        r = requests.get(requestURL, headers={"Accept" : "application/json"})
            
        if not r.ok:
            r.raise_for_status()
            sys.exit()
            
            json = r.json()
            
            if "accession" in json and json["accession"] == acc:
                if "organism" in json and "taxonomy" in json["organism"] :
                    entities.append([max_id, json["organism"]["taxonomy"], acc])
                else:
                    print("No taxonomy info for " + acc)

                if "protein" in json:
                    if "recommendedName" in json["protein"] and "fullName" in json["protein"]["recommendedName"]:
                        preferred.appen([max_id, json["protein"]["recommendedName"]["fullName"]["value"]])
                    elif "submittedName" in json["protein"]:
                        n = json["protein"]["submittedName"]

                        if len(n) == 1:
                            synonyms.append([max_id, json["protein"]["submittedName"][0]["fullName"]["value"]])
                        else:
                            print("There are " + str(len(n)) + " submitted names for " + acc)
                    else:
                        print("No label for " + acc)

                    if "component" in json["protein"]:
                        for comp in json["protein"]["component"]:
                            synonyms.append([max_id, comp["recommendedName"]["fullName"]["value"]])

                    if "gene" in json:
                        for gene in json["gene"]:
                            if "name" in gene:
                                synonyms.append([max_id, gene["name"]["value"]])
                            elif "orfNames" in gene:
                                for orf in gene["orfNames"]:
                                    synonyms.append([max_id, orf["value"]])

                max_id = max_id+1



if __name__ == "__main__":
    max_id = 1016027000
    path_to_file = "input_files/uniprot_accessions.tsv"

    accessions = []

    with open(path_to_file) as tsvfile:
        reader = csv.reader(tsvfile, delimiter='\t')
        for row in reader:
            accessions.append(row[0])

    format = "%(asctime)s: %(message)s"
    logging.basicConfig(format=format, level=logging.INFO,
                        datefmt="%H:%M:%S")

    start = 0
    finish = 500

    with concurrent.futures.ThreadPoolExecutor(max_workers=3) as executor:
        executor.map(entry_retrieval(accessions[start:finish]))

    with open('output_files/uniprot_entities.tsv', 'w') as entities_out_file:
        entities_writer = csv.writer(entities_out_file, delimiter='\t')

        with open('output_files/uniprot_preferred.tsv', 'w') as preferred_out_file:
            preferred_writer = csv.writer(preferred_out_file, delimiter='\t')

            with open('output_files/uniprot_names.tsv', 'w') as names_out_file:
                names_writer = csv.writer(names_out_file, delimiter='\t')