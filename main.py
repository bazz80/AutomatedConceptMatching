import csv
import pandas as pd


def read_xml():
    # Use a breakpoint in the code line below to debug your script.
    from bs4 import BeautifulSoup

    name_list = []
    description_list = []

    # Opens mimosa xsd file
    with open("standards_files/mimosa_standards.xsd") as fp:
        soup = BeautifulSoup(fp, "xml")

    # Finds concept names in xml file
    for concept_name in soup.find_all("complexType", {'name': True}):
        if concept_name is not None:
            name_list.append(concept_name['name'])

    # Removes duplicates from array
    name_list = list(dict.fromkeys(name_list))
    print(name_list)

    # Prints name and description of every complexType from xsd file
    for stored_name in name_list:
        for complex_type in soup.find_all('xs:complexType', {'name': stored_name}):
            complex_description = complex_type.find('xs:documentation')
            if complex_description is not None:
                description_value = complex_description.get_text()
                description_list.append(description_value)
            else:
                description_list.append('N/A')

    print(description_list)
    print(name_list)

    csv_list = {'name': name_list, 'description': description_list}
    df = pd.DataFrame(csv_list)
    df.to_csv('Data/extracted_concepts.csv')


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    read_xml()