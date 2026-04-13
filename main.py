import customtkinter as ctk
from tkinter import messagebox
import pandas as pd, numpy as np
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from battle import simulate_battle

ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")

df = pd.read_csv("All_Pokemon.csv")

def find(pokemon):
    q = pokemon.strip().lower()
    if q.isdigit():
        row = df[df["Number"] == int(q)]
    else:
        row = df[df["Name"].str.lower() == q]
    
    if not row.empty:
        return row.iloc[0]
    else:
        return None

root = ctk.CTk()
root.title("Pokedex")
pokemon = [None, None]

e1 = ctk.CTkEntry(root, width=150, corner_radius=10, border_width=2, font=("Roboto", 12))
e1.grid(row=0, column=0, padx=10, pady=10)
e2 = ctk.CTkEntry(root, width=150, corner_radius=10, border_width=2, font=("Roboto", 12))
e2.grid(row=1, column=0, padx=10, pady=10)

stat_frame = ctk.CTkFrame(root, fg_color="transparent")
stat_frame.grid(row=2, column=0, columnspan=3, pady=10)
labels = [[], []]

Stats = ["HP", "Atk", "Def", "Sp.Atk", "Sp.Def", "Spd"]
def show_Stats(i, p):
    for w in labels[i]:
        w.destroy()
    labels[i].clear()
    if i==1: 
        col = 2
    else :
        col = 0
    name_lbl = ctk.CTkLabel(stat_frame, text=f"#{int(p['Number']):03d} {p['Name']}", font=("Roboto", 16, "bold"))
    name_lbl.grid(row=0, column=col, columnspan=2, pady=(4, 6))
    labels[i].append(name_lbl)

    badge_frame = ctk.CTkFrame(stat_frame, fg_color="transparent")
    badge_frame.grid(row=1, column=col, columnspan=2, pady=(0, 10))
    labels[i].append(badge_frame)
    for t in [p.get("Type 1"), p.get("Type 2")]:
        if t and str(t) != "nan":
            match str(t).lower():
                case "fire": c = "#FF6434"
                case "water": c = "#6890F0"
                case "grass": c = "#78C850"
                case "electric": c = "#F8D030"
                case "ice": c = "#98D8D8"
                case "fighting": c = "#C03028"
                case "poison": c = "#A040A0"
                case "ground": c = "#E0C068"
                case "flying": c = "#A890F0"
                case "psychic": c = "#F85888"
                case "bug": c = "#A8B820"
                case "rock": c = "#B8A038"
                case "ghost": c = "#705898"
                case "dragon": c = "#7038F8"
                case "dark": c = "#705848"
                case "steel": c = "#B8B8D0"
                case "fairy": c = "#EE99AC"
                case "normal": c = "#A8A878"
                case _: c = "#888"
            lbl = ctk.CTkLabel(badge_frame,text=str(t).upper(),fg_color=c,corner_radius=6,padx=8,pady=2,font=("Roboto", 11, "bold"))
            lbl.pack(side="left", padx=4)


    for r, s in enumerate(Stats, start=2):
        lbl = ctk.CTkLabel(stat_frame, text=f" {s}: {int(p[s])}", anchor="w", font=("Roboto", 13))
        lbl.grid(row=r, column=col, columnspan=2, sticky="w", padx=15, pady=2)
        labels[i].append(lbl)
    total = ctk.CTkLabel(stat_frame, text=f"Total: {sum(int(p[s]) for s in Stats)}", font=("Roboto", 13, "bold"), text_color="#1F6AA5")
    total.grid(row=len(Stats)+2, column=col, columnspan=2, pady=(6, 10))
    labels[i].append(total)

def search(idx, entry):
    p = find(entry.get())
    if p is None:
        messagebox.showwarning("Not found", f"'{entry.get()}' not found.")
        return
    pokemon[idx] = p
    show_Stats(idx, p)
    draw_radar()

ctk.CTkButton(root, text="Search", command=lambda: search(0, e1), corner_radius=8, font=("Roboto", 12, "bold"), border_width=0, width=80).grid(row=0, column=1, padx=5)
ctk.CTkButton(root, text="Search", command=lambda: search(1, e2), corner_radius=8, font=("Roboto", 12, "bold"), border_width=0, width=80).grid(row=1, column=1, padx=5)

# ── Radar chart ──────────────────────────────────────────────────────────────
chart_frame = ctk.CTkFrame(root, fg_color="transparent")
chart_frame.grid(row=3, column=0, columnspan=3, pady=(10, 0))

def draw_radar():
    for w in chart_frame.winfo_children():
        w.destroy()
    plt.style.use('dark_background')
    fig, ax = plt.subplots(figsize=(3.5, 3.5), subplot_kw=dict(polar=True))
    fig.patch.set_facecolor('#242424')
    ax.set_facecolor('#242424')
    angles = np.linspace(0, 2*np.pi, len(Stats), endpoint=False).tolist() + [0]
    ax.set_thetagrids(np.degrees(angles[:-1]), [s.replace("Att", "Attack").replace("Def", "Defense").replace("Spa", "Sp.Atk").replace("Spd", "Sp.Def").replace("Spe", "Speed") for s in Stats], fontsize=8)
    for p, color in zip(pokemon, ["red", "blue"]):
        if p is None:
            continue
        vals = [int(p[s]) for s in Stats] + [int(p[Stats[0]])]
        ax.plot(angles, vals, color=color, linewidth=2, label=p["Name"])
        ax.fill(angles, vals, color=color, alpha=0.15)
    ax.legend(fontsize=8, loc="upper right", bbox_to_anchor=(1.35, 1.15))
    plt.tight_layout()
    canvas = FigureCanvasTkAgg(fig, chart_frame)
    canvas.draw()
    canvas.get_tk_widget().pack()
    plt.close(fig)

# ── Battle log ───────────────────────────────────────────────────────────────
def run_battle():
    if pokemon[0] or pokemon[1] == None:
        messagebox.showwarning("Missing", "Search both Pokemon first.")
        return
    log = simulate_battle(pokemon[0].to_dict(), pokemon[1].to_dict())
    log_box.configure(state="normal")
    log_box.delete("1.0", "end")
    log_box.insert("end", log)
    log_box.configure(state="disabled")

ctk.CTkButton(root, text="Simulate Battle", command=run_battle, corner_radius=10, font=("Roboto", 14, "bold"), height=40, fg_color="#b22222").grid(row=4, column=0, columnspan=3, pady=15)
log_box = ctk.CTkTextbox(root, height=450, width=320, state="disabled", corner_radius=12, border_width=2, font=("Consolas", 12))
log_box.grid(row=0, column=3, rowspan=6, padx=15, pady=15, sticky="nsew")

root.update_idletasks()
width = root.winfo_reqwidth() + 100
height = root.winfo_reqheight() + 275
root.geometry(f"{width}x{height}")
root.mainloop()