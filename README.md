# Keasal:turtle:
## Handy for anyone learning a new language!
This program helps expand your vocabulary when learning a new language

You can store words in different languages and have them categorized!
#
The name of this project is **Keasal**, a Kurdish word meaning **turtle**,
which is a symbol of wisdom and patience.

May you enjoy your journey ;)
#
#### Library requirements are mentioned in `requirements.txt`
#### To have a visual understanding of SQL tables check `.schema.PNG`
#### `KeasalDB.db` stores the data
#### and  the main code is contained in `Keasal.py`
#
*You can add and store similar words in different languages and categories but while taking test in the related section, your answer must match the meaning in THAT word in THAT section.*

*Pay attention to the prompts and follow them.*

*You can always enter `help` to be prompted of available commands.*
#
### App requirements:
- sqlite3
- CS50 python library
#
### How to lunch the app:
- Have `Keasal.py` and `KeasalDB.db` on a directory
- Check if you have python3 installed on your device
- Go to the directory with your terminal and type `python3 Keasal.py`
#
### Following are my design choices and the ideas I came up with throught the creation of this project:

##### Phase 1:
- [x] Create SQL structure (with default lang and category and words)
- [x] Simple inputting
- [x] Debugging

##### Phase 2:
- [x] Personalization in Languages and Categories and Words(Adding, Edditing, Removing, etc.)
- [x] Debugging
    * fix this bug: edit an name to another already existing element, leaving repetition problem behind :heavy_check_mark:
        * see if you can use fetch_id to recognize repetition after user input and before updating(done but regretted) :white_circle:
    * fix this bug: if user add repeated words, the program crashes :heavy_check_mark:
        * no need for words to be unique, change this in sql :heavy_check_mark:
    * add a cancel option in the middle of operations :heavy_check_mark:

##### Phase 3:
- [x] Generate tests
- [x] Debugging

##### Phase 4:
- [x] Remember test results and conclude user`s dominance on each word
- [x] Debugging

##### Phase 5:
- [ ] Add GUI
- [ ] Debugging

* new option: sorting the words before showing them with cmd=5
* if there isn`t any "KeasalDB.db" named database, create one when program is executed in the local folder
