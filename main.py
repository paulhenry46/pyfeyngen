from pyfeyngen.parser import parse_reaction
from pyfeyngen.layout import get_s_channel_nodes
from pyfeyngen.exporter import to_tikz_feynman

# 1. L'utilisateur entre sa réaction
reaction = "e+ e- > Z0 > mu+ mu-"

# 2. Pipeline de la library
structure = parse_reaction(reaction)
topology = get_s_channel_nodes(structure)
tikz_output = to_tikz_feynman(topology)

print(tikz_output)