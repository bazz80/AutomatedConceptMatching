import csv


def read_xml():
    # Use a breakpoint in the code line below to debug your script.
    from bs4 import BeautifulSoup

    element_array = []

    # Opens mimosa xsd file
    with open("standards_files/mimosa_standards.xsd") as fp:
        soup = BeautifulSoup(fp, "xml")

    # Adds element names to array
    for element_name in soup.find_all('xs:element'):
        element_array.append(element_name['name'])

    # Removes duplicates from array
    element_array = list(dict.fromkeys(element_array))
    print(element_array)

    # Prints name and description of every complexType from xsd file
    for stored_name in element_array:
        for complex_type in soup.find_all('xs:complexType', {'name': stored_name}):
            print(complex_type['name'])
            complex_description = complex_type.find('xs:documentation')
            if complex_description is not None:
                description_value = complex_description.get_text()
                print(description_value, '\n')
            else:
                print('N/A \n')

    with open('extracted_data.csv', 'w') as f:
         headers = [string['name'] for tag in complex_type]
         writer = csv.DictWriter(f, fieldnames=headers)
         writer.writeheader()


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    read_xml()