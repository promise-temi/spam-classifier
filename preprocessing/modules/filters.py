from langdetect import detect, DetectorFactory

# Pour avoir des résultats reproductibles
DetectorFactory.seed = 0

def is_english(text: str) -> bool:
    try:
        # Retourne True si c'est de l'anglais
        return detect(text) == "en"
    except:
        # S'il y a une erreur (texte trop court, caractères spéciaux), on gère ici
        return False
