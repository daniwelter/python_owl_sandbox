import argparse
import logging
import os
import json


ignore_data = ['@context', 'description']

class CSVGenerator:

    def __init__(self):
        self.logger = logging.getLogger(__name__)


    def generateSchemaSummary(self,schemas):
        file = open("schema_summary_old.tsv", "w")

        file.write("Schema\tRequiredProps?\tAdditionalProps?\tDescription\n")

        for path in schemas:
            if '.md' not in path:
                schema = self.get_json_from_file(path)

                file.write(schema["title"] + "\t"
                           + ("1" if "required" in schema else "0") + "\t"
                           + ("1" if "additionalProperties" in schema else "0") + "\t"
                           + schema["description"] + "\n")


    def generatePropertiesSummary(self, json_files):

        # file = open("properties_data.tsv", "w")

        # file.write("Property\tDescription\tType\tRequired\tSchema?\n")

        all_properties = []
        all_values = {}
        for path in json_files:
            data = self.get_json_from_file(path)

            for prop in data.keys():
                if prop not in ignore_data:
                    if prop not in all_properties:
                        all_properties.append(prop)
                    if prop not in all_values.keys():
                        all_values[prop] = []

                    if type(data[prop]) == list or type(data[prop]) == dict:
                            self.process_object(prop, data[prop], all_properties, all_values)

                    else:
                        all_values[prop].append(data[prop])


        prop_file = open("properties.tsv", "w")

        for property in all_properties:
            prop_file.write(property + "\n")

        prop_file.close()

        data_file = open("values.tsv", "w")

        for property in all_values.keys():
            line = property
            for val in all_values[property]:
                line = line + '\t' +  str(val)
            data_file.write(line + "\n")

        data_file.close()


    def process_object(self, prop, object, all_properties, all_values):
        if type(object) == list:
            for item in object:
                if type(item) == list or type(item) == dict:
                    self.process_object(prop, item, all_properties, all_values)

        elif type(object) == dict:
            for subprop in object.keys():
                if subprop not in ignore_data:
                    chain_prop = prop + '.' + subprop
                    if type(object[subprop]) == list or type(object[subprop]) == dict:
                        self.process_object(chain_prop, object[subprop], all_properties, all_values)
                    else:
                        if subprop == '@type':
                            chain_prop = chain_prop + '[' + object[subprop] + ']'
                        if chain_prop not in all_properties:
                            all_properties.append(chain_prop)
                        if chain_prop not in all_values.keys():
                            all_values[chain_prop] = []
                        if object[subprop] not in all_values[chain_prop]:
                            all_values[chain_prop].append(object[subprop])

    def get_values(self, data, prop):
        if type(data[prop]) == list:
            for item in data[prop]:
                val = item
        elif type(data[prop]) == dict:
            for subprop in data[prop].keys:
                val = subprop
        return val


    def get_json_from_file(self, filename):
        """Loads json from a file."""
        f = open(filename, 'r')
        return json.loads(f.read())

if __name__ == '__main__':

    parser = argparse.ArgumentParser(description='Throw away script json schemas to csv')
    parser.add_argument('--path_to_files', '-p', help='Path to the JSON files, e.g. ~/metadata-schema/json_schema/', type=str)
    args = parser.parse_args()

    generator = CSVGenerator()

    if not args.path_to_files:
        print("You must supply the path to the metadata schema directory")
        exit(2)
    else:
        base_schema_path = args.path_to_files

        schemas = [os.path.join(dirpath, f)
                   for dirpath, dirnames, files in os.walk(base_schema_path)
                   for f in files if f.endswith('.json') and not f.endswith('versions.json')]

        # generator.generateSchemaSummary(schemas)

        generator.generatePropertiesSummary(schemas)


