# --- NOTE FOR DEVS ------- #
"""

"""

import io
import glob
#import json
#from datetime import datetime
#import random


# --- GLOBAL VARIABLES ----- #

DEBUG=True
PATH_FOLDER_BOOKS = "data/books_offline/"
# PATH_FOLDER_BOOKS = "data/books_online/"
PATH_FILE_METADATA = "data/meta/books_meta_data.csv"


# --- FUNCTIONS ------------ #

class Extractor:

    def extract_meta_data():
        """
        void -> void
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
    Extractor.extract_meta_data()



# --- EXECUTION -------------- #
main()