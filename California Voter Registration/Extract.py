from bs4 import BeautifulSoup
import urllib.request
from urllib.error import URLError, HTTPError
import os
from datetime import datetime


def extract_california(download_directory, date_after = '1-1-2001'):
    """Scrapes voter registration data from CA Secretary of State site"""
    
    try:
        site = 'https://www.sos.ca.gov'
        with urllib.request.urlopen(site + '/elections/report-registration/') as resp:
            soup = BeautifulSoup(resp,'lxml')
    except HTTPError as e:
        print('Error Code: ', e.code)
    except URLError as e:
        print('Reason: ', e.reason)
    
    #Make a dictionary of all pages on the site which lead to voter files.
    #Only include those dates after the date_after parameter.
    pages = {}
    for link in soup.find_all('a', href=True):
        if '/elections/report-registration/' in link['href']:
            date = link.string[link.string.rfind('-') + 2:]
            if datetime.strptime(date, '%B %d, %Y') \
                > datetime.strptime(date_after, '%m-%d-%Y'):
                    pages[date] = site + link['href']
            
    #Make a dictionary of all excel files contained on each page
    files = {}
    for page_key, page_item in pages.items():
        try:
            with urllib.request.urlopen(page_item) as resp:
                soup = BeautifulSoup(resp, 'lxml')
        except HTTPError as e:
            print('Error Code: ', e.code)
        except URLError as e:
            print('Reason: ', e.reason)
        for link in soup.find_all('a', href=True):
            if 'xls' in link['href']:
                if page_key in files:
                    files[page_key].append(link['href'])
                else:
                    files[page_key] = []
                    files[page_key].append(link['href'])
    
    #Download all files into chosen directory
    for path_key, path in files.items():
        for file in path:
            last_slash = file.rfind('/')    
            folder = datetime.strptime(path_key, '%B %d, %Y').strftime('%Y-%m-%d')
            filename = download_directory + '\\' + folder + '\\' + file[last_slash + 1:]
            
            try:
                os.makedirs(os.path.dirname(filename), exist_ok=True)
            except OSError:
                pass
            try:
                urllib.request.urlretrieve(file, filename)
            except HTTPError as e:
                print('Error Code: ', e.code)
            except URLError as e:
                print('Reason: ', e.reason)
                
extract_california(r'C:\Users\ASUS\voter_registration\California Voter Registration', '1-1-2018')