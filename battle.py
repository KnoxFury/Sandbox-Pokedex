TYPE_CHART = {
    "normal":   {"rock":0.5,"ghost":0,"steel":0.5},
    "fire":     {"fire":0.5,"water":0.5,"grass":2,"ice":2,"bug":2,"rock":0.5,"dragon":0.5,"steel":2},
    "water":    {"fire":2,"water":0.5,"grass":0.5,"ground":2,"rock":2,"dragon":0.5},
    "grass":    {"fire":0.5,"water":2,"grass":0.5,"poison":0.5,"ground":2,"flying":0.5,"bug":0.5,"rock":2,"dragon":0.5,"steel":0.5},
    "electric": {"water":2,"electric":0.5,"grass":0.5,"ground":0,"flying":2,"dragon":0.5},
    "ice":      {"fire":0.5,"water":0.5,"grass":2,"ice":0.5,"ground":2,"flying":2,"dragon":2,"steel":0.5},
    "fighting": {"normal":2,"ice":2,"poison":0.5,"flying":0.5,"psychic":0.5,"bug":0.5,"rock":2,"ghost":0,"dark":2,"steel":2,"fairy":0.5},
    "poison":   {"grass":2,"poison":0.5,"ground":0.5,"rock":0.5,"ghost":0.5,"steel":0,"fairy":2},
    "ground":   {"fire":2,"electric":2,"grass":0.5,"poison":2,"flying":0,"bug":0.5,"rock":2,"steel":2},
    "flying":   {"electric":0.5,"grass":2,"fighting":2,"bug":2,"rock":0.5,"steel":0.5},
    "psychic":  {"fighting":2,"poison":2,"psychic":0.5,"dark":0,"steel":0.5},
    "bug":      {"fire":0.5,"grass":2,"poison":0.5,"fighting":0.5,"flying":0.5,"psychic":2,"ghost":0.5,"dark":2,"steel":0.5,"fairy":0.5},
    "rock":     {"fire":2,"ice":2,"fighting":0.5,"ground":0.5,"flying":2,"bug":2,"steel":0.5},
    "ghost":    {"normal":0,"psychic":2,"ghost":2,"dark":0.5},
    "dragon":   {"dragon":2,"steel":0.5,"fairy":0},
    "dark":     {"fighting":0.5,"psychic":2,"ghost":2,"dark":0.5,"fairy":0.5},
    "steel":    {"fire":0.5,"water":0.5,"electric":0.5,"ice":2,"rock":2,"steel":0.5,"fairy":2},
    "fairy":    {"fire":0.5,"fighting":2,"poison":0.5,"dragon":2,"dark":2,"steel":0.5},
}

def get_multiplier(atk_types, def_types):
    best = 1.0
    for at in atk_types:
        m = 1.0
        chart = TYPE_CHART.get(at, {})
        for dt in def_types:
            m *= chart.get(dt, 1.0)
        best = max(best, m)
    return best

def eff_label(m):
    return ("Super effective!" if m >= 2 else "Not very effective..." if m < 1 else "")

def simulate_battle(p1, p2):
    def types(p): return [t for t in [str(p.get("type1","")), str(p.get("type2",""))] if t and t != "nan"]

    hp1, hp2 = int(p1["hp"]), int(p2["hp"])
    n1, n2 = p1["name"], p2["name"]
    log = [f"⚔️  {n1}  vs  {n2}\n{'─'*36}"]

    first, second = (p1, p2) if int(p1["speed"]) >= int(p2["speed"]) else (p2, p1)
    hp = {n1: hp1, n2: hp2}

    turn = 1
    while hp[n1] > 0 and hp[n2] > 0:
        log.append(f"\n🔄 Turn {turn}")
        for atk, dfn in [(first, second), (second, first)]:
            if hp[atk["name"]] <= 0 or hp[dfn["name"]] <= 0:
                break
            m = get_multiplier(types(atk), types(dfn))
            phys_ratio = int(atk["attack"])    / int(dfn["defense"])
            spec_ratio = int(atk["sp_attack"]) / int(dfn["sp_defense"])
            dmg = max(1, int(int(dfn["hp"]) * max(phys_ratio, spec_ratio) * m * 0.07))
            hp[dfn["name"]] -= dmg
            label = eff_label(m)
            remaining = max(0, hp[dfn["name"]])
            line = f"  {atk['name']} → {dfn['name']}: {dmg} dmg (×{m}){(' '+label) if label else ''} | {dfn['name']} HP: {remaining}"
            log.append(line)
        turn += 1
        if turn > 50: log.append("  ⏱️ Draw — too many turns!"); break

    winner = n1 if hp[n1] > 0 else n2
    if hp[n1] <= 0 and hp[n2] <= 0: winner = "Draw"
    log.append(f"\n{'─'*36}\n🏆 Winner: {winner}")
    return "\n".join(log)
