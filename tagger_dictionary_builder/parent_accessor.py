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

    path_to_ontology = "file:///Users/daniellewelter/Ontologies/human-phenotype-ontology/hp.owl"
    ontology = loadOntology(path_to_ontology)

    all_classes = list(ontology.classes())
    # print(len(all_classes))

    path_to_file = "/Users/daniellewelter/Documents/TaggerDictionaries/hpo_dictionary/hpo_entities.tsv"

    hp_ids = {}

    with open(path_to_file) as tsvfile:
        reader = csv.reader(tsvfile, delimiter='\t')
        for row in reader:
            hp_ids[row[2]] = row[0]

    with open('hp_groups.tsv', 'w') as out_file:
        tsv_writer = csv.writer(out_file, delimiter='\t')

        with open('../tagger_dictionaries/other_hp_classes.tsv', 'w') as second_out_file:
            second_writer = csv.writer(second_out_file, delimiter='\t')


            for cls in all_classes:
                n = cls.name.replace('_', ':')
                if n in hp_ids.keys():
                    parents = get_parents(ontology, cls)

                    for p in parents:
                        if p.name.replace('_', ':') in hp_ids.keys():
                            tsv_writer.writerow([hp_ids[n], hp_ids[p.name.replace('_', ':')]])
                        else:
                            second_writer.writerow([n, hp_ids[n], p.name.replace('_', ':')])

                else:
                   second_writer.writerow([n,'n/a','n/a'])





