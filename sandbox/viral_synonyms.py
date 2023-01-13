import duckdb


con = duckdb.connect()
c = con.cursor()


# table for tagger entities
c.execute("CREATE TABLE viral_entities(id INTEGER)")
c.execute("COPY viral_entities FROM '/Users/danielle.welter/Documents/COVID-19/Viruses/reflect_ids.txt' ( DELIMITER '\t')")
print("Entities loaded")


# table for tagger names
c.execute("CREATE TABLE tagger_names(id INTEGER, name varchar)")
c.execute("COPY tagger_names FROM '/Users/danielle.welter/Documents/COVID-19/Viruses/full_names.tsv' ( DELIMITER '\t', QUOTE '§' )")
print("Names loaded")

c.execute("select count(*) from tagger_names")
print(c.fetchall())

c.execute("Select count(*) from tagger_names where id in (select id from viral_entities)")
print(c.fetchall()
      )
c.execute("COPY (select * from tagger_names where id in (select id from viral_entities)) "
          "TO '/Users/danielle.welter/Documents/COVID-19/Viruses/viral_syns.tsv' WITH (DELIMITER '\t')")

# import csv
#
# viral_entities = "/Users/danielle.welter/Documents/COVID-19/Viruses/reflect_ids.txt"
# syns_file = "/Users/danielle.welter/Documents/COVID-19/Viruses/full_names.tsv"
#
# all_syns = {}
# entities = []
# with open(syns_file) as tsvfile:
#     reader = csv.reader(tsvfile, delimiter='\t')
#     for row in reader:
#         if row[0] not in all_syns:
#             print(row[0])
#             all_syns[row[0]] = [row[1]]
#         else:
#             all_syns[row[0]].append(row[1])
#
#     print(len(all_syns.keys()))
#
#     with open(viral_entities) as entitiesfile:
#         reader = csv.reader(entitiesfile)
#         for row in reader:
#             entities.append(row[0])
#         with open('viral_synonyms.tsv') as out_file:
#             tsv_writer = csv.writer(out_file, delimiter='\t')
#
#             for entity in entities:
#                 if entity in all_syns.keys():
#                     syns = all_syns[entity]
#
#                     for s in syns:
#                         tsv_writer.writerow([entity, s])