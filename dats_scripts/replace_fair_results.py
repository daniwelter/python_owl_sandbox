import copy
import json
import csv

fairIndicators = "FAIR Dataset Maturity (DSM) Model v1.0"
fairIndicatorsHref = "https://fairplus.github.io/Data-Maturity/docs/Indicators/"
file_path = '../data/imi_projects/'

category_object = {
        "values": [
            {
                "value": "",
                "@type": "Annotation",
                "@context": "https://w3id.org/dats/context/sdo/annotation_sdo_context.jsonld"
            }
        ],
        "@type": "CategoryValuesPair",
        "category": "",
    }

def replace_results(object, project, data):
    if "projectAssets" in object:
        for study in object['projectAssets']:
            if 'output' in study:
                for dataset in study['output']:
                    update_properties(dataset, data, project)
            elif study['@type'] == 'Dataset':
                 update_properties(study, data, project)

    return object


def update_properties(dataset, data, project):
    if 'extraProperties' in dataset:
        dataset['extraProperties'] = []

        for row in data:
            if row[0] == project:
                dataset['extraProperties'].append(create_prop(row[1], row[2]))

        dataset['extraProperties'].append(create_prop("fairIndicatorsPre", fairIndicators))
        dataset['extraProperties'].append(create_prop("fairIndicatorsPost", fairIndicators))
        dataset['extraProperties'].append(create_prop("fairIndicatorsHrefPre", fairIndicatorsHref))
        dataset['extraProperties'].append(create_prop("fairIndicatorsHrefPost", fairIndicatorsHref))
        dataset['extraProperties'].append(create_prop("fairEvaluation", "true"))


def create_prop(category, value):
    result = copy.deepcopy(category_object)
    result['category'] = category
    result['values'][0]['value'] = value
    return result




def get_json(name):
    f = open(file_path + name.lower()+'.json', 'r')
    return json.loads(f.read())



if __name__ == '__main__':

    # TO DO:
    # save file for project

    results_file = 'fair_results3.csv'
    # projects = ['BIOMAP', 'ABIRISK', 'APPROACH', 'c4c', 'CARE', 'COMBINE', 'EBiSC', 'eTOX', 'EUbOPEN', 'GNA-NOW', 'IMIDIA', 'ND4BB', 'OncoTrack', 'ReSOLUTE', 'RHAPSODY', 'ULTRA-DD', 'COMBINE']
    projects = ['eTRANSAFE', 'ESCulab', 'GNA-NOW']

    with open(results_file, encoding='utf-8') as data_file:
        data = csv.reader(data_file)
        results =[]
        for row in data:
            results.append(row)

        results.pop(0)

        for project in projects:
            current = get_json(project)
            updated = replace_results(current, project, results)

            new_file = project.lower() + '_updated.json'
            with open(new_file, 'w') as outfile:
                json.dump(updated, outfile, indent=4)