# --- NOTE FOR DEVS ------- #
"""

"""

import glob
#import json
#from datetime import datetime
#import random


# --- GLOBAL VARIABLES ----- #

DEBUG=True
SIMILARITY_THRESHOLD = 500

PATH_FOLDER_INDEX_UNIQUE_WORD = "data/index/unique_word/"
PATH_FILE_DISTANCE = "data/distance/books_distance.csv"
PATH_FILE_WORDS_SCORE = "data/distance/words_scores.csv"
DISTANCE_INDEX = dict()
DICT_ALL_WORDS = dict()


# --- FUNCTIONS ------------ #


def compare_unique_indexes(idx1, idx2):
    """compare 2 books to find out how close they are.
    Similarity is calculated with 
    - the number of different words in common affected by the score of each word
    - divided by the average number of different words of the 2 texts 
    
    a threshold can be set to decide if 2 books are similar or not"""

    id1 = idx1[41:-4]
    id2 = idx2[41:-4]
            
    file_index_1 = open(idx1, 'r')
    file_index_2 = open(idx2, 'r')
    
    lines1 = file_index_1.readlines()
    size1 = len(lines1)
    dict1 = dict()
    for line in lines1:
        tab = line.split(";")
        dict1[tab[0]] = 1
    
    lines2 = file_index_2.readlines()
    size2 = len(lines2)
    cpt_unique_words_similar = 0
    for line in lines2:
        tab = line.split(";")
        if dict1.get(tab[0]) != None:
            score = DICT_ALL_WORDS[tab[0]]
            cpt_unique_words_similar += score

    similarity = cpt_unique_words_similar/((size1+size2)/2)
    if similarity > SIMILARITY_THRESHOLD:
        print("total id " + id1 +  " : " + str(size1) + ", total id " + id2 + " : " + str(size2) + ", similar : " + str(cpt_unique_words_similar))    
        print("similarity " + str(similarity))
        if DISTANCE_INDEX.get(id1) == None:
            DISTANCE_INDEX[id1] = []     
        DISTANCE_INDEX[id1].append(id2)
        if DISTANCE_INDEX.get(id2) == None:
            DISTANCE_INDEX[id2] = []     
        DISTANCE_INDEX[id2].append(id1)
        
    return

def create_distance_index():
    """create an index file listing for each book, its neighbours using the compare_unique_indexes function on all the unique indexes of each book"""
    try:
        files_of_unique_indexes = [file for file in glob.glob(PATH_FOLDER_INDEX_UNIQUE_WORD+"*.csv")]
        files_of_unique_indexes.sort()
        
        for i in range(0, len(files_of_unique_indexes)):
            file_index_name_1 = files_of_unique_indexes[i]

            for j in range(i+1, len(files_of_unique_indexes)):
                file_index_name_2 = files_of_unique_indexes[j]
                
                #print("1 : " + file_index_name_1)
                #print("2 : " + file_index_name_2)
                #print("1 : " + file_index_name_1[41:-4])
                #print("2 : " + file_index_name_2[41:-4])       

                compare_unique_indexes(file_index_name_1, file_index_name_2)
        
        file_distance = open(PATH_FILE_DISTANCE, "w")
        for elem in DISTANCE_INDEX.items():  
            file_distance.write(elem[0]+";")
            for neighbour in elem[1]:
                file_distance.write(neighbour+";")
            file_distance.write("\n")
                
                    
    except IOError as e:
        print(e)

def create_word_scores():
    """create an index file where each word appearing in the book database
    is given a score associated with its rarity.
    a word appearing in 2 books among 2000 will be rarer than a word appearing in every book.
    
    score formula : total_number_of_books_in_database / number_of_books_containing_the_word """
    

    try:
        file_distance = open(PATH_FILE_DISTANCE, "w")
        files_of_unique_indexes = [file for file in glob.glob(PATH_FOLDER_INDEX_UNIQUE_WORD+"*.csv")]
        files_of_unique_indexes.sort()
        
        for i in range(0, len(files_of_unique_indexes)):
            file_index_name = files_of_unique_indexes[i]
            file_index = open(file_index_name, 'r')

            lines = file_index.readlines()
            for line in lines:
                tab = line.split(";")
                if DICT_ALL_WORDS.get(tab[0]) == None:
                    DICT_ALL_WORDS[tab[0]] = 1
                else:
                    DICT_ALL_WORDS[tab[0]] += 1
        print(DICT_ALL_WORDS)
        file_scores = open(PATH_FILE_WORDS_SCORE, "w")
        for elem in DICT_ALL_WORDS.items():
            score = len(files_of_unique_indexes)/elem[1]
            print(str(elem[0]) + " : " + str(score))
            file_scores.write(elem[0] + ";" + str(score) + ";\n")
        

    except IOError as e:
        print(e)
    
create_word_scores()
create_distance_index()
