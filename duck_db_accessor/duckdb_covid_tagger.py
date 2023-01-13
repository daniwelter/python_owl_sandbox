import duckdb


con = duckdb.connect()
c = con.cursor()

# table for tagger entities
c.execute("CREATE TABLE tagger_entities(reflect_id INTEGER primary key, type integer, entity varchar)")
c.execute("COPY tagger_entities FROM 'tagger_dictionaries/updated_tagger/updated_tagger_entities.tsv' ( DELIMITER '\t')")

c.execute("CREATE TABLE covid_entities(entity varchar)")
c.execute("COPY covid_entities FROM '/Users/danielle.welter/Documents/COVID-19/COVID-ontology/COVID_concepts.csv'")
c.execute("update covid_entities set entity = replace(entity, 'NCBITaxon:', '')")

c.execute("select count(*) from covid_entities where entity in (select entity from tagger_entities)")
print(c.fetchall())

c.execute("select count(*) from covid_entities where entity not in (select entity from tagger_entities)")
print(c.fetchall())

c.execute("copy (select * from tagger_entities where entity in (select entity from covid_entities)) to 'output_files/covid_existing_v2.tsv'")


c.execute("copy (select * from covid_entities where entity not in (select entity from tagger_entities)) to 'output_files/covid_new_v2.tsv'")


# # table for tagger names
# c.execute("CREATE TABLE tagger_names(reflect_id INTEGER, name varchar)")
# c.execute("COPY tagger_names FROM 'tagger_dictionaries/updated_tagger/updated_tagger_names.tsv' ( DELIMITER '\t', QUOTE '§' )")
#
# c.execute("CREATE TABLE tagger_preferred(reflect_id INTEGER, preferred varchar)")
# c.execute("COPY tagger_preferred FROM 'tagger_dictionaries/updated_tagger/updated_tagger_preferred.tsv' ( DELIMITER '\t')")
#
# c.execute("CREATE TABLE tagger_texts(reflect_id INTEGER, text varchar)")
# c.execute("COPY tagger_texts FROM 'tagger_dictionaries/updated_tagger/updated_tagger_texts.tsv' ( DELIMITER '\t', QUOTE '§' )")
#
# c.execute("CREATE TABLE tagger_groups(reflect_id INTEGER, second_id INTEGER)")
# c.execute("COPY tagger_groups FROM 'tagger_dictionaries/updated_tagger/updated_tagger_groups.tsv' ( DELIMITER '\t')")
#
#
