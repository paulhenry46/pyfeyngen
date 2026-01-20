from .physics import get_info

def generate_physical_tikz(graph):
    tikz_lines = []
    vertex_usage = {}

    # 1. FILTRAGE ET COMPTAGE PRÉALABLE
    # On identifie les chemins (src, dst) empruntés par plusieurs particules
    path_totals = {}
    valid_edges = []
    for edge in graph.edges:
        src, dst, particle = edge
        if isinstance(particle, str):
            valid_edges.append(edge)
            path_id = tuple(sorted((src, dst)))
            path_totals[path_id] = path_totals.get(path_id, 0) + 1

    path_current_count = {}

    # 2. GÉNÉRATION DES LIGNES TIKZ
    for src, dst, particle in valid_edges:
        info = get_info(particle)
        style = info['style']
        label = info['label']
        path_id = tuple(sorted((src, dst)))
        
        # --- Gestion du Multi-Bending (Répartition dynamique) ---
        bend_style = ""
        total_lines = path_totals[path_id]
        
        if total_lines > 1:
            idx = path_current_count.get(path_id, 0)
            path_current_count[path_id] = idx + 1
            
            # On définit l'amplitude maximale de la "bulle" (ex: 50 degrés)
            max_bend = 50 
            
            # Formule de répartition linéaire :
            # Pour 2 lignes : -50, 50
            # Pour 3 lignes : -50, 0, 50
            # Pour 4 lignes : -50, -16, 16, 50
            step = (max_bend * 2) / (total_lines - 1)
            angle = -max_bend + (step * idx)
            
            # Inversion pour les antifermions pour que la flèche suive la courbure
            if info['is_anti'] and style == 'fermion':
                angle = -angle
            
            # Application du style TikZ
            if abs(angle) > 0.1:  # On ignore les angles proches de 0 (ligne droite)
                side = "left" if angle > 0 else "right"
                bend_style = f"bend {side}={abs(int(angle))}"
        
        # --- Gestion du Label Side (Prime) ---
        # Alterne le côté du label si le vertex est très utilisé
        count_usage = vertex_usage.get(src, 0)
        label_side = "'" if count_usage % 2 != 0 else "" 
        vertex_usage[src] = count_usage + 1
        
        # --- Construction des options de l'arête ---
        label_cmd = fr"edge label{label_side}=\({label}\)" if label else ""
        
        options = [style]
        if bend_style: options.append(bend_style)
        if label_cmd: options.append(label_cmd)
        
        options_str = ", ".join(options)

        # --- Assemblage de la commande (Gestion du flux des fermions) ---
        if info['is_anti'] and style == 'fermion':
            line = fr"  {dst} -- [{options_str}] {src}"
        else:
            line = fr"  {src} -- [{options_str}] {dst}"
            
        tikz_lines.append(line)
    
    # Header utilisant layered layout pour gérer les racines multiples et les cycles
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