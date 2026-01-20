def parse_reaction(reaction_str):
    """
    Transform "e+ e- > Z0 > mu+ mu-" 
    to [['e+', 'e-'], ['Z0'], ['mu+', 'mu-']]
    """
    parts = [p.strip() for p in reaction_str.split(">")]
    return [p.split() for p in parts]