import spacy

# Chargement du modèle français de spaCy
nlp = spacy.load("fr_core_news_sm")

texte = "Napoléon Bonaparte est mort le 05/05/1821. Justin Trudeau est né le 25/12/1971 à Ottawa."

# Traitement du texte avec spaCy
doc = nlp(texte)

def trouver_actions(doc):
    actions = []
    for token in doc:
        print(f"{token} : {token.pos_}")
        # Recherche des verbes au participe passé utilisés avec un auxiliaire
        if token.pos_ == "VERB" and token.tag_ == "VPP" and token.dep_ == "acl":
            aux = [child for child in token.head.children if child.dep_ == "aux"]
            if aux:  # Si un auxiliaire est présent
                action = f"{aux[0].text} {token.text}"
                actions.append((action, token.idx))
    return actions

actions = trouver_actions(doc)
for action, index in actions:
    print(f"Action détectée: {action}, à l'index de départ: {index}")
