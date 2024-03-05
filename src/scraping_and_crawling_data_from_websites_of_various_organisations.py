from bs4 import BeautifulSoup
import requests
import pandas as pd

websites = ["https://www.panfoundation.org/","https://www.healthwellfoundation.org/","https://rxoutreach.org/","https://www.harborpath.org/","https://www.merckconnect.com/","https://www.bauschhealthpap.com/","https://www.lillycares.com/","https://novocare.com/diabetes/help-with-costs/pap.html"]

headers = {
  "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36"
}

df = pd.DataFrame(columns=["Link","Html Text","Website text"])

for website in websites:
  web_page = requests.get(website, headers=headers).text
  soup = BeautifulSoup(web_page, 'lxml')
  website_text = soup.text

  website_text = ' '.join(website_text.split())

  df.loc[len(df.index)] = list((website, str(soup.encode("utf-8")), website_text))

df.to_excel("data/Contents_of_Web_Pages_of_Websites.xlsx")