import tkinter as tk
from tkinter import messagebox
from itertools import combinations
import matplotlib.pyplot as plt

# Funkcja sprawdzająca poprawność wprowadzonych współrzędnych 
def is_valid_segment(values):
    try:
        return all(val.strip() != "" for val in values) and len(values) == 4
    except:
        return False

# Iloczyn wektorowy 2D
def cross(a, b):
    return a[0]*b[1] - a[1]*b[0]

# Sprawdzanie przecięcia dwóch odcinków z uwzględnieniem przypadków brzegowych
def sprawdz_przeciecie(A, B, C, D):
    def subtract(p, q):
        return (p[0] - q[0], p[1] - q[1])
    
    def on_segment(p, q, r):
        return min(p[0], r[0]) <= q[0] <= max(p[0], r[0]) and \
               min(p[1], r[1]) <= q[1] <= max(p[1], r[1])

    AB = subtract(B, A)
    CD = subtract(D, C)
    AC = subtract(C, A)
    AD = subtract(D, A)
    CA = subtract(A, C)
    CB = subtract(B, C)

    d1 = cross(AB, AC)
    d2 = cross(AB, AD)
    d3 = cross(CD, CA)
    d4 = cross(CD, CB)

    if d1 * d2 < 0 and d3 * d4 < 0:
        denom = AB[0]*CD[1] - AB[1]*CD[0]
        if denom == 0:
            return "Przecięcie: punkt (ale niewyznaczalny - równoległe?)"
        t = ((C[0] - A[0]) * (D[1] - C[1]) - (C[1] - A[1]) * (D[0] - C[0])) / denom
        px = A[0] + t * AB[0]
        py = A[1] + t * AB[1]
        return f"Punkt przecięcia: ({round(px, 2)}, {round(py, 2)})"

    if d1 == 0 and on_segment(A, C, B):
        return f"Punkt przecięcia (brzegowy): {C}"
    if d2 == 0 and on_segment(A, D, B):
        return f"Punkt przecięcia (brzegowy): {D}"
    if d3 == 0 and on_segment(C, A, D):
        return f"Punkt przecięcia (brzegowy): {A}"
    if d4 == 0 and on_segment(C, B, D):
        return f"Punkt przecięcia (brzegowy): {B}"

    if d1 == d2 == d3 == d4 == 0:
        punkty = sorted([A, B, C, D])
        max_start = max(min(A, B), min(C, D))
        min_end = min(max(A, B), max(C, D))
        if max_start <= min_end:
            if max_start == min_end:
                return f"Punkt przecięcia (brzegowy): {max_start}"
            else:
                return f"Odcinek wspólny: {max_start} do {min_end}"
        else:
            return "Brak przecięcia (współliniowe, ale rozłączne)"

    return "Brak przecięcia"

# Rysowanie odcinków i punktów przecięcia
def rysuj_odcinki(odcinki, przeciecia):
    plt.figure(figsize=(6, 6))
    plt.title("Rysunek odcinków i punktów przecięcia")
    plt.axhline(0, color='black', lw=0.5)
    plt.axvline(0, color='black', lw=0.5)

    for idx, ((x1, y1), (x2, y2)) in enumerate(odcinki):
        plt.plot([x1, x2], [y1, y2], label=f"Odcinek {idx+1}")

    for p in przeciecia:
        if isinstance(p, tuple) and len(p) == 2:
            plt.plot(p[0], p[1], 'ro')

    plt.xlabel("X")
    plt.ylabel("Y")
    plt.grid(True)
    plt.legend()
    plt.axis('equal')
    plt.show()

# Analiza przecięć między odcinkami
def analiza():
    odcinki = []
    try:
        for pola in pola_odcinkow:
            dane = [entry.get() for entry in pola]
            if is_valid_segment(dane):
                odcinki.append(((float(dane[0]), float(dane[1])), (float(dane[2]), float(dane[3]))))
    except ValueError:
        messagebox.showerror("Błąd", "Wprowadź poprawne liczby (x, y).")
        return

    if len(odcinki) < 2:
        messagebox.showwarning("Uwaga", "Podaj pełne współrzędne co najmniej dwóch odcinków.")
        return

    wyniki = []
    przeciecia_do_rysowania = []

    for (i1, s1), (i2, s2) in combinations(enumerate(odcinki), 2):
        A, B = s1
        C, D = s2
        wynik = sprawdz_przeciecie(A, B, C, D)
        wyniki.append(f"Odcinek {i1+1} i {i2+1}:\n{wynik}\n")

        if "Punkt przecięcia" in wynik:
            wsp = wynik.split(":")[1].strip().strip("()").split(",")
            przeciecia_do_rysowania.append((float(wsp[0]), float(wsp[1])))

    messagebox.showinfo("Wyniki przecięć", "\n".join(wyniki))
    rysuj_odcinki(odcinki, przeciecia_do_rysowania)

# Czyszczenie pól formularza
def wyczysc_pola():
    for pola in pola_odcinkow:
        for entry in pola:
            entry.delete(0, tk.END)

# GUI
root = tk.Tk()
root.title("Przecięcia odcinków")

pola_odcinkow = []
for i in range(4):
    tk.Label(root, text=f"Odcinek {i+1} (x1, y1, x2, y2):").grid(row=i, column=0, padx=5, pady=2)
    pola = []
    for j in range(4):
        entry = tk.Entry(root, width=5)
        entry.grid(row=i, column=j+1)
        pola.append(entry)
    pola_odcinkow.append(pola)

tk.Button(root, text="Analizuj", command=analiza).grid(row=5, column=0, columnspan=2, pady=10)
tk.Button(root, text="Wyczyść", command=wyczysc_pola).grid(row=5, column=2, columnspan=2, pady=10)

root.mainloop()
