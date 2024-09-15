import requests
response = requests.get('https://ut.ac.id')
print(response.text)


from bs4 import BeautifulSoup
soup = BeautifulSoup(response.text, 'html.parser')

for judul in soup.find_all('h1'):
    print(judul.text.strip())

import csv
with open('hasilcecep3.csv', 'w', newline='', encoding='utf-8') as file:
    writer = csv.writer(file)
    writer.writerow(['Judul'])
    for judul in soup.find_all('h1'):
        writer.writerow([judul.text.strip()])
