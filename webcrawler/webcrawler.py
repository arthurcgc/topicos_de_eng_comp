import requests
import bs4 as bs
import re


def write_urldoc(url_list, url_path):
    try:
        urltxt_file = open(url_path, 'r')
        old_links = urltxt_file.readlines() # saves each line in a list of lines
        new_links = set(old_links) - set(url_list)
        urltxt_file.close()
        
        for link in new_links:
            urltxt_file = open(url_path, 'a')
            urltxt_file.writelines(str(link))
            urltxt_file.writelines("\n")
                


    except FileNotFoundError:
        for link in url_list:
            if link is not False:
                urltxt_file = open(url_path, 'a+')
                urltxt_file.writelines(str(link))
                urltxt_file.writelines("\n")

    urltxt_file.close()
    
    return url_path

""" main function,  creates the txt files and populates them"""
def getwebdoc(url, html_path, url_path):
    # rawtxt_name = input("Type File Name\n")
    # html_path = file_location + '/' + "html_doc.txt"
    rawtxt_file = open(html_path, 'w')
    docs = [html_path] # list which will contain the filepaths of the original docs
    resp = requests.get(url) # Obtaining first url to scrape
    soup = bs.BeautifulSoup(resp.content,"html.parser")
    rawtxt_file.write(soup.prettify()) # writing first txt file with html tags
    rawtxt_file.close()
    #Populating url links
    urls = ishtmltag(html_path) # urls contains all the non duplicate links found in the html file
    url_doc = write_urldoc(urls, url_path) # auxiliary variable for clarity, it contains the text file location containing all the hyperlinks
    docs.append(url_doc) # appends url_doc to the list of file_locations
    return docs


""" receives a string as an arg and returns the hiperlink 
or returns False if the string does not contain a hyperlink """
def isurllink(line):
    link_regex = re.compile(r"href=(\"|\')(http[s|\.|/*|:]*\w*[\.|/|\w|-]*)(\"|\')")
    match = link_regex.findall(line)
    if match:
        return match[0][1]
    else:
        return False

        
""" filters html tags, purging them and returns hyperlink list """
def ishtmltag(html_path):
    file = open(html_path,"r")
    lines = file.readlines() # saves each line in a list of lines
    file.close()
    tag_regex = re.compile(r"<.*|.*>") # regex to detect html tag
    file = open(html_path, "w") #reopens the file
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


def iterate_urllinks(fp_list, iter_limit): #fp_list = docs ; iter_limit = iteration limit determined by the user
    og_html = fp_list[0] # original html filepath
    url_doc = fp_list[1] # original urls filepath
    strip_txt = og_html[0:-4] # strips the ".txt" from the string
    file = open(url_doc, "r") # opens the doc containing all the hyperlinks of the original page
    lines = file.readlines()
    file.close()
    for i in range(0,len(lines)):
        if i == iter_limit:
            break
        else:
            newdoc = strip_txt + "_link[" + str(i) + "].txt"
            getwebdoc(lines[i], newdoc, url_doc)


if __name__ == "__main__":
    og_url = input("Type the target url\n")
    location = input("Type the location of the txt files\n")
    html_path = location + '/' + "html_doc.txt"
    url_path = location + '/' + "url_doc.txt"
    docs = getwebdoc(og_url, html_path, url_path)
    print(docs)
    n_iters = input("Type the maximum number of iterations in decimal form:")
    iterate_urllinks(docs, int(n_iters))