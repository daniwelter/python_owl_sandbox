import duckdb


con = duckdb.connect()
c = con.cursor()

c.execute("CREATE TABLE omop_concepts(concept_id varchar, concept_name varchar, domain_id varchar, vocabulary_id varchar, concept_class_id varchar, standard_concept varchar, concept_code varchar,  valid_start_date varchar, 	valid_end_date varchar, invalid_reason varchar)")
c.execute("COPY omop_concepts FROM '/Users/danielle.welter/Development/python_sandbox/biomap_omop/omop_concepts.csv' ( DELIMITER '\t', QUOTE '§' )")
print("Entities loaded")

c.execute("CREATE TABLE biomap(concept varchar, identifier varchar, vocabulary varchar, code varchar)")
c.execute("COPY biomap FROM '/Users/danielle.welter/Development/python_sandbox/biomap_omop/biomap_dd_pt2.tsv' ( DELIMITER '\t')")
print("Data dictionary loaded")


c.execute("CREATE TABLE biomap_omop as (select distinct b.*, o.* from biomap b "
          "left join omop_concepts o on o.concept_code = b.code and o.vocabulary_id = b.vocabulary)")
c.execute("select count(*) from biomap_omop")
print(c.fetchall())

c.execute("CREATE TABLE omop_rels(concept_id_1 varchar, concept_id_2 varchar, relationship_id varchar, valid_start_date varchar, valid_end_date varchar, invalid_reason varchar)")
c.execute("COPY omop_rels FROM '/Users/danielle.welter/Development/python_sandbox/biomap_omop/omop_rels.csv' ( DELIMITER '\t', QUOTE '§' )")



c.execute("CREATE TABLE nonstd_to_std as (select distinct b.concept, b.identifier, b.vocabulary, b.code, c.* from biomap_omop b "
          "join omop_rels r on r.concept_id_1 = b.concept_id "
          "join omop_concepts c on c.concept_id = r.concept_id_2 "
          "where r.relationship_id = 'Maps to')")

c.execute("select count(*) from nonstd_to_std")
print(c.fetchall())


c.execute("CREATE TABLE biomap_omop_label as (select b.concept, b.identifier, b.vocabulary, b.code, o.* from biomap_omop b "
          "left join omop_concepts o on o.concept_name = b.concept "
          "where b.concept_id = '')")

c.execute("select count(*) from biomap_omop_label")

print(c.fetchall())



# c.execute("COPY (select distinct * from nonstd_to_std) "
#            "TO 'biomap_omop_mappings_to_std.tsv' WITH (DELIMITER '\t')")


# c.execute("COPY (select distinct b.*, o.* from biomap b "
#           "left join omop_concepts o on o.concept_code = b.code and o.vocabulary_id = b.vocabulary) "
#           "TO 'biomap_omop_mappings_by_id.tsv' WITH (DELIMITER '\t')")


# c.execute("CREATE TABLE standard_mappings as (select * from biomap where trim(lower(concept)) in (select trim(lower(concept_name)) from omop_concepts where standard_concept = 'S'))")
#
# c.execute(("select count(*) from standard_mappings"))
# print("Standard concept mapping available: ")
# print(c.fetchall())
#
# c.execute("CREATE TABLE nonstandard_mappings as (select * from biomap where trim(lower(concept)) in (select trim(lower(concept_name)) from omop_concepts where standard_concept != 'S'))")
#
# c.execute(("select count(*) from nonstandard_mappings"))
# print("Non-standard concept mapping available: ")
# print(c.fetchall())
#
# c.execute("CREATE TABLE need_review as (select * from biomap where trim(lower(concept)) not in (select trim(lower(concept_name)) from omop_concepts) and identifier != 'none')")
#
# c.execute("select count(*) from need_review")
# print("No mapping available in OMOP: ")
# print(c.fetchall())
#
# c.execute("CREATE TABLE need_mapping as (select * from biomap where trim(lower(concept)) not in (select trim(lower(concept_name)) from omop_concepts) and identifier = 'none')")
# c.execute("select count(*) from need_mapping")
# print("Completely unmapped: ")
# print(c.fetchall())
#
# c.execute("COPY (select b.*, o.* from standard_mappings b "
#           "join omop_concepts o on trim(lower(o.concept_name)) = trim(lower(b.concept))"
#           "where o.standard_concept = 'S') TO 'standard_mappings.tsv' WITH (DELIMITER '\t')")
#
# c.execute("COPY (select b.*, o.* from nonstandard_mappings b "
#           "join omop_concepts o on trim(lower(o.concept_name)) = trim(lower(b.concept))"
#           "where o.standard_concept != 'S') TO 'nonstandard_mappings.tsv' WITH (DELIMITER '\t')")
#
# c.execute("COPY (select * from need_review) "
#           "TO 'need_review.tsv' WITH (DELIMITER '\t')")
#
# c.execute("COPY (select * from need_mapping) "
#           "TO 'need_mapping.tsv' WITH (DELIMITER '\t')")
