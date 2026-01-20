from .physics import get_particle_info

def to_tikz_feynman(topology_data):
    """Génère le code LaTeX complet à partir des données de topologie."""
    
    in_p = [get_particle_info(p) for p in topology_data["incoming"]]
    prop = get_particle_info(topology_data["propagator"])
    out_p = [get_particle_info(p) for p in topology_data["outgoing"]]

    lines = []
    
    # Particules Initiales (Entrées)
    # i1/i2 -> v1
    for i, p in enumerate(in_p):
        node_name = f"i{i+1}"
        label_side = "'" if i == 1 else "" # Label en bas pour la 2ème particule
        if p['is_anti']:
            lines.append(fr"v1 -- [{p['style']}, edge label{label_side}=\({p['label']}\)] {node_name}")
        else:
            lines.append(fr"{node_name} -- [{p['style']}, edge label{label_side}=\({p['label']}\)] v1")

    # Propagateur
    # v1 -> v2
    lines.append(fr"v1 -- [{prop['style']}, edge label=\({prop['label']}\)] v2")

    # Particules Finales (Sorties)
    # v2 -> f1/f2
    for i, p in enumerate(out_p):
        node_name = f"f{i+1}"
        label_side = "'" if i == 1 else ""
        if p['is_anti'] and p['style'] == "fermion":
            lines.append(fr"{node_name} -- [{p['style']}, edge label{label_side}=\({p['label']}\)] v2")
        else:
            lines.append(fr"v2 -- [{p['style']}, edge label{label_side}=\({p['label']}\)] {node_name}")

    # Assemblage du template
    content = ",\n  ".join(lines)
    tikz_code = (
        "\\feynmandiagram [horizontal=v1 to v2]{\n"
        f"  {content}\n"
        "};"
    )
    return tikz_code