import re

def replace_splitted_urls(text: str) -> str:
    """
    Recherche dans chaque ligne les fragments de la forme :
      - http : / / (ou https : / /)
      - www .
    puis capture tout le reste jusqu'à la fin de la ligne.
    Ensuite, on recolle les espaces et si on obtient bien un "http://", "https://" ou "www.",
    on remplace par le token [URL].
    """

    # (?:https?\s*:\s*/\s*/)   = "http : //..." ou "https : //..." (tolérant des espaces)
    # (?:www\s*\.)            = "www." (tolérant des espaces avant le point)
    #
    # [^\n]*                  = on capture tout le reste jusqu'à la fin de la ligne
    pattern = re.compile(r'((?:https?\s*:\s*/\s*/)|(?:www\s*\.))[^\n]*', flags=re.IGNORECASE)

    def replace_match(m: re.Match) -> str:
        # Partie de texte capturée qui ressemble à une URL fragmentée
        splitted_url = m.group(0)
        # On retire tous les espaces au sein de cette portion
        cleaned_url = re.sub(r'\s+', '', splitted_url)
        
        # Vérif basique : est-ce que le résultat commence par "http://", "https://" ou "www." ?
        if re.match(r'^(?:https?://|www\.)', cleaned_url, flags=re.IGNORECASE):
            return '[ENTITY]'
        else:
            # Sinon, on peut laisser tel quel ou avoir une autre logique
            return splitted_url

    return pattern.sub(replace_match, text)




def replace_splitted_emails(text: str) -> str:
    """
    Détecte les adresses e-mail fragmentées (ex: ab _ karol @ fastermail . com),
    recolle les morceaux, puis remplace par [EMAIL].
    """

    # Pattern qui capture tout ce qui ressemble à : 
    #   <suite de caractères> @ <suite de caractères> . <extension>
    # en tolérant des espaces
    #
    # [\w.\-_]+ correspond à un ensemble de caractères usuels pour la partie locale (avant le @)
    # \s*@\s* tolère les espaces autour du @
    # [\w.\-]+ tolère lettres, chiffres, point, tiret pour le domaine
    # \s*\.\s* tolère les espaces autour du point
    # [a-zA-Z]{2,} => extension de 2 lettres ou plus (com, fr, net, co.uk plus compliqué, etc.)
    pattern = re.compile(r'([\w.\-_]+\s*@\s*[\w.\-]+\s*\.\s*[a-zA-Z]{2,})', flags=re.IGNORECASE)

    def replace_match(m: re.Match) -> str:
        splitted_email = m.group(1)
        # Retirer tous les espaces intérieurs
        cleaned_email = re.sub(r'\s+', '', splitted_email)
        # Vérif basique : est-ce que ça ressemble à un email standard ?
        # Par ex: "ab_karol@fastermail.com"
        if re.match(r'^[\w.\-_]+@[\w.\-]+\.[a-zA-Z]{2,}$', cleaned_email, flags=re.IGNORECASE):
            return '[ENTITY]'
        else:
            return splitted_email  # ou remplacer inconditionnellement par [EMAIL]

    return pattern.sub(replace_match, text)










import re

def replace_phone_numbers(text: str) -> str:
    """
    Remplace des numéros de téléphone (y compris courts) par [PHONE].
    Exemples détectés : +33 6 12 34 56 78, (202) 555-0147, 88039, etc.
    """

    # Ajustement du pattern pour inclure des numéros courts
    # 1. Capture des numéros avec ou sans "+"
    # 2. Accepte des longueurs de 5 à 16 chiffres
    # 3. Tolère des espaces, tirets, parenthèses, points
    phone_pattern = re.compile(r'(\+?\s*\d[\d\-\(\)\s\.]{3,}\d)')

    def phone_replacer(m: re.Match) -> str:
        raw_phone = m.group(1)
        # Enlever espaces, tirets, parenthèses, points
        cleaned_phone = re.sub(r'[\s\-\(\)\.]+', '', raw_phone)

        # Vérification stricte : 5 à 16 chiffres, avec ou sans "+"
        if re.match(r'^\+?\d{5,16}$', cleaned_phone):
            return '[ENTITY]'
        else:
            return raw_phone  # Ne pas remplacer si ça ne ressemble pas à un numéro

    return phone_pattern.sub(phone_replacer, text)












