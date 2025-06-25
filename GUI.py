import tkinter as tk # Importa il modulo tkinter per creare interfacce grafiche
import subprocess # Importa il modulo subprocess per eseguire comandi esterni
import sys # Importa il modulo sys per accedere a parametri specifici del sistema, come l'eseguibile Python
import threading # Importa il modulo threading per eseguire operazioni in un thread separato
import platform # Importa il modulo platform per ottenere informazioni sul sistema operativo
import os # Importa il modulo os per interagire con il sistema operativo, come l'apertura di file

def esegui_script():

    # Recupero parametri fissi della camera
    x, y, z = 0, 0, 0  # Imposta le coordinate fisse della telecamera a (0, 0, 0)

    # Recupero parametro numero di sfere
    num_spheres = selected_spheres.get() # Ottiene il numero di sfere selezionato dal menu

    # Recupero per Sfera 1
    material_1 = selected_material_1.get() # Ottiene il materiale selezionato per la Sfera 1
    color_1 = f"{slider_r1.get()} {slider_g1.get()} {slider_b1.get()}" # Ottiene i valori RGB per il colore della Sfera 1
    fuzz_1 = slider_fuzz1.get() if material_1 == "Metal" else 0.0 # Ottiene il valore di fuzz per la Sfera 1, solo se il materiale è "Metal"

    # Recupero per Sfera 2
    material_2 = selected_material_2.get() # Ottiene il materiale selezionato per la Sfera 2
    color_2 = f"{slider_r2.get()} {slider_g2.get()} {slider_b2.get()}" # Ottiene i valori RGB per il colore della Sfera 2
    fuzz_2 = slider_fuzz2.get() if material_2 == "Metal" else 0.0 # Ottiene il valore di fuzz per la Sfera 2, solo se il materiale è "Metal"

    # Recupero per Sfera 3
    material_3 = selected_material_3.get() # Ottiene il materiale selezionato per la Sfera 3
    color_3 = f"{slider_r3.get()} {slider_b3.get()} {slider_b3.get()}" # Ottiene i valori RGB per il colore della Sfera 3
    fuzz_3 = slider_fuzz3.get() if material_3 == "Metal" else 0.0 # Ottiene il valore di fuzz per la Sfera 3, solo se il materiale è "Metal"

    cmd = [sys.executable, "main.py", str(x), str(y), str(z), str(num_spheres),
           material_1, color_1, str(fuzz_1),
           material_2, color_2, str(fuzz_2),
           material_3, color_3, str(fuzz_3)] # Costruisco la lista di argomenti da passare a main.py

    button.config(state=tk.DISABLED) # Disabilito il bottone per evitare esecuzioni multiple

    def run_process():
        subprocess.run(cmd) # Esegue lo script main.py con gli argomenti specificati
        sistema = platform.system() # Ottiene il nome del sistema operativo
        if sistema == "Darwin": # Se il sistema è macOS
            subprocess.run(["open", "image2.ppm"]) # Apre il file image2.ppm 
        elif sistema == "Windows": # Se il sistema è Windows
            subprocess.run(["magick", "image2.ppm", "output.png"]) # Converte image2.ppm in output.png usando ImageMagick
            os.startfile("output.png") # Apre il file output.png 
        else: # Per altri sistemi operativi (come Linux)
            subprocess.run(["xdg-open", "image2.ppm"]) # Apre il file image2.ppm 
        button.config(state=tk.NORMAL) # Riabilito il tasto di avvio al termine dell'esecuzione

    threading.Thread(target=run_process, daemon=True).start() # Avvia la funzione run_process in un nuovo thread

# Funzione per mostrare e nascondere fuzz
def aggiorna_fuzz(material_var, label_fuzz, slider_fuzz):
    # Funzione per aggiornare la visibilità di fuzz in base al materiale selezionato 
    def callback(*args):
        if material_var.get() == "Metal": # Se il materiale selezionato è il metal
            label_fuzz.grid() # Rende visibile la label fuzz
            slider_fuzz.grid() # Rende visibile lo slider fuzz
        else: # Se il materiale selezionato non è metal
            label_fuzz.grid_remove() # Nasconde la label fuzz
            slider_fuzz.grid_remove() # Nasconde lo slider fuzz
    material_var.trace_add("write", callback) # Associa la callback al cambiamento della variabile material_var
    callback() # Chiama la callback una volta all'inizio per impostare lo stato iniziale

# Interfaccia utente
root = tk.Tk() # Crea la finestra principale di Tkinter
root.title("Interfaccia per main.py") 
root.geometry("435x750") 
root.resizable(False, False) # Per non ridimensionarla

# Creo un'area rettangolare all'interno della finestra principale 
container = tk.Frame(root) # Crea un frame contenitore all'interno della finestra principale
container.pack(fill="both", expand=True) # Impacchetta il frame per riempire lo spazio disponibile

canvas = tk.Canvas(container) # Crea un widget Canvas all'interno del contenitore
scrollbar = tk.Scrollbar(container, orient="vertical", command=canvas.yview) # Crea una scrollbar verticale
scrollable_frame = tk.Frame(canvas) # Crea un frame all'interno del Canvas che sarà scrollabile

# Ogni volta che lo scrollable_frame subisce un cambiamento nella sua configurazione 
# (cioè, viene ridimensionato o spostato), aggiorna la regione scorrevole del canvas 
# in modo che includa perfettamente tutto il contenuto presente nel scrollable_frame.
scrollable_frame.bind(
    "<Configure>",
    lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
) 

# Crea una finestra all'interno del canvas per il frame scrollable_frame
canvas.create_window((0, 0), window=scrollable_frame, anchor="nw") 
canvas.configure(yscrollcommand=scrollbar.set) # Colleghiamo la scrollbar al canvas

canvas.pack(side="left", fill="both", expand=True) # Impacchettiamo il canvas a sinistra riempiendo lo spazio
scrollbar.pack(side="right", fill="y") # Impacchettiamo la scrollbar a destra, riempiendo verticalmente

# Frame per la scena
frame_scene = tk.LabelFrame(scrollable_frame, text="Impostazioni Scena", padx=10, pady=10) # Crea un LabelFrame per le impostazioni della scena
frame_scene.pack(fill="x", padx=10, pady=10) # Impacchetta il LabelFrame
tk.Label(frame_scene, text="Numero di sfere:").grid(row=0, column=0, padx=5, pady=5, sticky="e") # Aggiunge una label per il numero di sfere
selected_spheres = tk.StringVar(value="1") # Crea una variabile di controllo per il numero di sfere, con valore iniziale "1"
option_num = tk.OptionMenu(frame_scene, selected_spheres, "1", "2", "3") # Crea un OptionMenu per selezionare il numero di sfere
option_num.grid(row=0, column=1, padx=5, pady=5, sticky="w") # Posizione del menu

# Frame per le sfere
frame_spheres = tk.LabelFrame(scrollable_frame, text="Impostazioni Sfere", padx=10, pady=10) #Impostazioni sfere
frame_spheres.pack(fill="both", expand=True, padx=10, pady=10) 

materials = ["Lambertian", "Metal"] # Definisco i materiali disponibili

def create_sphere_controls(parent, sphere_number):
    # Funzione per creare i controlli (materiale, colore e fuzz) per una singola sfera
    f = tk.LabelFrame(parent, text=f"Sfera {sphere_number}", padx=10, pady=10) 
    f.pack(fill="x", padx=5, pady=5) #

    # Materiale
    tk.Label(f, text="Materiale:").grid(row=0, column=0, padx=5, pady=5, sticky="e") 
    material_var = tk.StringVar(value=materials[0]) # Crea una variabile di controllo per il materiale con valore di default "Lambertian"
    material_menu = tk.OptionMenu(f, material_var, *materials) # Crea un menu per selezionare il materiale
    material_menu.grid(row=0, column=1, padx=5, pady=5, sticky="w") 

    # Sliders colore
    tk.Label(f, text="Colore R (0.0-1.0):").grid(row=1, column=0, padx=5, pady=5, sticky="e") # Aggiunge label per il colore R
    slider_r = tk.Scale(f, from_=0, to=1, resolution=0.1, orient=tk.HORIZONTAL, length=200) # Crea uno slider per il componente R del colore
    slider_r.grid(row=1, column=1, padx=5, pady=5, sticky="w") # Posiziona lo slider

    tk.Label(f, text="Colore G (0.0-1.0):").grid(row=2, column=0, padx=5, pady=5, sticky="e") # Aggiunge label per il colore G
    slider_g = tk.Scale(f, from_=0, to=1, resolution=0.1, orient=tk.HORIZONTAL, length=200) # Crea uno slider per il componente G del colore
    slider_g.grid(row=2, column=1, padx=5, pady=5, sticky="w") # Posiziona lo slider

    tk.Label(f, text="Colore B (0.0-1.0):").grid(row=3, column=0, padx=5, pady=5, sticky="e") # Aggiunge label per il colore B
    slider_b = tk.Scale(f, from_=0, to=1, resolution=0.1, orient=tk.HORIZONTAL, length=200) # Crea uno slider per il componente B del colore
    slider_b.grid(row=3, column=1, padx=5, pady=5, sticky="w") # Posiziona lo slider

    # Label e slider fuzz (che saranno nascosti se Lambertian)
    label_fuzz = tk.Label(f, text="Fuzz (0.0-1.0):") 
    label_fuzz.grid(row=4, column=0, padx=5, pady=5, sticky="e") 

    slider_fuzz = tk.Scale(f, from_=0, to=1, resolution=0.1, orient=tk.HORIZONTAL, length=200) # Slider per il fuzz
    slider_fuzz.grid(row=4, column=1, padx=5, pady=5, sticky="w") 

    # Chiama la funzione per gestire la visibilità del fuzz
    aggiorna_fuzz(material_var, label_fuzz, slider_fuzz) 

    return material_var, slider_r, slider_g, slider_b, slider_fuzz # Restituisce le variabili di controllo create

selected_material_1, slider_r1, slider_g1, slider_b1, slider_fuzz1 = create_sphere_controls(frame_spheres, 1) # Crea i controlli per la Sfera 1
selected_material_2, slider_r2, slider_g2, slider_b2, slider_fuzz2 = create_sphere_controls(frame_spheres, 2) # Crea i controlli per la Sfera 2
selected_material_3, slider_r3, slider_g3, slider_b3, slider_fuzz3 = create_sphere_controls(frame_spheres, 3) # Crea i controlli per la Sfera 3

# Bottone per eseguire
frame_button = tk.Frame(scrollable_frame, padx=10, pady=10) # Crea un frame per il bottone
frame_button.pack(pady=10) # Impacchetta il frame
button = tk.Button(frame_button, text="Esegui main.py", command=esegui_script, width=30, height=2) # Crea il bottone per eseguire lo script
button.pack() # Impacchetta il bottone

root.mainloop() # Avvia il ciclo principale degli eventi di Tkinter (che mantiene la finestra aperta)