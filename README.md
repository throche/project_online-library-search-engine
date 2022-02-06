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
+ [Offline work & scripts](#offline-work-&-scripts)
+ [Data structure](#data-structure)
+ [Suggestions : graph algorithms](#suggestions-graph-algorithms)
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

`python -m src.main_extractor` this generates indexes, you can open the file to toggle in/out certain function, see more in the [offline work : scripts](#offline-work-&-scripts)

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
+ the search results and suggestions are obtained very quickly (< 1sec)

## back end (offline)

+ we use scripts to crawl and download books from the Gunteberg Project (respectfully)
+ we have 2000 books in english language registered, we can add more easily
+ we run scripts to index all books and filter out lots of junk
+ we run scripts to prerun suggestions, using the Jaccard graph algorithm (proximity of lexical fields)


# Exemple of usage

1) follow the [How to start](#how-to-start) procedure to get the server & client running. You must have generated the indexes and the suggestions also.

2) search for `mozart` it shows a large number of results

3) search for `mozart piano jazz` it shows only one result, because the search function look for the intersection of all words in books.

4) search for `averyrandomword` and it won't give any results.

Results are ranked by a score : the sum of occurences the words are found in the book.

Suggestions are also ranked, by a score of proximity with the book's lexical field.


# Program architecture

![diagram of program architecture](/support_de_rendu/img_rapport/program_architecture.drawio.png)

## client side

There is no data on the client side. When performing a search request, the client will receive small json files containing : book_id, title, author, release date, score.

The score is used to rank the results on screen.

The book_id is used to generate a link to the proper book section in the Guntenberg Project.

## server side (online)

When the server is booted, it will load three files in Python dictionnaries then it won't read any other files. The loaded files are :

+ `books_meta_data.csv` which contains meta-data for all books
+ `index_global_unique_word_to_id.csv` which contains all unique words and book_ids which have them
+ `books_distance.csv` which contains suggestions for every books

From `project/src/server/main.py` :

The server side uses a Rest API structure using the fastapi python package.

The function `read_item(q: str)` are the endpoint to access for the search function and the suggestion function.

They access the 3 indexes made during the offline pre-treatment operations. 

The indexes are loaded into dictionnaries, implemented using hashmaps.

When several words are searched, the query string is broken into single words and only books containing all words will be returned as results.


# Offline work & scripts

Scripts are used to ease the work load on the server when it's online.

## download and unzip books

From `project/scripts` :

Gutenberg provides books in different format, we chose to download books in ASCII format to generated our indexes, we use :

`wget -w 2 -m -H "http://www.gutenberg.org/robot/harvest?filetypes[]=txt&langs[]=en"`

to download books in english and `.txt` format and :

`find . -name "*.zip" | while read filename; do unzip -o -d "./data/" "$filename"; done;`

to unzip all the files into a single `./data` folder. Some books are US-ASCII instead of ASCII, we filter them out with :

`xargs rm -f <<< $(find . -regex "./[0-9]+-[0-9].txt")`

## extracting meta-data and generating indexes

Functions are defined in `project/src/main_extractor.py` there are three functions, which can be commented out in the main. By default they are run one after the other when performing the following :

Open a terminal in `project` then enter :

`python -m src.main_extractor` 

### extracting meta-data

From `project/src/main_extractor.py` :

we use `Extractor.extract_meta_data()` to extract meta-data from all books into single csv file containing all books's meta-data : book_id, title, author, release date

it generates the file : `project/data/meta/books_meta_data.csv`

Each line is : `book_id;title;author;release_date;` where book_id is sorted

### unique word index for every book

From `project/src/main_extractor.py` :

we use `Extractor.index_unique_word_for_all_books()` to generate one index per book in the foler `project/data/index/unique_word/`.

each file name is : `index_unique_word_#.csv` where # is the book id

each line is : `word;nb_occurences;` where word is sorted and is a unique word from the book which was not filtered out as junk

### global index of unique words

From `project/src/main_extractor.py` :

we use `Extractor.global_index_unique_word()` to generate a single global index which contains all unique words in every book's index with the list of book_ids using said word along with number of occurences.

it generates the file : `project/data/index/global/index_global_unique_word_to_id.csv`

each line is : `word;book_id1;nb_occurences;book_id2;nb_occurences;...;` where word is sorted and unique, there can be one or more `book_id;nb_occurences;` following a word per line.


## comparing book indexes and generating neighbours for suggestions

### graph of neighbours

From `project/src/main_distance_books.py` :

we use `create_distance_index()` to generate an index file which contains for each book index the list of indexes of neighbours based on a closeness calculation algorithm.

it generates the file : `project/data/distance/books_distance.csv`

each line is : `id;id_neighbour_1;id_neighbour_2;id_neighbour_3;...;` where id is sorted and unique.


### calculate closeness between 2 books

From `project/src/main_distance_books.py` :

we use `compare_unique_indexes(idx1, idx2)` to compare 2 books indexes file which contains for each book index all unique words. If the 2 books are similar, we define them as neighbours for the suggestion feature. It uses for each word a calculated score based on the rarity of the word.


### calculate words scores

From `project/src/main_distance_books.py` :

we use `create_word_scores()` to define for each word appearing in all the books of the database, a score based on its rarity. A word with a higher score means that the word appears in less books than a word with a lower score.

it generates the file : `project/data/distance/words_scores.csv`

each line is : `word;score;` where word is sorted and unique, and score a float representing the word's rarity in the book database.


# Suggestions : graph algorithms

The algorithm for determining if 2 books are related or not is based on the calculation of a Jaccard distance with a closeness score using the unique index of each book. 

The unique index of a book lists every word and its number of occurences. 

Our first approach for determining if 2 books were related was to count the number of different words they had in common. 2 books on the same topic should have a lot of words in common. 

After trying this implementation, we decided to improve our algorithm by attributing different weight to the different words in common that 2 books had. If 2 books have a specific word in common, they have a much higher chance to be related (for example 2 books with the word 'algorithm') than 2 books with a very common word (for example 2 books with the word 'england'). This implementation was inspired from the Term Frequency-Inverse Document Frequency ranking method (TF-IDF). 

We calculated a rarity score for each word based on the number of books in which the word could be found, among all the books in our database. The calculated score is higher for words that are present in fewer books.

When comparing 2 book indexes, if a word is present in both books, the closeness score is increased by the amount of the rarity score of the found word. If the total closeness score is higher than a threshold, we consider the 2 books as neighbours for suggestions.

We decided for each book to keep the 50 highest 'closeness scores' in the file books_distance.csv


# Credits

Book database https://www.gutenberg.org/

Jaccard distance https://www-apr.lip6.fr/~buixuan/daar2021

TF-IDF ranking method https://kmwllc.com/index.php/2020/03/20/understanding-tf-idf-and-bm-25/