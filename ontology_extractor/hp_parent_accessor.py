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

    path_to_ontology = "file:///Users/danielle.welter/Ontologies/human-phenotype-ontology/hp-full.owl"
    ontology = loadOntology(path_to_ontology)

    all_classes = list(ontology.classes())
    # print(len(all_classes))

    path_to_file = "/Users/danielle.welter/Documents/TaggerDictionaries/full_dictionary/full_entities.tsv"
    path_to_groups = "/Users/danielle.welter/Documents/TaggerDictionaries/full_dictionary/full_groups.tsv"

    hp_ids = {}
    hp_groups = {}

    with open(path_to_file) as tsvfile:
        reader = csv.reader(tsvfile, delimiter='\t')
        for row in reader:
            hp_ids[row[2]] = row[0]

    with open(path_to_groups) as tsvfile:
        reader = csv.reader(tsvfile, delimiter='\t')
        for row in reader:
            if row[0] not in hp_groups.keys():
                hp_groups[row[0]] = []

            hp_groups[row[0]].append(row[1])

    with open('../output/new_hp_groups.tsv', 'w') as out_file:
        tsv_writer = csv.writer(out_file, delimiter='\t')

        with open('../output/existing_hp_groups.tsv', 'w') as extra_file:
            extra_writer = csv.writer(extra_file, delimiter='\t')

            with open('../output/other_hp_classes.tsv', 'w') as second_out_file:
                second_writer = csv.writer(second_out_file, delimiter='\t')


                for cls in all_classes:
                    n = cls.name.replace('_', ':')
                    if n in hp_ids.keys():
                        parents = get_parents(ontology, cls)

                        for p in parents:
                            if p.name.replace('_', ':') in hp_ids.keys():
                                id = hp_ids[p.name.replace('_', ':')]
                                if hp_ids[n] not in hp_groups or id not in hp_groups[hp_ids[n]]:
                                    tsv_writer.writerow([hp_ids[n], hp_ids[p.name.replace('_', ':')]])
                                else:
                                    extra_writer.writerow([hp_ids[n], p])
                            else:
                                second_writer.writerow([n, hp_ids[n], p.name.replace('_', ':')])

                    else:
                       second_writer.writerow([n,'n/a','n/a'])





