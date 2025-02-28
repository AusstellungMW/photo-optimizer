import os
import tkinter as tk
from tkinter import filedialog, messagebox
from PIL import Image


# Funktion zur Verarbeitung des Bildes
def process_image():
    # Datei-Dialog öffnen
    input_path = filedialog.askopenfilename(filetypes=[("Bilder", "*.jpg;*.jpeg;*.png;*.webp")])

    if not input_path:
        return  # Falls keine Datei ausgewählt wurde, nichts tun

    # Zielpfad für das komprimierte Bild
    directory, filename = os.path.split(input_path)
    output_path = os.path.join(directory, f"{os.path.splitext(filename)[0]}_komprimiert.jpg")

    # Bild öffnen
    image = Image.open(input_path)

    # Seitenverhältnisse berechnen
    original_ratio = image.width / image.height
    target_ratio = 1920 / 1080

    # Neue Größe berechnen, ohne das Seitenverhältnis zu verzerren
    if original_ratio > target_ratio:
        new_width = 1920
        new_height = round(1920 / original_ratio)
    else:
        new_height = 1080
        new_width = round(1080 * original_ratio)

    # Bild proportional skalieren
    image_resized = image.resize((new_width, new_height), Image.LANCZOS)

    # Neuen 1920x1080 Hintergrund mit schwarzer Farbe erstellen
    canvas = Image.new("RGB", (1920, 1080), (0, 0, 0))  # (0,0,0) = Schwarz, (255,255,255) = Weiß

    # Bild in die Mitte des Hintergrunds einfügen
    x_offset = (1920 - new_width) // 2
    y_offset = (1080 - new_height) // 2
    canvas.paste(image_resized, (x_offset, y_offset))

    # Bild auf max. 300 KB komprimieren
    quality = 95
    while quality > 10:
        canvas.save(output_path, "JPEG", quality=quality)
        if os.path.getsize(output_path) <= 300 * 1024:
            break
        quality -= 5

    # Nachricht anzeigen
    messagebox.showinfo("Fertig!", f"Das Bild wurde optimiert und gespeichert:\n{output_path}")


# Hauptfenster erstellen
root = tk.Tk()
root.title("Foto Optimierer")
root.geometry("400x200")

# Button zum Auswählen und Verarbeiten des Bildes
btn = tk.Button(root, text="Bild auswählen", command=process_image, font=("Arial", 14))
btn.pack(pady=50)

# Programm starten
root.mainloop()













































