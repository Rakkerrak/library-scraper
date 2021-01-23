import mechanicalsoup

import re
import time
import json



def tagattrcheck(*, element, attribute, target ):
#    print(element.get(attribute))
    if element.get(attribute) == target:
         return True
    else:
        print(f"no {target}")
        return False


def jpnsearch():

    ofile = "jpbooks.json"
    
    browser = mechanicalsoup.StatefulBrowser(user_agent = 'PersonalLibrary: cowstaktetime@gmail.com')
    browser.set_verbose(2)

    isbn = ["9784048910835", "97848322025101", "9784840221306"]

    browser.open("https://www.books.or.jp/free-search")
    browser.select_form()
    counter = 0
    idcounter = 0
    currbook = {}
    for num in isbn:
        currbook["_id"] = idcounter
        browser.open("https://www.books.or.jp/free-search")
        browser.select_form()
        browser["free-word-text"] = num
        browser.submit_selected()
        book = browser.page
        booktable = book.find_all('td')
        print(len(booktable))
        if len(booktable) == 0:
            print(f"Error on ISBN {counter} {num}: No data found")
            counter += 1
            continue
        numsdict = {0 : "'nothing'", 1 : ['books__type-title'], 2 : ['books__type-author'], 3 : ['books__type-date'], 4 : ["books__type-publisher"]}
        numsdicttojson = {0 : "nothing", 1 : "title", 2 : "author", 3 : "published_date", 4 : "publisher"}
        counter += 1
        idcounter += 1
        for i in range(1, len(numsdict)):
            if tagattrcheck(target=numsdict[i], attribute='class', element=booktable[i]):
                if i == 2:
                    currbook[numsdicttojson[i]] = re.sub('\n', '|', re.sub(' +', ' ', booktable[i].get_text().strip()))
                else:
                    currbook[numsdicttojson[i]] = booktable[i].get_text().strip()
        currjson = (json.dumps(currbook, ensure_ascii=False))
        print(currjson)
        with open(ofile, "a") as file:
            file.write(currjson + ",\n")
            print(f"isbn {counter} {num} success")
        time.sleep(1)

jpnsearch()

