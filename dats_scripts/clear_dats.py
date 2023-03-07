import json


def empty_property(schema, property):
    schema[property] = ""


def process_dictionary(dictionary):
    for property in dictionary.keys():
        identify_type(dictionary, property)

def identify_type(schema, property):
    if isinstance(schema[property], dict):
        process_dictionary(schema[property])

    elif isinstance(schema[property], list):
        process_list(schema[property])

    elif "@" not in property:
        empty_property(schema, property)

def process_list(list):
    if not isinstance(list[0], str):
        for property in list[0].keys():
            identify_type(list[0], property)

        if len(list) > 1:
            for el in list[1:]:
                list.remove(el)

if __name__ == '__main__':

    f = open('blank_dats.json', 'r')

    schema = json.loads(f.read())

    for property in schema.keys():
        identify_type(schema, property)


    new_file = 'really_blank.json'
    with open(new_file, 'w') as outfile:
        json.dump(schema, outfile, indent=4)