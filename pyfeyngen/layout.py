
class FeynmanGraph:
    def __init__(self, structure):
        self.nodes = []      
        self.edges = []      
        self.v_count = 0
        self.in_count = 0
        self.f_count = 0
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
        v_start = self.new_v()
        for p in structure[0]:
            in_node = self.new_in()
            self.edges.append((in_node, v_start, p))
        self._process_steps(v_start, structure[1:])

    def _process_steps(self, current_v, steps):
        if not steps: return
        step = steps[0]

        # --- NOUVELLE LOGIQUE POUR LES BOUCLES ---
        # Si l'étape contient un dictionnaire 'loop', c'est une bulle
        if isinstance(step[0], dict) and 'loop' in step[0]:
            loop_particles = step[0]['loop']
            # On crée le vertex où la boucle se referme
            v_loop_end = self.new_v()
            
            # On connecte toutes les particules de la boucle entre les mêmes deux vertex
            for p in loop_particles:
                self.edges.append((current_v, v_loop_end, p))
            
            # On continue le reste du diagramme à partir de la sortie de la boucle
            self._process_steps(v_loop_end, steps[1:])
            return

        # --- LOGIQUE EXISTANTE (BRANCHEMENTS ET CASCADES) ---
        if len(step) == 1 and not isinstance(step[0], list):
            v_next = self.new_v()
            self.edges.append((current_v, v_next, step[0]))
            self._process_steps(v_next, steps[1:])
        else:
            for item in step:
                if isinstance(item, list):
                    v_decay = self.new_v()
                    parent_particle = item[0][0]
                    self.edges.append((current_v, v_decay, parent_particle))
                    self._process_steps(v_decay, item[1:])
                else:
                    f_node = self.new_f()
                    self.edges.append((current_v, f_node, item))


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

    