import os
import sys
import json

# import requests



def profileSamplesFromURL(requestURL, characteristics, examples, counter):

    if counter < 10:
        print("Processing round " + str(counter))
        r = requests.get(requestURL)

        if not r.ok:

            r.raise_for_status()
            sys.exit()

        else:
            json = r.json()

            samples = json['_embedded']['samples']

            for sample in samples:
                if 'characteristics' in sample:
                    for key in sample['characteristics'].keys():
                        if key not in characteristics:
                            characteristics[key] = 1
                            examples[key] = sample['characteristics'][key]
                        else:
                            characteristics[key] = characteristics[key] + 1

            next = json['_links']['next']['href']
            counter = counter + 1

            profileSamples(next, characteristics, examples, counter)

    else:
        print("Total number of characteristics: " + str(len(characteristics.keys())))
        for key in characteristics.keys():
            print(key + '\t' + str(characteristics[key]) + '\t' + examples[key][0]['text'])


def profileSamples(filePath):

    properties = []
    prop_count = {}
    characteristics = []
    char_count = {}
    examples = {}

    with os.scandir(filePath) as data_files:
        for data_file in data_files:
            if '.json' in data_file.name:
                with open(data_file, 'r') as jsonfile:
                    content = json.loads(jsonfile.read())

                    for sample in content:
                        for key in sample.keys():
                            if key not in properties:
                                properties.append(key)

                            if key not in prop_count.keys():
                                prop_count[key] = 1
                            else:
                                prop_count[key] = prop_count[key] + 1



                        # if 'characteristics' in sample:
                        #     for char in sample['characteristics'].keys():
                        #         if char not in characteristics:
                        #             characteristics.append(char)
                        #         if char not in char_count.keys():
                        #             char_count[char] = 1
                        #         else:
                        #             char_count[char] = char_count[char]+1
                        #
                        #         val = sample['characteristics'][char][0]['text']
                        #         if char not in examples.keys():
                        #             examples[char] = [val]
                        #         elif val not in examples[char]:
                        #             examples[char].append(val)


    print("*Properties:")
    for prop in properties:
        print(prop + ": " +  str(prop_count[prop]))
    print("----------------------")
    # print("*Characteristics")

    # with open('examples_v2.text', "w") as out_file:
    #     for char in characteristics:
    #         # rep = examples[char]
    #         rep = []
    #         if len(examples[char]) > 10:
    #             rep = examples[char][0:10]
    #         else:
    #             rep = examples[char]
    #         out_file.write(char + ": " + ', '.join(rep) + "\n")
    #     out_file.close()



if __name__ == "__main__":
    # baseURL = 'https://www.ebi.ac.uk/biosamples/api/samples/search/findByText?text=homo+sapiens'
    #
    # characteristcs = []
    # properties = []
    #
    # counter= 0

    filePath = '/Users/danielle.welter/Development/python_sandbox/biosd_profiler'
    path = os.path.join(os.path.dirname(__file__), filePath)


    profileSamples(filePath)
