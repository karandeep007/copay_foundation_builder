from bs4 import BeautifulSoup
import requests
import pandas as pd

record = ['drug_name','drug_expiration_date','drug_last_updated',
        'drug_desc','prescription','Offer Type:','Activate By:',
        'Coverage Requirements:',  'Pharmacy Support Number',
        'manu_link','print1','email1','print2',
        'email2','text2','ic1','ic2','ic3','ic4','ic5','ic6']

df = pd.DataFrame(columns=record)

for alphabet in "ABCDEFGHIJKLMNOPQRSTUVWXYZ":
    print(alphabet)
    html_text = requests.get(f"https://www.needymeds.org/coupons/list/{alphabet}").text
    soup = BeautifulSoup(html_text, 'lxml')
    card = soup.find_all('div', class_='row coupon-new')
    # t = len(card)
    # p = 1

    for drug in card:
        # print(p,"/",t)
        # p+=1
        drug_name = drug.find('div', class_='coupon-drugname').text.strip()
        drug_expiration_date = drug.find('div', class_='col-md-4').text.strip().split()[2:][0]
        drug_last_updated = drug.find('div', class_='col-md-8').text.strip().split()[2:][0]
        drug_desc = drug.find('div', class_='coupon-savings').text.strip()

        bullets = {
            'prescription': '',
            'Offer Type:' : '',
            'Activate By:' : '',
            'Coverage Requirements:' : '',
            'Pharmacy Support Number' : ''
        }

        bul = drug.find('div', class_='coupon-bullets').find_all('li')
        for bullet in bul:
            if bullet.text == "Prescription" or bullet.text == "Over-the-counter":
                bullets['prescription'] = bullet.text
                continue
            if (' '.join(bullet.text.split(' ')[:3])) == 'Pharmacy Support Number':
                bullets[' '.join(bullet.text.split()[:3])] = ' '.join(bullet.text.split()[3:])
            else:
                bullets[' '.join(bullet.text.split()[:2])] = ' '.join(bullet.text.split()[2:])

        link = ['']*6
        drug_link = drug.find('div', class_='coupon-actions').find_all('a')

        link[3]=drug_link[-3]['onclick']
        link[4]=drug_link[-2]['onclick']
        link[5]=drug_link[-1]['onclick']

        if drug_link[0]['alt']:
            link[0]=drug_link[0]['onclick']

            if len(drug_link)==6:
                link[1]=drug_link[1]['onclick']
                link[2]=drug_link[2]['onclick']
            else:
                link[2]=''
                link[1]=''

        else:
            link[0]=''
            
            if len(drug_link)==5:
                link[1]=drug_link[0]['onclick']
                link[2]=drug_link[1]['onclick']
            else:
                link[2]=''
                link[1]=''

        ic={
            'Patient Assistance Programs' : '',
            '4 dollar generic programs' : '',
            'Coupons, rebates and more' : '',
            'Support Pages' : '',
            'MedsOnCue Drug Videos' : '',
            'Drugs.Com Information' : ''
        }

        if icons := drug.find('div', class_='coupon-icons').find_all('a'):
            for icon in icons:
                try:
                    ic[icon.find('img')['title']] = icon['href']
                except KeyError:
                    ic[icon.find('img')['title']] = icon['onclick']
                except:
                    ic[icon.find('img')['title']] = ''
                    

        record = {
            'drug_name' : drug_name,
            'drug_expiration_date' : drug_expiration_date,
            'drug_last_updated' : drug_last_updated,
            'drug_desc' : drug_desc,
            'prescription' : bullets['prescription'], 
            'Offer Type:' : bullets['Offer Type:'], 
            'Activate By:' : bullets['Activate By:'], 
            'Coverage Requirements:' : bullets['Coverage Requirements:'], 
            'Pharmacy Support Number' : bullets['Pharmacy Support Number'],
            'manu_link' : link[0],
            'print1' : link[1],
            'email1' : link[2],
            'print2' : link[3],
            'email2' : link[4],
            'text3' : link[5],
            'ic1' : ic['Patient Assistance Programs'],
            'ic2' : ic['4 dollar generic programs'],
            'ic3' : ic['Coupons, rebates and more'],
            'ic4' : ic['Support Pages'],
            'ic5' : ic['MedsOnCue Drug Videos'],
            'ic6' : ic['Drugs.Com Information'],
        }

        df.loc[len(df.index)] = list(record.values())



df.to_csv('Drug_details.csv')