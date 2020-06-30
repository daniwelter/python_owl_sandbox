import duckdb


con = duckdb.connect()
c = con.cursor()

# table for tagger entities
c.execute("CREATE TABLE tagger_entities(id INTEGER, type integer, entity varchar)")
c.execute("COPY tagger_entities FROM 'tagger_dictionaries/tagger_entities.tsv' ( DELIMITER '\t')")
# c.execute("SELECT COUNT(distinct type) from tagger_entities")
# print(c.fetchall())

# table for tagger names
c.execute("CREATE TABLE tagger_names(id INTEGER, name varchar)")
c.execute("COPY tagger_names FROM 'tagger_dictionaries/tagger_names.tsv' ( DELIMITER '\t', QUOTE '§' )")
# c.execute("SELECT COUNT(1) from tagger_names")
# print(c.fetchall())

c.execute("COPY tagger_names FROM 'tagger_dictionaries/tagger_preferred.tsv' ( DELIMITER '\t')")

# table for uniprot data
c.execute("CREATE TABLE uniprot_main(uniprot_id VARCHAR, protein_name VARCHAR, gene_name VARCHAR, protein_alt_name VARCHAR, gene_synonym VARCHAR, orf_name VARCHAR)")
c.execute("COPY uniprot_main FROM 'input_files/uniprot-all-virus--name--gene-name--altname--synonyms--orfnames.txt' ( DELIMITER '\t')")
c.execute("update uniprot_main set uniprot_id = replace(uniprot_id, 'UNIPROT:', '')")

# c.execute("SELECT COUNT(*) from uniprot_main")
# print(c.fetchall())

# table for uniprot species
c.execute("create table uniprot_organism(uniprot_id VARCHAR, organism_name VARCHAR, ncbi_taxid integer, host_organism VARCHAR)")
c.execute("COPY uniprot_organism FROM 'input_files/uniprot-all-virus--org--NCBI_TaxId--HostOrganism.txt' ( DELIMITER '\t')")
# c.execute("select count(distinct ncbi_taxid) from uniprot_organism")
# print(c.fetchall())
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

# table for entrezgene data
c.execute("CREATE TABLE entrez_main(entrez_id VARCHAR, gene_symbol VARCHAR, alias_symbol VARCHAR, protein_name VARCHAR)")
c.execute("COPY entrez_main FROM 'input_files/ENTREZGENE-viruses--GeneSymbol--AliasSymbol--ProteinName.txt' ( DELIMITER '\t')")
# c.execute("SELECT COUNT(*) from entrez_main")
# print(c.fetchall())

# table for entrezgene species
c.execute("create table entrez_organism(entrez_id VARCHAR, organism_name VARCHAR, ncbi_taxid integer)")
c.execute("COPY entrez_organism FROM 'input_files/ENTREZGENE-viruses--organism-name--NCBI-TaxId.txt' ( DELIMITER '\t')")
# c.execute("select count(distinct ncbi_taxid) from entrez_organism")
# print(c.fetchall())

# find the missing species
c.execute("create table missing_species(ncbi_taxid integer, organism_name VARCHAR)")
c.execute("insert into missing_species select distinct ncbi_taxid, organism_name from entrez_organism where ncbi_taxid not in (select distinct entity from tagger_entities)")
# c.execute("insert into missing_species select distinct ncbi_taxid, organism_name from swissprot_organism where ncbi_taxid not in (select distinct entity from tagger_entities)")
c.execute("insert into missing_species select distinct ncbi_taxid, organism_name from uniprot_organism where ncbi_taxid not in (select distinct entity from tagger_entities)")
c.execute("select count(distinct ncbi_taxid) from missing_species")
print("Number of missing species " + str(c.fetchall()))
# c.execute("create table species_count(ncbi_taxid integer, count integer)")
# c.execute("insert into species_count select ncbi_taxid, count(*) from missing_species group by ncbi_taxid order by count(*) desc")
# c.execute("COPY (select * from missing_species where ncbi_taxid in (select ncbi_taxid from species_count where count > 1))"
#           "TO 'output_files/missing_species_duplicates.tsv' WITH (DELIMITER '\t')")

c.execute("COPY (select distinct ncbi_taxid from missing_species)"
          "TO 'output_files/missing_species.tsv' WITH (DELIMITER '\t')")

# find missing proteins
c.execute("create table missing_proteins(ncbi_taxid integer, organism_name VARCHAR)")
c.execute("insert into missing_species select distinct ncbi_taxid, organism_name from entrez_organism where ncbi_taxid not in (select distinct entity from tagger_entities)")
c.execute("insert into missing_species select distinct ncbi_taxid, organism_name from uniprot_organism where ncbi_taxid not in (select distinct entity from tagger_entities)")
# select distinct
# find missing genes


