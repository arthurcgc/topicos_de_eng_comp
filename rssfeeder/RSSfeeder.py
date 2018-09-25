import feedparser as fp
import re


def ask_urls():
    urls =[]
    while True:
        url = input("Type the url of an RSS feed or type \"quit\" if you're done\n")
        if url != "quit" and url not in urls:
            urls.append(url)
        elif url == "quit":
            break
        else:
            print("You've already typed this url\n")
    return urls


def remove_url(url,urls):
    return urls.remove(url)

def feeder(urls):
    feeds = []
    for i in range(len(urls)):
        feeds[i] = fp.parse(urls[i])
    return feeds
    
def store_RSS_urls(urls,file_path):
    rss_urls = open(file_path, 'w+')
    for url in urls:
        rss_urls.writelines(url)

""" def select_url(url,urls):
    if url in urls:
        feed = fp.parse(url)
    return feed """

def display_articles(feed):
    print(len(feed.entries))
    for i in range(len(feed.entries)):
        print("Article {}".format(i+1))
        try:
            title = feed.entries[i].title
        except:
            title = "Unknown"
        try:
            author = feed.entries[i].source.title
        except:
            try:
                author = feed.entries[i].author
            except:
                author = "Unknown"
        try:
            category = feed.entries[i].category
        except:
            category = "Unknown"
        try:
            date = feed.entries[i].published
        except:
            date = "Unknown"
        print("Title: {}\nAuthor: {}\nCategory: {}\nDate Published: {}\n".format(title, author, category, date))

def display_description(feed_entry):
    summary = feed_entry.summary
    remove_tag = re.compile(r"(<.*>)([^.]*)")
    match = remove_tag.findall(summary)
    #print(match[0][1])
    #import pdb;pdb.set_trace()
    if match[0][1] != None:
        print(match[0][1] + "...")
    else:
        print(match[0][0] + "...")
    ask_summary = input("Do you wish to display the whole text of the article? [Y/N]\n")
    if ask_summary == "Y":
        print(summary)


if __name__=="__main__":
    urls = ask_urls()
    print(urls)
    delete_url = input("Do you want to exclude any previously typed url? If so type 1:\n")
    if delete_url == 1:
        remove = input("type the url you wish to remove:\n")
        remove_url(remove,urls)
    print(urls)
    file_path = input("Type the file path you wish to save your RSS urls:\n")
    store_RSS_urls(urls, file_path)
    for i in range(len(urls)):
        print("\n{}st url:\t{}\n".format(i+1, urls[i]))
    index = int(input("From the list above, type the number that corresponds to the url you wish to see the articles from\n"))
    feed = fp.parse(urls[index-1])
    display_articles(feed)
    while True:
        q_read_article = input("Do you wish to see a description from an article from the list above? Y/N\n")
        if q_read_article == "Y":
            art_index = int(input("Type the article number you wish to see:\n")) - 1
            display_description(feed.entries[art_index])
        elif q_read_article == "N":
            break
        else:
            pass


