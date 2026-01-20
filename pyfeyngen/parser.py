import re
from .errors import InvalidReactionError

def parse_reaction(reaction_str):
    """
    Transforme une chaîne de réaction en structure de listes imbriquées.
    Supporte les branchements (...), les boucles multi-particules [...] et les ancres @.
    """
    if not reaction_str.strip():
        raise InvalidReactionError("La chaîne de réaction est vide.")
    
    # Vérification de l'équilibre des parenthèses et crochets
    if reaction_str.count('(') != reaction_str.count(')'):
        raise InvalidReactionError("Parenthèses non équilibrées.")
    if reaction_str.count('[') != reaction_str.count(']'):
        raise InvalidReactionError("Crochets non équilibrés.")
    
    s = reaction_str.strip()
    steps = []
    current_step = ""
    depth = 0
    
    # Étape 1 : Séparer par les '>' de premier niveau
    for char in s:
        if char == '(': depth += 1
        elif char == ')': depth -= 1
        
        if char == '>' and depth == 0:
            steps.append(current_step.strip())
            current_step = ""
        else:
            current_step += char
    steps.append(current_step.strip())
    
    final_structure = []
    for step in steps:
        if step: # Évite les étapes vides si doubles '>'
            final_structure.append(_parse_step(step))
        
    return final_structure

def _parse_step(step_str):
    """Analyse une étape pour séparer les particules, blocs ( ), boucles [ ] et ancres @"""
    tokens = []
    i = 0
    while i < len(step_str):
        if step_str[i].isspace():
            i += 1
            continue
            
        # 1. GESTION DES PARENTHÈSES (Cascades / Branchements)
        if step_str[i] == '(':
            start = i + 1
            depth = 1
            i += 1
            while i < len(step_str) and depth > 0:
                if step_str[i] == '(': depth += 1
                elif step_str[i] == ')': depth -= 1
                i += 1
            tokens.append(parse_reaction(step_str[start:i-1]))

        # 2. GESTION DES CROCHETS (Boucles multi-particules)
        elif step_str[i] == '[':
            start = i + 1
            depth = 1
            i += 1
            while i < len(step_str) and depth > 0:
                if step_str[i] == '[': depth += 1
                elif step_str[i] == ']': depth -= 1
                i += 1
            # On extrait toutes les particules à l'intérieur, séparées par des espaces
            # Exemple: [gamma Z0 H] -> ['gamma', 'Z0', 'H']
            loop_content = [p.strip() for p in step_str[start:i-1].split() if p.strip()]
            tokens.append({'loop': loop_content})

        # 3. GESTION DES ANCRES (@nom ou @nom:particule)
        elif step_str[i] == '@':
            start = i + 1
            # On s'arrête si on croise un espace ou un début de bloc
            while i < len(step_str) and not step_str[i].isspace() and step_str[i] not in '([':
                i += 1
            anchor_text = step_str[start:i]
            if ':' in anchor_text:
                name, part = anchor_text.split(':', 1)
                tokens.append({'anchor': name, 'particle': part})
            else:
                tokens.append({'anchor': anchor_text, 'particle': None})

        # 4. PARTICULES SIMPLES (Noms de particules)
        else:
            start = i
            # Une particule s'arrête avant un espace, un @, un ( ou un [
            while i < len(step_str) and not step_str[i].isspace() and step_str[i] not in '([@':
                i += 1
            token = step_str[start:i]
            if token:
                tokens.append(token)
    return tokens