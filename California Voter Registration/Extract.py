from bs4 import BeautifulSoup
import urllib.request
import os
from datetime import datetime

site = 'https://www.sos.ca.gov'

resp = urllib.request.urlopen(site + '/elections/report-registration/')
soup = BeautifulSoup(resp, from_encoding=resp.info().get_param('charset'))


pages = {}
for link in soup.find_all('a', href=True):
    if '/elections/report-registration/' in link['href']:
        pages[link.string[link.string.rfind('-') + 2:]] = site + link['href']


files = {}
for page_key, page_item in pages.items():
    print(page_key)
    resp = urllib.request.urlopen(page_item)
    soup = BeautifulSoup(resp, from_encoding=resp.info().get_param('charset'))
    for link in soup.find_all('a', href=True):
        if 'xls' in link['href'] and 'politicalsub' in link['href']:
            if page_key in files:
                files[page_key].append(link['href'])
            else:
                files[page_key] = []
                files[page_key].append(link['href'])

directory = r'C:\Users\ASUS\voter_registration\California Voter Registration'


for path_key, path in files.items():
    for file in path:
        last_slash = file.rfind('/')    
        folder = datetime.strptime(path_key, '%B %d, %Y').strftime('%Y-%m-%d')
        filename = directory + '\\' + folder + '\\' + file[last_slash + 1:]
        
        os.makedirs(os.path.dirname(filename), exist_ok=True)
        urllib.request.urlretrieve(file, filename)
    