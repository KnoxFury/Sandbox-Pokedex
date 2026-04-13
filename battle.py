import random

def get_multiplier(atk_types, defender):
    best = 1.0
    for atk_type in atk_types:
        col_name = f"Against {atk_type}"
        multiplier = defender.get(col_name, 1.0)
        best = max(best, multiplier)
    return best

def eff_label(m):
    if m >= 2:
        return "Super effective!"
    elif m < 1:
        return "Not very effective..."
    else:
        return ""

def simulate_battle(p1, p2):
    def types(p):
        result = []
        for t in [str(p.get("Type 1","")), str(p.get("Type 2",""))]:
            if t and t != "nan":
                result.append(t)
        return result

    hp1, hp2 = int(p1["HP"]), int(p2["HP"])
    n1, n2 = p1["Name"], p2["Name"]
    log = [f"{n1} vs {n2}\n{'─'*35}"]

    if int(p1["Spd"]) >= int(p2["Spd"]):
        first, second = p1, p2
    else:
        first, second = p2, p1
    hp = {n1: hp1, n2: hp2}

    turn = 1
    while hp[n1] > 0 and hp[n2] > 0:
        log.append(f"Turn {turn}")
        for atk, dfn in [(first, second), (second, first)]:
            if hp[atk["Name"]] <= 0 or hp[dfn["Name"]] <= 0:
                break
            m = get_multiplier(types(atk), dfn)
            phys_ratio = int(atk["Atk"]) / int(dfn["Def"])
            spec_ratio = int(atk["Sp.Atk"]) / int(dfn["Sp.Def"])
            dmg = max(1, int(int(dfn["HP"]) * max(phys_ratio, spec_ratio) * m * 0.07) + random.randint(-3, 3))
            hp[dfn["Name"]] -= dmg
            label = eff_label(m)
            remaining = max(0, hp[dfn["Name"]])
            if label:
                extra = ' ' + label
            else:
                extra = ''
            line = f"  {atk['Name']} => {dfn['Name']}:\n {dmg} dmg (×{m}){extra}\n {dfn['Name']} HP: {remaining}\n"
            log.append(line)
        turn += 1
        if turn > 50:
            log.append("Draw — too many turns!")
            break

    if hp[n1] > 0:
        winner = n1
    else:
        winner = n2
    
    if hp[n1] <= 0 and hp[n2] <= 0:
        winner = "Draw"
    log.append(f"\n{'─'*35}\nWinner: {winner}")
    return "\n".join(log)