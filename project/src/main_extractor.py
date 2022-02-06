# --- NOTE FOR DEVS ------- #
"""

"""

import io
import glob
#import json
#from datetime import datetime
#import random


# --- GLOBAL VARIABLES ----- #

DEBUG=False

PATH_FOLDER_BOOKS = "data/books_offline/"
# PATH_FOLDER_BOOKS = "data/books_online/"  # for testing purposes, careful for extracting book_id from path, online is shorter and offline

PATH_FILE_METADATA = "data/meta/books_meta_data.csv"
PATH_FOLDER_INDEX_UNIQUE_WORD = "data/index/unique_word/"


# --- FUNCTIONS ------------ #

class Extractor:

    def extract_meta_data():
        """
        void -> void
        IO: read from PATH_FOLDER_BOOKS
        IO: write in PATH_FILE_METADATA
        extract meta data for every books into a single file books_meta_data.csv
        each line is : id;title;author;...
        """
        book_id = ""
        title = ""
        author = ""
        date = ""
        try:
            file_meta = open(PATH_FILE_METADATA, "w")
            files_of_books = [file for file in glob.glob(PATH_FOLDER_BOOKS+"*.txt")]
            files_of_books.sort()

            # for every books:
            for file_book in files_of_books:
                book = open(file_book, 'r', encoding='ascii')
                if DEBUG:
                    print("opening: "+file_book)
                book_id = file_book[19:24]
                
                # default values
                title = "unknown"
                author = "unknown"
                date = "unknown"
                
                # extract meta data 
                lines = book.readlines(750)
                for line in lines:
                    linestart = line[0:6]
                    if (linestart == "Title:"):
                        title = line[7:-1]
                    if (linestart == "Author"):
                        author = line[8:-1]
                    if (linestart == "Releas"):
                        date = line[14:-16]
                        break
                if DEBUG:
                    print(book_id+";"+title+";"+author+";"+date+"\n")
                file_meta.write(book_id+";"+title+";"+author+";"+date+"\n")
                book.close()

            file_meta.close()
        except IOError as e:
            print(e)


    def index_unique_word_for_all_books():
        """
        void -> void
        call indexing unique word on every books in PATH_FOLDER_BOOKS
        """
        ignored_word_set_pronouns = {"i","we","you","he","she","it","they","me","us","him","her","them"}
        ignored_word_set_posessive = {"mine","yours","his","hers","ours","theirs"}
        ignored_word_set_reflexive = {"myself","yourself","himself","herself","itself","oneself","ourselves","yourselves","themselves"}
        ignored_word_set_reciprocal = {"each","other","another"}
        ignored_word_set_relative = {"that","which","who","whose","whom","where","when"}
        ignored_word_set_demonstrative = {"this", "that", "these", "those"}
        ignored_word_set_interrogative = {"who", "what", "why", "where", "when", "whatever"}
        ignored_word_set_indefinite = {"anything", "anybody", "anyone", "something", "somebody", "someone", "nothing", "nobody", "none"}
        ignored_word_set_other = {"gutenberg", "ebook"}
        ignored_word_set = set()
        ignored_word_set.update(ignored_word_set_pronouns)
        ignored_word_set.update(ignored_word_set_posessive)
        ignored_word_set.update(ignored_word_set_reflexive)
        ignored_word_set.update(ignored_word_set_reciprocal)
        ignored_word_set.update(ignored_word_set_relative)
        ignored_word_set.update(ignored_word_set_demonstrative)
        ignored_word_set.update(ignored_word_set_interrogative)
        ignored_word_set.update(ignored_word_set_indefinite)
        ignored_word_set.update(ignored_word_set_other)
        if DEBUG:
            print(ignored_word_set)

        files_of_books = [file for file in glob.glob(PATH_FOLDER_BOOKS+"*.txt")]
        files_of_books.sort()
        # for every books:
        try:
            for file_book in files_of_books:
                if not Extractor.index_unique_word_for_a_book(file_book, ignored_word_set):
                    print("ERROR : index_unique_word_for_a_book("+file_book+") didn't work")
        except UnicodeDecodeError as e:
            print(e)
            print("Error with : "+file_book)

    def index_unique_word_for_a_book(path_book, ignored_word_set):
        """
        string -> bool
        IO: read from path_book
        IO: write in PATH_FOLDER_INDEX_UNIQUE_WORD
        create an index csv file with contains every unique word from the book and its number of occurences
        each line is : word;nb_occ  where word is sorted
        common words are filtered out
        """
        try:
            book_id = path_book[19:23]
            if DEBUG:
                print(book_id)
                print(PATH_FOLDER_INDEX_UNIQUE_WORD+"index_unique_word_"+book_id+".csv")
            
            # create an index for the book
            index = open(PATH_FOLDER_INDEX_UNIQUE_WORD+"index_unique_word_"+book_id+".csv", "w")

            # open the book
            # book = open(path_book, 'r', encoding='ASCII')
            book = open(path_book, 'r', errors="ignore")#.read().decode('ascii', errors='ignore')
            if DEBUG:
                print("opening: "+path_book)
            
            # reading the book and keep all unique words with nb_occ
            dico = {}
            for line in book:
                for word in line.split():
                    word = word.replace('.','').replace(',','').replace(';','').replace('[','').replace(']','')
                    word = word.replace('?','').replace('!','').replace(':','').replace("'",'').replace("_",'')
                    word = word.replace('"','').replace('(','').replace(')','').replace("$",'').replace("*",'')
                    if not word.isnumeric():
                        word = word.lower()
                        if word in dico:
                            dico[word] = dico[word]+1
                        else:
                            dico[word] = 1
            # filter out words
            if DEBUG:
                print(dico)
                print(len(dico))
            for word in ignored_word_set:
                if word in dico:
                    del dico[word]
            if DEBUG:
                print(len(dico))
            
            # sort dico and write in index
            for word in sorted(dico.keys()):
                index.write(word+";"+str(dico[word])+"\n")

            book.close()
            index.close()            
        except IOError as e:
            print(e)
            return False
        return True


# --- TOOLBOX FUNCTIONS ------ #

class Toolbox:
    def generate_name():
        """
        None -> String
        return a random name among the list of given names
        """
        name = ""
        try:
            file = open(NAMES, "r")
            num_lines = sum(1 for _ in file)
            file.close()
            rn = random.randint(0, num_lines-1)
            cpt = 0
            file = open(NAMES, "r")
            for line in file:
                if (cpt == rn):
                    name = line.split()
                cpt += 1
            file.close()
        except IOError as e:
            print(e)
            print("Error in Toolbox.generate_name, file names.txt could be missing.")
        return name[0]
    
    def generate_company_id():
        """
        None -> String
        return a random company_id
        """
        return "COID_"+str(random.randint(10,10000))

    def reset_test_database(path):
        """
        String -> Boolean
        """
        try:
            new_file = open(path, "w")
            new_file.write("[]")
            new_file.close()
            return True
        except IOError as e:
            print(e)
            return False
        return False


# --- MAIN ------------------- #
def main():
    
    # extract meta-data from all books into single file csv file
    # Extractor.extract_meta_data()

    # create an index of unique word for every books
    Extractor.index_unique_word_for_all_books()


# --- EXECUTION -------------- #
main()