import argparse
import logging
import os
import json

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


    def generatePropertiesSummary(self, schemas):
        file = open("json_schema_fields_old.tsv", "w")

        file.write("Property\tDescription\tType\tRequired\tSchema?\n")

        for path in schemas:
            if '.md' not in path:
                schema = self.get_json_from_file(path)

                required = []

                if "required" in schema:
                    required = schema["required"]


                for property in schema["properties"]:
                    type = "N/A"
                    if "type" in schema["properties"][property]:
                        type = schema["properties"][property]["type"]

                        if type == "array":
                            t = schema["properties"][property]["items"]

                            if isinstance(t, dict):
                                if "$ref" in t:
                                    type = t["$ref"]
                                elif "anyOf" in t:
                                    l = []
                                    for e in t["anyOf"]:
                                        if "$ref" in e:
                                            l.append(e["$ref"])
                                    type = ",".join(l)

                            elif isinstance(t, list):
                                type = ",".join(t)
                            print(type)

                    elif "$ref" in schema["properties"][property]:
                        type = schema["properties"][property]["$ref"]
                        print(type)

                    elif "anyOf" in schema["properties"][property]:
                        options = schema["properties"][property]["anyOf"]
                        t = ""
                        for opt in options:
                            if "type" in opt:
                                if t == "":
                                    t = opt["type"]
                                else:
                                    t = t + ", " + opt["type"]

                        if t != "":
                            type = t
                        print(type)

                    file.write(property + "\t" +
                          (schema["properties"][property]["description"] if "description" in schema["properties"][property] else "N/A") + "\t" +
                          type + "\t"
                               + ("1" if property in required else "0")  + "\t"
                               + schema["title"] + "\n")



        file.close()

    def get_json_from_file(self, filename):
        """Loads json from a file."""
        f = open(filename, 'r')
        return json.loads(f.read())

if __name__ == '__main__':

    parser = argparse.ArgumentParser(description='Throw away script json schemas to csv')
    parser.add_argument('--path_to_schemas', '-p', help='Path to the JSON schemas, e.g. ~/metadata-schema/json_schema/', type=str)
    args = parser.parse_args()

    generator = CSVGenerator()

    if not args.path_to_schemas:
        print("You must supply the path to the metadata schema directory")
        exit(2)
    else:
        base_schema_path = args.path_to_schemas

        schemas = [os.path.join(dirpath, f)
                   for dirpath, dirnames, files in os.walk(base_schema_path)
                   for f in files if f.endswith('.json') and not f.endswith('versions.json')]

        generator.generateSchemaSummary(schemas)

        generator.generatePropertiesSummary(schemas)


