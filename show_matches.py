import sqlalchemy as db
import pandas as pd


def show_matches():
    meta = db.MetaData()
    # create sqlalchemy engine
    engine = db.create_engine("mysql+pymysql://{user}:{pw}@localhost/{db}"
                           .format(user="root",
                                   pw="alanna1",
                                   db="automatedmatching"))
    connection = engine.connect()
    name_weighting = 80
    description_weighting = 20
    desc_list = []
    threshold = 40

    if name_weighting + description_weighting > 100:
        print('Please enter values that total 100')
    else:
        while True:
            user_request = input('Enter your search query:\n')
            user_standard_query = input('Enter 1 if you are searching a Mimosa concept or 2 for PLCS:\n')
            if user_standard_query == '1':
                user_standard_query = 'MIMOSA'
                df = pd.read_sql("SELECT * FROM similarity WHERE name_mimosa=%s", engine, params=(user_request,))
                break
            elif user_standard_query == '2':
                user_standard_query = 'PLCS'
                df = pd.read_sql("SELECT * FROM similarity WHERE name_plcs=%s", engine, params=(user_request,))
                break
            else:
                print('Please enter 1 or 2')

        df['weighted_sim_name'] = (df['sim_name'] / 100) * name_weighting
        df['weighted_sim_description'] = (df['sim_description'] / 100) * description_weighting
        df['weighted_similarity'] = (df['weighted_sim_name'] + df['weighted_sim_description'])
        df2 = df[(df[['weighted_similarity']] >= threshold).all(axis=1)]

        if user_standard_query == 'MIMOSA':
            name_list = df2['name_plcs'].tolist()
            sql = "SELECT description FROM plcs WHERE name IN :values"
        else:
            name_list = df2['name_mimosa'].tolist()
            sql = "SELECT description FROM mimosa WHERE name IN :values"

        query = db.text(sql).bindparams(db.bindparam("values", expanding=True))
        results = connection.engine.execute(query, {"values": name_list})
        for retrieved_descriptions in results:
            desc_list.append(retrieved_descriptions)

        df3 = df2.assign(description=desc_list)
        df3 = df3.sort_values(by='weighted_similarity', ascending=False)
        df3['description'] = df3['description'].astype(str)
        df3['description'] = df3['description'].replace([r'\r+|\n+|\t+'], regex=True)

        print(f'{user_request} matches with the following {user_standard_query} concepts:\n')
        for ind in df3.index:
            print(f'{user_standard_query} Name: ', df3['name_plcs'][ind], '\nSimilarity Score: ',
                  df3['weighted_similarity'][ind], '\nDescription: ', df3['description'][ind], '\n')


show_matches()