import spacy
import re 

# Charger le modèle linguistique français
nlp = spacy.load("fr_core_news_sm")

# Définir le texte à analyser
texte = "Christophe Colomb a découvert l'Amérique."

# Analyser le texte
doc = nlp(texte)

# Détecter les dates
def detecter_dates(texte):
    # Formats acceptés :  04-01-1997, 09/07/1897"
    pattern = r'\d{2}.\d{2}.\d{4}'
    dates = re.findall(pattern, texte)
    return dates

def contient_date(phrase):
    # Modèle d'expression régulière pour les dates au format jj/mm/aaaa ou jj-mm-aaaa
    pattern = r'\b(?:0[1-9]|[12][0-9]|3[01])[-/](?:0[1-9]|1[0-2])[-/]\d{4}\b'
    # Recherche de correspondances dans la phrase
    if re.search(pattern, phrase):
        return True
    else:
        return False

def generer_questions(texte):
    questions = []
    
    for phrase in texte.split(". "):
        phrase_analysee = nlp(phrase)
        nom = None
        verbe = []
        reste_phrase = ""  # Initialiser la variable reste_phrase ici

        # Détecter les dates dans la phrase
        dates = detecter_dates(phrase)

        for token in phrase_analysee:
            if token.pos_ == "AUX" or token.pos_ == "VERB":
                verbe.append(token.text)  # Ajouter le texte du token, pas l'objet Token lui-même
                
        
        verbe_concatene = " ".join(verbe)
        # Récupérer le reste de la phrase après le verbe
        verbe_position = -1
        for i, token in enumerate(phrase_analysee):
            if token.text in verbe:
                verbe_position = i
                break
        if verbe_position != -1:
            for token in phrase_analysee[verbe_position + 1:]:
                reste_phrase += token.text_with_ws

        for ent in phrase_analysee.ents:
            if ent.label_ == "PER":
                nom = ent.text
                if contient_date(phrase):
                    questions.append(f"Quand est-ce que {nom} {verbe_concatene} ?")
                else : 
                    questions.append(f"Qui {verbe_concatene} {reste_phrase}?")         

    return questions

def generer_reponses(texte):
    
    reponses = []
    
    for phrase in texte.split(". "):
        phrase_analysee = nlp(phrase)
        nom = None
        verbe = []

        # Détecter les dates dans la phrase
        dates = detecter_dates(phrase)

        for token in phrase_analysee:
            if token.pos_ == "AUX" or token.pos_ == "VERB":
                verbe.append(token.text)  # Ajouter le texte du token, pas l'objet Token lui-même
        
        verbe_concatene = " ".join(verbe)

        for ent in phrase_analysee.ents:
            if ent.label_ == "PER":
                nom = ent.text
                if contient_date(phrase):
                    reponses.append(f"En {detecter_dates(phrase)}")

    return reponses

# Test
questions = generer_questions(texte)
for question in questions:
    print(question)

# reponses = generer_reponses(texte)

# for reponse in reponses : 
#     print(reponse)