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

# c.execute("select * from tagger_entities where entity like 'HIV'")
# print(c.fetchall())

# c.execute("select * from tagger_entities where id in (select distinct id from tagger_names where name like 'HIV')")
# print(c.fetchdf())

# c.execute("COPY (select * from tagger_entities where id in (select distinct id from tagger_names where name like 'HIV')) to 'distinct_hiv.csv' (DELIMITER '\t')")

# c.execute("select * from tagger_names where name in ('tat','vpr','gag','vif','env','vpu','pol','rev','nef')")
# print(c.fetchdf())
#
# c.execute("select * from tagger_names where name in ('Protein Tat (Transactivating regulatory protein)','Protein Vpr (R ORF protein) (Viral protein R)','Gag polyprotein','Virion infectivity factor (Vif) (SOR protein) [Cleaved into: p17; p7]','Envelope glycoprotein gp160 (Env polyprotein) [Cleaved into: Surface protein gp120 (SU) (Glycoprotein 120) (gp120); Transmembrane protein gp41 (TM) (Glycoprotein 41) (gp41)]','Protein Vpu (U ORF protein) (Viral protein U)','POL polyprotein (Fragment)','Protein Rev (ART/TRS) (Anti-repression transactivator) (Regulator of expression of viral proteins)','Protein Nef (3ORF) (Negative factor) (F-protein) [Cleaved into: C-terminal core protein]')")
# print(c.fetchdf())

c.execute(" select * from tagger_names where name like 'pol'")
print(c.fetchdf())


c.execute(" select * from tagger_names where name like 'rev'")
print(c.fetchdf())
c.execute(" select * from tagger_names where name like 'tat'")
print(c.fetchdf())
c.execute(" select * from tagger_names where name like 'vif'")
print(c.fetchdf())
c.execute(" select * from tagger_names where name like 'nef'")
print(c.fetchdf())
c.execute(" select * from tagger_names where name like 'gag'")
print(c.fetchdf())
c.execute(" select * from tagger_names where name like 'env'")
print(c.fetchdf())
c.execute(" select * from tagger_names where name like 'vpu'")
print(c.fetchdf())
c.execute(" select * from tagger_names where name like 'vpr'")
print(c.fetchdf())