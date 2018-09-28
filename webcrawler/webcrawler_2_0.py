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

def iterate(og_links,html_path,max_iter,links_path):
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
                # appended_links.write("\n\nAppended link after iteration n{}:\n".format(i))
                appended_links.write(new_links[j]+"\n")
                appended_links.close()
                # now we iterate getting the raw text from the webdoc
    
    
    attempts = 0
    success = 0
    failed = 0
    all_links = open(links_path,"r")
    for link in all_links:
        print("\nGetting web doc from: {}".format(link))
        try:
            text = get_raw_txt(link)
            print("Success!\n")
            success += 1
        except:
            print("Failed ;(\n")
            failed += 1
        html_doc = open(html_path,'a')
        html_doc.write("\n\n___________________________________________________________________________________________________________________\n\n")
        html_doc.write("\n\n___________________________________________________________________________________________________________________\n\n")
        html_doc.write("\n\n___________________________________________________________________________________________________________________\n\n")
        html_doc.writelines(text)
        html_doc.close()
        attempts += 1
    
    all_links.close()
    print("Total attempts = {}".format(attempts))
    print("Total successfull connections = {}".format(success))
    print("Total failures = {}".format(failed))
    


def unicorn():
    print("""
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



if __name__ == "__main__":
    unicorn()
    # html_path = "/home/gonkaos/Documents/faculdade/inf1803/webcrawler/html_doc.txt"
    while True:
        try:
            html_path = input("\nType the path you wish to save your html pasta:(i.e /home/gonkaos/Documents/faculdade/inf1803/webcrawler/html_doc.txt)\n")
            f = open(html_path,"w+")
            f.close()
            break
        except:
            print("\nNot a valid path\n")
    
    # url = "https://hackernoon.com/the-secret-hacker-code-974bc55af261"
    url = input("\nType the url you wish to scrape:(i.e https://hackernoon.com/the-secret-hacker-code-974bc55af261)\n")

    # links_path = "/home/gonkaos/Documents/faculdade/inf1803/webcrawler/links.txt"
    while True:
        try:
            links_path = input("\nType the path you wish to save your html pasta:(i.e /home/gonkaos/Documents/faculdade/inf1803/webcrawler/links.txt)\n")
            f = open(html_path,"w+")
            f.close()
            break
        except:
            print("\nNot a valid path\n")
        
    text = get_raw_txt(url)
    write_html_txt(html_path,text)
    links = get_links(url)
    save_links(links, links_path)
    while True:
        whish_to_iter = input("Do you wish to start the iteration now?[Y/N]\n")
        if whish_to_iter == "Y":
            iterations = int(input("Please type the number of iterations:\n"))
            iterate(links,html_path,iterations,links_path)
            break
        elif whish_to_iter == "N":
            terminate = input("Type \"quit\" if you wish to quit the program\n")
            if terminate == "quit":
                break
        else:
            print("Please check your given input\n")
