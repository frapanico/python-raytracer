import random
from abc import ABC, abstractmethod
from vec3 import Vec3
from ray import Ray
from hitrecord import HitRecord

class Material(ABC):
    @abstractmethod
    def scatter(self, ray_in: Ray, rec: HitRecord):
        pass

class Lambertian(Material):
    def __init__(self, albedo: Vec3):
        # parametro di attenuazione, colore intrinseco del materiale
        self.albedo = albedo

    def scatter(self, ray_in: Ray, rec: HitRecord): # gli si passa il raggio di luce che colpisce l'oggetto e l'hit record

        # Non viene implementato un Lambertiano come nella definizione matematica
        # è possibile avere un comportamento analogo generando un vettore 
        # vicino alla normale del punto di incidenza
        scatter_direction = rec.normal + Vec3.random_unit_vector()

        # Se il raggio riflesso è vicino lo zero allora viene restituita la normale 
        # succede ad esempio se il vettore randomico è generato nel senso opposto
        if scatter_direction.near_zero():
            scatter_direction = rec.normal

        # Generazione del raggio riflesso con origine il punto di incidenza e direzione quella calcolata precedentemente
        scattered = Ray(rec.p, scatter_direction)
        attenuation = self.albedo 
        return True, scattered, attenuation

class Metal(Material):
    def __init__(self, albedo: Vec3, fuzz: float):
        self.albedo = albedo
        self.fuzz = min(fuzz, 1) # parametro tra 0 e 1 per la "lucidità" della riflessione
        # 0 = specchio perfetto
        # 1 = una sorta di metallo satinato

    def scatter(self, ray_in: Ray, rec: HitRecord):
        # Generazione del raggio riflesso con il parametro fuzz per randomizzare la direzione di riflessione
        reflected = Vec3.reflect(ray_in.direction.unit_vector(), rec.normal) # R = V − 2⋅(V⋅N)⋅N
        # Aggiunto vettore casuale alla direzione di riflessione scalato con fuzz
        scattered = Ray(rec.p, reflected + self.fuzz * Vec3.random_in_unit_sphere()) 
        attenuation = self.albedo
        # ritorna true solo il raggio è sopra la superficie, perché può essere è assorbito (per effetto di fuzz)
        return (scattered.direction.dot(rec.normal) > 0), scattered, attenuation
