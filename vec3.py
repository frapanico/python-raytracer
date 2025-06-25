import math
import random  #Usata per eventuali funzioni matematiche e generazione di numeri random

class Vec3:
    #Costruttore: inizializza il vettore con coordinate x, y, z
    def __init__(self, x: float, y: float, z: float):
        self.x = x
        self.y = y
        self.z = z

    # Conversione in stringa (per la stampa del vettore se serve)
    def __str__(self):
        return f"{self.x} {self.y} {self.z}"

    # Di seguito abbiamo l'overloading degli operatori

    # Somma vettoriale: permette l'uso di v1 + v2
    def __add__(self, other):
        return Vec3(self.x + other.x, self.y + other.y, self.z + other.z)

    # Sottrazione vettoriale: v1 - v2
    def __sub__(self, other):
        return Vec3(self.x - other.x, self.y - other.y, self.z - other.z)

    # Moltiplicazione: se l'altro è un vettore, componente per componente
    # altrimenti effettua il prodotto scalare su ogni componente
    def __mul__(self, t):
        if isinstance(t, Vec3):
            return Vec3(self.x * t.x, self.y * t.y, self.z * t.z)
        return Vec3(self.x * t, self.y * t, self.z * t)

    # Permette la moltiplicazione con uno scalare quando lo scalare è a sinistra dell'operatore (aggiunta per comodità)
    def __rmul__(self, t):
        return self * t

    # Divisione per uno scalare
    def __truediv__(self, t):
        return self * (1 / t)

    # Prodotto scalare tra due vettori
    def dot(self, other):
        return self.x * other.x + self.y * other.y + self.z * other.z

    # Prodotto vettoriale tra due vettori
    def cross(self, other):
        return Vec3(
            self.y * other.z - self.z * other.y,
            self.z * other.x - self.x * other.z,
            self.x * other.y - self.y * other.x,
        )

    # Lunghezza (ovvero il modulo) del vettore
    def length(self):
        return math.sqrt(self.length_squared())

    # Quadrato della lunghezza (utile per ottimizzare calcoli, 
    # perchè evita di fare la radice della lunghezza quando non serve)
    def length_squared(self):
        return self.x ** 2 + self.y ** 2 + self.z ** 2

    # Ritorna un vettore unitario con la stessa direzione
    def unit_vector(self):
        return self / self.length()
    
    # Verifica se il vettore è praticamente nullo 
    def near_zero(self):
        s = 1e-8
        return abs(self.x) < s and abs(self.y) < s and abs(self.z) < s
    
    # Inversione del segno di tutte le componenti (difatti effettua -v)
    def __neg__(self):
        return Vec3(-self.x, -self.y, -self.z)

    # Riflessione di un vettore rispetto a una normale (usata nei materiali metallici)
    @staticmethod
    def reflect(v: 'Vec3', n: 'Vec3') -> 'Vec3': # i parametri passati sono il vettore incidente e la normale alla superficie 
        return v - 2 * v.dot(n) * n # formula standard per la riflessione speculare
    
    # Genera un vettore casuale sulla superficie di una sfera unitaria (un punto sulla sfera)
    @staticmethod
    def random_unit_vector():
        a = random.uniform(0, 2 * math.pi)  # angolo a casuale tra 0 e 2 pigreco (in orizzontale)
        z = random.uniform(-1, 1)          # quota z casuale tra -1 e +1 (0 equatore, 1 polo N, -1 polo S)
        r = math.sqrt(1 - z*z)             # raggio 
        return Vec3(r * math.cos(a), r * math.sin(a), z) # coordinate 

    # Genera un vettore casuale dentro una sfera unitaria
    @staticmethod
    def random_in_unit_sphere():
        while True:
            p = Vec3.random(-1, 1) # punto casuale in un cubo con ogni dimensione tra -1 e 1
            if p.length_squared() >= 1: # verifica la distanza del punto dal centro della sfera (se >= 1 non va bene)
                continue  # è fuori (o sul confine) dalla sfera, scarta e ripeti
            return p

    # Genera un vettore con componenti casuali nell'intervallo [min_val, max_val]
    @staticmethod
    def random(min_val=0.0, max_val=1.0):
        return Vec3(
            random.uniform(min_val, max_val),
            random.uniform(min_val, max_val),
            random.uniform(min_val, max_val),
        )
