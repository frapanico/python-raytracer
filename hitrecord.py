from vec3 import Vec3
from ray import Ray

#Questa classe tiene traccia del punto colpito (normale, il punto, il materiale ecc.)
class HitRecord:
    def __init__(self):
        self.p: Vec3 = None           # Punto di impatto
        self.normal: Vec3 = None      # Normale nel punto di impatto
        self.t: float = 0.0           # Parametro t lungo il raggio
        self.front_face: bool = True  # True se il raggio colpisce il lato esterno dell'oggetto
        self.material = None          # Materiale dell'oggetto colpito

    #Questa funzione permette di capire se il punto di incidenza è dentro o fuori un oggetto,
    #se la normale e il raggio sono nella stessa direzione, allora il punto di incidenza è dentro l'oggetto,
    #altrimenti se in direzioni opposte il punto è fuori l'oggetto
    def set_face_normal(self, ray: Ray, outward_normal: Vec3):
        # prodotto scalare tra la direzione del raggio e la normale che punta all'esterno
        # ovvero vettore dal centro della sfera al punto di impatto (vedi sphere.py)
        # il prodotto scalare è negativo se puntano in direzioni opposte
        self.front_face = ray.direction.dot(outward_normal) < 0 # se negativo, front_face = true
        self.normal = outward_normal if self.front_face else -outward_normal # imposto la normale
