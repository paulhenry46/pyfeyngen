def calculate_layout(steps):
    """
    Entrée: [['e+', 'e-'], ['Z0'], ['mu+', 'mu-']]
    Sortie: Un dictionnaire avec les coordonnées de chaque point
    """
    nodes = {}
    
    # 1. Particules initiales (Entrées)
    # On les espace verticalement autour de y=0
    for i, p in enumerate(steps[0]):
        y_pos = 1 if i == 0 else -1
        nodes[f"in_{i}"] = {"pos": (0, y_pos), "label": p}
        
    # 2. Vertex 1 (Fusion)
    nodes["v1"] = {"pos": (2, 0), "label": ""}
    
    # 3. Vertex 2 (Scission)
    nodes["v2"] = {"pos": (4, 0), "label": ""}
    
    # 4. Particules finales (Sorties)
    for i, p in enumerate(steps[2]):
        y_pos = 1 if i == 0 else -1
        nodes[f"out_{i}"] = {"pos": (6, y_pos), "label": p}
        
    return nodes


def get_s_channel_nodes(steps):
    """
    Définit les rôles des nœuds pour une topologie S-Channel.
    """
    return {
        "incoming": steps[0],   # ex: ['e+', 'e-']
        "propagator": steps[1][0], # ex: 'Z0'
        "outgoing": steps[2]    # ex: ['mu+', 'mu-']
    }