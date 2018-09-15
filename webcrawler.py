import requests
import bs4 as bs
import re

""" main function,  creates the txt files and populates them"""
def crawler(url, file_location):
    rawtxt_name = input("Type File Name\n")
    file_path = file_location + '/' + rawtxt_name + '.txt'
    rawtxt_file = open(file_path, 'w')
    resp = requests.get(url) # Obtaining first url to scrape
    soup = bs.BeautifulSoup(resp.content,"html.parser")
    rawtxt_file.write(soup.prettify()) # writing first txt file with html tags
    rawtxt_file.close()
    #Populating url links
    urls = ishtmltag(file_path) # filtering html tags and returning hyperlink list
    urltxt_name = input("Type urltxt name\n")
    file_path = file_location + '/' + urltxt_name + '.txt'
    urltxt_file = open(file_path, 'w')
    for link in urls:
        if link:
            urltxt_file.writelines(link+"\n")
    urltxt_file.close()


""" receives a string as an arg and returns the hiperlink 
or returns False if the string does not contain a hyperlink """
def isurllink(line):
    link_regex = re.compile(r"href=(\"|\')(http[s|\.|/*|:]*\w*[\.|/|\w|-]*)(\"|\')")
    match = link_regex.findall(line)
    if match:
        #print(line)
        #print(match)
        return match[0][1]
    else:
        return False

        
""" Gets the raw html file and purges the html tags, 
leaving only raw text in the original file """
def ishtmltag(file_path):
    file = open(file_path,"r")
    lines = file.readlines() # saves each line in a list of lines
    file.close()
    tag_regex = re.compile(r"<.*|.*>") # regex to detect html tag
    file = open(file_path, "w") #reopens the file
    url_list = []
    for line in lines:
        match = tag_regex.match(line)
        if match is not None:
            link = isurllink(line)
            if link is not None and link not in url_list:
                url_list.append(link) #populates list of hyperlinks
        else:
            file.write(line) # if it's not an html tag, rewrites the line in the file
    file.close()
    return url_list

if __name__ == "__main__":
    og_url = input("Type the target url\n")
    location = input("Type the location of the txt files\n")
    crawler(og_url, location)