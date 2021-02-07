import mechanicalsoup

import re
import time
import json


#checks if class matches the given element so only author info goes into the author spot etc. this might be unecessary but I don't know.
def tagattrcheck(*, element, attribute, target ):
#    print(element.get(attribute))
    if element.get(attribute) == target:
         return True
    else:
        print(f"no {target}")
        return False


def ensearch():
    pass


def jpnsearch(*, ofile = "jpbooks.json", ifile = "isbnlist.txt", startid = 0):

#    ofile = "jpbooks.json"
#    ifile = "isbnlist.txt"
#    startid = 0        #to continue numbering an existing json
#creating the browser 
    browser = mechanicalsoup.StatefulBrowser(user_agent = 'PersonalLibrary: cowstaktetime@gmail.com')
    browser.set_verbose(2)
    isbns = []
#takes in the file without newline
    with open(ifile,"r", newline = "") as ilf:
        badisbn  = ilf.readlines()
        for arf in badisbn:
            isbns.append(arf.strip())
#    isbns = ["97840490078931", "4757719884"]       #error isbns
#    print(isbns[0])
    browser.open("https://www.books.or.jp/free-search")
    browser.select_form()
    counter = 1
    idcounter = startid
    currbook = {}
#iterate over list of isbns
    for num in isbns:
        currbook["_id"] = idcounter
        browser.open("https://www.books.or.jp/free-search")
        browser.select_form()
        browser["free-word-text"] = num
        browser.submit_selected()
        book = browser.page
#returns list of td elements. these are the search results.
        booktable = book.find_all('td')
#        print(len(booktable))
#account for no data from this site.
        if len(booktable) == 0:
            print(f"Error on ISBN {counter} {num}: No data found")
            with open("errors.txt", "a") as errfile:
                errfile.write(f"No data: ISBN {counter} {num}\n")
            counter += 1
            continue 
#creating dict of html tags to use in the tagattrcheck function. custom to site.
        numsdict = {0 : "'nothing'", 1 : ['books__type-title'], 2 : ['books__type-author'], 3 : ['books__type-date'], 4 : ["books__type-publisher"]}
        numsdicttojson = {0 : "nothing", 1 : "title", 2 : "author", 3 : "published_date", 4 : "publisher"}
#counter is for list of ISBNs for good error reports. idcounter iterates the id up for the json.
        counter += 1
        idcounter += 1
        for i in range(1, len(numsdict)):
#uses the order that the website returns
            if tagattrcheck(target=numsdict[i], attribute='class', element=booktable[i]):
#formatting the text for pretty json entries
                if i == 2:
                    currbook[numsdicttojson[i]] = re.sub('\n', '|', re.sub(' +', ' ', booktable[i].get_text().strip()))
                else:
                    currbook[numsdicttojson[i]] = booktable[i].get_text().strip()
            else:
                print(f"Something went wrong: ISBN no. {counter} {num}, numsdict iter{i}")
#ascii=False because it hates jp characters by default?
        currjson = (json.dumps(currbook, ensure_ascii=False))
#        print(currjson)
#print valid entries to file
        with open(ofile, "a") as file:
            file.write(currjson + ",\n")
            print(f"isbn {counter} {num} success")
#be a nice scraper and don't bombard. TODO: randomize the 1
#        break
        time.sleep(1)

#jpnsearch()

