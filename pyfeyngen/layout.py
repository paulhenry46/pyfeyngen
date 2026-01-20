class FeynmanGraph:
    def __init__(self, structure):
        self.nodes = []      
        self.edges = []      
        self.v_count = 0
        self.in_count = 0
        self.f_count = 0
        self.anchor_points = {} 
        
        self.build_graph(structure)

    def new_v(self):
        self.v_count += 1
        return f"vx{self.v_count}"

    def new_in(self):
        self.in_count += 1
        return f"inx{self.in_count}"

    def new_f(self):
        self.f_count += 1
        return f"fx{self.f_count}"

    def build_graph(self, structure):
        first_step = structure[0]
        
        # Séparation des types d'éléments dans le premier bloc
        in_particles = [p for p in first_step if isinstance(p, str)]
        in_anchors = [p for p in first_step if isinstance(p, dict)]
        in_cascades = [p for p in first_step if isinstance(p, list)]

        # CAS 1 : Il y a des particules parentes (ex: u ubar > ...)
        if in_particles:
            v_start = self.new_v()
            for a in in_anchors:
                self._register_anchor(v_start, a)
            for p in in_particles:
                in_node = self.new_in()
                self.edges.append((in_node, v_start, p))
            
            # On lance la suite du diagramme normalement
            self._process_steps(v_start, structure[1:])

        # CAS 2 : Le diagramme commence directement par des blocs (ex: (e- > @A) (e- > @A))
        elif in_cascades:
            # On traite chaque cascade comme une racine indépendante
            for cascade in in_cascades:
                # Chaque racine commence par un vertex d'entrée propre
                v_root = self.new_v()
                
                # On extrait la particule de départ de cette cascade
                # Exemple pour (e- > @A) -> 'e-'
                p_start_name = next((t for t in cascade[0] if isinstance(t, str)), "unknown")
                
                # On crée l'entrée physique pour cette branche
                in_node = self.new_in()
                self.edges.append((in_node, v_root, p_start_name))
                
                # On enregistre les ancres sur ce vertex de départ
                for t in cascade[0]:
                    if isinstance(t, dict) and 'anchor' in t:
                        self._register_anchor(v_root, t)
                
                # On lance la récursion pour cette branche spécifique
                self._process_steps(v_root, cascade[1:])
            
            # Note : On ignore structure[1:] ici car dans ce format, 
            # tout est contenu dans les cascades initiales.
        
        # 3. Soudure finale des cycles
        self._connect_anchors()

    def _process_steps(self, current_v, steps):
        if not steps: return
        step = steps[0]

        particles = [item for item in step if isinstance(item, str) or isinstance(item, list)]
        anchors = [item for item in step if isinstance(item, dict) and 'anchor' in item]

        for a in anchors:
            self._register_anchor(current_v, a)

        if not particles:
            self._process_steps(current_v, steps[1:])
            return

        if len(particles) == 1 and not isinstance(particles[0], list):
            v_next = self.new_v()
            self.edges.append((current_v, v_next, particles[0]))
            self._process_steps(v_next, steps[1:])
        else:
            for item in particles:
                if isinstance(item, list):
                    v_decay = self.new_v()
                    p_name = next((t for t in item[0] if isinstance(t, str)), "unknown")
                    for t in item[0]:
                        if isinstance(t, dict) and 'anchor' in t:
                            self._register_anchor(v_decay, t)
                    
                    self.edges.append((current_v, v_decay, p_name))
                    self._process_steps(v_decay, item[1:])
                else:
                    f_node = self.new_f()
                    self.edges.append((current_v, f_node, item))

    def _register_anchor(self, vertex, anchor_dict):
        name = anchor_dict['anchor']
        if name not in self.anchor_points:
            self.anchor_points[name] = []
        self.anchor_points[name].append({
            'vertex': vertex,
            'particle': anchor_dict.get('particle')
        })

    def _connect_anchors(self):
        for name, points in self.anchor_points.items():
            if len(points) >= 2:
                for i in range(len(points) - 1):
                    src = points[i]['vertex']
                    dst = points[i+1]['vertex']
                    p_name = points[i]['particle'] or "gamma"
                    self.edges.append((src, dst, p_name))
if __name__ == "__main__":
    # Simulation d'une structure parsée complexe : 
    # u ubar > H > (Z0 > e+ e-) (Z0 > mu+ mu-)
    mock_structure = [
        ['u', 'ubar'],                                     # Entrées
        ['H'],                                             # Étape 1
        [                                                  # Étape 2 (Branchement)
            [['Z0'], ['e+', 'e-']],                        # Cascade 1
            [['Z0'], ['mu+', 'mu-']]                       # Cascade 2
        ]
    ]

    mock_structure =  [['H'], [[['Z0'], ['e+', 'e-']], 'Z0']]
    mock_structure = [['e+', 'e-'], ['Z0'], ['mu+', 'mu-']]

    print("--- TEST DU GENERATEUR DE GRAPHE ---")
    graph = FeynmanGraph(mock_structure)

    print(f"\nNoeuds créés : {graph.v_count} vertex, {graph.in_count} entrées, {graph.f_count} sorties.")
    
    print("\nListe des connexions (Edges) :")
    print(f"{'Source':<10} | {'Cible':<10} | {'Particule':<10}")
    print("-" * 35)
    for src, dst, particle in graph.edges:
        print(f"{src:<10} | {dst:<10} | {particle:<10}")

    