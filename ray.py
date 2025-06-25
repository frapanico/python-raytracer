from vec3 import Vec3  # Importa la classe Vec3, la quale gestisce vettori in 3 dimensioni.

class Ray:
    def __init__(self, origin: Vec3, direction: Vec3):
        
        #Costruttore della classe Ray.
        
        #Parametri:
        #  origin (Vec3): Il punto di origine del raggio.
        #  direction (Vec3): La direzione del raggio.
        
        self.origin = origin       # Assegna il punto di partenza del raggio.
        self.direction = direction # Assegna la direzione in cui il raggio si muove.

    def at(self, t: float) -> Vec3:
        
        #Calcola il punto lungo il raggio a una distanza parametrica t.
        
        #Formula:
        #  punto = origine + t * direzione
          
        #Dove:
        #  - origine: il punto da cui parte il raggio.
        #  - direzione: vettore che indica la direzione del raggio.
        #  - t: parametro scalare che "cammina" lungo la direzione.
          
        #Restituisce:
        #  Un'istanza di Vec3 che rappresenta il punto raggiunto a t.
        
        return self.origin + t * self.direction
