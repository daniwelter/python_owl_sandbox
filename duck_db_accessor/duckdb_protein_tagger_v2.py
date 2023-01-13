import duckdb


con = duckdb.connect()
c = con.cursor()

# c.execute("create sequence reflect_ids start 1016027959")
c.execute("create sequence reflect_ids start 1019500100")
c.execute("select nextval('reflect_ids')")
print(c.fetchall())

# table for tagger entities
c.execute("CREATE TABLE tagger_entities(id INTEGER, type integer, entity varchar)")
c.execute("COPY tagger_entities FROM '/Users/danielle.welter/Documents/TaggerDictionaries/full_dictionary/full_entities.tsv' ( DELIMITER '\t')")
print("Entities loaded")


# table for tagger names
c.execute("CREATE TABLE tagger_names(id INTEGER, name varchar)")
c.execute("COPY tagger_names FROM '/Users/danielle.welter/Documents/TaggerDictionaries/full_dictionary/full_names.tsv' ( DELIMITER '\t', QUOTE '§' )")
print("Names loaded")

c.execute("select count(*) from tagger_names")
print(c.fetchall())

c.execute("CREATE TABLE tagger_preferred(id INTEGER, preferred varchar)")

c.execute("COPY tagger_preferred FROM '/Users/danielle.welter/Documents/TaggerDictionaries/full_dictionary/full_preferred.tsv' ( DELIMITER '\t')")
print("Preferred loaded")

# 
# # table for uniprot data
# c.execute("CREATE TABLE uniprot_main(uniprot_id VARCHAR, protein_name VARCHAR, gene_name VARCHAR, protein_alt_name VARCHAR, gene_synonym VARCHAR, orf_name VARCHAR)")
# c.execute("COPY uniprot_main FROM 'input_files/uniprot-all-virus--name--gene-name--altname--synonyms--orfnames.txt' ( DELIMITER '\t')")
# c.execute("update uniprot_main set uniprot_id = replace(uniprot_id, 'UNIPROT:', '')")
# 
# c.execute("SELECT COUNT(*) from uniprot_main")
# print(c.fetchall())
# 
# 
# # table for uniprot species
# c.execute("create table uniprot_organism(uniprot_id VARCHAR, organism_name VARCHAR, ncbi_taxid integer, host_organism VARCHAR)")
# c.execute("COPY uniprot_organism FROM 'input_files/uniprot-all-virus--org--NCBI_TaxId--HostOrganism.txt' ( DELIMITER '\t')")
# c.execute("update uniprot_organism set uniprot_id = replace(uniprot_id, 'UNIPROT:', '')")
# 
# c.execute("select count(distinct ncbi_taxid) from uniprot_organism")
# 
# print(c.fetchall())
# 
# c.execute("select count(*) from uniprot_organism where uniprot_id in (select name from tagger_names)")
# 
# print(c.fetchall())
# 
# c.execute("create table new_uniprot as (select * from uniprot_organism where uniprot_id not in (select name from tagger_names))")
# 
# # 1. get species that arent' already in tagger
# c.execute("create table new_species(id integer, ncbi_taxid integer, organism_name VARCHAR)")
# c.execute("insert into new_species(ncbi_taxid, organism_name) select distinct ncbi_taxid, organism_name from uniprot_organism where ncbi_taxid not in (select distinct entity from tagger_entities where type = -2)")
# c.execute("update new_species set id = nextval('reflect_ids') where id IS NULL")
# 
# c.execute("COPY (select id, '-2', ncbi_taxid from new_species) TO 'output_28-9-20/species_entities.tsv' WITH (DELIMITER '\t')")
# c.execute("COPY (select id, organism_name from new_species) TO 'output_28-9-20/species_preferred.tsv' WITH (DELIMITER '\t')")
# print("New species done")
# 
# # 2. get proteins that aren't already in tagger names > entities = uniprot IDs
# c.execute("create table new_proteins(id integer, ncbi_taxid integer, uniprot_id varchar, protein_name VARCHAR)")
# c.execute("insert into new_proteins(ncbi_taxid, uniprot_id, protein_name) select n.ncbi_taxid, n.uniprot_id, p.protein_name from new_uniprot n join uniprot_main p on n.uniprot_id = p.uniprot_id")
# c.execute("update new_proteins set id = nextval('reflect_ids') where id IS NULL")
# 
# c.execute("COPY (select id, ncbi_taxid, uniprot_id from new_proteins) TO 'output_28-9-20/uniprot_entities.tsv' WITH (DELIMITER '\t')")
# c.execute("COPY (select id, protein_name from new_proteins) TO 'output_28-9-20/uniprot_preferred.tsv' WITH (DELIMITER '\t')")
# print("New proteins done")
# 
# c.execute("create table protein_synonyms(id integer, name varchar)")
# # c.execute("insert into protein_synonyms select n.id, p.gene_name from new_proteins n join uniprot_main p on p.uniprot_id = n.uniprot_id")
# c.execute("insert into protein_synonyms select n.id, p.protein_alt_name from new_proteins n join uniprot_main p on p.uniprot_id = n.uniprot_id")
# # c.execute("insert into protein_synonyms select n.id, p.gene_synonym from new_proteins n join uniprot_main p on p.uniprot_id = n.uniprot_id")
# # c.execute("insert into protein_synonyms select n.id, p.orf_name from new_proteins n join uniprot_main p on p.uniprot_id = n.uniprot_id")
# 
# c.execute("select count(*) from protein_synonyms")
# print(c.fetchall())
# 
# c.execute("select count(*) from protein_synonyms where name is not null")
# print(c.fetchall())
# 
# c.execute("COPY (select * from protein_synonyms where name is not null) TO 'output_28-9-20/uniprot_names.tsv' WITH (DELIMITER '\t')")
# print("New protein synonyms done")


# c.execute("COPY (select ) TO 'output_28-9-20/.tsv' WITH (DELIMITER '\t')")


# table for entrez data
c.execute("CREATE TABLE entrez_main(entrez_id VARCHAR, gene_name VARCHAR, alias VARCHAR, protein_name VARCHAR)")
c.execute("COPY entrez_main FROM 'input_files/ENTREZGENE-viruses--GeneSymbol--AliasSymbol--ProteinName.txt' ( DELIMITER '\t')")
c.execute("update entrez_main set entrez_id = replace(entrez_id, 'ENTREZGENE:', '')")

c.execute("SELECT COUNT(*) from entrez_main")
print(c.fetchall())


# table for entrez species
c.execute("create table entrez_organism(entrez_id VARCHAR, organism_name VARCHAR, ncbi_taxid integer)")
c.execute("COPY entrez_organism FROM 'input_files/ENTREZGENE-viruses--organism-name--NCBI-TaxId.txt' ( DELIMITER '\t')")
c.execute("update entrez_organism set entrez_id = replace(entrez_id, 'ENTREZGENE:', '')")

c.execute("select count(distinct ncbi_taxid) from entrez_organism")

print(c.fetchall())

# print("Existing gene names: ")
# c.execute("select count(distinct m.gene_name, t.type) from entrez_main m join entrez_organism o on m.entrez_id = o.entrez_id join tagger_entities t on t.type = o.ncbi_taxid where m.gene_name in (select name from tagger_names)")
# print(c.fetchall())
# c.execute("select count(distinct m.gene_name, t.type) from entrez_main m join entrez_organism o on m.entrez_id = o.entrez_id join tagger_entities t on t.type = o.ncbi_taxid where m.gene_name in (select preferred from tagger_preferred)")
# print(c.fetchall())
#
# print("Existing protein names: ")
# c.execute("select count(distinct m.protein_name, t.type) from entrez_main m join entrez_organism o on m.entrez_id = o.entrez_id join tagger_entities t on t.type = o.ncbi_taxid where m.protein_name in (select name from tagger_names)")
# print(c.fetchall())
# c.execute("select count(distinct m.protein_name, t.type) from entrez_main m join entrez_organism o on m.entrez_id = o.entrez_id join tagger_entities t on t.type = o.ncbi_taxid where m.protein_name in (select preferred from tagger_preferred)")
# print(c.fetchall())

# c.execute("create table new_entrez as (select * from entrez_organism where entrez_id not in (select name from tagger_names))")

# 1. get species that arent' already in tagger
c.execute("create table new_species(id integer, ncbi_taxid integer, organism_name VARCHAR)")
c.execute("insert into new_species(ncbi_taxid, organism_name) select distinct ncbi_taxid, organism_name from entrez_organism where ncbi_taxid not in (select distinct entity from tagger_entities where type = -2)")
c.execute("update new_species set id = nextval('reflect_ids') where id IS NULL")

c.execute("COPY (select id, '-2', ncbi_taxid from new_species) TO 'output_1-10-20/species_entities.tsv' WITH (DELIMITER '\t')")
c.execute("COPY (select id, organism_name from new_species) TO 'output_1-10-20/species_preferred.tsv' WITH (DELIMITER '\t')")
print("New species done")

# 2. get proteins that aren't already in tagger names > entities = entrez IDs
c.execute("create table new_proteins(id integer, ncbi_taxid integer, entrez_id varchar, gene_name VARCHAR)")
c.execute("insert into new_proteins(ncbi_taxid, entrez_id, gene_name) select n.ncbi_taxid, n.entrez_id, p.gene_name from entrez_organism n join entrez_main p on n.entrez_id = p.entrez_id")
c.execute("update new_proteins set id = nextval('reflect_ids') where id IS NULL")

c.execute("COPY (select id, ncbi_taxid, entrez_id from new_proteins) TO 'output_1-10-20/entrez_entities.tsv' WITH (DELIMITER '\t')")
c.execute("COPY (select id, gene_name from new_proteins) TO 'output_1-10-20/entrez_preferred.tsv' WITH (DELIMITER '\t')")
print("New proteins done")

c.execute("create table protein_synonyms(id integer, name varchar)")
# c.execute("insert into protein_synonyms select n.id, p.gene_name from new_proteins n join entrez_main p on p.entrez_id = n.entrez_id")
c.execute("insert into protein_synonyms select n.id, p.protein_name from new_proteins n join entrez_main p on p.entrez_id = n.entrez_id")
c.execute("insert into protein_synonyms select n.id, p.alias from new_proteins n join entrez_main p on p.entrez_id = n.entrez_id")
# c.execute("insert into protein_synonyms select n.id, p.orf_name from new_proteins n join entrez_main p on p.entrez_id = n.entrez_id")

c.execute("select count(*) from protein_synonyms")
print(c.fetchall())

c.execute("select count(*) from protein_synonyms where name is not null")
print(c.fetchall())

c.execute("COPY (select * from protein_synonyms where name is not null) TO 'output_1-10-20/entrez_names.tsv' WITH (DELIMITER '\t')")
print("New protein synonyms done")





