from cs50 import SQL

db = SQL("sqlite:///KeasalDB.db")

position = 0

positions = ["about", "language", "category", "word"]

DEFAULT_UNDERLINES = 15

CANCEL_PROMPT = "Cancelled"

def keasalpy(cmd, ref_id):
    global position

    if not is_valid_command(cmd):
        print("Bad command!")
        return ref_id

    print(f"cmd: {cmd} || ref_id: {ref_id}")

    if cmd == "00":
        position = 0
        ref_id = 0
        guide(ref_id)

    if cmd == "0":
        position = 1
        ref_id = 0
        guide(ref_id)

    cur_lvl = positions[position]

    if cmd == "1":
        prev_ref = ref_id

        if 0 < position:
            entry = take_entry(ref_id)
            if entry == CANCEL_PROMPT:
                print(CANCEL_PROMPT)
                return ref_id

            target_element = fetch_element(entry, ref_id)

            if target_element == False:         # Exception
                print(f"Such {cur_lvl} does not exist!")
                return ref_id

            ref_id = target_element["id"]

        position +=1
        guide(ref_id)


    elif cmd == "2":
        new_element = take_entry(ref_id, "add")
        if new_element == CANCEL_PROMPT:
            print(CANCEL_PROMPT)
            return ref_id
        if cur_lvl == "language" and already_exists(new_element):
            print(f"This {cur_lvl} already exists!")
            return ref_id

        add(ref_id, new_element)

    elif cmd in {"3", "4"}:
        entry = take_entry(ref_id, "edit or remove")
        if entry == CANCEL_PROMPT:
            print(CANCEL_PROMPT)
            return ref_id

        target_element = fetch_element(entry, ref_id)

        if target_element == False:    # Exception
            print(f"Such {cur_lvl} does not exist!")
            return ref_id

        element_id = target_element["id"]

        if cmd == "3":
            edit(element_id)
        if cmd == "4":
            remove(element_id)

    elif cmd in {"5", "6", "7"} :
        represent_lang_words(cmd, ref_id)

        return ref_id

    # print(f"cmd: {cmd}; position: {position}")
    if cmd in {"2", "3", "4"}:
        print_elements(ref_id)

    return ref_id

def guide(reference):
    prev_level = positions[position-1]       #TODO: fix level problems
    level = positions[position]

    print(f"lvl: {level}")

    # header = "WHAAT!?"     # By default
    if reference == 0:
        if position == 0:
            header = "Keasal"
        if position == 1:
            header = "Your Languages"

    else:
        element = db.execute("SELECT * FROM ? WHERE id=?", prev_level, reference)
        header = element[0]["name"]

    generate_borderline(header, DEFAULT_UNDERLINES)

    if position in range(1, 4):
       print_elements(reference)

    if position == 0:
        print_about()

    ### PROPMTS

    if position == 1:
        print("00.About")

    # 0-command also works anywhere but it`s more user friendly not to
    # prompt it in position=0
    if 1 < position:
        print("0.Go to main")

    if position < 3:
        next_level = positions[position+1]
        print(f"1.Manage in {next_level} level")

    if 0 < position:
        print(f"2.Add new {level}")
        print(f"3.Edit {level}")
        print(f"4.Remove {level}")

    if position == 2:
        print(f"5.Show all words in this {level}")

    if 1 < position:
        print(f"6.Take a peek at words")
        print(f"7.Take test")

    print("exit.To stop the program")

    generate_borderline(position, DEFAULT_UNDERLINES)

def generate_borderline(title, n):
    edge_size = n - len(str(title))//2

    for x in range(0, edge_size):
        print("_", end="")

    print(title, end="")

    for x in range(0, edge_size):
        print("_", end="")

    print()

def cancelling(text):
    if text == "cancel":
        return True
    return False

def is_valid_command(cmd):
    if cmd == "00":
        if position in [0, 1]:
            return True
        return False

    if cmd in {"0", "2"}:
        return True

    if cmd == "1":
        if position in range(0, 3):
            return True
        return False

    if cmd in {"3", "4"}:
        if position in range(1, 4):
            return True
        return False

    if cmd == "5":
        if position == 2:
            return True
        return False

    if cmd in {"6", "7"}:
        if position in {2, 3}:
            return True
        return False

    else:
        return False

def represent_lang_words(cmd, reference):
    level = positions[position]
    # level is either category or word
    if level == "language":
        words = db.execute("SELECT * FROM word WHERE category_id=?", reference)
    else:
        words = db.execute("SELECT * FROM word WHERE category_id IN (SELECT id FROM category WHERE language_id=?)", reference)

    for word in words:
        print(word["name"], end=": ")

        if cmd == "7":
            answer = input()
            if answer != word["meaning"]:
                print("Correct answer: " + word["meaning"])

        else:
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
        meaning = take_entry(reference, "add", "meaning")
        if meaning == CANCEL_PROMPT:
            print(CANCEL_PROMPT)
            return
        db.execute("INSERT INTO word (name, meaning, category_id) VALUES (?, ?, ?)", new_name, meaning, reference)

def edit(element_id):
    level = positions[position]
    # print(level + str(element_id))
    if level == "word":
        editting_col = input(f"Do you want to edit name or meaning(Enter 'cancel' to cancel this operation)? ")
        if cancelling(editting_col):
            print(CANCEL_PROMPT)
            return
        #
        if editting_col not in {"name","meaning"}:
            print(f"Such attribute does not exist in a {level}")
            return
        #
        new_value = input(f"Enter the new {editting_col}(Enter 'cancel' to cancel this operation): ")
        if cancelling(new_value):
            print(CANCEL_PROMPT)
            return

        db.execute("UPDATE ? SET ?=? where id=?;", level, editting_col, new_value, element_id)
    else:
        updated_name = input(f"Enter the new name for this {level}(Enter 'cancel' to cancel this operation): ")
        if cancelling(updated_name):
            print(CANCEL_PROMPT)
            return
            #
        if level == "language" and already_exists(updated_name):
            print(f"Such {level} already exists!")
            return
        db.execute("UPDATE ? SET name=? where id=?;", level, updated_name, element_id)

def remove(element_id):
    level = positions[position]
    db.execute("DELETE FROM ? where id = ?;", level, element_id)

def fetch_element(target, reference): #, prompt="access"):
    # level = positions[position]
    # target = input(f"The name of the {level} you want to {prompt}(Enter 'cancel' to cancel this operation): ")
    # if cancelling(target):
    #     return CANCEL_PROMPT
    result = already_exists(target, reference)
    if not result:
        # such element does not exist
        return False

    print(result)
    return result

def already_exists(name, reference=0):
    level = positions[position]

    if level == "language":
        selected = db.execute("SELECT * FROM ? WHERE name = ?", level, name)
    elif level == "category":
        selected = db.execute("SELECT * FROM category WHERE language_id = ? AND name = ?", reference, name)
    else:
        selected = db.execute("SELECT * FROM word WHERE category_id = ? AND name = ?", reference, name)

    if len(selected) == 0:
        return False
    # return False
    return selected[0]

def take_entry(reference, action_prompt="access", attribute_prompt="name"):
    level = positions[position]
    entry = input(f"The {attribute_prompt} of the {level} you want to {action_prompt}(Enter 'cancel' to cancel this operation): ")
    if cancelling(entry):
        return CANCEL_PROMPT
    return entry

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

def print_about():
    print("This program helps expand your vocabulary when learning a new language")
    print("It provides you three levels of: language, category and word")
    print("That`s right! you can store words in different languages and have them categorized!")
    print("The name of this project is 'Keasal', a Kurdish word meaning 'turtle',")
    print("which is a symbol of wisdom and patience. May you enjoy your journey ;)")
    print("!)Pay attention to the prompts and follow them")
    print()

def main():
    reference_id = 0
    command = "0"
    while command != "exit":
        reference_id = keasalpy(command, reference_id)
        command = input("command: ")
        print()

if __name__ == "__main__":
    main()
