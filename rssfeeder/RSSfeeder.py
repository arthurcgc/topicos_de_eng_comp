import feedparser as fp

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
        print("\t\tTitle\t\tAuthor\t\tCategory\t\tPublished\t\t")
        print()
        print("\t\t{0}\t\t{1}\t\t{2}\t\t{3}\t\t".format(feed.entries[i].title, feed.entries[i].source.title, feed.entries[i].category, feed.entries[i].published))
            
    

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

