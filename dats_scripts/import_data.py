import argparse
import csv
import json
import logging
import uuid

BLANK_JSON = 'blank_dats.json'

class JsonGenerator:
    def __init__(self):
        self.logger = logging.getLogger(__name__)

    def generateJson(self, data, title, study_count, dataset_count):

        project = self.get_blank('project')
        project['identifier']['identifier'] = str(uuid.uuid1())

        studies = list(range(study_count))

        for s in range(0, study_count):
            study = self.get_blank('study')
            study['identifier']['identifier'] = str(uuid.uuid1())
            studies[s] = study

        datasets = list(range(dataset_count))
        for d in range(0, dataset_count):
            dataset = self.get_blank('dataset')
            dataset['identifier']['identifier'] = str(uuid.uuid1())
            datasets[d] = dataset

        for item in data:
            print(item)
            if item[0] == 'project':
                path = item[1].split('.')
                value = item[2]
                type = None
                if len(item) == 4:
                    type = item[3]
                self.build_object(path, value, project, type)

            elif item[0] == 'study':
                path = item[1].split('.')
                value = item[2]
                type = None
                if len(item) == 4:
                    type = item[3]
                self.build_object(path[1:], value, studies[int(path[0])], type)

            elif item[0] == 'dataset':
                path = item[1].split('.')
                value = item[2]
                type = None
                if len(item) == 4:
                    type = item[3]
                self.build_object(path[1:], value, datasets[int(path[0])], type)



        for dataset in datasets:
            if dataset['title'] != "":
                if 'study' in dataset:
                    studies[int(dataset['study'])]['output'].append(dataset)
                    del dataset['study']
                else:
                    project['projectAssets'].append(dataset)


        for study in studies:
            if study['name'] != "":
                project['projectAssets'].append(study)

        with open(title + '.json', 'w') as outfile:
            json.dump(project, outfile, indent=4)

    def build_object(self, path, value, object, schemaType):
        for element in path:
            if type(object) == dict:
                if path.index(element) == len(path) - 1:
                    object[element] = value
                else:
                    current = object[element]
                    self.build_object(path[path.index(element)+1:], value, current, schemaType)
                    break
            elif element.isnumeric():
                index = int(element)
                if index < len(object):
                    current = object[index]
                    if current is None or (schemaType is not None and current['@type'] != schemaType):
                        lastEl = True
                        if current is not None and current['@type'] != 'Organization':
                            for e in path:
                                if e.isnumeric():
                                    lastEl = False

                        if lastEl:
                            current = self.get_blank(schemaType)
                        object[index] = current
                    self.build_object(path[path.index(element) + 1:], value, current, schemaType)
                    break
                else:
                    if schemaType is not None:
                        data_type = schemaType
                    else:
                        data_type = object[0]['@type']
                    empty = self.get_blank(data_type)
                    for i in range(len(object), index-1):
                        object.insert(i, None)
                    object.insert(index, empty)
                    self.build_object(path[path.index(element) + 1:], value, empty, schemaType)
                    break


    def get_json_from_file(self, filename):
        """Loads json from a file."""
        f = open(filename, 'r')
        return json.loads(f.read())

    def get_blank(self, type):
        blank = self.get_json_from_file(BLANK_JSON)
        if type.lower() in blank:
            return blank[type.lower()]



if __name__ == '__main__':

    parser = argparse.ArgumentParser(description='Throw away script json schemas to csv')
    parser.add_argument('--path_to_file', '-p', help='Path to the data file, e.g. ~/data/my_data.csv', type=str)
    parser.add_argument('--project_title', '-t', help='Title of the project - will be used as filename', type=str)
    parser.add_argument('--study_count', '-s', help='Number of studies', type=int)
    parser.add_argument('--dataset_count', '-d', help='Number of datasets', type=int)
    args = parser.parse_args()

    generator = JsonGenerator()

    if not args.path_to_file:
        print("You must supply the path to the data file")
        exit(2)
    if not args.project_title:
        print("You must supply a project title")
        exit(2)
    else:
        data_file_path = args.path_to_file
        project = args.project_title

        study_count = 1
        if args.study_count:
            study_count = args.study_count

        dataset_count = 1
        if args.dataset_count:
            dataset_count = args.dataset_count

        with open(data_file_path, encoding='utf-8') as data_file:
            data_file = csv.reader(data_file, delimiter='\t')
            data = []
            for row in data_file:
                data.append(row)

            generator.generateJson(data, project, study_count, dataset_count)