from bs4 import BeautifulSoup
import pandas as pd
from sqlalchemy import create_engine
from fuzzywuzzy import fuzz


def read_mimosa_xml(engine):
    i = 1
    name_list = []
    description_list = []
    relationship_list = []
    id_list = []

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

    for stored_name in name_list:
        list_length = len(name_list)
        for complex_type in soup.find_all('xs:complexType', {'name': stored_name}):
            headers = [tag['type'] for tag in complex_type.find_all("xs:element", {'type': True})]
            relationship_list.append(headers)

        while i <= list_length:
            id_list.append(i)
            i += 1


    # Write name and description to df
    csv_list = {'idMimosa': id_list, 'name': name_list, 'description': description_list, 'relationships': 'test'}
    mimosa_df = pd.DataFrame(csv_list)
    mimosa_df.to_csv('Data/test_concepts.csv', sep='\t')

    # mimosa_df.to_sql('mimosa', con=engine, if_exists='append', chunksize=1000, index=False)
    return mimosa_df


def read_plcs_xml(engine):
    i = 1
    id_list = []
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
        list_length = len(name_list)
        for complex_type in soup.find_all('xsd:complexType', {'name': stored_name}):
            complex_description = complex_type.find('xsd:documentation')
            if complex_description is not None:
                description_value = complex_description.get_text()
                description_list.append(description_value)
            else:
                description_list.append('N/A')

        while i <= list_length:
            id_list.append(i)
            i += 1


    # Write name and description to df
    df_list = {'idPLCS': id_list, 'name': name_list, 'description': description_list, 'relationships': 'test'}
    plcs_df = pd.DataFrame(df_list)
    plcs_df.to_csv('Data/test_plcs.csv', sep='\t')

    # plcs_df.to_sql('plcs', con=engine, if_exists='append', chunksize=1000, index=False)
    return plcs_df


def connect_to_db():
    # create sqlalchemy engine
    engine = create_engine("mysql+pymysql://{user}:{pw}@localhost/{db}"
                           .format(user="root",
                                   pw="alanna1",
                                   db="automatedmatching"))
    return engine


def name_match(dfm, dfp):
    threshold = 0
    mlist = []
    plist = []
    slist = []
    id_list = []
    i = 0

    test = dfp['name'].values.tolist()
    test2 = dfm['name'].values.tolist()
    for potential in test:
        for example in test2:
            similarity = fuzz.ratio(example, potential)
            if similarity >= threshold:
                mlist.append(example)
                plist.append(potential)
                slist.append(similarity)
                i += 1
                id_list.append(i)


    df_list = {'idSIM': id_list, 'id_plcs': plist, 'id_mimosa': mlist, 'sim_name': slist}
    sim_df = pd.DataFrame(df_list)
    return sim_df

def description_matching(dfm, dfp, df):
    s_description = []

    test = dfp['description'].values.tolist()
    test2 = dfm['description'].values.tolist()
    for potential in test:
        for example in test2:
            if example == 'N/A':
                s_description.append('0')
            else:
                similarity = fuzz.ratio(example, potential)
                s_description.append(similarity)

    df2 = df.assign(sim_description=s_description)
    df2.to_sql('similarity', con=engine, if_exists='append', chunksize=1000, index=False)
    return df2

engine = connect_to_db()
mimosa_df = read_mimosa_xml(engine)
plcs_df = read_plcs_xml(engine)
sim_df = name_match(mimosa_df, plcs_df)
description_matching(mimosa_df, plcs_df, sim_df)