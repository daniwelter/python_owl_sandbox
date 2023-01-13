import os, csv



if __name__ == "__main__":
    path_to_vocabulary = "/Users/danielle.welter/Development/omop_vocabulary_v5/CONCEPT.csv"

    path_to_biomap = "/Users/danielle.welter/Development/python_sandbox/biomap_omop/biomap_dd.tsv"


    omop_concepts = []
    concept_names = []

    with open(path_to_vocabulary) as tsvfile:
        reader = csv.reader(tsvfile, delimiter='\t')
        for row in reader:
            omop_concepts.append(row)
            concept_names.append(row[1].lower())

    biomap = []
    bm_names = []
    bm_mapped = {}

    with open(path_to_biomap) as tsvfile:
        reader = csv.reader(tsvfile, delimiter='\t')
        for row in reader:
            biomap.append(row)
            bm_names.append(row[0].strip().lower())
            if len(row) > 1 and row[1] != 'none':
                bm_mapped[row[0].strip().lower()] = row[1].strip()

    in_omop = []
    not_omop = []
    to_extract = []
    to_check = []

    for concept in bm_names:
        if concept in concept_names:
            in_omop.append(concept)

            if concept not in bm_mapped.keys():
                to_extract.append(concept)


        else:
            not_omop.append(concept)

            if concept in bm_mapped.keys():
                to_check.append(concept)

    print("In OMOP: " + str(len(in_omop)))
    print("Easily mapped: " + str(len(to_extract)))
    print("Not in OMOP: " + str(len(not_omop)))
    print("Has mapping in BIOMAP: " + str(len(to_check)))