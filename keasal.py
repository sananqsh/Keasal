from cs50 import SQL

db = SQL("sqlite:///KeasalDB.db")

position = 0

positions = ["main", "language", "category", "word"]

def guide(cmd, ref_id):
    # TODO: Handle exceptions: pos=0 & cmd > 2 || (pos in {1,2} & cmd > 4) || (pos == 3 & cmd in {1, 5, 6, ...})

    global position
    if cmd == "0":
        position = 0
        next_lvl = positions[position+1]
        print(f"1.Manage in {next_lvl} level")
        print("2.About")
        return 0
    else:
        cur_lvl = positions[position]
        if cmd == "1":
            if 0 < position:
                new_id = fetch_id(cur_lvl)
                if new_id == -1:
                    # Exception
                    return ref_id
                ref_id = new_id

            position +=1
            cur_lvl = positions[position]

            if position in range(1, 4):
                print_elements(cur_lvl, ref_id)

            # Uncomment to debug:
            # print(f"ref_id: {ref_id}")
            if position < 3:
                next_lvl = positions[position+1]

            print("0.Go to main")
            if position in {1, 2}:
                print(f"1.Manage in {next_lvl} level")
            print(f"2.Add new {cur_lvl}")
            print(f"3.Edit {cur_lvl}")
            print(f"4.Remove {cur_lvl}")

            return ref_id
        else:
            if cmd == "2":
                if position == 0:
                    print("This program helps expand your vocabulary when learning a new language")
                    print("It provides you three levels of: language, category and word")
                    print("That`s right! you can store words in different languages and have them categorized!")
                    print("The name of this project is 'Keasal', a Kurdish word meaning 'turtle',")
                    print("which is a symbol of wisdom and patience. May you enjoy your journey ;)")
                    return ref_id
                add(cur_lvl, ref_id)
            elif cmd == "3" or cmd == "4":
                element_id = fetch_id(cur_lvl, "edit or remove")
                if element_id == -1:
                    return ref_id
                print(element_id)
                if cmd == "3":
                    edit(cur_lvl, element_id)
                if cmd == "4":
                    remove(cur_lvl, element_id)
            else:
                print("Incorrect command!")
                position = 0
                reference_id = 0
                return ref_id

def add(level, reference):
    new_name = input(f"Name for the new {level}: ")
    if level == "language":
        db.execute("INSERT INTO language (name) VALUES (?)", new_name)
    elif level == "category":
        db.execute("INSERT INTO category (name, language_id) VALUES (?,?)", new_name, reference)
    elif level == "word":
        meaning = input("Meaning for the new word: ")
        db.execute("INSERT INTO word (name, meaning, category_id) VALUES (?, ?, ?)", new_name, meaning, reference)

def edit(level, element_id):
    print(level + str(element_id))
    if level == "word":
        editting_col = input("What do you want to edit in this element(only name or meaning)? ")
        if editting_col not in {"name","meaning"}:
            print(f"Such attribute does not exist in a {level}")
        new_value = input(f"Enter the new {editting_col}: ")

        db.execute("UPDATE ? SET ?=? where id=?;", level, editting_col, new_value, element_id)
    else:
        updated_name = input(f"new name for this {level}: ")
        db.execute("UPDATE ? SET name=? where id=?;", level, updated_name, element_id)

def remove(level, element_id):
    db.execute("DELETE FROM ? where id = ?;", level, element_id)

def print_elements(level, reference):
    print("Current elements: { ")

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

    print("}")

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
        print("______________________")
        command = input("command: ")
        print()

if __name__ == "__main__":
    main()
