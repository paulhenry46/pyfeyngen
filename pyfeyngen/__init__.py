from .parser import parse_reaction
from .layout import get_s_channel_nodes
from .exporter import to_tikz_feynman

__version__ = "0.1.0"
__author__ = "Ton Nom"

def quick_generate(reaction_str):
    """Fonction 'clé en main' pour l'utilisateur."""
    structure = parse_reaction(reaction_str)
    topology = get_s_channel_nodes(structure)
    return to_tikz_feynman(topology)