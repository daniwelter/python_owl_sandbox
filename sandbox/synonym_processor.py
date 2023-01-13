import csv

path_to_file = "../duck_db_accessor/output_28-9-20/uniprot_names.tsv"
uniprot_syns = {}
with open(path_to_file) as tsvfile:
    reader = csv.reader(tsvfile, delimiter='\t')
    for row in reader:
        uniprot_syns[row[0]] = row[1]

    print(len(uniprot_syns.keys()))

    needs_splitting = {}
    split = {}

    for key in uniprot_syns.keys():
        if "{" in uniprot_syns[key] or "|" in uniprot_syns[key]:
            needs_splitting[key] = uniprot_syns[key]
            syns = []

            if "{" in uniprot_syns[key]:
                tokens = uniprot_syns[key].split("{")
                for t in tokens:
                    if "}" in t:
                        t= t.replace("}", "")
                    if "|" in t:
                        t2 = t.split("|")

                        for e in t2:
                            if "}" in e:
                                e= e.replace("}", "")
                            if isinstance(e, int):
                                e = str(e)
                            syns.append(e)
                    else:
                        if isinstance(t, int):
                            t = str(t)
                        syns.append(t)

            if "|" in uniprot_syns:
                tokens = uniprot_syns[key].split("|")

                for t in tokens:
                    if isinstance(t, int):
                        t = str(t)
                    syns.append(t)





        else:
            syns = [uniprot_syns[key]]

        for s in syns:
            if "ECO" in s:
                syns.remove(s)
            elif "HAMAP" in s:
                syns.remove(s)
            elif "PubMed" in s:
                syns.remove(s)
            elif "RuleBase" in s:
                syns.remove(s)
        syns = [s.replace("EMBL:", "") for s in syns]
        syns = [s.strip() for s in syns]

        split[key] = syns

    with open('../duck_db_accessor/output_28-9-20/uniprot_names_split.tsv', 'w') as out_file:
        tsv_writer = csv.writer(out_file, delimiter='\t')

        for key in split.keys():
            for syn in split[key]:
                if "HAMAP" not in syn and "ECO" not in syn and "PubMed" not in syn and "RuleBase" not in syn:
                    tsv_writer.writerow([key, syn])