from .physics import get_info

def generate_physical_tikz(graph):
    tikz_lines = []
    vertex_usage = {}

    # 1. FILTRAGE ET COMPTAGE (Une seule passe propre)
    path_totals = {}
    valid_edges = []
    
    for edge in graph.edges:
        src, dst, particle = edge
        # On ne traite que les vraies particules (chaînes)
        if isinstance(particle, str):
            valid_edges.append(edge)
            path_id = tuple(sorted((src, dst)))
            path_totals[path_id] = path_totals.get(path_id, 0) + 1

    path_current_count = {}

    # 2. GÉNÉRATION DES LIGNES
    for src, dst, particle in valid_edges:
        info = get_info(particle)
        style = info['style']
        label = info['label']
        path_id = tuple(sorted((src, dst)))
        
        # --- Gestion du Bending Symétrique ---
        bend_style = ""
        if path_totals[path_id] > 1:
            current = path_current_count.get(path_id, 0)
            side_bend = "left" if current % 2 == 0 else "right"

            # Correction d'orientation pour les antifermions
            if info['is_anti'] and style == 'fermion':
                side_bend = "right" if side_bend == "left" else "left"

            bend_style = f"bend {side_bend}=45"
            path_current_count[path_id] = current + 1
        
        # --- Gestion du Label Side (Prime) ---
        count_usage = vertex_usage.get(src, 0)
        label_side = "'" if count_usage % 2 != 0 else "" 
        vertex_usage[src] = count_usage + 1
        
        # --- Construction des options ---
        label_cmd = fr"edge label{label_side}=\({label}\)" if label else ""
        
        options = [style]
        if bend_style: options.append(bend_style)
        if label_cmd: options.append(label_cmd)
        
        options_str = ", ".join(options)

        # --- Assemblage final (respect du sens des fermions) ---
        if info['is_anti'] and style == 'fermion':
            line = fr"  {dst} -- [{options_str}] {src}"
        else:
            line = fr"  {src} -- [{options_str}] {dst}"
            
        tikz_lines.append(line)
    
    # Configuration du Header : 
    # layered layout est indispensable pour les ancres et les racines multiples
    header = "\\feynmandiagram [layered layout, horizontal=inx1 to fx1] {"
    footer = "};"
    
    return header + "\n" + ",\n".join(tikz_lines) + "\n" + footer
if __name__ == "__main__":
    from .parser import parse_reaction
    from .layout import FeynmanGraph
    
    # Test avec une réaction à ancre (Échange de photon entre deux branches)
    reactions = [
        'u ubar > H > (Z0 @link > e+ e-) (Z0 @link > mu+ mu-)',
        'e- > @box:gamma e- > @box'
    ]
    
    for reaction in reactions:
        print(f"\n--- Test: {reaction} ---")
        structure = parse_reaction(reaction)
        graph = FeynmanGraph(structure)
        print(generate_physical_tikz(graph))