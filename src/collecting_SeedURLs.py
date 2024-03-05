import requests
from bs4 import BeautifulSoup
import time
import pandas as pd
from fake_user_agent import UserAgent

def search_keyword(keyword, num_results=100):

    print('-'*10 , keyword, '-'*10)

    url = f'https://www.google.com/search?q={keyword}&num={num_results}'  # 429 (exceed rate limit) - to be worked upon

    # Problem (cause) - getting None / 0 results (cause google loads its content dynamically), 403 forbidden (may detect as bot)
    # Solution - adding headers -> treat request send by user, allow access to dynamic loading of content
    headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36 Edg/121.0.0.0"}      

    response = requests.get(url, headers=headers)
    
    seed_urls = []
    
    if response.status_code == 200:
        soup = BeautifulSoup(response.text, 'lxml')
        cards = soup.find_all('div', {"class":"g"})
        print(len(cards))

        for i in range(0, len(cards)):
            link = cards[i].find('a').get('href')
            if link is not None:
                if link.find('http') != -1 and link.find('http') == 0:
                    print(link)
                    seed_urls.append(link)

    return seed_urls

# Search list
keywords = ['Copay assistance program', '501c3 charity copay foundation', 'patient assistance foundation']

df = pd.DataFrame()

for keyword in keywords:
    seed_urls = search_keyword(keyword)
    temp = pd.DataFrame({'Program' : [keyword]*len(seed_urls), 'URLs' : seed_urls})
    print(temp)
    df = pd.concat([df, temp], ignore_index=True)


print(df)
df.to_csv('data\Seed URLs.csv', columns=['Program', 'URLs'], index=True, header=['Program', 'URLs'])
