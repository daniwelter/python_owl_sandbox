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

    path_to_ontology = "file:///Users/daniellewelter/Ontologies/NCBITaxon/ncbitaxon.owl"
    ontology = loadOntology(path_to_ontology)

    all_classes = list(ontology.classes())
    print("Ontology class count: " + str(len(all_classes)))

    path_to_entities = "/Users/daniellewelter/Documents/TaggerDictionaries/organisms_dictionary/organisms_entities.tsv"
    path_to_labels = "/Users/daniellewelter/Documents/TaggerDictionaries/organisms_dictionary/organisms_preferred.tsv"
    path_to_names = "/Users/daniellewelter/Documents/TaggerDictionaries/organisms_dictionary/organisms_names.tsv"
    path_to_parents = "/Users/daniellewelter/Documents/TaggerDictionaries/organisms_dictionary/organisms_groups.tsv"

    mapped_terms = "mapped_terms.tsv"

    ncbi_ids = {}
    ncbi_labels = {}
    ncbi_names = {}

    mapped_labels = {}
    mapped_synonyms = {}

    with open(mapped_terms) as tsvfile:
        reader = csv.reader(tsvfile, delimiter='\t')
        for row in reader:
            if row[2] not in mapped_labels.keys():
                mapped_labels[row[2]] = row[1]
            if row[2] not in mapped_synonyms.keys():
                mapped_synonyms[row[2]] = []
            mapped_synonyms[row[2]].append(row[0])

    max_id = 0
    with open(path_to_entities) as tsvfile:
        reader = csv.reader(tsvfile, delimiter='\t')
        for row in reader:
            ncbi_ids[row[2]] = row[0]
            if int(row[0]) > max_id:
                max_id = int(row[0])

    # max_id = max_id+1
    #
    # with open(path_to_labels) as tsvfile:
    #     reader = csv.reader(tsvfile, delimiter='\t')
    #     for row in reader:
    #         ncbi_labels[row[0]] = row[1]
    #
    # with open(path_to_names) as tsvfile:
    #     reader = csv.reader(tsvfile, delimiter='\t')
    #     for row in reader:
    #         if row[0] not in ncbi_names.keys():
    #             ncbi_names[row[0]] = []
    #         ncbi_names[row[0]].append(row[1])

    # with open('additional_entities.tsv', 'w') as out_file:
    #     entities_writer = csv.writer(out_file, delimiter='\t')
    #
    #     with open('additional_preferred.tsv', 'w') as second_out_file:
    #         preferred_writer = csv.writer(second_out_file, delimiter='\t')
    #
    #         with open('additional_names.tsv', 'w') as second_out_file:
    #             names_writer = csv.writer(second_out_file, delimiter='\t')
    #
    #             for taxon_id in mapped_labels.keys():
    #                 if taxon_id in ncbi_ids.keys():
    #                     internal_id = ncbi_ids[taxon_id]
    #
    #                     if internal_id in ncbi_names.keys():
    #                         if mapped_synonyms[taxon_id] not in ncbi_names[internal_id]:
    #                             for syn in mapped_synonyms[taxon_id]:
    #                                 names_writer.writerow([internal_id, syn])
    #                         if mapped_labels[taxon_id] not in ncbi_names[internal_id]:
    #                             names_writer.writerow([internal_id, mapped_labels[taxon_id]])
    #                 else:
    #                     entities_writer.writerow([max_id, "-2", taxon_id])
    #
    #                     preferred_writer.writerow([max_id, mapped_labels[taxon_id]])
    #                     names_writer.writerow([max_id, mapped_labels[taxon_id]])
    #                     for syn in mapped_synonyms[taxon_id]:
    #                         names_writer.writerow([max_id, syn])
    #
    #                     max_id = max_id+1

    new_entries = {}
    with open('additional_entities.tsv') as tsvfile:
        reader = csv.reader(tsvfile, delimiter='\t')
        for row in reader:
            new_entries[row[2]] = row[0]

    # with open('additional_groups.tsv', 'w') as out_file:
    #     groups_writer = csv.writer(out_file, delimiter='\t')

        for cls in all_classes:
            n = cls.name.replace('NCBITaxon_', '')
            # if n in new_entries.keys():
            if n not in ncbi_ids.keys():
                print(n)
                # parents = get_parents(ontology, cls)
                #
                # for p in parents:
                #     if p.name.replace('NCBITaxon_', '') in ncbi_ids.keys():
                #         groups_writer.writerow([new_entries[n], ncbi_ids[p.name.replace('NCBITaxon_', '')]])
                #     elif p.name.replace('NCBITaxon_', '') in new_entries.keys():
                #         groups_writer.writerow([new_entries[n], new_entries[p.name.replace('NCBITaxon_', '')]])







