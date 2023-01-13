import os
import json
import bs4
import uuid
from bs4 import BeautifulSoup


def correctData(html, dats, file_name):
    soup = BeautifulSoup(html, 'lxml')

    title = dats['title']

    end_date = ''
    fact_figs = soup.find_all(id="project-facts-figures")
    if len(fact_figs) >0:
        ed = soup.find_all(class_="field--name-field-end-date")[0].text.rstrip().split('/')
        end_date = ed[2] + '-' + ed[1] + '-' + ed[0]

    dats['endDate']['date'] = end_date

    if len(dats['projectLeads']) > 1:
        for pc in dats['projectLeads']:
            loc = dats['projectLeads'].index(pc)
            for next in dats['projectLeads'][loc+1:]:
                if pc['fullName'] == next['fullName']:
                    i = dats['projectLeads'].index(next)
                    new_role = next['roles'][0]
                    if new_role['value'] != pc['roles'][0]['value']:
                        pc['roles'].append(new_role)
                        print(title + ": Role " + new_role[0]['value'] + " added to contact " + pc['fullName'])
                    dats['projectLeads'].pop(i)


            if 'firstName' not in pc or pc['firstName'] == '':
                print("Project contact too complicated: " + pc['fullName'] + "\t" + title)

    save_json(dats, file_name)

def getContacts(html):
    soup = BeautifulSoup(html, 'lxml')
    project_title = soup.h1.text.rstrip()
    contacts = soup.find_all(class_="project-contact")

    contact_list = []
    for c in contacts:
        elements = c.contents
        person = project_title + '\t'
        for e in elements:
            if isinstance(e, bs4.element.Tag):
                if len(e.contents)>0:
                    person = person + e.text.rstrip() + '\t'
            else:
                person = person + e + '\t'
        if person not in contact_list:
            contact_list.append(person)

    for p in contact_list:
        print(p)

def correctContacts(html, dats, filename):
    soup = BeautifulSoup(html, 'lxml')

    contacts = soup.find_all(class_="project-contact")

    for c in contacts:
        elements = c.contents
        person = []
        for e in elements:
            if isinstance(e, bs4.element.Tag):
                if len(e.contents) > 0:
                    person.append(e.text.rstrip())
            else:
                person.append(e)

        for pl in dats['projectLeads']:
            if person[1] == pl['fullName']:
                if len(pl['roles']) == 1:
                    pl['roles'][0]['value'] = person[0]
                else:
                    print(dats['title'] + " Check roles for: " + pl['fullName'])
                if len(person) > 2:
                    pl['affiliations'][0]['name'] = person[2]

                    if len(person) == 4:
                        pl['affiliations'][0]['location']['postalAddress'] = person[3]

    save_json(dats, filename)



def get_json_from_file(filename):
    """Loads json from a file."""
    f = open(filename, 'r')
    return json.loads(f.read())

def save_json(dats, filename):
    new_file = 'dats_json_updated_v2/' + filename.replace("html", "json")
    with open(new_file, 'w') as outfile:
        json.dump(dats, outfile, indent=4)


if __name__ == "__main__":
    path_to_files = "/Users/danielle.welter/Documents/FAIRplus/IMI projects"

    path = os.path.join(os.path.dirname(__file__), path_to_files)


    with os.scandir(path) as data_files:
        for data_file in data_files:
            if ".html" in data_file.name:
                with open(data_file, 'r') as htmlfile:
                    dats = get_json_from_file('dats_json_updated/'+data_file.name.replace("html", "json"))
                    # contents = htmlfile.read()
                    # correctData(contents, dats, data_file.name)

                    # getContacts(htmlfile.read())

                    correctContacts(htmlfile.read(), dats, data_file.name)

