import duckdb


con = duckdb.connect()
c = con.cursor()

# table for tagger entities
c.execute("CREATE TABLE tagger_entities(id INTEGER, type integer, entity varchar)")
c.execute("COPY tagger_entities FROM 'tagger_dictionaries/tagger_entities.tsv' ( DELIMITER '\t')")
# c.execute("SELECT COUNT(distinct type) from tagger_entities")
# print(c.fetchall())

# table for tagger names
# c.execute("CREATE TABLE tagger_names(id INTEGER, name varchar)")
# c.execute("COPY tagger_entities FROM '/Users/danielle.welter/Documents/TaggerDictionaries/tagger_dictionary/updates_21-7-2020/updated_tagger_names.tsv' ( DELIMITER '\t', QUOTE '§' )")
# c.execute("SELECT COUNT(1) from tagger_names")
# print(c.fetchall())

# c.execute("COPY tagger_names FROM '/Users/danielle.welter/Documents/TaggerDictionaries/tagger_dictionary/updates_21-7-2020/updated_tagger_preferred.tsv' ( DELIMITER '\t')")

# c.execute("COPY (select * from tagger_entities where entity in (11137,11128,227984,277944,290028,694007,694008,694006,693998,694001,393767,694015,11152,572290,572289,864596,693999,502102,1159907,1159906,1159903,1159904,1159908,1159902,1160968,1241933,1335626,1384461,766791,1541205,1590370,1699095,1766554,1264898,1892416,1920748,1508224,1964806,1508228,572288,1263720,1385427,1159905,1508220,31631,2697049)) TO 'protein_files/species_check.tsv' ( DELIMITER '\t')")

# table for uniprot data
c.execute("CREATE TABLE uniprot_main(uniprot_id VARCHAR, protein_name VARCHAR, gene_name VARCHAR, protein_alt_name VARCHAR, gene_synonym VARCHAR, orf_name VARCHAR)")
c.execute("COPY uniprot_main FROM 'input_files/uniprot-all-virus--name--gene-name--altname--synonyms--orfnames.txt' ( DELIMITER '\t')")
c.execute("update uniprot_main set uniprot_id = replace(uniprot_id, 'UNIPROT:', '')")

c.execute("SELECT COUNT(*) from uniprot_main")
print(c.fetchall())


# table for uniprot species
c.execute("create table uniprot_organism(uniprot_id VARCHAR, organism_name VARCHAR, ncbi_taxid integer, host_organism VARCHAR)")
c.execute("COPY uniprot_organism FROM 'input_files/uniprot-all-virus--org--NCBI_TaxId--HostOrganism.txt' ( DELIMITER '\t')")
c.execute("update uniprot_organism set uniprot_id = replace(uniprot_id, 'UNIPROT:', '')")

c.execute("select count(distinct ncbi_taxid) from uniprot_organism")

print(c.fetchall())

# c.execute("select u.protein_name, o.organism_name, u.uniprot_id from uniprot_main u join uniprot_organism o on o.uniprot_id = u.uniprot_id limit 25")
# c.execute("select u.protein_name, o.organism_name, count(u.uniprot_id) from uniprot_main u join uniprot_organism o on o.uniprot_id = u.uniprot_id group by u.protein_name, o.organism_name order by count(u.uniprot_id) desc limit 25")


# c.execute("create table uniprot_coronavirus as select * from uniprot_organism where organism_name like '%oronavirus%'")
# c.execute("select count(*) from uniprot_coronavirus")
# print(c.fetchall())
#
# c.execute("COPY (select distinct ncbi_taxid, organism_name from uniprot_coronavirus where ncbi_taxid not in (select entity from tagger_entities where type = -2 or type = -3)) "
#           "TO 'protein_files/missing_species.tsv' WITH (DELIMITER '\t')")
#
# c.execute("create table uniprot_subset as select * from uniprot_main where uniprot_id in (select uniprot_id from uniprot_coronavirus)")
#
# c.execute("COPY (select distinct u.uniprot_id, o.ncbi_taxid, u.protein_name, u.gene_name, u.protein_alt_name, u.gene_synonym, u.orf_name from uniprot_main u join uniprot_organism o on u.uniprot_id = o.uniprot_id ) "
#           "TO 'protein_files/all_uniprot_terms.tsv' WITH (DELIMITER '\t')")

c.execute("COPY (select distinct uniprot_id from uniprot_main) "
          "TO '../api_querying_service/input_files/uniprot_accessions.tsv' WITH (DELIMITER '\t')")


#
# # table for swissprot data
# c.execute("CREATE TABLE swissprot_main(swissprot_id VARCHAR, protein_name VARCHAR, gene_name VARCHAR, protein_alt_name VARCHAR, gene_synonym VARCHAR, orf_name VARCHAR)")
# c.execute("COPY swissprot_main FROM 'input_files/swissprot-all-virus--name--gene-name--altname--synonyms--orfnames.txt' ( DELIMITER '\t')")
# c.execute("update swissprot_main set swissprot_id = replace(swissprot_id, 'UNIPROT_SWISSPROT:', '')")
# # c.execute("SELECT COUNT(*) from swissprot_main")
# # print(c.fetchall())
#
# # table for swissprot species
# c.execute("create table swissprot_organism(swissprot_id VARCHAR, organism_name VARCHAR, ncbi_taxid integer, host_organism VARCHAR)")
# c.execute("COPY swissprot_organism FROM 'input_files/swissprot-all-virus--org--NCBI_TaxId--HostOrganism.txt' ( DELIMITER '\t')")
# # c.execute("select count(distinct ncbi_taxid) from swissprot_organism")
# # print(c.fetchall())

# stop here!
#
# # table for entrezgene data
# c.execute("CREATE TABLE entrez_main(entrez_id VARCHAR, gene_symbol VARCHAR, alias_symbol VARCHAR, protein_name VARCHAR)")
# c.execute("COPY entrez_main FROM 'input_files/ENTREZGENE-viruses--GeneSymbol--AliasSymbol--ProteinName.txt' ( DELIMITER '\t')")
# c.execute("SELECT COUNT(*) from entrez_main")
# print(c.fetchall())
# #
# # # table for entrezgene species
# c.execute("create table entrez_organism(entrez_id VARCHAR, organism_name VARCHAR, ncbi_taxid integer)")
# c.execute("COPY entrez_organism FROM 'input_files/ENTREZGENE-viruses--organism-name--NCBI-TaxId.txt' ( DELIMITER '\t')")
# c.execute("select count(distinct ncbi_taxid) from entrez_organism")
# print(c.fetchall())
# #
# # c.execute("create table entrez_coronavirus as select * from entrez_organism where organism_name like '%oronavirus%'")
# # c.execute("select count(*) from entrez_coronavirus")
# # print(c.fetchall())
# #
# # c.execute("COPY (select distinct ncbi_taxid, organism_name from entrez_coronavirus where ncbi_taxid not in (select entity from tagger_entities where type = -2 or type = -3)) "
# #           "TO 'protein_files/missing_species.tsv' WITH (DELIMITER '\t')")
# #
# # c.execute("create table entrez_subset as select * from entrez_main where entrez_id in (select entrez_id from entrez_coronavirus)")
# #
# c.execute("COPY (select distinct u.entrez_id, o.ncbi_taxid, u.protein_name, u.gene_symbol, u.alias_symbol from entrez_main u join entrez_organism o on u.entrez_id = o.entrez_id ) "
#           "TO 'protein_files/all_entrez_terms.tsv' WITH (DELIMITER '\t')")
#
#
# # # find the missing species
# c.execute("create table missing_species(ncbi_taxid integer, organism_name VARCHAR)")
# c.execute("insert into missing_species select distinct ncbi_taxid, organism_name from entrez_organism where ncbi_taxid not in (select distinct entity from tagger_entities where type = -2)")
# # # c.execute("insert into missing_species select distinct ncbi_taxid, organism_name from swissprot_organism where ncbi_taxid not in (select distinct entity from tagger_entities)")
# c.execute("insert into missing_species select distinct ncbi_taxid, organism_name from uniprot_organism where ncbi_taxid not in (select distinct entity from tagger_entities where type = -2)")
# c.execute("select count(distinct ncbi_taxid) from missing_species")
# print("Number of missing species " + str(c.fetchall()))
# # # c.execute("create table species_count(ncbi_taxid integer, count integer)")
# # # c.execute("insert into species_count select ncbi_taxid, count(*) from missing_species group by ncbi_taxid order by count(*) desc")
# # # c.execute("COPY (select * from missing_species where ncbi_taxid in (select ncbi_taxid from species_count where count > 1))"
# # #           "TO 'output_files/missing_species_duplicates.tsv' WITH (DELIMITER '\t')")
# #
# c.execute("COPY (select distinct ncbi_taxid from missing_species)"
#           "TO 'output_files/missing_species.tsv' WITH (DELIMITER '\t')")
# #
# # # find missing proteins
# # c.execute("create table missing_proteins(ncbi_taxid integer, organism_name VARCHAR)")
# # c.execute("insert into missing_species select distinct ncbi_taxid, organism_name from entrez_organism where ncbi_taxid not in (select distinct entity from tagger_entities)")
# # c.execute("insert into missing_species select distinct ncbi_taxid, organism_name from uniprot_organism where ncbi_taxid not in (select distinct entity from tagger_entities)")
# # # select distinct
# # # find missing genes
# #
# #
