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
        
        in_particles = [p for p in first_step if isinstance(p, str)]
        in_anchors = [p for p in first_step if isinstance(p, dict) and 'anchor' in p]
        in_cascades = [p for p in first_step if isinstance(p, list)]

        # CAS 1 : Tronc commun
        if in_particles:
            v_start = self.new_v()
            for a in in_anchors:
                self._register_anchor(v_start, a)
            for p in in_particles:
                in_node = self.new_in()
                self.edges.append((in_node, v_start, p))
            self._process_steps(v_start, structure[1:])

        # CAS 2 : Racines multiples
        elif in_cascades:
            for cascade in in_cascades:
                v_root = self.new_v()
                p_start_name = next((t for t in cascade[0] if isinstance(t, str)), "unknown")
                in_node = self.new_in()
                self.edges.append((in_node, v_root, p_start_name))
                for t in cascade[0]:
                    if isinstance(t, dict) and 'anchor' in t:
                        self._register_anchor(v_root, t)
                self._process_steps(v_root, cascade[1:])
        
        self._connect_anchors()

    def _process_steps(self, current_v, steps):
        if not steps: return
        step = steps[0]

        # 1. Extraction des différents types de tokens
        # On identifie spécifiquement les dictionnaires 'loop'
        loops = [item for item in step if isinstance(item, dict) and 'loop' in item]
        anchors = [item for item in step if isinstance(item, dict) and 'anchor' in item]
        # Particules simples ou sous-cascades
        real_particles = [item for item in step if isinstance(item, (str, list))]

        # 2. Enregistrement des ancres sur le vertex actuel
        for a in anchors:
            self._register_anchor(current_v, a)

        # 3. GESTION DES CROCHETS MULTI-PARTICULES [...]
        if loops:
            # On récupère la liste des particules dans le crochet
            loop_particles = loops[0]['loop']
            v_loop_end = self.new_v()
            
            # On crée autant d'arêtes parallèles que de particules spécifiées
            for p in loop_particles:
                self.edges.append((current_v, v_loop_end, p))
            
            # On poursuit le diagramme à partir de la sortie du bloc [...]
            self._process_steps(v_loop_end, steps[1:])
            return

        # 4. GESTION CLASSIQUE (Propagation ou Branchement)
        if not real_particles:
            self._process_steps(current_v, steps[1:])
            return

        if len(real_particles) == 1 and not isinstance(real_particles[0], list):
            v_next = self.new_v()
            self.edges.append((current_v, v_next, real_particles[0]))
            self._process_steps(v_next, steps[1:])
        else:
            for item in real_particles:
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

    