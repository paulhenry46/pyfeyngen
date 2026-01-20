from .physics import get_info

def generate_physical_tikz(graph):
    tikz_lines = []
    vertex_usage = {}
    
    # ÉTAPE PRÉALABLE : Compter combien de fois chaque chemin est utilisé
    path_totals = {}
    for src, dst, _ in graph.edges:
        path_id = tuple(sorted((src, dst)))
        path_totals[path_id] = path_totals.get(path_id, 0) + 1

    # ÉTAPE DE GÉNÉRATION
    path_current_count = {} # Pour savoir si on est à la 1ère ou 2ème ligne du chemin

    for src, dst, particle in graph.edges:
        info = get_info(particle)
        style = info['style']
        label = info['label']
        path_id = tuple(sorted((src, dst)))
        
        # Gestion du Bending Symétrique
        bend_style = ""
        total_lines = path_totals[path_id]
        
        if total_lines > 1:
            # On initialise le compteur pour ce chemin si besoin
            current = path_current_count.get(path_id, 0)
            # La 1ère ligne va à gauche, la 2ème à droite
            side_bend = "left" if current % 2 == 0 else "right"

            if info['is_anti'] and style == 'fermion':
                side_bend = "right" if side_bend == "left" else "left"

            bend_style = f", bend {side_bend}=45"
            path_current_count[path_id] = current + 1
        
        # Gestion du Label Side (Prime)
        count_usage = vertex_usage.get(src, 0)
        label_side = "'" if count_usage % 2 != 0 else "" 
        vertex_usage[src] = count_usage + 1
        
        # Construction de la ligne
        if info['is_anti'] and style == 'fermion':
            line = fr"  {dst} -- [{style}{bend_style}, edge label{label_side}=\({label}\)] {src}"
        else:
            line = fr"  {src} -- [{style}{bend_style}, edge label{label_side}=\({label}\)] {dst}"
            
        tikz_lines.append(line)
    
    header = "\\feynmandiagram [horizontal=inx1 to fx1] {"
    footer = "};"
    return header + "\n" + ",\n".join(tikz_lines) + "\n" + footer

if __name__ == "__main__":
    from parser import parse_reaction
    from layout import FeynmanGraph
    reactions = ['u ubar > H > (Z0 > e+ e-) (Z0 > mu+ mu-)', 'u ubar > H > (Z0 > e+ e-) Z0', 'e+ e- > Z0 > mu+ mu-']
    for reaction in reactions:

        # 1. Analyse
        structure = parse_reaction(reaction)
        
        # 2. Topologie
        graph = FeynmanGraph(structure)
        
        # 3. Code TikZ
        tikz_final = generate_physical_tikz(graph)
        
        print(tikz_final)