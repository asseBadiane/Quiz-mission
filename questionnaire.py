import json

class Question:
    def __init__(self, titre, choix, bonne_reponse):
        self.titre = titre
        self.choix = choix
        self.bonne_reponse = bonne_reponse

    def form_json_data(data):
        titre = data['titre']
        choix = [i[0] for i in data['choix']]
        bonne_reponse = [i[0] for i in data['choix'] if i[1]] 
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

    def form_data_json(data):
        questionnaire_data = data['questions']
        # print(questionnaire_data[0])
        questions = [Question.form_json_data(x) for x in questionnaire_data]
        return Questionnaire(questions, data['categorie'], data['titre'], data['difficulte'])

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


"""questionnaire = (
    ("Quelle est la capitale de la France ?", ("Marseille", "Nice", "Paris", "Nantes", "Lille"), "Paris"), 
    ("Quelle est la capitale de l'Italie ?", ("Rome", "Venise", "Pise", "Florence"), "Rome"),
    ("Quelle est la capitale de la Belgique ?", ("Anvers", "Bruxelles", "Bruges", "Liège"), "Bruxelles")
                )

lancer_questionnaire(questionnaire)"""

# q1 = Question("Quelle est la capitale de la France ?", ("Marseille", "Nice", "Paris", "Nantes", "Lille"), "Paris")
# q1.poser()

# data = (("Marseille", "Nice", "Paris", "Nantes", "Lille"), "Paris", "Quelle est la capitale de la France ?")
# q = Question.FromData(data)
# print(q.__dict__)

# Questionnaire(
#     (
#     Question("Quelle est la capitale de la France ?", ("Marseille", "Nice", "Paris", "Nantes", "Lille"), "Paris"), 
#     Question("Quelle est la capitale de l'Italie ?", ("Rome", "Venise", "Pise", "Florence"), "Rome"),
#     Question("Quelle est la capitale de la Belgique ?", ("Anvers", "Bruxelles", "Bruges", "Liège"), "Bruxelles")
#     )
# ).lancer()


fileName = "animaux_leschats_debutant.json"
file = open(fileName, "r")

jsonData = file.read()
file.close()

questionnaire_data_json = json.loads(jsonData)

Questionnaire.form_data_json(questionnaire_data_json).lancer()
