from cs50 import SQL

db = SQL("sqlite:///KeasalDB.db")

position = 0

positions = ["main", "language", "category", "word"]

def guide(cmd, ref_id):
    # TODO: (1.Show word) option in word level
    # TODO: Handle exceptions: pos=0 & cmd > 2 || (pos in {1,2} & cmd > 4) || (pos == 3 & cmd in {1, 5, 6, ...})

    global position
    # print(f"ref_id: {ref_id}")
    if cmd == "0":
        ref_id = 0
        position = 0
        next_lvl = positions[position+1]
        print(f"1.Manage in {next_lvl} level")
        print("2.About")
        return 0
    else:
        # print(f"position: {position}")
        cur_lvl = positions[position]
        if cmd == "1":
            if 0 < position:
                new_id = fetch_id(cur_lvl)
                if new_id == -1:
                    # Exception
                    return
                ref_id = new_id

            position +=1
            cur_lvl = positions[position]

            if position in range(1, 4):
                print_elements(cur_lvl, ref_id)

            print(f"ref_id: {ref_id}")
            if position < 3:
                next_lvl = positions[position+1]

            print("0.Go to main")
            if position in {1, 2}:
                print(f"1.Manage in {next_lvl} level")
            print(f"2.Add new {cur_lvl}")
            print(f"3.Edit {cur_lvl}")
            print(f"4.Remove {cur_lvl}")

            return ref_id
        elif cmd == "2":
            print("TODO ADD")
            add(cur_lvl, ref_id)
        elif cmd == "3" or cmd == "4":
            element_id = fetch_id(cur_lvl, "edit or remove")

            if cmd == "3":
                print("TODO Edit")
                # edit(cur_lvl, ref_id)
            if cmd == "4":
                remove(cur_lvl, element_id)
        else:
            print("Incorrect command!")
            position = 0
            reference_id = 0
            return


def add(level, reference):
    print("$")
    print(level)
    new_name = input(f"Name for the new {level}: ")
    if level == "language":
        db.execute("INSERT INTO language (name) VALUES (?)", new_name)
    elif level == "category":
        db.execute("INSERT INTO category (name, language_id) VALUES (?,?)", new_name, reference)
    elif level == "word":
        meaning = input("Meaning for the new word: ")
        db.execute("INSERT INTO word (name, meaning, category_id) VALUES (?, ?, ?)", new_name, meaning, reference)
    print("$$$")

def remove(level, element_id):
    db.execute("DELETE FROM ? where id = ?", level, element_id)

def print_elements(level, reference):
    print("Current elements:")

    if level == "word":
        elements = db.execute("SELECT * FROM ? WHERE category_id = ?;", level, reference)
        for el in elements:
            print(el["name"], end=": ")
            print(el["meaning"])
    else:
        if level == "language":
            elements = db.execute("SELECT name FROM ?;", level)
        elif level == "category":
            elements = db.execute("SELECT name FROM ? WHERE language_id = ?;", level, reference)

        for el in elements:
            print(el["name"])

def fetch_id(level, prompt="access"):
    selected = db.execute("SELECT * FROM ? WHERE name = ?", level, input(f"Input the {level} you want to {prompt}: "))
    if len(selected) == 0:
        print(f"Such {level} does not exist in the database!")
        return -1
    return selected[0]["id"]

def main():
    reference_id = 0
    command = "0"
    # Enter a non-digit input to exit the program
    while command.isdigit():
        reference_id = guide(command, reference_id)
        print(f"position: {position}")
        print("______________________")
        command = input("command: ")
        print()

if __name__ == "__main__":
    main()


#!!!a different approach to add new word:
        # print("Input the word, its meaning and its category")
        # word = list(map(str,input().strip().split()))[:2 * n]
        # print(word)
