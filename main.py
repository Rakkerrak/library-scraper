import scraper

def main():
    print("This will search https://www.books.or.jp/free-search . Please make sure your input file has one isbn per line.")
    print("Leave blank for defaults")
    ifile = input("\nType file name with isbns: ")
    ofile = input("\nType output file name: ")
    valid = False
    nones = ["", " ", "\n", None]
    while valid == False:
        try:
            startid = input("\nType integer to start id of json items: ")
            if startid not in nones:
                startid = int(startid)
            valid = True
        except ValueError:
            print("Must be an integer") 
    nones = ["", " ", "\n", None]
    if ifile in nones:
        ifile = "isbnlist.txt"
    if ofile in nones:
        ofile = "jpbooks.json"
    if startid in nones:
        startid = 0

    print(f"{ifile} {ofile} {startid} ")
    scraper.jpnsearch(ifile = ifile, ofile = ofile, startid = startid)

if __name__ == "__main__":
    main()
