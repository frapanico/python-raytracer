from hittable import Hittable
from hitrecord import HitRecord
from ray import Ray
from vec3 import Vec3

class Sphere(Hittable): # Rappresenta una sfera come oggetto colpibile da un raggio
    def __init__(self, center: Vec3, radius: float, material):
        self.center = center
        self.radius = radius
        self.material = material

    # Funzione che determina se un raggio colpisce la sfera
    def hit(self, ray: Ray, t_min: float, t_max: float, rec: HitRecord) -> bool:

        # Le variabili fanno riferimento all'equazione di una sfera
        # Sono state effettuate delle semplificazioni
        #Originariamente avevamo:

        #a = dot(ray.direction(), ray.direction()), ovvero direzione del raggio al quadrato d^2
        #b = -2.0 * dot(ray.direction(), oc), ovvero -2d*(C-A)
        #c = dot(oc,oc) - radius^2, ovvero (C-A)^2-r^2
        #discriminant = b*b-4*a+*c 

        #Notando che: 
        # 1. b = -2*h con h = dot((ray.direction(), oc))
        # 2. il prodotto scalare di un vettore con se stesso è uguale 
        # al quadrato della sua lunghezza

        # Le soluzioni si trovano come (h+-sqrt(h^2-a*c))/a
        # Quindi:
        # b = -2*d*oc -> -2*h
        # h = -b/2 = d*oc

        oc = ray.origin - self.center
        a = ray.direction.length_squared() # a=d^2, un vettore moltiplicato per se stesso è uguale al quadrato della propria lunghezza
        half_b = oc.dot(ray.direction) # sarebbe h=-b/2=d*oc 
        c = oc.length_squared() - self.radius * self.radius #distanza tra l'origine del raggio e il centro - il raggio al quadrato
        # Calcolo del delta/4 
        discriminant = half_b * half_b - a * c 

        # Se il discriminante è negativo non c'è nessun punto d'intersezione 
        if discriminant < 0: 
            return False
        
        sqrtd = discriminant ** 0.5 # sqrt(discriminante)
        # Trova la radice più vicina nel range valido
        root = (-half_b - sqrtd) / a # Prima soluzione
        if root < t_min or root > t_max: # la prima è scartata se troppo grande o troppo piccola
            root = (-half_b + sqrtd) / a # Seconda soluzione
            if root < t_min or root > t_max: 
                return False # Nessuna soluzione valida nel range

        # Se siamo qui, il raggio ha colpito la sfera in una posizione valida

        # Le informazioni riguardo il punto di hit ed il materiale della sfera sono salvati in rec
        rec.t = root # salva nel record il parametro t dell’intersezione
        rec.p = ray.at(rec.t)  # calcola il punto d’impatto usando la funzione at(t)

        # Calcola la normale in quel punto: vettore dal centro della sfera al punto di impatto,
        # normalizzato dividendo per il raggio
        outward_normal = (rec.p - self.center) / self.radius
        rec.set_face_normal(ray, outward_normal) # Imposta la normale in modo che punti sempre contro il raggio in arrivo
        rec.material = self.material  # Assegna il materiale della sfera al record d'impatto (solo se c'è un colpo valido)
        return True # impatto valido
    
    
