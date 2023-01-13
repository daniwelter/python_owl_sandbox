from owlready2 import *
import csv


def loadOntology(path):
    onto = get_ontology(path).load()
    print("Loaded " + onto.base_iri)

    return onto


def get_parents(ontology, cls):
    # print(cls.name)

    return cls.ancestors(include_self=False)



if __name__ == '__main__':

    path_to_ontology = "file:///Users/danielle.welter/Ontologies/COVID_ontology/COVID-merged.owl"
    ontology = loadOntology(path_to_ontology)
    all_classes = list(ontology.classes())
    # print(len(all_classes))

    path_to_file = "/Users/danielle.welter/Documents/TaggerDictionaries/full_dictionary/covid_dictionary/covid_entities.tsv"
    path_to_entities = "/Users/danielle.welter/Documents/TaggerDictionaries/full_dictionary/full_entities.tsv"
    path_to_groups = "/Users/danielle.welter/Documents/TaggerDictionaries/full_dictionary/full_groups.tsv"

    covid_ids = {}
    tagger_ids = {}
    tagger_groups = {}

    with open(path_to_file) as tsvfile:
        reader = csv.reader(tsvfile, delimiter='\t')
        for row in reader:
            covid_ids[row[2]] = row[0]

    with open(path_to_entities) as tsvfile:
        reader = csv.reader(tsvfile, delimiter='\t')
        for row in reader:
            tagger_ids[row[2]] = row[0]

    with open(path_to_groups) as tsvfile:
        reader = csv.reader(tsvfile, delimiter='\t')
        for row in reader:
            if row[0] not in tagger_groups.keys():
                tagger_groups[row[0]] = []

            tagger_groups[row[0]].append(row[1])

    with open('../output/new_covid_groups.tsv', 'w') as out_file:
        tsv_writer = csv.writer(out_file, delimiter='\t')

        with open('../output/existing_covid_groups.tsv', 'w') as extra_file:
            extra_writer = csv.writer(extra_file, delimiter='\t')

            with open('../output/other_covid_classes.tsv', 'w') as second_out_file:
                second_writer = csv.writer(second_out_file, delimiter='\t')


                for cls in all_classes:
                    if 'APOLLO_SV' in cls.name:
                        n = cls.name.replace('APOLLO_SV_', 'APOLLO_SV:')
                    elif 'NCBITaxon' in cls.name:
                        n = cls.name.replace('NCBITaxon_', '')
                    else:
                        n = cls.name.replace('_', ':')
                    if n in covid_ids.keys():
                        parents = get_parents(ontology, cls)

                        for par in parents:
                            if 'APOLLO_SV' in par.name:
                                p = par.name.replace('APOLLO_SV_', 'APOLLO_SV:')
                            elif 'NCBITaxon' in par.name:
                                p = par.name.replace('NCBITaxon_', '')
                            else:
                                p = par.name.replace('_', ':')
                            if p in covid_ids.keys():
                                if covid_ids[n] not in tagger_groups or id not in tagger_groups[covid_ids[n]]:
                                    tsv_writer.writerow([covid_ids[n], covid_ids[p]])
                                else:
                                    extra_writer.writerow([covid_ids[n], p])
                            elif p in tagger_ids.keys():
                                if covid_ids[n] not in tagger_groups or id not in tagger_groups[covid_ids[n]]:
                                    tsv_writer.writerow([covid_ids[n], tagger_ids[p]])
                                else:
                                    extra_writer.writerow([covid_ids[n], p])
                            else:
                                second_writer.writerow([n, covid_ids[n], p])

                    else:
                       second_writer.writerow([n,'n/a','n/a'])





