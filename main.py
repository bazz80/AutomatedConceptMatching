import csv

import pandas as pd
from bs4 import BeautifulSoup
from fuzzywuzzy import fuzz
from fuzzywuzzy import process


def read_xml():

    name_list = []
    description_list = []

    # Opens mimosa xsd file
    with open("standards_files/mimosa_standards.xsd") as fp:
        soup = BeautifulSoup(fp, "xml")

    # Finds concept names in xml file
    for concept_name in soup.find_all("complexType", {'name': True}):
        if concept_name is not None:
            name_list.append(concept_name['name'])

    # Removes duplicates from list
    name_list = list(dict.fromkeys(name_list))

    # Finds and appends concept description to list
    for stored_name in name_list:
        for complex_type in soup.find_all('xs:complexType', {'name': stored_name}):
            complex_description = complex_type.find('xs:documentation')
            if complex_description is not None:
                description_value = complex_description.get_text()
                description_list.append(description_value)
            else:
                description_list.append('N/A')

    # Write name and description to csv file
    csv_list = {'name': name_list, 'description': description_list}
    mimosa_df = pd.DataFrame(csv_list)
    return mimosa_df


def read_plcs_xml():

    name_list = []
    description_list = []

    # Opens mimosa xsd file
    with open("standards_files/plcs_standards.xsd") as fp:
        soup = BeautifulSoup(fp, "xml")

    # Finds concept names in xml file
    for concept_name in soup.find_all("complexType", {'name': True}):
        if concept_name is not None:
            name_list.append(concept_name['name'])

    # Removes duplicates from list
    name_list = list(dict.fromkeys(name_list))

    # Finds and appends concept description to list
    for stored_name in name_list:
        for complex_type in soup.find_all('xsd:complexType', {'name': stored_name}):
            complex_description = complex_type.find('xsd:documentation')
            if complex_description is not None:
                description_value = complex_description.get_text()
                description_list.append(description_value)
            else:
                description_list.append('N/A')

    # Write name and description to dataframe
    df_list = {'name': name_list, 'description': description_list}
    plcs_df = pd.DataFrame(df_list)
    return plcs_df


def matches(dfm, dfp):
    threshold = 70
    mlist = []
    plist = []
    slist = []

    test = dfp['name'].values.tolist()
    test2 = dfm['name'].values.tolist()
    for potential in test:
        for example in test2:
            similarity = fuzz.ratio(example, potential)
            if similarity >= threshold:
                mlist.append(example)
                plist.append(potential)
                slist.append(similarity)

    df_list = {'mimosa_name': mlist, 'plcs_name': plist, 'similarity': slist}
    df = pd.DataFrame(df_list)
    df.to_csv("output.csv", index=False)
    return df


def readCsv():
    mimosa_name = 1

    prompt = "Enter a concept"
    found_name = False

    with open('output.csv', 'rt') as file:
        reader = csv.reader(file)
        next(reader, None)
        name = input(prompt)
        while not found_name:
            for row in reader:
                if name == row[mimosa_name]:
                    found_name = True
                    print(row)
                    break
            else:
                name = input(f"Concept not in file. {prompt}")
                file.seek(0)


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    mimosa_df = read_xml()
    plcs_df = read_plcs_xml()
    df = matches(mimosa_df, plcs_df)
    readCsv()