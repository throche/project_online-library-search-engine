# project_online-library-search-engine

DAAR Project choice A: online search engine for a library

front + back + indexing + no-DB : using gutenberg online DB

**Teacher : Binh-Minh Bui-Xuan**

"buixuan" <buixuan@lip6.fr>



# Members (binôme)

**Thibault ROCHE 3677376**

"Thibault Roche" <thibault.roche.1@etu.sorbonne-universite.fr>

thibault.roche.fr@gmail.com


**Paul NGUYEN DIT SYVALA 3876651**

"Paul NGUYEN_DIT_SYVALA" <paul.nguyen_dit_syvala@etu.sorbonne-universite.fr>

pnds.5791@gmail.com


# Project summary



# Table of content

+ Installation
+ Use cases (features)
+ Exemple of usage
+ Program architecture
+ Data structure
+ Credits and references


# Installation

## Back-end API in python (using fastapi package)

`pip install fastapi`

`pip install uvicorn`

`pip install -r requirements.txt `

## Front-end Client in Angular Typescript

sudo apt install nodejs

sudo apt install npm

sudo npm install -g n

sudo n stable  #update node to latest version

hash -r

sudo npm install -g @angular/cli


# Use cases (features)
# Exemple of usage

## Back end API in python (using fastapi package)

from the project/src/server folder

`uvicorn main:app --reload`

or, from the project folder

`uvicorn src.server.main:app --reload`

## Front-end Client in Angular Typescript

from the project/src/client folder

npm install

npm run start

open a browser at http://localhost:4200

# Program architecture
# Data structure
# Credits and references


code : ```...```
image : ![schema](/schema/schema1.png)



# scrap book:

1) download 2000 (raw txt / ascii / english) books from gutenberg

2) unzip the books into project/data/books_offline (750Mo)

3) copy 50 books into project/data/books_online (<20Mo)

4) use python script to extract meta-data from every books into single file `project/data/meta/books_meta_data.csv`

each line is : `#;title;author;release date;` where # is the book_id sorted

5) use python script to make index for every books into `project/data/index/unique_word/`

file name is : `index_unique_word_#.csv` (where # is the book id)

each line is : `a_word;nb_occurences;` (alpha ascended sort on first field)

6) use python script to make a global index for all unique words into a single file `project/data/index/global/index_global_unique_word_to_id.csv`

each line is : `a_word;#;nb_occurences;#;nb_occurences;...;` (alpha ascended sort on first field, where # is a book id)

7) fonction to search a word in the indexes (@param : string, @return : (id, scores)[])

8) fonction to split a string containing several words with spaces into an array of words(@param : string, @return: string[])

