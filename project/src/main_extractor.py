# --- NOTE FOR DEVS ------- #
"""

"""

#import json
#from datetime import datetime
#import random


# --- GLOBAL VARIABLES ----- #

PATH_FOLDER_BOOKS = "project/data/books_offline/"
PATH_FOLDER_META = "project/data/meta/"


# --- COMMENTS ON CLASSES --- #
"""
TestDatabaseAnnuaire(TestDatabaseBlacklist) :
wav_files and sound vectors are ignored in this subclass
update_database_location must be used prior to every test where the test database is used instead of the real database 
"""

# --- CLASSES --------------- #

class TestDisplay(unittest.TestCase):
    def test_default_language(self):
        self.assertEqual(display.LANGUAGE, 'fr')
    def test_display_change_language_to_fr(self):
        display.change_language('fr')
        self.assertEqual(display.LANGUAGE, 'fr')
    def test_display_change_language_to_en(self):
        display.change_language('en')
        self.assertEqual(display.LANGUAGE, 'en')
    def test_display_change_language_to_invalid_lang(self):
        display.change_language('invalid_lang')
        self.assertEqual(display.LANGUAGE, 'fr')

    def test_display_various_msgs_in_fr(self):
        display.change_language('fr')
        self.assertEqual(display.get_message("menu_auth", "welcome"), "\nBienvenue sur V-Access (v0.1)\n")
        self.assertEqual(display.get_message("menu_auth", "exit"), "Arrêt du programme d'authentification.")
        self.assertEqual(display.get_message("menu_auth", "authentification_success_but_denied"), "Accès Refusé. Vous avez été reconnu mais votre autorisation d'accès a été désactivée.\nVeuillez quitter les lieux.")
        self.assertEqual(display.get_message("error", "input_error"), "Choix invalide, veuillez réessayer.")
        self.assertEqual(display.get_message("menu_admin", "select_language"), "Veuillez choisir la langue: 1) Anglais 2 Français")
        self.assertEqual(display.get_message("record", "no_voice_detected"), "Pas de voix détectée")

    def test_display_various_msgs_in_en(self):
        display.change_language('en')
        self.assertEqual(display.get_message("menu_auth", "welcome"), "\nWelcome to V-Access (v0.1)\n")
        self.assertEqual(display.get_message("menu_auth", "exit"), "Authentification program stopped.")
        self.assertEqual(display.get_message("menu_auth", "authentification_success_but_denied"), "Access Denied. You have been recognized but your authorization has been disabled.\nPlease leave the area.")
        self.assertEqual(display.get_message("error", "input_error"), "Invalid choice, please try again.")
        self.assertEqual(display.get_message("menu_admin", "select_language"), "Please select the language: 1) English 2) French")
        self.assertEqual(display.get_message("record", "no_voice_detected"), "no voice detected")

class TestDatabaseAnnuaire(unittest.TestCase):
    def test_00_default_correct_database_location(self):
        file_exists = False
        try:
            file = open(annuaire.FILE_DATABASE, "r")
            file.close()
            file_exists = True
        except IOError:
            file_exists = False
        self.assertTrue(file_exists)

    def test_01_make_new_test_database_file(self):
        self.assertTrue(Toolbox.reset_test_database(ANNUAIRE_FILE))

    def test_02_update_database_location(self):
        if annuaire.update_database_location(ANNUAIRE_FILE):
            file_exists = False
            try:
                file = open(annuaire.FILE_DATABASE, "r")
                file.close()
                file_exists = True
            except IOError:
                file_exists = False
            self.assertTrue(file_exists)
            self.assertEqual(annuaire.FILE_DATABASE, ANNUAIRE_FILE)

    def test_03_register_100_random_new_users(self):
        if annuaire.update_database_location(ANNUAIRE_FILE):
            first_name = []
            last_name = []
            company_id = []
            files = []
            vectors = []
            for id in range(100):
                first_name.append(Toolbox.generate_name())
                last_name.append(Toolbox.generate_name())
                company_id.append(Toolbox.generate_company_id())
                files.append([str(id)+"_1.wav",str(id)+"_2.wav",str(id)+"_3.wav",str(id)+"_4.wav",str(id)+"_5.wav"])
                vectors.append(None)
                annuaire.save_new_user(first_name[id], last_name[id], company_id[id], files[id], vectors[id])
            for id in range(100):
                self.assertTrue(annuaire.is_user_exist(id))
                user = annuaire.search_user_by_id(id)
                self.assertEqual(user["firstname"],first_name[id])
                self.assertEqual(user["lastname"],last_name[id])
                self.assertEqual(user["company_id"],company_id[id])
            self.assertEqual(len(annuaire.search_all_users()), 100)

    def test_04_change_authorisation(self):
        if annuaire.update_database_location(ANNUAIRE_FILE):
            for id in range(100):
                self.assertTrue(annuaire.is_user_exist(id))
                user = annuaire.search_user_by_id(id)
                self.assertTrue(user["authorized"])
                annuaire.change_permissions(id, False)
                user = annuaire.search_user_by_id(id)
                self.assertFalse(user["authorized"])
                annuaire.change_permissions(id, True)
                user = annuaire.search_user_by_id(id)
                self.assertTrue(user["authorized"])

    def test_05_clean_test_database_file(self):
        self.assertTrue(Toolbox.reset_test_database(ANNUAIRE_FILE))

class TestDatabaseBlacklist(unittest.TestCase):
    def test_00_default_correct_database_location(self):
        file_exists = False
        try:
            file = open(blacklist.FILE_DATABASE, "r")
            file.close()
            file_exists = True
        except IOError:
            file_exists = False
        self.assertTrue(file_exists)

    def test_01_make_new_test_database_file(self):
        self.assertTrue(Toolbox.reset_test_database(BLACKLIST_FILE))

    def test_02_update_database_location(self):
        if blacklist.update_database_location(BLACKLIST_FILE):
            file_exists = False
            try:
                file = open(blacklist.FILE_DATABASE, "r")
                file.close()
                file_exists = True
            except IOError:
                file_exists = False
            self.assertTrue(file_exists)
            self.assertEqual(blacklist.FILE_DATABASE, BLACKLIST_FILE)

    def test_03_append_100_new_blacklisted_users(self):
        if blacklist.update_database_location(BLACKLIST_FILE):
            sound_vector = [0.10,0.2,0.3]
            dates = ["01","02","03"]
            for id in range(100):
                wav_files = [str(id)+"_1.wav",str(id)+"_2.wav",str(id)+"_3.wav"]
                self.assertTrue(blacklist.save_black_listed_person(sound_vector, wav_files, dates))
            self.assertEqual(len(blacklist.search_all_black_listed_persons()), 100)
        
    def test_04_append_attempts_of_blacklisted_user(self):
        if blacklist.update_database_location(BLACKLIST_FILE):
            id = 0
            item = blacklist.search_black_listed_person_by_id(id)
            self.assertEqual(len(item["wav_files"]), 3)
            sound_vector = [0.4,0.5]
            wav_files = [str(id)+"_4.wav",str(id)+"_5.wav"]
            dates = ["04","05"]
            self.assertTrue(blacklist.add_date_attempt_to_black_listed_person(sound_vector, wav_files, dates, id))
            item = blacklist.search_black_listed_person_by_id(id)
            self.assertEqual(len(item["wav_files"]), 5)

    def test_05_delete_blacklisted_users(self):
        # deletes all test_blacklist users in two batch
        if blacklist.update_database_location(BLACKLIST_FILE):
            for id in range(50):
                self.assertTrue(blacklist.delete_black_listed_person(id))
            self.assertEqual(len(blacklist.search_all_black_listed_persons()), 50)
            for id in range(50,100):
                self.assertTrue(blacklist.delete_black_listed_person(id))
            self.assertEqual(len(blacklist.search_all_black_listed_persons()), 0)

class TestSoundProcessing(unittest.TestCase):
    def test_identical_voice_vectors(self):
        v0 = sound_extraction.extractVector(WAV_FILE_00)
        v10 = sound_extraction.extractVector(WAV_FILE_10)
        (best_cost1, mean_cost1) = identification.compare_vectors(v0,v0, returnParam="both")
        (best_cost2, mean_cost2) = identification.compare_vectors(v10,v10, returnParam="both")
        self.assertEqual(identification.compare_vectors(v0,v0, returnParam="both"), (0.0, 0.0))
        self.assertEqual(identification.compare_vectors(v10,v10, returnParam="both"), (0.0, 0.0))
        self.assertTrue(identification.cost_under_threshold(best_cost1, mean_cost1))
        self.assertTrue(identification.cost_under_threshold(best_cost2, mean_cost2))

    def test_different_voice_vectors(self):
        v0 = sound_extraction.extractVector(WAV_FILE_00)
        v10 = sound_extraction.extractVector(WAV_FILE_10)
        (best_cost1, mean_cost1) = identification.compare_vectors(v0,v10, returnParam="both")
        (best_cost2, mean_cost2) = identification.compare_vectors(v10,v0, returnParam="both")
        self.assertFalse(identification.cost_under_threshold(best_cost1, mean_cost1))
        self.assertFalse(identification.cost_under_threshold(best_cost2, mean_cost2))

    def test_voices_found_in_db_blacklist(self):
        self.assertTrue(Toolbox.reset_test_database(BLACKLIST_FILE))
        if blacklist.update_database_location(BLACKLIST_FILE):
            v0 = sound_extraction.extractVector(WAV_FILE_00)
            v1 = sound_extraction.extractVector(WAV_FILE_01)
            v2 = sound_extraction.extractVector(WAV_FILE_02)
            sound_vectors = []
            sound_vectors.append(v0.tolist())
            sound_vectors.append(v1.tolist())
            sound_vectors.append(v2.tolist())
            wav_files = [WAV_FILE_00,WAV_FILE_01,WAV_FILE_02]
            dates = ["date0","date1","date2"]
            self.assertTrue(blacklist.save_black_listed_person(sound_vectors, wav_files, dates))
            self.assertEqual(identification.compare_to_blacklist(v0),(True, 0))
            self.assertEqual(identification.compare_to_blacklist(v1),(True, 0))
            self.assertEqual(identification.compare_to_blacklist(v2),(True, 0))
            v10 = sound_extraction.extractVector(WAV_FILE_10)
            self.assertEqual(identification.compare_to_blacklist(v10),(False, -1))
            
    def test_voices_found_in_db_annuaire(self):
        self.assertTrue(Toolbox.reset_test_database(ANNUAIRE_FILE))
        if annuaire.update_database_location(ANNUAIRE_FILE):
            v0 = sound_extraction.extractVector(WAV_FILE_00)
            v1 = sound_extraction.extractVector(WAV_FILE_01)
            v2 = sound_extraction.extractVector(WAV_FILE_02)
            v3 = sound_extraction.extractVector(WAV_FILE_03)
            v4 = sound_extraction.extractVector(WAV_FILE_04)
            sound_vectors = []
            sound_vectors.append(v0.tolist())
            sound_vectors.append(v1.tolist())
            sound_vectors.append(v2.tolist())
            sound_vectors.append(v3.tolist())
            sound_vectors.append(v4.tolist())
            wav_files = [WAV_FILE_00,WAV_FILE_01,WAV_FILE_02,WAV_FILE_03,WAV_FILE_04]
            dates = ["date0","date1","date2","date3","date4"]
            self.assertTrue(annuaire.save_new_user("Gordon", "Freeman", "MX001", wav_files, sound_vectors))
            self.assertEqual(identification.compare_to_directory(v0),(True, 0))
            self.assertEqual(identification.compare_to_directory(v1),(True, 0))
            self.assertEqual(identification.compare_to_directory(v2),(True, 0))
            self.assertEqual(identification.compare_to_directory(v3),(True, 0))
            self.assertEqual(identification.compare_to_directory(v4),(True, 0))


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
if __name__ == '__main__':
    unittest.main()