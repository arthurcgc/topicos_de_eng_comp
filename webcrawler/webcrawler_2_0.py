#!/usr/bin/python3
import requests
import bs4 as bs
import re
import os
import sqlite3

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
    """     links_txt = open(links_path, 'w')
    for link in links:
        links_txt.write(link + '\n')
    links_txt.close() """
    if os.path.exists(".db"):
        os.remove("rss_urls.db")


def create_html_db():
    """     html_raw_txt = open(html_path,"w", encoding='utf-8')
    html_raw_txt.writelines(text)
    html_raw_txt.close() """
    if os.path.exists("webcrawler.db"):
        os.remove("webcrawler.db")

    html_db = sqlite3.connect("webcrawler.db")
    cursor = html_db.cursor()
    cursor.execute(""" 
    CREATE TABLE IF NOT EXISTS document 
    (
        doc_url TEXT PRIMARY KEY,
        doc TEXT
    );
    """)
    html_db.commit()

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS links
    (
        parent_url TEXT,
        url TEXT PRIMARY KEY,
            FOREIGN KEY (parent_url) REFERENCES document(doc_url)
    );
     """)
    html_db.commit()
    html_db.close()

def populate_db(doc_url, doc_text, links):
    html_db = sqlite3.connect("webcrawler.db")
    cursor = html_db.cursor()
    cursor.execute(""" 
    INSERT INTO document 
    VALUES (?, ?);
     """, (doc_url, doc_text))
    html_db.commit()

    for link in links:
        cursor.execute(""" 
        INSERT INTO links
        VALUES (?, ?);
         """, (doc_url, link))
        html_db.commit()
    html_db.close()


def iterate(og_links,max_iter):
    html_db = sqlite3.connect("webcrawler.db")
    cursor = html_db.cursor()
    j = 0
    for i in range(0,max_iter):
        print("Visiting : {}".format(og_links[i]))
        new_links = get_links(og_links[i])
        n = len(new_links)
        while(j < n):
            # import pdb;pdb.set_trace()
            if new_links[j] in og_links:
                # not_appended = new_links[j]
                print("link already in old links that won't be appended: {}".format(new_links.pop(j)))
                n -= 1
            else:
                cursor.execute(""" 
                INSERT INTO links
                VALUES (?, ?);
                """, (og_links[i], new_links[j]))
                html_db.commit()
                og_links.append(new_links[j])
            j += 1

    attempts = 0
    success = 0
    failed = 0

    """     cursor.execute("SELECT url from links")
        all_links = list(sum(cursor.fetchall(), ())) """\

    for link in og_links:
        print("\nGetting web doc from: {}".format(link))
        try:
            text = get_raw_txt(link)
            print("Success!\n")
            success += 1
            cursor.execute(""" 
            INSERT INTO document
            VALUES (?, ?);
             """, (link, text))
            html_db.commit()

        except:
            print("Failed ;(\n")
            failed += 1
        attempts += 1

    print("Total attempts = {}".format(attempts))
    print("Total successfull connections = {}".format(success))
    print("Total failures = {}".format(failed))

    html_db.close()


def unicorn():
    print(r"""
                  ,,))))))));,
           __)))))))))))))),
\|/       -\(((((''''((((((((.
-*-==//////((''  .     `)))))),
/|\      ))| o    ;-.    '(((((                                  ,(,
         ( `|    /  )    ;))))'                               ,_))^;(~
            |   |   |   ,))((((_     _____------~~~-.        %,;(;(>';'~
            o_);   ;    )))(((` ~---~  `::           \      %%~~)(v;(`('~
                  ;    ''''````         `:       `:::|\,__,%%    );`'; ~
                 |   _                )     /      `:|`----'     `-'
           ______/\/~    |                 /        /
         /~;;.____/;;'  /          ___--,-(   `;;;/
        / //  _;______;'------~~~~~    /;;/\    /
       //  | |                        / ;   \;;,\
      (<_  | ;                      /',/-----'  _>
       \_| ||_                     //~;~~~~~~~~~
           `\_|                   (,~~  -Tua Xiong
                                   \~\
                                    ~~
        """)


r""" def test1():
    unicorn()
    html_path = r"C:\Users\tubas\Desktop\topicos_de_eng_comp\webcrawler\html.txt"
    url = r"https://hackernoon.com/the-secret-hacker-code-974bc55af261"
    links_path = r"C:\Users\tubas\Desktop\topicos_de_eng_comp\webcrawler\links.txt"
    text = get_raw_txt(url)
    write_html_db(text)
    links = get_links(url)
    save_links(links, links_path)
    iterations = 1
    iterate(links,html_path,iterations,links_path) """



if __name__ == "__main__":
    unicorn()
    # html_path = "/home/gonkaos/Documents/faculdade/inf1803/webcrawler/html_doc.txt"
    """     while True:
        try:
            html_path = input("\nType the path you wish to save your html pasta:(i.e /home/gonkaos/Documents/faculdade/inf1803/webcrawler/html_doc.txt)\n")
            f = open(html_path,"w+")
            f.close()
            break
        except:
            print("\nNot a valid path\n") """

    # url = "https://hackernoon.com/the-secret-hacker-code-974bc55af261"
    url = input("\nType the url you wish to scrape:(i.e https://hackernoon.com/the-secret-hacker-code-974bc55af261)\n")

    # links_path = "/home/gonkaos/Documents/faculdade/inf1803/webcrawler/links.txt"
    """     while True:
        try:
            links_path = input("\nType the path you wish to save your links:(i.e /home/gonkaos/Documents/faculdade/inf1803/webcrawler/links.txt)\n")
            f = open(html_path,"w+")
            f.close()
            break
        except:
            print("\nNot a valid path\n") """

    create_html_db()
    text = get_raw_txt(url)
    links = get_links(url)
    populate_db(url, text, links)
    """     save_links(links, links_path) """
    while True:
        whish_to_iter = input("Do you wish to start the iteration now?[Y/N]\n")
        if whish_to_iter == "Y" or whish_to_iter == "y":
            iterations = int(input("Please type the number of iterations:\n"))
            iterate(links,iterations)
            break
        elif whish_to_iter == "N":
            terminate = input("Type \"quit\" if you wish to quit the program\n")
            if terminate == "quit":
                break
        else:
            print("Please check your given input\n")
