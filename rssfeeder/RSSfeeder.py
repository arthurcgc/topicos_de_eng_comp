import requests
import bs4 as bs

def feeder(urls, file_location):
    txt_file = open(file_location, 'w')
    for url in urls:
        resp = requests.get(url)
        soup = bs.BeautifulSoup(resp.content, features="xml")
        txt_file.write(soup.prettify())
    txt_file.close()