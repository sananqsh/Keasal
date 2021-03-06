import random
from cs50 import SQL

db = SQL("sqlite:///KeasalDB.db")

position = 0

positions = ["about", "language", "category", "word"]

DEFAULT_UNDERLINES = 16

ABOUT_PAGE_UNDERLINES = 38

CANCEL_PROMPT = "Cancelled"

MINIMUM_TEST_SUBJECTS = 10

def keasalpy(cmd, ref_id):
    global position

    if not is_valid_command(cmd):
        print("Bad command!")
        return ref_id

    # Uncomment to debug
    # print(f"cmd: {cmd} || ref_id: {ref_id}")

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
        if cur_lvl != "category" and already_exists(new_element, ref_id):
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

    elif cmd in {"5", "6"} :
        represent_lang_words(cmd, ref_id)
        return ref_id

    elif cmd == "7":
        take_test(ref_id)
        return ref_id

    elif cmd == "help":
        guide(ref_id)
        return ref_id

    if cmd in {"2", "3", "4"}:
        print_elements(ref_id)

    return ref_id

def guide(reference):
    prev_level = positions[position-1]
    level = positions[position]

    no_of_underlines = DEFAULT_UNDERLINES
    if reference == 0:
        if position == 0:
            header = "Keasal"
            no_of_underlines = ABOUT_PAGE_UNDERLINES
        if position == 1:
            header = "Home"

    else:
        element = db.execute("SELECT * FROM ? WHERE id=?", prev_level, reference)
        header = element[0]["name"]

    generate_borderline(no_of_underlines, header)

    if position in range(1, 4):
       print_elements(reference)

    if position == 0:
        print_about()

    ### PROPMTS

    if position == 1:
        print("00.About")

    # 0-command works everywhere but it`s more user friendly not to
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
        next_level = positions[position+1]
        print(f"5.Show all {next_level}s")

    if 1 < position:
        print(f"6.Peek at words")
        print(f"7.Take test")

    print("exit.To stop the program")

    generate_borderline(no_of_underlines)

def generate_borderline(n, title=""):
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
    if cmd == "help":
        return True

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

#TODO: def fetch_words(ref_id)
def represent_lang_words(cmd, reference):
    level = positions[position]
    # Level is either category or word
    if level == "category":
        words = db.execute("SELECT * FROM word WHERE category_id IN (SELECT id FROM category WHERE language_id=?) ORDER BY id DESC", reference)
    else:
        words = db.execute("SELECT * FROM word WHERE category_id=? ORDER BY id DESC", reference)

    for word in words:
        print(word["name"], end=": ")

        if cmd == "6":
            input()
        print(word["meaning"])


def take_test(reference):
    optimize_test(reference)

    level = positions[position]
    # Level is either category or word
    if level == "category":
        words = db.execute("SELECT * FROM word WHERE category_id IN (SELECT id FROM category WHERE language_id=?) ORDER BY id DESC", reference)
    else:
        words = db.execute("SELECT * FROM word WHERE category_id=? ORDER BY id DESC", reference)

    # MINIMUM_TEST_SUBJECTS is complied; if there`s surplus in older words, user`s dominance on them determines if it is considered in test or not (so priority is with newer words and then user dominance)
    no_of_subjects = 0
    for word in words:
        probability = word["probability_to_be_in_test"]

        if no_of_subjects < MINIMUM_TEST_SUBJECTS:
            test_word(word)
            no_of_subjects += 1

        elif is_considered(probability):
            test_word(word)


def optimize_test(reference):
    level = positions[position]

    if level == "category":
        words = db.execute("SELECT * FROM word WHERE category_id IN (SELECT id FROM category WHERE language_id=?) ORDER BY id DESC", reference)
    else:
        words = db.execute("SELECT * FROM word WHERE category_id=? ORDER BY id DESC", reference)

    for word in words:
        if word["times_tested"] == 0:
            ratio = 1

        elif word["times_answered_wrong"] == 0:
                ratio = 0.5

        else:
            ratio = word["times_answered_wrong"] / word["times_tested"]

        db.execute("UPDATE word SET probability_to_be_in_test = ? WHERE id=?", ratio, word["id"])
    return

def is_considered(probability):
    return random.random() < probability

def test_word(word):
    print(word["name"], end=": ")

    answer = input()
    if answer != word["meaning"]:
        print("Correct answer: " + word["meaning"])
        db.execute("UPDATE word SET times_answered_wrong = times_tested + 1 WHERE id=?", word["id"])

    db.execute("UPDATE word SET times_tested = times_tested + 1 WHERE id=?", word["id"])

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
    if level == "word":
        editting_col = input(f"Do you want to edit name or meaning(Enter 'cancel' to cancel this operation)? ")
        if cancelling(editting_col):
            print(CANCEL_PROMPT)
            return

        if editting_col not in {"name","meaning"}:
            print(f"Such attribute does not exist in a {level}")
            return

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

        if level == "language" and already_exists(updated_name):
            print(f"Such {level} already exists!")
            return
        db.execute("UPDATE ? SET name=? where id=?;", level, updated_name, element_id)

def remove(element_id):
    level = positions[position]
    db.execute("DELETE FROM ? where id = ?;", level, element_id)

def fetch_element(target, reference):
    result = already_exists(target, reference)
    if not result:
        # Such element does not exist
        return False

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

    return selected[0]

def take_entry(reference, action_prompt="access", attribute_prompt="name"):
    level = positions[position]
    entry = input(f"The {attribute_prompt} of the {level} you want to {action_prompt}(Enter 'cancel' to cancel this operation): ")
    if cancelling(entry):
        return CANCEL_PROMPT
    return entry

def plural(word):
    if word[-1] == "y":
        return word[0:-1] + "ies"
    else:
        return word + "s"

def print_elements(reference):
    level = positions[position]
    elements_plur = plural(level)
    print(f"{elements_plur}: [")

    if level == "word":
        elements = db.execute("SELECT * FROM ? WHERE category_id = ? ORDER BY id DESC", level, reference)
        for el in elements:
            print(el["name"], end=": ")
            print(el["meaning"])
    else:
        if level == "language":
            elements = db.execute("SELECT name FROM ? ORDER BY id DESC", level)
        elif level == "category":
            elements = db.execute("SELECT name FROM ? WHERE language_id = ? ORDER BY id DESC", level, reference)

        for el in elements:
            print(el["name"])

    print("]")

def print_about():
    print("This program helps expand your vocabulary when learning a new language")
    print("You can store words in different languages and have them categorized!")
    print("The name of this project is 'Keasal', a Kurdish word meaning 'turtle',")
    print("a symbol of wisdom and patience.")
    print("May you have a wonderful journey ;)")
    print("!)You can always enter 'help' to be prompted of available commands")
    print("!)If (KeasalDB.db) file is lost, you can have it back in this repository:")
    print("     github.com/sananqsh/Keasal")

def main():
    reference_id = 0
    command = "0"
    while command != "exit":
        reference_id = keasalpy(command, reference_id)
        command = input("command: ")
        print()

if __name__ == "__main__":
    main()
