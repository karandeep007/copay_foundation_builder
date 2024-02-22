import pandas as pd
import requests
from bs4 import BeautifulSoup

cols = ['Drug Name', 'PAP', 'Content']

data = pd.read_csv("C:/Users/teesh/Veersa/Task3_PAP/Drug_details.csv")

data = data.fillna(0)

df = pd.DataFrame(columns = cols)

for indx in range(int(len(data)/2)):
    print(f"{indx} / {int(len(data)/2)}")
    sample = data.iloc[indx]['Patient Assistance Programs']
    if not sample :
        continue
    html_page = requests.get(sample).text
    soup = BeautifulSoup(html_page, 'lxml')

    td_lst = soup.find_all('td', height=90)
    for td in td_lst:
        heading = td.find('h2').text
        content = td.find('strong').text

        record = {
            'Drug Name' : data.iloc[indx]['drug_name'],
            'PAP' : heading,
            'Content' : content
        }
    
    df.loc[len(df.index)] = list(record.values())

df.to_csv('PAP.csv')

# count_name = data["PAP"].value_counts()
# df = pd.DataFrame(count_name)
# # df.to_csv("PAP_counts.csv")
        