import sqlalchemy
from bs4 import BeautifulSoup
import pandas as pd
import sqlalchemy as db
from fuzzywuzzy import fuzz
import configparser as cp


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
    mimosa_df.to_sql('mimosa', con=engine, if_exists='replace', chunksize=1000, index=False)

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

    # Removes duplicates from list.
    name_list = list(dict.fromkeys(name_list))

    # Finds and appends concept description to list.
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
    plcs_df.to_sql('plcs', con=engine, if_exists='replace', chunksize=1000, index=False)

    return plcs_df


def connect_to_db():
    # read_default_group = 'client'
    # read_default_file = '/etc/my.cnf'
    #
    # cfg = cp.Parser()
    # cfg.read(defaults_file)
    #
    # def _config(key, arg=None):
    #     try:
    #         return cfg.get(read_default_group, key)
    #     except Exception:
    #         return arg
    #
    # user = _config("user")
    # password = _config("password")
    # host = _config("host")
    # database = _config("database")
    # port = int(_config("port", 3306))
    # charset = _config("charset", "utf8mb4")
    # engine = create_engine(f'mysql+pymysql://{user}:{password}@{host}:{port}/{database}?charset={charset}')

    meta = db.MetaData()
    # create sqlalchemy engine
    engine = db.create_engine("mysql+pymysql://{user}:{pw}@localhost/{db}"
                           .format(user="root",
                                   pw="alanna1",
                                   db="automatedmatching"))

    mimosa = db.Table(
        'mimosa',
        meta,
        db.Column('id_mimosa', db.Integer, primary_key=True),
        db.Column('name', db.String(256)),
        db.Column('description', db.String(5000)),
        db.Column('relationships', db.String(5000)),
    )

    plcs = db.Table(
        'plcs',
        meta,
        db.Column('id_plcs', db.Integer, primary_key = True),
        db.Column('name', db.String(256)),
        db.Column('description', db.String(5000)),
        db.Column('relationships', db.String(5000)),
    )
    meta.create_all(engine)

    similarity = db.Table(
        'similarity',
        meta,
        db.Column('id_sim', db.Integer, primary_key=True),
        db.Column('name_plcs', db.String(256)),
        db.Column('name_mimosa', db.String(256)),
        db.Column('sim_name', db.Integer),
        db.Column('sim_description', db.Integer),
        db.Column('sim_relationship', db.Integer),
    )

    meta.create_all(engine)
    print("Tables were created")
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


    df_list = {'id_sim': id_list, 'name_plcs': plist, 'name_mimosa': mlist, 'sim_name': slist}
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
    df2.to_sql('similarity', con=engine, if_exists='replace', chunksize=1000, index=False)
    return df2


engine = connect_to_db()
mimosa_df = read_mimosa_xml(engine)
plcs_df = read_plcs_xml(engine)
sim_df = name_match(mimosa_df, plcs_df)
df2 = description_matching(mimosa_df, plcs_df, sim_df)