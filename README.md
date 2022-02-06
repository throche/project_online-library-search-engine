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

This project is about creating a website with a search engine capable of researching through thousands of books in a near instant response time. The user is also given suggestions of other books based on certain algorithms studied during the semester.

At the time of delivery we have implemented the following :
+ a front-end with Angular Framework
+ a server made in Python3 with fastapi package
+ multiple scripts in Bash and Python3
+ multiple features explained with [more details here](#use-cases-features)

# Table of content

+ [Installation](#installation)
+ [How to start](#how-to-start)
+ [Use cases : features](#use-cases-features)
+ [Exemple of usage](#exemple-of-usage)
+ [Program architecture](#program-architecture)
+ [Offline work : scripts](#scripts)
+ [Data structure](#data-structure)
+ [Suggestions : graph algorithms](#suggestions-graph-algorithm)
+ [Credits](#credits)


# Installation

## Back-end API in python (using fastapi package)

Open a terminal in `project/src/server` then enter :

`pip install fastapi`

`pip install uvicorn`

`pip install -r requirements.txt `

## Front-end Client in Angular Typescript

Open a terminal in `project/src/client` then enter :

`sudo apt install nodejs`

`sudo apt install npm`

`sudo npm install -g n`

`sudo n stable`  (update node to latest version)

`hash -r`

`sudo npm install -g @angular/cli`

# How to start

## (Only run once) : pre-indexing data is the offline work

Open a terminal in `project` then enter :

`python -m src.main_extractor` this generates indexes

## Server

Open a terminal in `project` then enter :

`uvicorn src.server.main:app --reload`

## Client

Open a terminal in `project/src/client` then enter :

`npm install`

`npm run start` then open a brower and go to `http://localhost:4200`

**You're good to go!**


# Use cases : features

## client side

+ the user can use the website to search for a specific book using keywords (seperated by whitespace)
+ the research's results give the books's basic info and link to the Guntenberg Project book page
+ the research's results are ranked
+ the results from the search function is very fast (<1s)
+ the user is given suggestions of books based on its last research (graph algorithms used)

## server side (online)

+ we use a score system to rank our search results and suggestions
+ the search results and suggestions are obtained very quickly (<1s)

## back end (offline)

+ we use scripts to crawl and download books from the Gunteberg Project (respectfully)
+ we have 2000 books in english language registered, we can add more easily
+ we run scripts to index all books and filter out lots of junk
+ we run scripts to prerun suggestions, using the Jaccard graph algorithm (proximity of lexical fields)

# Exemple of usage

1) follow the [How to start](#how-to-start) procedure

2) search for `energy nuclear`

3) see

# Program architecture

# Offline work : scripts

Scripts are used to eased the workcharge on the server when it's online.

## download and unzip books

From `project/scripts` :

Gutenberg provides books in different format, we chose to download books in ASCII format to generated our indexes, we use :

`wget -w 2 -m -H "http://www.gutenberg.org/robot/harvest?filetypes[]=txt&langs[]=en"`

to download books in english and `.txt` format and :

`find . -name "*.zip" | while read filename; do unzip -o -d "./data/" "$filename"; done;`

to unzip all the files into a single `./data` folder. Some books are US-ASCII instead of ASCII, we filter them out with :

`xargs rm -f <<< $(find . -regex "./[0-9]+-[0-9].txt")`

## extracting meta-data

From `project/src/main_extractor.py` :

we use `Extractor.extract_meta_data()` to extract meta-data from all books into single csv file containing all books's meta-data : book_id, title, author, release date

it generates the file : `project/data/meta/books_meta_data.csv`

Each line is : `book_id;title;author;release_date;` where book_id is sorted

## generation of indexes

### unique word index for every book

From `project/src/main_extractor.py` :

we use `Extractor.index_unique_word_for_all_books()` to generate one index per book in the foler `project/data/index/unique_word/`.

each file name is : `index_unique_word_#.csv` where # is the book id

each line is : `word;nb_occurences;` where word is sorted and is a unique word from the book which was not filtered out as junk

### global index of unique words

From `project/src/main_extractor.py` :

we use `Extractor.global_index_unique_word()` to generate a single global index which contains all unique words in every book's index with the list of book_ids using said word along with number of occurences.

it generates the file : `project/data/index/global/index_global_unique_word_to_id.csv`

each line is : `word;book_id1;nb_occurences;book_id2;nb_occurences;...;` where word is sorted and unique, there can be one or more `book_id;nb_occurences;` following a word per line

# Data structure



# Suggestions : graph algorithms


# Credits



code : ```...```
image : ![schema](/schema/schema1.png)



# scrap book:



7) fonction to search a word in the indexes (@param : string, @return : (id, scores)[])

8) fonction to split a string containing several words with spaces into an array of words(@param : string, @return: string[])

