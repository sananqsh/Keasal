### Following are my design choices and the ideas I came up with throught the creation of this project:

##### Phase 1:
- [x] Create SQL structure (with default lang and category and words)
- [x] Simple inputting
- [x] Debugging

##### Phase 2:
- [x] Personalization in Languages and Categories and Words(Adding, Edditing, Removing, etc.)
- [x] Debugging
    * fix this bug: edit an name to another already existing element, leaving repetition problem behind :heavy_check_mark:
        * see if you can use fetch_id to recognize repetition after user input and before updating(done but regretted) :white_check_mark:
        * no need for words to be unique, change this in sql :heavy_check_mark:
    * fix this bug: if user add repeated words, the program crashes :heavy_check_mark:
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
