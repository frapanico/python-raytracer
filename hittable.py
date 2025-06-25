from abc import ABC, abstractmethod
from ray import Ray
from hitrecord import HitRecord

#E' una classe astratta ereditata da qualunque oggetto
class Hittable(ABC):
    @abstractmethod
    def hit(self, ray: Ray, t_min: float, t_max: float, rec: HitRecord) -> bool:
        pass
