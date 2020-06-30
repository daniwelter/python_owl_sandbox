import pandas as pd




if __name__ == '__main__':

    path_to_entities = "/Users/daniellewelter/Documents/TaggerDictionaries/tagger_dictionary/reflect_dicts4-6-20/tagger_entities_v2.tsv"
    path_to_labels = "/Users/daniellewelter/Documents/TaggerDictionaries/tagger_dictionary/reflect_dicts4-6-20/tagger_preferred_v2.tsv"
    path_to_names = "/Users/daniellewelter/Documents/TaggerDictionaries/tagger_dictionary/reflect_dicts4-6-20/tagger_names_v2.tsv"
    path_to_parents = "/Users/daniellewelter/Documents/TaggerDictionaries/tagger_dictionary/reflect_dicts4-6-20/tagger_groups_v2.tsv"

    # path_to_new_genes = "/Users/daniellewelter/Documents/COVID-19/covid19-info-from-uniport-and-ncbi-gene-dbs/ENTREZGENE-viruses--GeneSymbol--AliasSymbol--ProteinName.txt"
    # path_to_new_species = "/Users/daniellewelter/Documents/COVID-19/covid19-info-from-uniport-and-ncbi-gene-dbs/ENTREZGENE-viruses--organism-name--NCBI-TaxId.txt"

    # path_to_new_genes = "/Users/daniellewelter/Documents/COVID-19/covid19-info-from-uniport-and-ncbi-gene-dbs/swissprot-all-virus--name--gene-name--altname--synonyms--orfnames.txt"
    # path_to_new_species = "/Users/daniellewelter/Documents/COVID-19/covid19-info-from-uniport-and-ncbi-gene-dbs/swissprot-all-virus--org--NCBI_TaxId--HostOrganism.txt"

    path_to_new_genes = "/Users/daniellewelter/Documents/COVID-19/covid19-info-from-uniport-and-ncbi-gene-dbs/uniprot-all-virus--name--gene-name--altname--synonyms--orfnames.txt"
    path_to_new_species = "/Users/daniellewelter/Documents/COVID-19/covid19-info-from-uniport-and-ncbi-gene-dbs/uniprot-all-virus--org--NCBI_TaxId--HostOrganism.txt"

    proteins = {}
    species = {}
    spec_prot = {}

    distinct_prot_species = []

    entities = pd.read_csv(path_to_entities, sep='\t', header=None)
    print(entities.head(8))

    types = entities[1]

    proteins = entities[entities[1] > 0]
    species = entities[entities[1] == -2]
    spec_prot = entities[entities[1] == -3]
    distinct_prot_species = pd.unique(proteins[1])

    # print(proteins.head(5))
    # print(species.head(5))
    # print(spec_prot.head(5))
    # print(distinct_prot_species[2])

    tagger_names = pd.read_csv(path_to_names, sep='\t', header=None)

    new_species = pd.read_csv(path_to_new_species, sep='\t', header=None)

    new_tax_id = []

    for spec in new_species[2]:
        if spec not in new_tax_id:
            new_tax_id.append(spec)

    print(str(len(new_tax_id)))
    # with open(path_to_new_species) as tsvfile:
    #     reader = csv.reader(tsvfile, delimiter='\t')
    #     for row in reader:
    #         if row[2] not in new_tax_id:
    #             new_tax_id.append(row[2])
    #
    # new_genes_proteins1 = []
    # new_genes_proteins2 = []
    # new_genes_proteins3 = []
    # new_genes_proteins4 = []
    # new_genes_proteins5 = []
    # new_genes_proteins6 = []
    #
    # with open(path_to_new_genes) as tsvfile:
    #     reader = csv.reader(tsvfile, delimiter='\t')
    #     for row in reader:
    #         new_genes_proteins1.append(row[0])
    #         new_genes_proteins2.append(row[1])
    #         if (row[2] != ''):
    #             new_genes_proteins3.append(row[2])
    #         if (row[3] != ''):
    #             new_genes_proteins4.append(row[3])
    #         if (row[4] != ''):
    #             new_genes_proteins5.append(row[4])
    #         if (row[5] != ''):
    #             new_genes_proteins6.append(row[5])
    #
    # found_tax = []
    # not_found_tax = []
    # for tax_id in new_tax_id:
    #     if tax_id not in species.keys():
    #         not_found_tax.append(tax_id)
    #     else:
    #         found_tax.append(tax_id)
    #
    # found_protein1 = []
    # not_found_protein1 = []
    # for prot in new_genes_proteins1:
    #     if prot not in tagger_names.keys():
    #         not_found_protein1.append(prot)
    #     else:
    #         found_protein1.append(prot)
    #
    # found_protein2 = []
    # not_found_protein2 = []
    # for prot in new_genes_proteins2:
    #     if prot not in tagger_names.keys():
    #         not_found_protein2.append(prot)
    #     else:
    #         found_protein2.append(prot)
    #
    # found_protein3 = []
    # not_found_protein3 = []
    # for prot in new_genes_proteins3:
    #     if prot not in tagger_names.keys():
    #         not_found_protein3.append(prot)
    #     else:
    #         found_protein3.append(prot)
    #
    # found_protein4 = []
    # not_found_protein4 = []
    # for prot in new_genes_proteins4:
    #     if prot not in tagger_names.keys():
    #         not_found_protein4.append(prot)
    #     else:
    #         found_protein4.append(prot)
    #
    # found_protein5 = []
    # not_found_protein5 = []
    # for prot in new_genes_proteins5:
    #     if prot not in tagger_names.keys():
    #         not_found_protein5.append(prot)
    #     else:
    #         found_protein5.append(prot)
    #
    # found_protein6 = []
    # not_found_protein6 = []
    # for prot in new_genes_proteins6:
    #     if prot not in tagger_names.keys():
    #         not_found_protein6.append(prot)
    #     else:
    #         found_protein6.append(prot)
    #
    # print("Species: found - " + str(len(found_tax)) + "; not found - " + str(len(not_found_tax)))
    # print("Uniprot ID: found - " + str(len(found_protein1)) + "; not found - " + str(len(not_found_protein1)))
    # print("Protein: found - " + str(len(found_protein2)) + "; not found - " + str(len(not_found_protein2)))
    # print("Gene: found - " + str(len(found_protein3)) + "; not found - " + str(len(not_found_protein3)))
    # print("Protein alt: found - " + str(len(found_protein4)) + "; not found - " + str(len(not_found_protein4)))
    # print("Gene syn: found - " + str(len(found_protein5)) + "; not found - " + str(len(not_found_protein5)))
    # print("ORF: found - " + str(len(found_protein6)) + "; not found - " + str(len(not_found_protein6)))
    #
    # with open('swissprot_found_species_v2.tsv', 'w') as out_file:
    #     tsv_writer = csv.writer(out_file, delimiter='\t')
    #     for tax in found_tax:
    #         tsv_writer.writerow([species[tax], tax])
    #
    # with open('swissprot_missing_species_v2.tsv', 'w') as out_file:
    #     tsv_writer = csv.writer(out_file, delimiter='\t')
    #     for tax in not_found_tax:
    #         tsv_writer.writerow([tax])
    #
    # with open('swissprot_found_genes_v2.tsv', 'w') as out_file:
    #     tsv_writer = csv.writer(out_file, delimiter='\t')
    #     for prot in found_protein3:
    #         tsv_writer.writerow([tagger_names[prot], prot])
    #
    # with open('swissprot_missing_genes_v2.tsv', 'w') as out_file:
    #     tsv_writer = csv.writer(out_file, delimiter='\t')
    #     for prot in not_found_protein3:
    #         tsv_writer.writerow([prot])
    #
    #
    #
