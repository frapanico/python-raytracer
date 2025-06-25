from hittable import Hittable
from hitrecord import HitRecord
from ray import Ray


#E' una lista di oggetti, permette l'aggiunta di un oggetto e verificare se un raggio ha colpito uno degli oggetti nella lista
class HittableList(Hittable):
    def __init__(self):
        self.objects = []

    def add(self, obj: Hittable):
        self.objects.append(obj)

    #Viene definito un intervallo in cui la hit è considerata valida (t_min, t_max)
    def hit(self, ray: Ray, t_min: float, t_max: float, rec: HitRecord) -> bool:
        temp_rec = HitRecord()
        hit_anything = False
        #tiene traccia dell'oggetto colpito più vicino
        closest_so_far = t_max

        #La lista objects viene esplorata, quando si trova l'oggetto più vicino colpito dal ray, vengono salvate le
        #caratteristiche salienti in "rec"
        for obj in self.objects:
            if obj.hit(ray, t_min, closest_so_far, temp_rec):
                hit_anything = True
                closest_so_far = temp_rec.t
                rec.p = temp_rec.p
                rec.normal = temp_rec.normal
                rec.t = temp_rec.t
                rec.material = temp_rec.material
        
        #Si ritorna TRUE o FALSE in base all'esito della hit
        return hit_anything

