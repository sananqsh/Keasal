from cs50 import SQL

db = SQL("sqlite:///KeasalDB.db")

def guide(position):
    if position == "0" or not position.isdigit():
        print("1.Manage languages")
        print("2.About")
        return
    else:
        print("0.Go to main")
        if position == "1":
            print_langs()
            print("11.Add new language")    #TODO
            print("12.Manage current languages")
            return
        if position == "11":
            print("Input a name for the new language: ")
            new_lang = input()
            db.execute("INSERT INTO langs(name) VALUES(?);", new_lang)
            # print("Input the word, its meaning and its category")
            # word = list(map(str,input().strip().split()))[:2 * n]
            # print(word)
            return
        if position == "12":
            print("Edit, Remove or Gain access to a current language by entering its name")
            input_lang = input("Language name: ")
            sel_lang = db.execute("SELECT name FROM langs WHERE name = ?", input_lang)
            if sel_lang == None:
                print("Such language does not exist in the database!")
                return
            # For debug:
            # print(sel_lang[0]["name"])

            
            return


def print_langs():
    print("Current Languages:")
    langs_names = db.execute("SELECT name FROM langs;")
    for lang in langs_names:
        print(lang["name"])
    print()

def main():
    #DEFAULT LANG IS ENG and has DEFCAT1 as its default category
    # db = SQL("sqlite:///KeasalDB.db")
    pos = "0"
    guide(pos);
    while pos != "-1":
        pos = input("command: ")
        guide(pos)
        print()

if __name__ == "__main__":
    main()
