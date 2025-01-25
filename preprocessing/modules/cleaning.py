import re
import string


#mettre en minuscule et supprimer les caractères spéciaux et les espaces multiples et les espaces en début et fin de texte 

def clean_text(text):
    text = text.lower()
    text = re.sub(r'[^a-z0-9\s\[\]]', '', text)
    text = re.sub(r'\s+', ' ', text)
    return text.strip()
