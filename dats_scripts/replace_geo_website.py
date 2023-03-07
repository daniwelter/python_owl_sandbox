import copy
import json
import csv
import os
import argparse

def remove_website(object):
    if "extraProperties" in object:
        if len(object['extraProperties']) == 1:
            if object['extraProperties'][0]['category'] == 'website':
                del object['extraProperties']
    return object




def get_json(path):
    f = open(path, 'r')
    return json.loads(f.read())



if __name__ == '__main__':

    parser = argparse.ArgumentParser(description='Throw away script json schemas to csv')
    parser.add_argument('--path_to_files', '-p', help='Path to the JSON files, e.g. ~/metadata-schema/json_schema/', type=str)
    args = parser.parse_args()

    if not args.path_to_files:
        print("You must supply the path to the metadata schema directory")
        exit(2)
    else:
        base_schema_path = args.path_to_files

        schemas = [os.path.join(dirpath, f)
                   for dirpath, dirnames, files in os.walk(base_schema_path)
                   for f in files if f.endswith('.json') and not f.endswith('versions.json')]

        for path in schemas:
            print(path)
            schema = get_json(path)
            updated = remove_website(schema)

            with open(path, 'w') as outfile:
                json.dump(updated, outfile, indent=4)
