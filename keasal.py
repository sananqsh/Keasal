from cs50 import SQL

db = SQL("sqlite:///KeasalDB.db")

position = 0

positions = ["main", "language", "category", "word"]

def guide(cmd, ref_id):
    # exceptions: pos=0 & cmd > 2 || (pos in {1,2} & cmd > 4) || (pos in {2,3} &)


    global position
    # print(f"cmd: {cmd}")
    # print(f"position: {position}")
    # print(f"ref_id: {ref_id}")

    if cmd == "0" or not cmd.isdigit():
        ref_id = 0
        # global position
        position = 0
        next_lvl = positions[position+1]
        print(f"1.Manage in {next_lvl} level")
        print("2.About")
        return 0
    else:
        print("0.Go to main")
        if 0 < position:
            print_elements(cur_lvl)

        if cmd == "1":

            
            position +=1
            cur_lvl = positions[position]
            if position < 3:
                next_lvl = positions[position+1]

            print(f"position: {position}")
            if position in {1, 2}:
                print(f"1.Manage in {next_lvl} level")

            print(f"2.Add new {cur_lvl}")
            print(f"3.Edit {cur_lvl}")
            print(f"4.Remove {cur_lvl}")

            return ref_id
        elif cmd == "2":
            print("TODO ADD")
            # add()
        elif cmd == "3" or cmd == "4":
            ###
            selected = db.execute("SELECT * FROM ? WHERE name = ?", cur_lvl, input(f"Input the {cur_lvl} you want to access: "))
            if len(selected) == 0:
                print(f"Such {cur_lvl} does not exist in the database!")
                return
            ref_id = selected[0]["id"]
            selected = selected[0]["name"]
            ###
            if cmd == "3":
                print("TODO Edit")
            # Edit()
            if cmd == "4":
                print("TODO Remove")
            # Remove()
        else:
            print("Incorrect command!")
            position = 0
            reference_id = 0
            return

def print_elements(level):
    print("Current elements:")
    elements = db.execute("SELECT name FROM ?;", level)
    for el in elements:
        print(el["name"])
    print()

def main():
    reference_id = 0
    command = "0"
    guide(command, reference_id);

    while reference_id != "-1":
        command = input("command: ")
        print()
        reference_id = guide(command, reference_id)
        print(f"position: {position}")
        print()

if __name__ == "__main__":
    main()
