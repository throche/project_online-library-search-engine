from typing import Optional

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware


# --- GLOBAL VARIABLES ----- #

DEBUG=False
# PATH_FOLDER_BOOKS = "data/books_offline/"
# PATH_FOLDER_BOOKS = "data/books_online/"
PATH_FILE_METADATA = "data/meta/books_meta_data.csv"
# PATH_FILE_GLOBAL_INDEX = "data/index/global/index_global_unique_word_to_id_test.csv"
PATH_FILE_GLOBAL_INDEX = "data/index/global/index_global_unique_word_to_id.csv"
GLOBAL_INDEX = dict()
META_DATA = dict()

# --- REST API ----- #

app = FastAPI()

origins = ["http://localhost:4200"]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def read_root():
    return {"Hello": "World"}


@app.get("/search")
def read_item(q: str):

    words = q.split(" ")
    lists = []
    print(words)
    for word in words: 
        l = search_word_in_global_index(word)
        lists.append(l)
    
    res = get_all_matches(lists)
    res_with_metadata = get_results_metadata(res)
    
    return res_with_metadata
    #return {"res":[{"id": "10001", "Title" : "Apocolocyntosis", "Author": "Lucius Seneca", "Release_Date":"November 10, 2003", "score": "40"},
    #	           {"id": "10010", "Title" : "The Eulogies of Howard", "Author": "William Hayley", "Release_Date":"November 7, 2003", "score": "15"},
    #	           {"id": "10024", "Title" : "Beneath the Banner", "Author": "F. J. Cross", "Release_Date":"November 9, 2003", "score": "190"}]}


# --- INDEX LOAD FUNCTIONS ----- #

def load_global_index():
    """loads in memory the global index into a dictionnary (python hashmap) 
    with each word being a key
    and values being a list of couples (id, occurences) """
    try:
        if DEBUG:
            print("opening global index")
        file_global_index = open(PATH_FILE_GLOBAL_INDEX, "r")
        lines = file_global_index.readlines()
        for line in lines:
            tab = line.split(";")[0:-1]
            list_couples = []
            for i in range(int((len(tab)-1)/2)):
                list_couples.append((tab[1+ 2*i], tab[1+ 2*i + 1]))  # list of couples (id, nb_occurences)
                        
            GLOBAL_INDEX[tab[0]]= list_couples
            if DEBUG:
                print(tab)
        if DEBUG:
            print("Global index : ")
            print(GLOBAL_INDEX)
    except IOError as e:
        print(e)
            
def load_meta_data():
    """loads in memory the metadata into a dictionnary (python hashmap) 
    with each book id being a key
    and values being a list containing title, author and date"""    
    try:
        if DEBUG:
            print("opening meta data")
        file_meta_data = open(PATH_FILE_METADATA, "r")
        lines = file_meta_data.readlines()
        for line in lines:
            tab = line.split(";")[0:]
            
            tab[-1] = tab[-1].rstrip()
            META_DATA[tab[0]]= tab[1:]
            if DEBUG:
                print(tab)
        if DEBUG:
            print("Meta data : ")
            print(META_DATA)
    except IOError as e:
        print(e)

# --- INDEX SEARCH FUNCTIONS ----- #

def search_word_in_global_index(word: str):
    """returns the list of couples (id, nb_occurences) for a word using the global index"""
    if GLOBAL_INDEX.get(word) == None:
        return []
    results = GLOBAL_INDEX[word]
    if DEBUG:
        print(results)
    return results
    
def get_results_metadata(results):  
    jsons = {"res":[]}
    for r in results: 
        metadata = META_DATA[r[0]]
        jsons["res"].append(write_json(r[0], metadata[0], metadata[1], metadata[2], r[1]))
        if DEBUG:
            print(metadata)
            print(jsons)
    return jsons

def get_all_matches(lists):
    """returns the list of ids that are in all the lists"""
    result = dict()
    for l in lists:
        for couple in l:
            if result.get(couple[0]) == None:
                result[couple[0]] = [couple[0], couple[1], 1]
            else:
                new_value = (couple[0], str(int(result[couple[0]][1]) + int(couple[1])), result[couple[0]][2] + 1)
                result[couple[0]] = new_value
    if DEBUG:
        print(result)
    list_of_matches = []
    for elem in result.values():
        if DEBUG:
            print(elem)
            print(int(elem[2]))
            print(len(lists))
        if int(elem[2]) == len(lists):
            list_of_matches.append((elem[0], elem[1]))
    if DEBUG:
        print("list of matches")
        print(list_of_matches)
    
    return list_of_matches

    

              
def write_json(id, title, author, date, score):
    """return for each book the json item to send to the client server"""
    json = {"id": id, "Title" : title, "Author": author, "Release_Date":date, "score": score}
    if DEBUG:
        print(json)
    return json

load_global_index()
load_meta_data()