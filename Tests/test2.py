import spacy
import re 

# Charger le modèle linguistique français
nlp = spacy.load("fr_core_news_sm")

# Définir le texte à analyser
texte = "Napoléon Bonaparte est mort le 05/05/1821. Justin Trudeau est né le 25/12/1971 à Ottawa."

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
    nom = None
    verbe = []

    for phrase in texte.split(". "):
        phrase_analysee = nlp(phrase)
        
        # Détecter les dates dans la phrase
        dates = detecter_dates(phrase)

        for token in phrase_analysee :
            if token.pos_ == "AUX" or token.pos_ == "VERB" : 
                verbe.append(token)
                continue
        
        verbe_concatene = " ".join(verbe)

        for ent in phrase_analysee.ents:


            if ent.label_ == "PER" : 
                nom = ent.label_
                if contient_date(phrase):
                    print(f"{ent} : {ent.label_}")
                    questions.append(f"Quand est-ce que {nom} {verbe_concatene} ?")
            # if ent.label_ == "DATE" and ent.text in dates:
            #     questions.append(f"En quelle année {ent.text} {phrase_analysee[ent.root.head.i]} ?")

    return questions

# Test
questions = generer_questions(texte)
for question in questions:
    print(question)

