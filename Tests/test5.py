import spacy
import re

# Charger le modèle linguistique français
nlp = spacy.load("fr_core_news_sm")

# Définir le texte à analyser
texte = "Napoléon Bonaparte est mort le 05/05/1821. Justin Trudeau est né le 25/12/1971 à Ottawa. Christophe Colomb a découvert l'Amérique."

# Analyser le texte
doc = nlp(texte)

def detecter_dates(texte):
    pattern = r'\d{2}.\d{2}.\d{4}'
    dates = re.findall(pattern, texte)
    return dates

def contient_date(phrase):
    pattern = r'\b(?:0[1-9]|[12][0-9]|3[01])[-/](?:0[1-9]|1[0-2])[-/]\d{4}\b'
    return re.search(pattern, phrase) is not None

def generer_questions_et_reponses(texte):
    questions = []
    reponses = []
    
    for phrase in texte.split(". "):
        phrase_analysee = nlp(phrase)
        verbe = None
        reste_phrase = ""
        
        dates = detecter_dates(phrase)
        
        for token in phrase_analysee:
            if token.pos_ == "AUX" or token.pos_ == "VERB":
                if verbe is None:
                    verbe = token.text  # Garder le premier verbe trouvé
                    break
        
        if verbe:
            verbe_position = [i for i, token in enumerate(phrase_analysee) if token.text == verbe][0]
            reste_phrase = ''.join([token.text_with_ws for token in phrase_analysee[verbe_position+1:] if token.pos_ != "PUNCT"])

        for ent in phrase_analysee.ents:
            if contient_date(phrase):
                if ent.label_ == "PER":
                    questions.append(f"Quand est-ce que {ent.text} {verbe} ?")
                    reponses.append(f"En {dates}")
                elif ent.label_ == "LOC":
                    questions.append(f"Quand {verbe} {reste_phrase}?")
                    reponses.append(f"En {dates}")
            else:
                if ent.label_ == "PER":
                    questions.append(f"Qui {verbe} {reste_phrase}?")
                elif verbe and not ent.label_ == "PER":
                    questions.append(f"Qui {verbe} {reste_phrase}?")

    return questions, reponses

# Test
questions, reponses = generer_questions_et_reponses(texte)
for question in questions:
    print(question)
for reponse in reponses:
    print(reponse)
