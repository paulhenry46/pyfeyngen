from particle import Particle, PDGID

def get_particle_info(name):
    try:
        p = Particle.findall(name)[0]
        id = p.pdgid
        style = "plain"
        if id.is_lepton or id.is_quark: style = "fermion"
        elif id == 22: style = "photon"
        elif abs(id) in [23, 24]: style = "boson"
        elif id == 21: style = "gluon"
        
        return {"label": p.latex_name, "style": style, "is_anti": id < 0}
    except:
        return {"label": name, "style": "plain", "is_anti": False}

def generate_s_channel_tikz(reaction):
    steps = [s.strip().split() for s in reaction.split(">")]
    
    in_1, in_2 = get_particle_info(steps[0][0]), get_particle_info(steps[0][1])
    prop = get_particle_info(steps[1][0])
    out_1, out_2 = get_particle_info(steps[2][0]), get_particle_info(steps[2][1])

    lines = []
    
    # ENTRES : On utilise 'edge label' au lieu des accolades pour éviter l'erreur endcsname
    # Pour in_1
    if in_1['is_anti']:
        lines.append(fr"v1 -- [{in_1['style']}, edge label=\({in_1['label']}\)] i1")
    else:
        lines.append(fr"i1 -- [{in_1['style']}, edge label=\({in_1['label']}\)] v1")
        
    # Pour in_2
    if in_2['is_anti']:
        lines.append(fr"v1 -- [{in_2['style']}, edge label'=\({in_2['label']}\)] i2") # Note le ' pour mettre le label de l'autre côté
    else:
        lines.append(fr"i2 -- [{in_2['style']}, edge label'=\({in_2['label']}\)] v1")

    # PROPAGATEUR
    lines.append(fr"v1 -- [{prop['style']}, edge label=\({prop['label']}\)] v2")
    
    # SORTIES
    lines.append(fr"v2 -- [{out_1['style']}, edge label=\({out_1['label']}\)] f1")
    lines.append(fr"v2 -- [{out_2['style']}, edge label'=\({out_2['label']}\)] f2")

    tikz_template = f"""
\\documentclass{{standalone}}
\\usepackage[compat=1.1.0]{{tikz-feynman}}
\\begin{{document}}
\\feynmandiagram [horizontal=v1 to v2] {{
  {lines[0]},
  {lines[1]},
  {lines[2]},
  {lines[3]},
  {lines[4]},
}};
\\end{{document}}
"""
    return tikz_template

# Execution
reaction_str = "mu+ e- > Z0 > mu+ mu-"
result = generate_s_channel_tikz(reaction_str)

with open("diagram.tex", "w") as f:
    f.write(result)

print("Fichier diagram.tex généré !")