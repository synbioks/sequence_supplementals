from requests_html import HTMLSession
import pandas as pd
import numpy as np

run_scraping = False
update_scraped_col = False

if run_scraping:
    df = pd.read_csv('test.csv')

    session = HTMLSession()
    ln_url_list = len(df)
    for ind, df_row in df.iterrows():
        igem_url = df_row['igem_link.value']
        if ind+1 > 13562:
            print(f'{ind+1} of {ln_url_list}')
            r = session.get(igem_url)
            grp_nm = r.html.search("Group: {}\n")
            with open('creator_list.txt', 'a') as f:
                f.write(f'{ind}, {df_row["s.value"]}, {igem_url}, {grp_nm}\n')
    with open('creator_list.txt', 'a') as f:
        f.write(f'{ind}, {igem_url}, {grp_nm}\n')

if update_scraped_col:
    df = pd.read_csv('creator_list.txt')
    df = df.drop(['extra_thing'], axis=1)
    team_name_str_col = df.team_name.str.split("'", expand=True).iloc[:, 1]
    team_name_str_col = team_name_str_col.str.split('  &', expand=True).iloc[:,0]
    df['team_name'] = team_name_str_col
    df.to_csv('creator_list_2.csv', index=False)

df_creators = pd.read_csv('creator_list_2.csv')
# print(df_creators)

df_creation_dates = pd.read_csv('creation_dates.csv')


# print(df_creation_dates)

df_merged = df_creators.merge(df_creation_dates, on='synbiohub_uri')
df_merged.drop(['ind_x', 'ind_y', 'igem_link.value'], axis=1, inplace=True)
df_merged.to_csv('teams_over_time.csv')
