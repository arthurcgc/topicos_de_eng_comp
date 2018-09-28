import requests
import bs4 as bs
import re

""" main function,  creates the txt files and populates them"""
def get_raw_txt(url):
    resp = requests.get(url) # Obtaining first url to scrape
    soup = bs.BeautifulSoup(resp.content,"html.parser")

    # kill all script and style elements
    for script in soup(["script", "style"]):
        script.decompose()    # rip it out

    # get text
    text = soup.get_text()
    # break into lines and remove leading and trailing space on each
    lines = (line.strip() for line in text.splitlines())
    # break multi-headlines into a line each
    chunks = (phrase.strip() for line in lines for phrase in line.split("  "))
    # drop blank lines
    text = '\n'.join(chunk for chunk in chunks if chunk)

    return text

def get_links(url):
    resp = requests.get(url) # Obtaining first url to scrape
    soup = bs.BeautifulSoup(resp.content,"html.parser")
    links = [] 
    for link in soup.findAll('a'):
        if link.get('href') not in links:
            links.append(link.get('href'))
    return links

def save_links(links,links_path):
    links_txt = open(links_path, 'w')
    for link in links:
        links_txt.write(link + '\n')
    links_txt.close()

def write_html_txt(html_path,text):
    html_raw_txt = open(html_path,"w")
    html_raw_txt.writelines(text)
    html_raw_txt.close()

def iterate(og_links,html_path,max_iter):
    for i in range(0,max_iter):
        print("Visiting : {}".format(links[i]))
        new_links = get_links(og_links[i])
        for j in range(0,len(new_links)):
            # import pdb;pdb.set_trace()
            if new_links[j] in links:
                not_appended = new_links[j]
                print("link already in old links that won't be appended: {}".format(not_appended))
            else:
                appended_links = open(links_path, "a")
                #appended_links.write("\n\nAppended link after iteration n{}:\n".format(i))
                appended_links.write(new_links[j]+"\n")
                appended_links.close() 


if __name__ == "__main__":
    html_path = "/home/gonkaos/Documents/faculdade/inf1803/webcrawler/html_doc.txt"
    url = "https://hackernoon.com/the-secret-hacker-code-974bc55af261"
    links_path = "/home/gonkaos/Documents/faculdade/inf1803/webcrawler/links.txt"
    text = get_raw_txt(url)
    write_html_txt(html_path,text)
    links = get_links(url)
    save_links(links, links_path)
    iterate(links,html_path,3)