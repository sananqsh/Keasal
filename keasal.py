from cs50 import SQL

db = SQL("sqlite:///KeasalDB.db")

def print_help(position):
    if position == "main":
        print("1.Manage language")
        print("2.About")
    else:
        print("0.Go to main")
        if position == "lang":
            print("11.Add new language")    #TODO
            print("Edit, Remove or Gain access to a current language by entering its name")

    print("Please enter your command")

def print_langs():
    print("Current Languages:")
    langs_names = db.execute("SELECT name FROM langs;")
    for lang in langs_names:
        print(lang["name"])
    print()

def main():
    #DEFAULT LANG IS ENG and has DEFCAT1 as its default category
    # db = SQL("sqlite:///KeasalDB.db")
    position = "main"
    print_help(position);

    while position != "exit":
        cmd = input("command: ")

        if cmd == "0":
            position = "main"
        elif cmd == "1":
            position = "lang"
            print_langs()
            print_help(position)
        elif cmd == "11":
            #TODO
            print("TODO")

if __name__ == "__main__":
    main()
