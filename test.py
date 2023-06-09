import unittest
from unittest.mock import patch
import questionnaire
import os
import questionnaire_import
import json


def additionner(a, b):
    return a+b

def conversion_number():
    nb_str = input("Rentrer un nombre")
    return int(nb_str)

class TestsUnitaireDemo(unittest.TestCase):
    def setUp(self):
        print("setUp")

    def tearDown(self):
        print("tearDown")

    def test_additionner_nombres_positifs(self):
        print("Les nombres positifs")
        self.assertEqual(additionner(5, 10), 15)
        self.assertEqual(additionner(6, 10), 16)
        self.assertEqual(additionner(6000, 5), 6005)

    def test_additionner_nombres_negatifs(self):
        print("Les nombres négatifs")
        self.assertEqual(additionner(-6, -10), -16)

    def test_conversion_number_valide(self):
        print("Les conversions valides")
        with patch('builtins.input', return_value="10"):
            self.assertEqual(conversion_number(), 10)
        with patch('builtins.input', return_value="55"):
            self.assertEqual(conversion_number(), 55)

    def test_conversion_entrer_invalide(self):
        print("Les conversions enter valides")
        with patch('builtins.input', return_value='jgdhddx'):
            self.assertRaises(ValueError, conversion_number)    


class TestsQuestions(unittest.TestCase):
    def test_question_bonne_or_mauvaise_reponse(self):
        choix = ('choix1', 'choix2', 'choix3') 
        q = questionnaire.Question("Titre", choix, "choix2")
        with patch('builtins.input', return_value="1"):
            self.assertFalse(q.poser(1, 1))
        with patch('builtins.input', return_value="2"):
            self.assertTrue(q.poser(1, 1))
        with patch('builtins.input', return_value="3"):
            self.assertFalse(q.poser(1, 1))

class TestQuestionnaire(unittest.TestCase):
    def test_questionnaire_lancer_leschats_debutants(self):
        fileName = os.path.join('test', 'animaux_leschats_debutant.json')
        q = questionnaire.Questionnaire.from_file_json(fileName)
        self.assertIsNotNone(q)
        # q.lancer()
        # q.categories()
       
        self.assertEqual(len(q.questions), 10) # Test le nombre de questions
        self.assertEqual(q.titre, "Les chats") # Test est ce que le titre est bien afficher
        self.assertTrue(q.categorie, "Animaux") # Test est ce que la categorie est bien afficher
        self.assertTrue(q.difficulte, "Débutant") # Test est ce que la difficulte est bien afficher
        with patch('builtins.input', return_value="3"): # Test est ce que le questionnaire est bien lancer 
            self.assertEqual(q.lancer(), 5)
    
    def test_questionnaire_format_invalide(self):
        fileName = os.path.join('test', 'animaux_pas_de_categorie_and_difficulte.json')
        q = questionnaire.Questionnaire.from_file_json(fileName)
        self.assertIsNotNone(q)
        self.assertEqual(q.categorie, "Inconnue")
        self.assertEqual(q.difficulte, "Inconnue")
        self.assertIsNotNone(q.questions)

        fileName = os.path.join('test', 'animaux_pas_de_questions.json')
        q = questionnaire.Questionnaire.from_file_json(fileName)
        self.assertIsNone(q)
        

        fileName = os.path.join('test', 'animaux_pas_de_titre.json')
        q = questionnaire.Questionnaire.from_file_json(fileName)
        self.assertIsNone(q)
        

class TestQuestionnaire_import(unittest.TestCase):
    def test_import_format_json(self):
        questionnaire_import.generate_json_file("Animaux", "Les chats", "https://www.codeavecjonathan.com/res/mission/openquizzdb_50.json")
        fileNames = ("animaux_leschats_debutant.json", "animaux_leschats_confirme.json", "animaux_leschats_expert.json")
        for fileName in fileNames:
            self.assertTrue(os.path.isfile(fileName))
            file = open(fileName, "r")
            json_data = file.read()
            file.close()
            try:
                data = json.loads(json_data)
            except:
                self.fail("Problème de déserialisation pour le fichier " + fileName) 

        self.assertIsNotNone(data.get("titre"))
        self.assertIsNotNone(data.get("categorie"))
        self.assertIsNotNone(data.get("difficulte"))
        self.assertIsNotNone(data.get("questions"))

        
        for question in data.get("questions"):
            self.assertIsNotNone(question.get("titre"))
            self.assertIsNotNone(question.get("choix"))
            for choix in question.get("choix"):
                self.assertGreater(len(choix[0]), 0)
                self.assertTrue(isinstance(choix[1], bool))
            bonne_reponse = [i[0] for i in question.get('choix') if i[1]]
            self.assertTrue(len(bonne_reponse), 1)

            # self.assertTrue(question['titre']) 
            # self.assertGreater(len(question['titre']) , 0)
            # self.assertTrue(question['choix'])
            # self.assertGreater(len(question['choix']), 2)
            # self.assertTrue(isinstance(question['choix'][1], bool))
            # self.assertGreater(len(question['choix'][1]), 1)

        
        


unittest.main()