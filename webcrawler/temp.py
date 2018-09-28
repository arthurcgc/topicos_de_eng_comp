
""" for i in range(0,max_iter):
        print("Visiting : {}".format(links[i]))
        new_links = get_links(links[i])
    for j in range(0,len(new_links)):
        if new_links[j] in links:
            print("link already in old links and won be appended: {}".format(new_links.pop(j)))
        else:
            appended_links = open(links_path, "a")
            appended_links.write("\n\nAppended link after iteration n{}:\n\n{}".format(i,new_links[j]))
            appended_links.write(new_links[j]+"\n")
            appended_links.close() 
"""
    

    """
    for i in range(0,max_iter):
        text = get_raw_txt(links[i])
        html_doc = open(html_path, "a+")
        html_doc.write("\n\n____________________________________________________________________________________________________________________\n\n")
        html_doc.write("\n\n____________________________________________________________________________________________________________________\n\n")
        html_doc.writelines(text)
        html_doc.close()
    """