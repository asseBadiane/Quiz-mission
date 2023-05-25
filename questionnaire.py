import json
import sys
class Question:
    def __init__(self, titre, choix, bonne_reponse):
        self.titre = titre
        self.choix = choix
        self.bonne_reponse = bonne_reponse

    def from_json_data(data):
        titre = data['titre']
        choix = [i[0] for i in data['choix']]
        bonne_reponse = [i[0] for i in data['choix'] if i[1]] 
        if len(bonne_reponse) != 1:
           return None
        q = Question(titre, choix, bonne_reponse[0])

        return q

    def poser(self, nm_question, nb_question):
        print(f"QUESTION {nm_question} / {nb_question}")
        print("  " + self.titre)
        for i in range(len(self.choix)):
            print("  ", i+1, "-", self.choix[i])

        print()
        resultat_response_correcte = False
        reponse_int = Question.demander_reponse_numerique_utlisateur(1, len(self.choix))
        if self.choix[reponse_int-1].lower() == self.bonne_reponse.lower():
            print("Bonne réponse")
            resultat_response_correcte = True
        else:
            print("Mauvaise réponse")
            
        print()
        return resultat_response_correcte

    def demander_reponse_numerique_utlisateur(min, max):
        reponse_str = input("Votre réponse (entre " + str(min) + " et " + str(max) + ") :")
        try:
            reponse_int = int(reponse_str)
            if min <= reponse_int <= max:
                return reponse_int

            print("ERREUR : Vous devez rentrer un nombre entre", min, "et", max)
        except:
            print("ERREUR : Veuillez rentrer uniquement des chiffres")
        return Question.demander_reponse_numerique_utlisateur(min, max)
    
class Questionnaire:
    def __init__(self, questions, categorie, titre, difficulte):
        self.questions = questions
        self.categorie = categorie
        self.titre = titre
        self.difficulte = difficulte

    def from_data_json(data):
        if not data.get("questions"):
            return None
        questionnaire_data = data['questions']
        # print(questionnaire_data[0])
        questions = [Question.from_json_data(x) for x in questionnaire_data]
        questions = [i for i in questions if i]
     
        if not data.get('titre'):
            return None
        if not data.get('categorie'):
            data['categorie'] = "Inconnue"
        if not data.get('difficulte'):
            data['difficulte'] = "Inconnue"
        return Questionnaire(questions, data['categorie'], data['titre'], data['difficulte'])

    def from_file_json(fileName):
        # fileName = "animaux_leschats_debutant.json"
        try:
            file = open(fileName, "r")

            jsonData = file.read()
            file.close()
            questionnaire_data_json = json.loads(jsonData)
        except:
            print("Exception lors de l'ouverture ou la lecture du fichier")
            return None
        return Questionnaire.from_data_json(questionnaire_data_json)


    def lancer(self):
        print("             ********* QUESTIONNAIRE **********")
        print(f"- Categorie : {self.categorie}")
        print(f"- Titre : {self.titre}")
        print(f"- Difficulte : {self.difficulte}")
        print("      *****  ***    *****")
        score = 0
        nb_question = len(self.questions)
        for i in range(nb_question):
            # print(f"QUESTION: {nb_question}")
            questions = self.questions[i]
            if questions.poser(i+1, nb_question):
                score += 1
            # nb_question += 1
        print("Score final :", score, "sur", len(self.questions))
        return score
    
if __name__ == "__main__":
    print(sys.argv)
    if len(sys.argv) < 2:
        print("ERREUR : Vous devez indiquer le nom du fichier à charger")
        exit(0)

    fileName = sys.argv[1]

    questionnaire = Questionnaire.from_file_json(fileName)
    if questionnaire:
       questionnaire.lancer()


# Questionnaire.from_file_json("animaux_leschats_debutant.json").lancer()


