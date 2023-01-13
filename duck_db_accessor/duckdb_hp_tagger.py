import duckdb


con = duckdb.connect()
c = con.cursor()

# table for tagger entities
c.execute("CREATE TABLE tagger_entities(reflect_id INTEGER primary key, type integer, entity varchar)")
c.execute("COPY tagger_entities FROM 'tagger_dictionaries/tagger_entities.tsv' ( DELIMITER '\t')")

# table for tagger names
c.execute("CREATE TABLE tagger_names(reflect_id INTEGER, name varchar)")
c.execute("COPY tagger_names FROM 'tagger_dictionaries/tagger_names.tsv' ( DELIMITER '\t', QUOTE '§' )")


c.execute("CREATE TABLE tagger_preferred(reflect_id INTEGER, preferred varchar)")
c.execute("COPY tagger_preferred FROM 'tagger_dictionaries/tagger_preferred.tsv' ( DELIMITER '\t')")

c.execute("CREATE TABLE tagger_texts(reflect_id INTEGER, text varchar)")
c.execute("COPY tagger_texts FROM 'tagger_dictionaries/tagger_texts.tsv' ( DELIMITER '\t', QUOTE '§' )")

c.execute("CREATE TABLE tagger_groups(reflect_id INTEGER, second_id INTEGER)")
c.execute("COPY tagger_groups FROM 'tagger_dictionaries/tagger_groups.tsv' ( DELIMITER '\t')")

c.execute("CREATE TABLE abnormal_phenotypes(uri varchar, hp_id varchar, preferred varchar, def varchar)")
c.execute("COPY abnormal_phenotypes FROM 'hp_v2/abnormal_phenotypes.tsv' ( DELIMITER '\t')")
c.execute("update abnormal_phenotypes set hp_id = replace(hp_id, '_', ':')")


c.execute("CREATE TABLE abnormal_pheno_syns(uri varchar, syn_type varchar, preferred varchar, hp_id varchar)")
c.execute("COPY abnormal_pheno_syns FROM 'hp_v2/abnormal_pheno_syns.tsv' ( DELIMITER '\t')")
c.execute("update abnormal_pheno_syns set hp_id = replace(hp_id, '_', ':')")

c.execute("select count(*) from abnormal_phenotypes")
print("Total abnormal phenotypes: ")
print(c.fetchall())
c.execute("select count(*) from tagger_entities where type = -40")
print("Total HP in tagger: ")
print(c.fetchall())

c.execute("select count(*) from tagger_entities where type = -40 and entity in (select hp_id from abnormal_phenotypes)")
print("Total abnormal phenotypes in tagger: ")
print(c.fetchall())
c.execute("select count(*) from abnormal_phenotypes where hp_id in (select entity from tagger_entities where type = -40)")
print("Total tagger entities in abnormal phenotypes: ")
print(c.fetchall())

c.execute("select count(*) from abnormal_phenotypes where hp_id not in (select entity from tagger_entities where type = -40)")
print("Total abnormal phenotypes not in tagger: ")
print(c.fetchall())
c.execute("create table missing_in_tagger as select * from abnormal_phenotypes where hp_id not in (select entity from tagger_entities where type = -40)")
c.execute("create table missing_synonyms as select * from abnormal_pheno_syns where hp_id not in (select entity from tagger_entities where type = -40)")
# c.execute("select count(*) from tagger_entities where type = -40 and entity not in (select hp_id from abnormal_phenotypes)")
# print(c.fetchall())

c.execute("create table missing_test as (select distinct entity from tagger_entities where type = -40 and entity in (select hp_id from abnormal_phenotypes))")
c.execute("create table wrong_in_tagger as (select * from tagger_entities where type = -40 and entity not in (select entity from missing_test))")
c.execute("drop table missing_test")
c.execute("select count(*) from wrong_in_tagger")
print("Total wrong HP terms in tagger: ")
print(c.fetchall())

c.execute("delete from tagger_entities where reflect_id in (select reflect_id from wrong_in_tagger)")
c.execute("delete from tagger_preferred where reflect_id in (select reflect_id from wrong_in_tagger)")
c.execute("delete from tagger_names where reflect_id in (select reflect_id from wrong_in_tagger)")
c.execute("delete from tagger_texts where reflect_id in (select reflect_id from wrong_in_tagger)")
c.execute("delete from tagger_groups where reflect_id in (select reflect_id from wrong_in_tagger)")
c.execute("delete from tagger_groups where second_id in (select reflect_id from wrong_in_tagger)")

c.execute("select count(*) from tagger_entities where type = -40")
print("Total tagger entities after deletion: ")
print(c.fetchall())

# c.execute("copy tagger_entities to 'output_files/tagger_entities.tsv' ( DELIMITER '\t')")
# c.execute("copy tagger_preferred to 'output_files/tagger_preferred.tsv' ( DELIMITER '\t')")
# c.execute("copy tagger_names to 'output_files/tagger_names.tsv' ( DELIMITER '\t')")
# c.execute("copy tagger_groups to 'output_files/tagger_groups.tsv' ( DELIMITER '\t')")
# c.execute("copy tagger_texts to 'output_files/tagger_texts.tsv' ( DELIMITER '\t')")
c.execute("copy missing_in_tagger to 'output_files/missing_phenos.tsv' ( DELIMITER '\t')")
c.execute("copy missing_synonyms to 'output_files/missing_syns.tsv' ( DELIMITER '\t')")

