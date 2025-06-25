import sys              
import random           # Per generare numeri casuali (usato principalmente er l'antialiasing)
import math             
from vec3 import Vec3   
from ray import Ray     
from sphere import Sphere               
from hittable_list import HittableList  
from material import Lambertian, Metal  
from hitrecord import HitRecord         

# Funzione per limitare un valore tra due estremi (evita colori fuori scala)
def clamp(x, minval, maxval):
    return max(minval, min(x, maxval))

# Scrive un colore in formato PPM con correzione gamma e media sui campioni
def write_color(pixel_color: Vec3, samples_per_pixel: int) -> str:

    # Normalizzazione del colore
    scale = 1.0 / samples_per_pixel                        

    #Applica una correzione gamma ai componenti del colore
    # Il math.sqrt() (radice quadrata) è usato come "gamma 2" 
    # (esponente 1/gamma, dove gamma è 2) 
    # per trasformare il colore dallo spazio lineare allo spazio gamma 
    # (si fa tipicamente per i monitor moderni)

    r = math.sqrt(pixel_color.x * scale)                   # Media per il componente rosso
    g = math.sqrt(pixel_color.y * scale)                   # Media per il componente verde
    b = math.sqrt(pixel_color.z * scale)                   # Media per il componente blu
    # Conversione in intero 0-255
    ir = int(256 * clamp(r, 0.0, 0.999))                   
    ig = int(256 * clamp(g, 0.0, 0.999))
    ib = int(256 * clamp(b, 0.0, 0.999))
    return f"{ir} {ig} {ib}\n"                             # Formattazione per il file PPM

# Algoritmo : calcolo del colore che un raggio "vede" nella scena, usando ricorsione

def ray_color(ray: Ray, world: HittableList, depth: int) -> Vec3:
    rec = HitRecord()                                      # Record per memorizzare l'intersezione

    if depth <= 0:                                         # Criterio di stop ricorsione
        return Vec3(0, 0, 0)                               # Nessun contributo luminoso

    if world.hit(ray, 0.001, float('inf'), rec):           # Se il raggio colpisce un oggetto (evita shadow acne con 0.001)
        scatter_result = rec.material.scatter(ray, rec)    # Comportamento del materiale (riflessione o diffusione)
        if scatter_result:                                 # Se viene generato un nuovo raggio
            success, scattered, attenuation = scatter_result
            if success:
                return attenuation * ray_color(scattered, world, depth - 1)  # Ricorsione con profondità ridotta
        return Vec3(0, 0, 0)                               # Se nessuno scatter: colore nero
    # Se il raggio non colpisce nulla: restituisce un gradiente (sfondo)

    # Metodo per fare un colore sfumato per lo sfondo
    unit_direction = ray.direction.unit_vector()           # Direzione normalizzata
    t = 0.5 * (unit_direction.y + 1.0)                     # Converte componente y del vettore normalizzato da [-1,1] a [0,1]
    return (1.0 - t) * Vec3(1.0, 1.0, 1.0) + t * Vec3(0.5, 0.7, 1.0)  # Bianco in alto, azzurro in basso

# Converte una stringa "r g b" in un oggetto colore Vec3, per prendere gli argomenti
def parse_color(color_str: str) -> Vec3:
    parts = color_str.split()
    if len(parts) != 3:
        raise ValueError("Il formato del colore deve essere 'R G B', con 3 valori")
    return Vec3(float(parts[0]), float(parts[1]), float(parts[2]))

# Ritorna l'oggetto materiale corretto in base al tipo e ai parametri
def get_material(material_type: str, color: Vec3, fuzz: float):
    if material_type == "Metal":
        return Metal(color, fuzz)
    return Lambertian(color)

# Funzione principale del ray tracer
def main():
    # Verifica il numero di argomenti (passati dalla GUI)
    if len(sys.argv) != 14:
        print("Uso: python main.py x y z num_spheres material1 color1 fuzz1 material2 color2 fuzz2 material3 color3 fuzz3")
        print(" - color_i deve essere nel formato \"r g b\" (valori da 0.0 a 1.0)")
        print(" - fuzz_i deve essere un valore tra 0.0 e 1.0")
        return

    # Estrazione dei parametri della fotocamera e delle sfere
    x, y, z = map(float, sys.argv[1:4]) # primi tre argomenti (float)
    num_spheres = int(sys.argv[4]) # quarto = numero di sfere
    material1 = sys.argv[5] 
    color1 = parse_color(sys.argv[6])
    fuzz1 = float(sys.argv[7])
    material2 = sys.argv[8]
    color2 = parse_color(sys.argv[9])
    fuzz2 = float(sys.argv[10])
    material3 = sys.argv[11]
    color3 = parse_color(sys.argv[12])
    fuzz3 = float(sys.argv[13])

    # Parametri immagine
    aspect_ratio = 16.0 / 9.0
    image_width = 1280
    image_height = int(image_width / aspect_ratio)
    samples_per_pixel = 100        # Campioni per pixel (antialiasing)
    # Profondità massima ricorsiva: quando un raggio colpisce
    # un oggetto, ne viene generato un altro (se il materiale lo consente)
    # max_depth limita il numero di volte che questo processo può ripetersi
    max_depth = 5                 

    # Costruzione camera e viewport
    origin = Vec3(0, 0, 0) # origine della camera (da dove vengono "sparati" i raggi)
    viewport_height = 2.0 # altezza viewport
    viewport_width = aspect_ratio * viewport_height # larghezza viewport
    focal_length = 1.0 # distanza tra origine della camera e piano del viewport
    horizontal = Vec3(viewport_width, 0, 0) 
    vertical = Vec3(0, viewport_height, 0)
    # Coordinate del vertice in basso a sinistra del viewport
    lower_left_corner = origin - horizontal / 2 - vertical / 2 - Vec3(0, 0, focal_length)

    # Costruzione del mondo
    world = HittableList() # Creiamo la lista di oggetti colpibili
    material_ground = Lambertian(Vec3(0.8, 0.8, 0.0)) # Creazione materiale
    world.add(Sphere(Vec3(0, -100.5, -1), 100, material_ground))  # Ground fatto con piano come grande sfera 

    # Posizioni predefinite per le sfere nella scena
    sphere_positions = [Vec3(0, 0, -1), Vec3(-1, 0, -1), Vec3(1, 0, -1)]

    # Inserisce le sfere nella scena in base al numero specificato
    for i in range(num_spheres):
        if i == 0:
            mat = get_material(material1, color1, fuzz1)
            pos = sphere_positions[0]
        elif i == 1:
            mat = get_material(material2, color2, fuzz2)
            pos = sphere_positions[1]
        elif i == 2:
            mat = get_material(material3, color3, fuzz3)
            pos = sphere_positions[2]
        world.add(Sphere(pos, 0.5, mat))  # Aggiunge la sfera al mondo

    # Rendering: apre il file e scrive l'immagine in formato PPM (Portable Pixmap)
    with open("image2.ppm", "w") as f: # apre image2 in scrittura (w)

        f.write(f"P3\n{image_width} {image_height}\n255\n")  # Header PPM con:
        # P3 = formato Plain PPM 
        # dimensioni
        # valore massimo per componenti di colore

        # Cicla su ogni pixel dell'immagine (riga per riga)
        for j in range(image_height - 1, -1, -1): # ciclo sulle righe
            print(f"Scanlines remaining: {j}", end='\r')  # Mostra progresso

            for i in range(image_width): # ciclo sulle colonne
                pixel_color = Vec3(0, 0, 0)  # Inizializza colore del pixel

                # Antialiasing: genera samples_per_pixel raggi per pixel con offset casuali
                for s in range(samples_per_pixel):

                    # Genera le coordinate u e v leggermente casuali all'interno del pixel 
                    # (sono delle frazioni del viewport in realtà, normalizzate)
                    u = (i + random.random()) / (image_width - 1)
                    v = (j + random.random()) / (image_height - 1)

                    # Ad esempio, se i indica 100, i + random.random() potrebbe indicare 100.34, 100.87, ecc. 
                    # Questo significa che il raggio non viene sparato esattamente al centro del pixel 100
                    # ma in un punto casuale all'interno dell'area di quel pixel.

                    direction = lower_left_corner + u * horizontal + v * vertical - origin # Indica la linea tra il punto del pixel e la camera
                    ray = Ray(origin, direction)  # Crea raggio per questo pixel
                    pixel_color += ray_color(ray, world, max_depth)  # Somma contributo di ogni raggio al pixel_color

                f.write(write_color(pixel_color, samples_per_pixel))  # Scrive colore nel file

    print("\nDone.")  # Stampa quando il rendering è finito

# Avvio del programma se eseguito come script principale
if __name__ == "__main__":
    main()
