import os
import json
import bs4
import uuid
from bs4 import BeautifulSoup


def extractData(contents, dats, file_name):
    soup = BeautifulSoup(contents, 'lxml')

    project_title = soup.h1.text.rstrip()
    title = soup.find_all("div", class_="field--name-field-project-title")

    dats['title'] = project_title
    dats['projectAssets'][0]['name'] = project_title
    dats['projectAssets'][0]['output'][0]['title'] = project_title

    expanded_title = ''
    for t in title:
        if expanded_title == '':
            expanded_title = t.text
        elif expanded_title != t.text:
            print("Multiple expanded titles for project " + project_title)

    dats['description'] = expanded_title
    dats['projectAssets'][0]['description'] = expanded_title

    status = soup.find_all("span", class_="project-status")
    project_status = ''

    # for s in status:
    #     if project_status == '':
    #         project_status = s.text.rstrip()
    #     elif project_status != s.text.rstrip():
    #         print("Multiple project statuses for project " + project_title)

    # print(project_title + "\t" + expanded_title)

    # programme = soup.find_all(class_="project-imi-programme")[0].text.rstrip()
    keywords = soup.find_all(class_="project-keyword")

    project_keywords = []
    for kw in keywords:
        if kw.text.rstrip() not in project_keywords:
            project_keywords.append(kw.text.rstrip())

    kw_struc = dats['keywords'][1]
    dats['keywords'].pop(1)
    for k in project_keywords:
        keyword = kw_struc.copy()
        keyword['value'] = k
        dats['keywords'].append(keyword)

    start_date = ''
    end_date = ''
    call = ''
    grant = ''

    fact_figs = soup.find_all(id="project-facts-figures")
    if len(fact_figs) >0:
        sd = soup.find_all(class_="field--name-field-start-date")[0].text.rstrip().split('/')
        start_date = sd[2] + '-' + sd[1] + '-' + sd[0]
        ed = soup.find_all(class_="field--name-field-end-date")[0].text.rstrip().split('/')
        end_date = ed[2] + '-' + ed[1] + '-' + ed[0]

        call = soup.find_all(class_="field--name-field-project-call")[0].text.rstrip()
        grant = soup.find_all(class_="field--name-field-project-grant")[0].text.rstrip()

    dats['startDate']['date'] = start_date
    dats['endDate']['date'] = end_date
    dats['fundedBy'][0]['name'] = call
    dats['fundedBy'][0]['identifier']['identifier'] = grant

    contacts = soup.find_all(class_="project-contact")
    project_contacts = []

    for c in contacts:
        elements = c.contents
        person = []
        for e in elements:
            if isinstance(e, bs4.element.Tag):
                if len(e.contents)>0:
                    person.append(e.text.rstrip())
            else:
                person.append(e)
        if person not in project_contacts:
            project_contacts.append(person)

    contact_struc = dats['projectLeads'][0]
    dats['projectLeads'].pop(0)

    for pc in project_contacts:
        contact = contact_struc.copy()
        contact['roles'][0]['value'] = pc[0]
        full_name = pc[1]
        contact['fullName'] = full_name
        els = full_name.split(' ')
        if len(els) == 2:
            contact['firstName'] = els[0]
            contact['lastName'] = els[1]
        elif len(els) == 3:
            contact['firstName'] = ' '.join(els[0:2])
            contact['lastName'] = els[2]
        else:
            print("Project contact too complicated: " + full_name + "\t" + project_title)

        if len(pc) > 2:
            contact['affiliations'][0]['name'] = pc[2]
        if len(pc) == 4:
            contact['affiliations'][0]['location']['postalAddress'] = pc[3]
        else:
            contact['affiliations'][0]['location']['postalAddress'] = ''

        dats['projectLeads'].append(contact)

    website = soup.find_all(class_="field--name-field-links-and-documents")
    project_website= ''
    for ws in website:
        for w in ws.contents:
            if isinstance(w, bs4.element.Tag) and ('website' in w.text.rstrip().lower() or 'web page' in w.text.rstrip().lower()):
                for c in w.contents:
                    if hasattr(c, 'attr')  and 'href' in c.attrs:
                        project_website = c.attrs['href']
    print(project_title + '\t'  + project_website)

    # description = soup.find_all(class_="field--name-body")
    # project_description = ''
    # for d in description:
    #     if d.next_element.name == 'p':
    #         project_description = d.text.rstrip()

    for prop in dats['extraProperties']:
        if prop['category'] == 'projectAcronym':
            prop['values'][0]['value'] = project_title
        elif prop['category'] == 'website':
            prop['values'][0]['value'] = project_website

    generate_identifers(dats)

    save_json(dats, file_name)

    # print(project_keywords)
    # print(start_date)
    # print(end_date)
    # print(call)
    # print(grant)
    # print(project_contacts)
    # print(project_website)
    # print(project_description)

def get_json_from_file(filename):
    """Loads json from a file."""
    f = open(filename, 'r')
    return json.loads(f.read())

def save_json(dats, filename):
    new_file = 'dats_json/' + filename.replace("html", "json")
    with open(new_file, 'w') as outfile:
        json.dump(dats, outfile, indent=4)

def generate_identifers(dats):
    dats['identifier']['identifier'] = str(uuid.uuid1())
    dats['projectAssets'][0]['identifier']['identifier'] = str(uuid.uuid1())
    dats['projectAssets'][0]['output'][0]['identifier']['identifier'] = str(uuid.uuid1())

if __name__ == "__main__":
    path_to_files = "/Users/danielle.welter/Documents/FAIRplus/IMI projects"

    path = os.path.join(os.path.dirname(__file__), path_to_files)

    blank_json = 'dats_blank.json'

    with os.scandir(path) as data_files:
        for data_file in data_files:
            if ".html" in data_file.name:
                with open(data_file, 'r') as htmlfile:
                    dats = get_json_from_file(blank_json)
                    contents = htmlfile.read()
                    extractData(contents, dats, data_file.name)

