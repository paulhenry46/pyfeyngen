from particle import Particle, PDGID

def get_particle_info(name):
    try:
        # Recherche robuste
        p = Particle.findall(name)[0]
        id = p.pdgid
        
        style = "plain"
        
        # On utilise les fonctions de vérification du PDGID (plus fiable)
        if id.is_lepton or id.is_quark:
            style = "fermion"
        elif id == 22: # Photon
            style = "photon"
        elif abs(id) in [23, 24]: # Z or W
            style = "boson"
        elif id == 21: # Gluon
            style = "gluon"
        elif id.is_hadron:
            style = "dashed"

        return {
            "label": p.latex_name,
            "style": style,
            "is_anti": id < 0,
            "pdgid": int(id)
        }
    except Exception as e:
        return {"label": name, "style": "plain", "is_anti": False, "error": str(e)}

# Test
print(get_particle_info("e+"))
# Devrait enfin afficher : 'style': 'fermion', 'is_anti': True