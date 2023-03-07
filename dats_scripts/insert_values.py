import argparse
import csv
import json
import logging
import os
import copy

TYPES = ['value', 'category', 'name']

IDENTIFIER = {
                "@type": "Identifier",
                "@context": "https://w3id.org/dats/context/sdo/identifier_info_sdo_context.jsonld",
                "identifier": "",
            }


def insert_values(object, values):
    # for prop in object.keys():
    process_object(object, values)

    return object

def process_object(object, values):

    if type(object) == list:
        for item in object:
            process_object(item, values)

    elif type(object) == dict:
        keys = object.copy().keys()
        for prop in keys:
            if prop in ['value', 'category']:
                if object[prop] in values.keys():
                    if prop == 'value':
                        if 'valueIRI' in object and object['valueIRI'] != '' and object['valueIRI'] != values[object[prop]]:
                            print(object[prop] + '\t' + object['valueIRI'])
                        else:
                            object['valueIRI'] = values[object[prop]]
                    if prop == 'category':
                        if 'categoryIRI' in object and object['categoryIRI'] != '' and object['categoryIRI'] != values[object[prop]]:
                            print(object[prop] + '\t' + object['categoryIRI'])
                        else:
                            object['categoryIRI'] = values[object[prop]]

            elif prop == 'name' and type(object[prop]) != dict:
                if object[prop] in values.keys():
                    if 'identifier' in object:
                        if 'identifier' in object['identifier']:
                            if object['identifier']['identifier'] != '' and object['identifier']['identifier'] != values[object[prop]]:
                                print(object[prop] + '\t' + object['identifier']['identifier'])
                            else:
                                object['identifier'] = copy.deepcopy(IDENTIFIER)
                                object['identifier']['identifier'] = values[object[prop]]
                    else:
                        object['identifier'] = copy.deepcopy(IDENTIFIER)
                        object['identifier']['identifier'] = values[object[prop]]
            else:
                process_object(object[prop], values)


def get_json(file_path):
    f = open(file_path, 'r')
    return json.loads(f.read())


if __name__ == '__main__':

    values_file = 'key_value_pairs.tsv'

    with open(values_file, encoding='utf-8') as data_file:
        data = csv.reader(data_file, delimiter='\t')
        results = {}
        for row in data:
            results[row[0]] = row[1]

        base_schema_path = '../data/geo_projects'

        projects = [os.path.join(dirpath, f)
                   for dirpath, dirnames, files in os.walk(base_schema_path)
                   for f in files if f.endswith('.json') and not f.endswith('versions.json')]

        for project in projects:
            current = get_json(project)
            updated = insert_values(current, results)

            new_file = 'updated/' + current['acronym'] + '.json'
            with open(new_file, 'w') as outfile:
                json.dump(updated, outfile, indent=4)
