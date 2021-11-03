from cs50 import SQL

db = SQL("sqlite:///KeasalDB.db")

position = 0

positions = ["database", "language", "category", "word"]

def keasalpy(cmd, ref_id):
    global position

    if not is_valid_command(cmd):
        print("Bad command!")
        return ref_id

    print(f"cmd: {cmd} || ref_id: {ref_id}")

    if cmd == "0":
        position = 0
        next_lvl = positions[position+1]
        print(f"1.Manage in {next_lvl} level")  # TODO: add this line to guide()
        print("2.About")                        # TODO: add this line to guide()
        return 0
    else:
        cur_lvl = positions[position]
        if position in range(0, 3) and cmd == "1":
            if 0 < position:
                target_element = fetch_element(ref_id)
                if target_element[0] == False:    # Exception
                    print(f"Such {cur_lvl} does not exist!")
                    return ref_id
                ref_id = target_element[0]["id"]

            position +=1
            cur_lvl = positions[position]

            if position in range(1, 4):
                print_elements(ref_id)

            # TODO: put next 16 lines in a function named "guide"
            print("0.Go to main")
            if position in {1, 2}:
                next_lvl = positions[position+1]
                print(f"1.Manage in {next_lvl} level")

            print(f"2.Add new {cur_lvl}")
            print(f"3.Edit {cur_lvl}")
            print(f"4.Remove {cur_lvl}")

            #NEW
            if position == 2:
                print(f"5.Show all words in this {cur_lvl}")
            if position in {2, 3}:
                print(f"6.Take a peek at words")
                print(f"7.Take test")
            return ref_id
            #####################################################

        if cmd == "2":
            if position == 0:
                print_about()
                return ref_id

            new_element = fetch_element(ref_id, "add")
            if new_element[0] != False:
                print("This element already exists!")
                return ref_id
            add(ref_id, new_element[1])

        elif 0 < position and (cmd == "3" or cmd == "4"):
            target_element = fetch_element(ref_id, "edit or remove")
            if target_element[0] == False:    # Exception
                print(f"Such {cur_lvl} does not exist!")
                return ref_id
            element_id = target_element[0]["id"]

            if cmd == "3":
                edit(element_id)
            if cmd == "4":
                remove(element_id)

        elif position in {2, 3} and  cmd in {"5", "6", "7"} :
            if cmd in {"5", "6"}:
                represent_lang_words(cmd, ref_id)
            else:
                print("TODO: test!")
                # take_test(, )

        else:
            print("Incorrect command!")
            return ref_id

        # print(f"cmd: {cmd}; position: {position}")
        if position != 0 and int(cmd) in range(0, 5):
            print_elements(ref_id)

        return ref_id

def is_valid_command(cmd):
    if cmd in {"0", "2"}:
        return True

    if cmd == "1":
        if position in range(0, 3):
            return True
        else:
            return False

    if cmd in {"3", "4"}:
        if position in range(1, 4):
            return True
        else:
            return False

    if cmd == "5":
        if position == 2:
            return True
        else:
            return False

    if cmd in {"6", "7"}:
        if position in {2, 3}:
            return True
        else:
            return False

    else:
        return False

def represent_lang_words(cmd, reference):
    level = positions[position]
    # level is either category or word
    if level == "category":
        words = db.execute("SELECT * FROM word WHERE category_id IN (SELECT id FROM category WHERE language_id=?)", reference)  #haven`t been tested
        for word in words:
            print(word["name"], end=": ")
            if cmd == "6":
                input()
            print(word["meaning"])

    else:
        words = db.execute("SELECT * FROM word WHERE category_id=?", reference)
        for word in words:
            print(word["name"], end=": ")
            if cmd == "6":
                input()
            print(word["meaning"])

def add(reference, new_name):
    level = positions[position]
    if level == "language":
        db.execute("INSERT INTO language (name) VALUES (?)", new_name)
    elif level == "category":
        print("adding category")
        db.execute("INSERT INTO category (name, language_id) VALUES (?,?)", new_name, reference)
    elif level == "word":
        meaning = input("Meaning for the new word: ")
        db.execute("INSERT INTO word (name, meaning, category_id) VALUES (?, ?, ?)", new_name, meaning, reference)

def edit(element_id):
    level = positions[position]
    # print(level + str(element_id))
    if level == "word":
        editting_col = input("What do you want to edit in this element(only name or meaning)? ")
        if editting_col not in {"name","meaning"}:
            print(f"Such attribute does not exist in a {level}")
        new_value = input(f"Enter the new {editting_col}(Enter 'cancel' to cancel this operation): ")
        if new_value == "cancel":
            return
        db.execute("UPDATE ? SET ?=? where id=?;", level, editting_col, new_value, element_id)
    else:
        updated_name = input(f"new name for this {level}: ")
        db.execute("UPDATE ? SET name=? where id=?;", level, updated_name, element_id)

def remove(element_id):
    level = positions[position]
    db.execute("DELETE FROM ? where id = ?;", level, element_id)

def print_elements(reference):
    level = positions[position]
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

def fetch_element(reference, prompt="access"):
    level = positions[position]
    target = input(f"Input the name of the {level} you want to {prompt}: ")

    if level == "language":
        selected = db.execute("SELECT * FROM ? WHERE name = ?", level, target)
    else:
        # print(f"level: {level}")
        # print(f"reference: {reference}")
        # print(target)
        selected = db.execute("SELECT * FROM category WHERE language_id = ? AND name = ?", reference, target)


    if len(selected) == 0:
        # such element does not exist
        return [False, target]
    # print(selected[0]["name"])
    return selected

def print_about():
    print("This program helps expand your vocabulary when learning a new language")
    print("It provides you three levels of: language, category and word")
    print("That`s right! you can store words in different languages and have them categorized!")
    print("The name of this project is 'Keasal', a Kurdish word meaning 'turtle',")
    print("which is a symbol of wisdom and patience. May you enjoy your journey ;)")
    print("     !)Pay attention to the prompts and follow them")
    print("     0.Go to main")
    print("  exit.To stop the program")

def main():
    reference_id = 0
    command = "0"
    while command != "exit":
        reference_id = keasalpy(command, reference_id)
        print(f"____________{position}_______________")     # TODO: add this line to guide()
        command = input("command: ")
        print()

if __name__ == "__main__":
    main()
