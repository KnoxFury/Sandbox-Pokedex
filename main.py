import tkinter as tk
from tkinter import messagebox
import pandas as pd, numpy as np
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from battle import simulate_battle

df = pd.read_csv("All_Pokemon.csv")
STATS = ["HP", "Att", "Def", "Spa", "Spd", "Spe"]
TYPE_COLORS = {
    "fire":"#FF6434", "water":"#6890F0", "grass":"#78C850", "electric":"#F8D030",
    "ice":"#98D8D8", "fighting":"#C03028", "poison":"#A040A0", "ground":"#E0C068",
    "flying":"#A890F0", "psychic":"#F85888", "bug":"#A8B820", "rock":"#B8A038",
    "ghost":"#705898", "dragon":"#7038F8", "dark":"#705848", "steel":"#B8B8D0",
    "fairy":"#EE99AC", "normal":"#A8A878",
}

def find(query):
    q = query.strip().lower()
    if q.isdigit():
        row = df[df["Number"] == int(q)]
    else:
        row = df[df["Name"].str.lower() == q]
    
    if not row.empty:
        return row.iloc[0]
    else:
        return None

# ── App ──────────────────────────────────────────────────────────────────────
root = tk.Tk()
root.title("Pokedex")
pokemon = [None, None]

# ── Search bars ──────────────────────────────────────────────────────────────
e1 = tk.Entry(root, width=20)
e1.grid(row=0, column=0, padx=4, pady=4)
e2 = tk.Entry(root, width=20)
# revealed by Compare button

# ── Stat display (two text columns) ──────────────────────────────────────────
stat_frame = tk.Frame(root)
stat_frame.grid(row=2, column=0, columnspan=3, pady=4)
labels = [[], []]

def show_stats(idx, p):
    for w in labels[idx]:
        w.destroy()
    labels[idx].clear()
    col = idx * 2
    name_lbl = tk.Label(stat_frame, text=f"#{int(p["Number"]):03d} {p['Name']}", font=("", 10, "bold"))
    name_lbl.grid(row=0, column=col, columnspan=2, pady=(4, 2))
    labels[idx].append(name_lbl)

    # Type badges — only colored elements in the app
    badge_frame = tk.Frame(stat_frame)
    badge_frame.grid(row=1, column=col, columnspan=2)
    labels[idx].append(badge_frame)
    for t in [p.get("Type 1"), p.get("Type 2")]:
        if t and str(t) != "nan":
            c = TYPE_COLORS.get(str(t).lower(), "#888")
            tk.Label(badge_frame, text=str(t).upper(), bg=c, fg="white", padx=6).pack(side="left", padx=2)

    # Plain stat list
    for r, s in enumerate(STATS, start=2):
        stat_label = s.replace("Att", "Attack").replace("Def", "Defense").replace("Spa", "Sp.Atk").replace("Spd", "Sp.Def").replace("Spe", "Speed")
        lbl = tk.Label(stat_frame, text=f"{stat_label}: {int(p[s])}", anchor="w")
        lbl.grid(row=r, column=col, columnspan=2, sticky="w", padx=8)
        labels[idx].append(lbl)
    total = tk.Label(stat_frame, text=f"Total: {sum(int(p[s]) for s in STATS)}", font=("", 9, "bold"))
    total.grid(row=len(STATS)+2, column=col, columnspan=2, pady=(2, 6))
    labels[idx].append(total)

def search(idx, entry):
    p = find(entry.get())
    if p is None:
        messagebox.showwarning("Not found", f"'{entry.get()}' not found.")
        return
    pokemon[idx] = p
    show_stats(idx, p)
    if pokemon[0] is not None:
        draw_radar()

tk.Button(root, text="Search", command=lambda: search(0, e1)).grid(row=0, column=1, padx=4)

def show_compare():
    e2.grid(row=1, column=0, padx=4, pady=2)
    tk.Button(root, text="Search", command=lambda: search(1, e2)).grid(row=1, column=1, padx=4)
    compare_btn.grid_forget()

compare_btn = tk.Button(root, text="Compare", command=show_compare)
compare_btn.grid(row=0, column=2, padx=4)

# ── Radar chart ──────────────────────────────────────────────────────────────
chart_frame = tk.Frame(root)
chart_frame.grid(row=3, column=0, columnspan=3)

def draw_radar():
    for w in chart_frame.winfo_children():
        w.destroy()
    fig, ax = plt.subplots(figsize=(3.5, 3.5), subplot_kw=dict(polar=True))
    angles = np.linspace(0, 2*np.pi, len(STATS), endpoint=False).tolist() + [0]
    ax.set_thetagrids(np.degrees(angles[:-1]), [s.replace("Att", "Attack").replace("Def", "Defense").replace("Spa", "Sp.Atk").replace("Spd", "Sp.Def").replace("Spe", "Speed") for s in STATS], fontsize=7)
    for p, color in zip(pokemon, ["red", "blue"]):
        if p is None:
            continue
        vals = [int(p[s]) for s in STATS] + [int(p[STATS[0]])]
        ax.plot(angles, vals, color=color, linewidth=1.5, label=p["Name"])
        ax.fill(angles, vals, color=color, alpha=0.1)
    ax.legend(fontsize=7, loc="upper right", bbox_to_anchor=(1.3, 1.1))
    plt.tight_layout()
    canvas = FigureCanvasTkAgg(fig, chart_frame)
    canvas.draw()
    canvas.get_tk_widget().pack()
    plt.close(fig)

# ── Battle log ───────────────────────────────────────────────────────────────
def run_battle():
    if any(p is None for p in pokemon):
        messagebox.showwarning("Missing", "Search both Pokemon first.")
        return
    log = simulate_battle(pokemon[0].to_dict(), pokemon[1].to_dict())
    log_box.config(state="normal")
    log_box.delete("1.0", "end")
    log_box.insert("end", log)
    log_box.config(state="disabled")

tk.Button(root, text="Simulate Battle", command=run_battle).grid(row=4, column=0, columnspan=3, pady=4)
log_box = tk.Text(root, height=20, width=35, state="disabled")
log_box.grid(row=0, column=3, rowspan=6, padx=8, pady=4, sticky="nsew")

root.update_idletasks()
width = root.winfo_reqwidth() + 80
height = root.winfo_reqheight() + 520
root.geometry(f"{width}x{height}")
root.mainloop()