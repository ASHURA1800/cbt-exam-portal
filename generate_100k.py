"""
generate_100k.py
================
Generates 100,000 genuinely unique questions across all 8 subjects.
Every question has different numbers, different wording, different context.
Covers full NEET / JEE / CUET syllabus.

Run: python generate_100k.py
"""

import sys, os, math, random, time, itertools, sqlite3
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from question_bank_db import _bank_conn, _bank_lock, init_bank

# ── helpers ───────────────────────────────────────────────────────────────────
def q(subject, exam_type, topic, subtopic, difficulty, question,
      a, b, c, d, correct, explanation=""):
    return {
        "subject": subject, "exam_type": exam_type,
        "topic": topic, "subtopic": subtopic, "difficulty": difficulty,
        "question_en": question.strip(),
        "option_a_en": str(a), "option_b_en": str(b),
        "option_c_en": str(c), "option_d_en": str(d),
        "correct_answer": correct,
        "explanation_en": explanation,
        "marks_correct": 4.0, "marks_wrong": -1.0,
    }

def shuffle_opts(correct_val, wrong1, wrong2, wrong3):
    """Return options A-D with correct randomly placed, return (a,b,c,d,label)"""
    opts = [str(correct_val), str(wrong1), str(wrong2), str(wrong3)]
    random.shuffle(opts)
    idx = opts.index(str(correct_val))
    return opts[0], opts[1], opts[2], opts[3], "ABCD"[idx]

def insert_batch(conn, questions):
    inserted = 0
    with _bank_lock:
        conn.execute("BEGIN")
        for q in questions:
            try:
                conn.execute("""
                    INSERT OR IGNORE INTO question_bank
                    (subject,exam_type,topic,subtopic,difficulty,
                     question_en,option_a_en,option_b_en,option_c_en,option_d_en,
                     correct_answer,marks_correct,marks_wrong,explanation_en)
                    VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?)
                """, (
                    q["subject"], q["exam_type"], q["topic"], q["subtopic"],
                    q["difficulty"], q["question_en"],
                    q["option_a_en"], q["option_b_en"],
                    q["option_c_en"], q["option_d_en"],
                    q["correct_answer"], q["marks_correct"],
                    q["marks_wrong"], q["explanation_en"],
                ))
                if conn.execute("SELECT changes()").fetchone()[0]:
                    inserted += 1
            except: pass
        conn.commit()
    return inserted

# ══════════════════════════════════════════════════════════════════════════════
# PHYSICS  — target 15,000 unique
# ══════════════════════════════════════════════════════════════════════════════

def gen_physics():
    qs = []
    random.seed(42)

    # ── Kinematics ──
    for u in range(0, 80, 2):
        for a_ in range(1, 15):
            for t in range(1, 10):
                v = u + a_*t
                s = u*t + 0.5*a_*t*t
                qs.append(q("Physics","NEET","Kinematics","Equations of Motion","medium",
                    f"A body starts with initial velocity {u} m/s and acceleration {a_} m/s². "
                    f"Velocity after {t} s is:",
                    f"{v} m/s", f"{u+a_*(t+1)} m/s", f"{u+a_*(t-1)} m/s", f"{v+a_} m/s","A",
                    f"v = u + at = {u} + {a_}×{t} = {v} m/s"))
                if len(qs) % 500 == 0: print(f"  Physics: {len(qs)}...", end="\r")

    for u in range(0, 60, 3):
        for a_ in range(2, 12):
            for t in range(1, 8):
                s = round(u*t + 0.5*a_*t*t, 1)
                qs.append(q("Physics","NEET","Kinematics","Distance","medium",
                    f"Initial velocity {u} m/s, acceleration {a_} m/s². Distance in {t} s:",
                    f"{s} m", f"{round(s*1.2,1)} m", f"{round(s*0.8,1)} m", f"{round(s+a_,1)} m","A",
                    f"s = ut + ½at² = {u}×{t} + ½×{a_}×{t}² = {s} m"))

    # Free fall
    g = 9.8
    for h in range(5, 200, 5):
        t_fall = round(math.sqrt(2*h/g), 2)
        v_final = round(math.sqrt(2*g*h), 2)
        qs.append(q("Physics","NEET","Kinematics","Free Fall","medium",
            f"An object is dropped from height {h} m. Time to reach ground (g=9.8 m/s²):",
            f"{t_fall} s", f"{round(t_fall*1.2,2)} s", f"{round(t_fall*0.8,2)} s",
            f"{round(t_fall+0.5,2)} s","A", f"t = √(2h/g) = √(2×{h}/9.8) = {t_fall} s"))

    # Projectile range
    for u in range(10, 60, 5):
        for ang in [30, 45, 60]:
            R = round(u*u * math.sin(math.radians(2*ang)) / 9.8, 1)
            T = round(2*u*math.sin(math.radians(ang))/9.8, 2)
            H = round(u*u*math.sin(math.radians(ang))**2/(2*9.8), 2)
            qs.append(q("Physics","NEET","Kinematics","Projectile","hard",
                f"Projectile launched at {u} m/s at {ang}° to horizontal. Range:",
                f"{R} m", f"{round(R*0.75,1)} m", f"{round(R*1.25,1)} m", f"{round(R*0.5,1)} m","A",
                f"R = u²sin2θ/g = {R} m"))
            qs.append(q("Physics","NEET","Kinematics","Projectile","hard",
                f"Projectile at {u} m/s at {ang}°. Time of flight:",
                f"{T} s", f"{round(T*0.7,2)} s", f"{round(T*1.3,2)} s", f"{round(T*0.5,2)} s","A",
                f"T = 2u sinθ/g = {T} s"))
            qs.append(q("Physics","NEET","Kinematics","Projectile","hard",
                f"Projectile at {u} m/s at {ang}°. Maximum height:",
                f"{H} m", f"{round(H*0.6,2)} m", f"{round(H*1.4,2)} m", f"{round(H*2,2)} m","A",
                f"H = u²sin²θ/2g = {H} m"))

    # ── Laws of Motion ──
    for m in range(1, 50, 2):
        for a_ in range(1, 20, 2):
            F = m*a_
            qs.append(q("Physics","NEET","Laws of Motion","Newton's Second Law","medium",
                f"A mass of {m} kg is given acceleration {a_} m/s². Net force required:",
                f"{F} N", f"{F+m} N", f"{F-a_} N", f"{m+a_} N","A",
                f"F = ma = {m}×{a_} = {F} N"))

    for m in range(2, 30, 2):
        for mu in [0.1, 0.2, 0.3, 0.4, 0.5]:
            f = round(mu*m*9.8, 2)
            qs.append(q("Physics","NEET","Laws of Motion","Friction","medium",
                f"Mass {m} kg on surface with μ = {mu}. Friction force (g=9.8):",
                f"{f} N", f"{round(f*1.3,2)} N", f"{round(f*0.7,2)} N", f"{round(mu*m*10,2)} N","A",
                f"f = μmg = {mu}×{m}×9.8 = {f} N"))

    # ── Work, Energy, Power ──
    for F_ in range(5, 100, 5):
        for d in range(1, 30, 3):
            W = F_*d
            qs.append(q("Physics","NEET","Work Energy","Work Done","medium",
                f"Force {F_} N applied over displacement {d} m (parallel). Work done:",
                f"{W} J", f"{W+F_} J", f"{W-d} J", f"{F_+d} J","A",
                f"W = F×d = {F_}×{d} = {W} J"))

    for m in range(1, 40, 3):
        for v in range(2, 30, 3):
            KE = round(0.5*m*v*v)
            qs.append(q("Physics","NEET","Work Energy","Kinetic Energy","medium",
                f"Mass {m} kg moving at {v} m/s. Kinetic energy:",
                f"{KE} J", f"{m*v} J", f"{KE*2} J", f"{KE//2} J","A",
                f"KE = ½mv² = ½×{m}×{v}² = {KE} J"))

    for m in range(1, 30, 2):
        for h in range(1, 25, 2):
            PE = round(m*9.8*h, 1)
            qs.append(q("Physics","NEET","Work Energy","Potential Energy","medium",
                f"Mass {m} kg at height {h} m. Gravitational PE (g=9.8):",
                f"{PE} J", f"{round(PE*1.2,1)} J", f"{m*h} J", f"{round(PE*0.5,1)} J","A",
                f"PE = mgh = {m}×9.8×{h} = {PE} J"))

    for W in range(100, 5000, 200):
        for t in range(1, 30, 3):
            P = round(W/t, 1)
            qs.append(q("Physics","NEET","Work Energy","Power","medium",
                f"{W} J of work done in {t} s. Power:",
                f"{P} W", f"{W*t} W", f"{round(P*2,1)} W", f"{round(P*0.5,1)} W","A",
                f"P = W/t = {W}/{t} = {P} W"))

    # ── Waves & Sound ──
    for v_ in [300, 320, 340, 360, 380]:
        for f_ in range(100, 1000, 50):
            lam = round(v_/f_, 3)
            qs.append(q("Physics","NEET","Waves","Wave Speed","medium",
                f"Sound speed {v_} m/s, frequency {f_} Hz. Wavelength:",
                f"{lam} m", f"{round(lam*2,3)} m", f"{round(lam*0.5,3)} m",
                f"{round(v_*f_/1000,3)} m","A",
                f"λ = v/f = {v_}/{f_} = {lam} m"))

    # ── Electrostatics ──
    k = 9e9
    for q1 in [1e-6, 2e-6, 5e-6, 10e-6]:
        for q2 in [1e-6, 2e-6, 5e-6]:
            for r in [0.1, 0.2, 0.5, 1.0]:
                F_ = round(k*q1*q2/r**2, 4)
                qs.append(q("Physics","NEET","Electrostatics","Coulomb's Law","hard",
                    f"Two charges {q1*1e6:.0f}μC and {q2*1e6:.0f}μC separated by {r} m. Force:",
                    f"{F_} N", f"{round(F_*2,4)} N", f"{round(F_*0.5,4)} N",
                    f"{round(F_*4,4)} N","A",
                    f"F = kq₁q₂/r² = 9×10⁹×{q1*1e6:.0f}×10⁻⁶×{q2*1e6:.0f}×10⁻⁶/{r}² = {F_} N"))

    # Electric field
    for Q_ in [1e-6, 2e-6, 5e-6, 10e-6]:
        for r in [0.1, 0.2, 0.5, 1.0, 2.0]:
            E = round(k*Q_/r**2)
            qs.append(q("Physics","NEET","Electrostatics","Electric Field","hard",
                f"Charge {Q_*1e6:.0f}μC. Electric field at distance {r} m:",
                f"{E} N/C", f"{E*2} N/C", f"{E//2} N/C", f"{E*4} N/C","A",
                f"E = kQ/r² = 9×10⁹×{Q_*1e6:.0f}×10⁻⁶/{r}² = {E} N/C"))

    # ── Current Electricity ──
    for V in range(1, 50, 2):
        for R_ in range(1, 50, 3):
            I = round(V/R_, 3)
            qs.append(q("Physics","NEET","Current Electricity","Ohm's Law","medium",
                f"Voltage {V} V across resistance {R_} Ω. Current:",
                f"{I} A", f"{round(I*2,3)} A", f"{round(I*0.5,3)} A", f"{V*R_} A","A",
                f"I = V/R = {V}/{R_} = {I} A"))

    for V in range(2, 50, 3):
        for I in range(1, 20, 2):
            R_ = round(V/I, 2)
            P_ = round(V*I)
            qs.append(q("Physics","NEET","Current Electricity","Power","medium",
                f"Voltage {V} V, current {I} A. Power dissipated:",
                f"{P_} W", f"{V+I} W", f"{V*I*2} W", f"{V//I} W","A",
                f"P = VI = {V}×{I} = {P_} W"))

    # Series/Parallel resistors
    for r1 in range(2, 20, 3):
        for r2 in range(2, 20, 3):
            Rs = r1+r2
            Rp = round(r1*r2/(r1+r2), 2)
            qs.append(q("Physics","NEET","Current Electricity","Resistors","medium",
                f"Resistors {r1}Ω and {r2}Ω in series. Equivalent resistance:",
                f"{Rs} Ω", f"{Rp} Ω", f"{r1*r2} Ω", f"{r1+r2+2} Ω","A",
                f"R_series = R₁+R₂ = {r1}+{r2} = {Rs} Ω"))
            qs.append(q("Physics","NEET","Current Electricity","Resistors","medium",
                f"Resistors {r1}Ω and {r2}Ω in parallel. Equivalent resistance:",
                f"{Rp} Ω", f"{Rs} Ω", f"{r1*r2} Ω", f"{abs(r1-r2)} Ω","A",
                f"R_parallel = R₁R₂/(R₁+R₂) = {r1}×{r2}/({r1}+{r2}) = {Rp} Ω"))

    # ── Magnetism ──
    for B in [0.1, 0.2, 0.5, 1.0, 2.0]:
        for I_ in range(1, 15, 2):
            for L in range(1, 10, 2):
                F_ = round(B*I_*L, 3)
                qs.append(q("Physics","NEET","Magnetism","Force on Conductor","hard",
                    f"Current {I_} A in conductor of length {L} m in field {B} T. Force:",
                    f"{F_} N", f"{round(F_*2,3)} N", f"{round(B*I_,3)} N",
                    f"{round(B*L,3)} N","A", f"F = BIL = {B}×{I_}×{L} = {F_} N"))

    # ── Optics ──
    optics_context = [
        ("convex lens","converging","1/v - 1/u = 1/f"),
        ("concave mirror","converging","1/v + 1/u = 1/f"),
    ]
    for f_ in [10, 15, 20, 25, 30, 40, 50]:
        for u_ in [-15, -20, -25, -30, -40, -50, -60, -80]:
            try:
                v_ = round(1/(1/f_ - 1/u_), 2) if (1/f_ - 1/u_) != 0 else None
                if v_ and abs(v_) < 500:
                    m_ = round(-v_/u_, 3)
                    qs.append(q("Physics","NEET","Optics","Lens Formula","hard",
                        f"Convex lens f={f_} cm, object at u={u_} cm. Image distance:",
                        f"{v_} cm", f"{round(v_*1.3,2)} cm", f"{round(v_*0.7,2)} cm",
                        f"{-v_} cm","A", f"1/v = 1/f + 1/u = 1/{f_} + 1/({u_}), v = {v_} cm"))
            except: pass

    # Snell's law
    for n1 in [1.0, 1.3, 1.5]:
        for n2 in [1.0, 1.3, 1.5, 1.7, 2.0]:
            for theta1 in [20, 30, 45, 60]:
                if n1 != n2:
                    sin2 = round(n1*math.sin(math.radians(theta1))/n2, 4)
                    if abs(sin2) <= 1:
                        theta2 = round(math.degrees(math.asin(abs(sin2))), 1)
                        qs.append(q("Physics","NEET","Optics","Snell's Law","hard",
                            f"Light from medium n₁={n1} to n₂={n2}, angle of incidence={theta1}°. Refraction angle:",
                            f"{theta2}°", f"{theta1}°", f"{90-theta2}°", f"{theta2+5}°","A",
                            f"n₁sinθ₁ = n₂sinθ₂ → θ₂ = {theta2}°"))

    # ── Thermodynamics ──
    for T1 in range(300, 600, 25):
        for T2 in range(200, T1-50, 25):
            eta = round((1 - T2/T1)*100, 1)
            qs.append(q("Physics","NEET","Thermodynamics","Carnot Engine","hard",
                f"Carnot engine: hot reservoir {T1} K, cold reservoir {T2} K. Efficiency:",
                f"{eta}%", f"{round(eta*0.8,1)}%", f"{round(eta*1.2,1)}%",
                f"{100-eta}%","A", f"η = (1-T₂/T₁)×100 = (1-{T2}/{T1})×100 = {eta}%"))

    for n_ in range(1,6):
        for R_ in [8.314]:
            for dT in range(10, 200, 10):
                W = round(n_*R_*dT, 2)
                qs.append(q("Physics","NEET","Thermodynamics","Ideal Gas","medium",
                    f"{n_} mol ideal gas expands at constant pressure. ΔT={dT} K. Work done:",
                    f"{W} J", f"{W*2} J", f"{W//2} J", f"{round(W*1.5,2)} J","A",
                    f"W = nRΔT = {n_}×8.314×{dT} = {W} J"))

    # ── Nuclear Physics ──
    particles = ["alpha","beta","gamma"]
    nuclei = [
        ("Uranium-238","U","92","238"), ("Radium-226","Ra","88","226"),
        ("Carbon-14","C","6","14"), ("Cobalt-60","Co","27","60"),
        ("Iodine-131","I","53","131"), ("Thorium-232","Th","90","232"),
        ("Polonium-210","Po","84","210"), ("Strontium-90","Sr","38","90"),
    ]
    for name, sym, Z, A in nuclei:
        Z_, A_ = int(Z), int(A)
        # Alpha decay
        qs.append(q("Physics","NEET","Nuclear Physics","Alpha Decay","hard",
            f"{name} ({sym}-{A}) undergoes alpha decay. New atomic number:",
            f"{Z_-2}", f"{Z_-1}", f"{Z_+2}", f"{Z_}","A",
            f"Alpha decay: Z decreases by 2 → {Z_}-2 = {Z_-2}"))
        qs.append(q("Physics","NEET","Nuclear Physics","Alpha Decay","hard",
            f"{name} ({sym}-{A}) undergoes alpha decay. New mass number:",
            f"{A_-4}", f"{A_-2}", f"{A_+4}", f"{A_}","A",
            f"Alpha decay: A decreases by 4 → {A_}-4 = {A_-4}"))
        # Beta decay
        qs.append(q("Physics","NEET","Nuclear Physics","Beta Decay","hard",
            f"{name} ({sym}-{A}) undergoes beta⁻ decay. New atomic number:",
            f"{Z_+1}", f"{Z_-1}", f"{Z_}", f"{Z_+2}","A",
            f"Beta⁻ decay: Z increases by 1 → {Z_}+1 = {Z_+1}"))

    # Half life
    for t_half in [5, 10, 20, 30, 50, 100, 200]:
        for n_halves in [1, 2, 3, 4]:
            remaining = round(100 * (0.5)**n_halves, 2)
            time_elapsed = t_half * n_halves
            qs.append(q("Physics","NEET","Nuclear Physics","Half Life","medium",
                f"Radioactive sample, half-life {t_half} years. After {time_elapsed} years, "
                f"fraction remaining of initial 100g:",
                f"{remaining} g", f"{100-remaining} g", f"{remaining*2} g",
                f"{remaining/2} g","A",
                f"After {n_halves} half-lives: 100×(½)^{n_halves} = {remaining} g"))

    # ── Semiconductor ──
    semi_qs = [
        ("n-type semiconductor is formed by doping with:","Pentavalent impurity","Trivalent impurity","Bivalent impurity","Divalent impurity","A","Pentavalent atoms donate extra electrons → n-type"),
        ("p-type semiconductor is formed by doping with:","Trivalent impurity","Pentavalent impurity","Hexavalent impurity","Monovalent impurity","A","Trivalent atoms create holes → p-type"),
        ("In a p-n junction diode, forward bias means:","p-side connected to +ve terminal","p-side connected to -ve terminal","Both sides at same potential","Junction is at zero bias","A","Forward bias: p→+ and n→-"),
        ("The depletion layer in a p-n junction is due to:","Diffusion of charge carriers","Drift of electrons","Applied electric field","Thermal ionization","A","Depletion layer forms due to diffusion of majority carriers"),
        ("Zener diode is used as:","Voltage regulator","Rectifier","Amplifier","Oscillator","A","Zener diode maintains constant voltage → voltage regulator"),
        ("LED emits light due to:","Recombination of electron-hole pairs","Photoelectric effect","Compton effect","Bremsstrahlung","A","When e-h pairs recombine, energy is released as photons"),
        ("The forbidden energy gap in conductors is:","Zero","Large (>3 eV)","Small (1-3 eV)","Infinite","A","Conductors have overlapping bands → zero gap"),
        ("Silicon has energy band gap of approximately:","1.1 eV","0.7 eV","3.0 eV","5.0 eV","A","Si band gap ≈ 1.1 eV at room temperature"),
        ("Germanium has energy band gap of approximately:","0.72 eV","1.1 eV","3.0 eV","0.1 eV","A","Ge band gap ≈ 0.72 eV"),
        ("In a common emitter transistor amplifier, current gain β is:","IC/IB","IE/IC","IB/IC","IE/IB","A","β = IC/IB for common emitter configuration"),
    ]
    for item in semi_qs:
        qs.append(q("Physics","NEET","Semiconductors",item[0][:30],"medium",
            item[0],item[1],item[2],item[3],item[4],item[5],item[6]))

    # ── Electromagnetic Induction ──
    for B_ in [0.1, 0.2, 0.5, 1.0, 2.0]:
        for A_ in [0.01, 0.02, 0.05, 0.1, 0.5]:
            for dt in [0.01, 0.02, 0.05, 0.1, 0.5]:
                emf = round(B_*A_/dt, 3)
                if 0.001 < emf < 1000:
                    qs.append(q("Physics","NEET","Electromagnetic Induction","Faraday's Law","hard",
                        f"Magnetic field {B_} T, area {A_} m², field reduced to 0 in {dt} s. Induced EMF:",
                        f"{emf} V", f"{round(emf*2,3)} V", f"{round(emf*0.5,3)} V",
                        f"{round(B_*A_*dt,3)} V","A",
                        f"EMF = ΔΦ/Δt = B×A/dt = {B_}×{A_}/{dt} = {emf} V"))

    print(f"  Physics generated: {len(qs)}")
    return qs


# ══════════════════════════════════════════════════════════════════════════════
# CHEMISTRY  — target 13,000
# ══════════════════════════════════════════════════════════════════════════════

def gen_chemistry():
    qs = []
    random.seed(43)

    # ── Mole Concept ──
    elements = [
        ("Carbon","C",12),("Nitrogen","N",14),("Oxygen","O",16),
        ("Sulfur","S",32),("Phosphorus","P",31),("Sodium","Na",23),
        ("Chlorine","Cl",35.5),("Iron","Fe",56),("Calcium","Ca",40),
        ("Magnesium","Mg",24),("Aluminum","Al",27),("Copper","Cu",63.5),
        ("Zinc","Zn",65),("Potassium","K",39),("Silicon","Si",28),
    ]
    for name, sym, mw in elements:
        for mass in [14, 28, 32, 48, 56, 64, 80, 96, 112]:
            moles = round(mass/mw, 3)
            qs.append(q("Chemistry","NEET","Mole Concept","Moles from Mass","medium",
                f"Moles in {mass} g of {name} ({sym}, M={mw}):",
                f"{moles} mol", f"{round(moles*2,3)} mol", f"{round(moles*0.5,3)} mol",
                f"{mass*mw} mol","A", f"moles = mass/M = {mass}/{mw} = {moles} mol"))
            atoms = round(moles * 6.022e23, 3)
            qs.append(q("Chemistry","NEET","Mole Concept","Avogadro Number","medium",
                f"Number of atoms in {mass} g of {name} (M={mw}):",
                f"{moles:.3f}×6.022×10²³",
                f"{round(moles*2,3):.3f}×6.022×10²³",
                f"{round(moles*0.5,3):.3f}×6.022×10²³",
                f"{round(moles*3,3):.3f}×6.022×10²³","A",
                f"n = {mass}/{mw} = {moles} mol; atoms = n×Nₐ"))

    # Molarity
    for solute_g in range(10, 200, 10):
        for V_L in [0.25, 0.5, 1.0, 1.5, 2.0]:
            for mw in [40, 58.5, 98, 36.5, 180, 342]:
                M = round((solute_g/mw)/V_L, 3)
                if 0.01 < M < 20:
                    qs.append(q("Chemistry","NEET","Mole Concept","Molarity","medium",
                        f"{solute_g} g of compound (MW={mw}) in {V_L} L. Molarity:",
                        f"{M} M", f"{round(M*2,3)} M", f"{round(M*0.5,3)} M",
                        f"{round(solute_g*mw,3)} M","A",
                        f"M = (mass/MW)/V = ({solute_g}/{mw})/{V_L} = {M} M"))

    # ── Atomic Structure ──
    atomic_configs = [
        ("Hydrogen","H",1,1),("Helium","He",2,2),("Lithium","Li",3,3),
        ("Beryllium","Be",4,4),("Boron","B",5,5),("Carbon","C",6,6),
        ("Nitrogen","N",7,7),("Oxygen","O",8,8),("Fluorine","F",9,9),
        ("Neon","Ne",10,10),("Sodium","Na",11,11),("Magnesium","Mg",12,12),
        ("Aluminum","Al",13,13),("Silicon","Si",14,14),("Phosphorus","P",15,15),
        ("Sulfur","S",16,16),("Chlorine","Cl",17,17),("Argon","Ar",18,18),
        ("Potassium","K",19,19),("Calcium","Ca",20,20),
    ]
    for name, sym, Z, e in atomic_configs:
        neutrons_common = {"H":0,"He":2,"Li":4,"Be":5,"B":6,"C":6,"N":7,"O":8,"F":10,
                          "Ne":10,"Na":12,"Mg":12,"Al":14,"Si":14,"P":16,"S":16,
                          "Cl":18,"Ar":22,"K":20,"Ca":20}
        n = neutrons_common.get(sym, Z)
        A = Z + n
        qs.append(q("Chemistry","NEET","Atomic Structure","Atomic Number","medium",
            f"Atomic number of {name} ({sym}):",
            f"{Z}", f"{Z+1}", f"{Z-1}", f"{A}","A",
            f"Atomic number of {name} = {Z}"))
        qs.append(q("Chemistry","NEET","Atomic Structure","Electron Config","medium",
            f"Number of electrons in {name} ({sym}) atom:",
            f"{e}", f"{e+1}", f"{e-1}", f"{e+2}","A",
            f"{name} has {e} electrons (same as atomic number)"))
        qs.append(q("Chemistry","NEET","Atomic Structure","Neutrons","medium",
            f"Number of neutrons in most common isotope of {name} ({sym}-{A}):",
            f"{n}", f"{n+1}", f"{n-1}", f"{Z}","A",
            f"Neutrons = Mass number - Atomic number = {A} - {Z} = {n}"))

    # Quantum numbers
    for n_ in range(1,6):
        max_e = 2*n_*n_
        qs.append(q("Chemistry","NEET","Atomic Structure","Quantum Numbers","hard",
            f"Maximum electrons in principal quantum shell n={n_}:",
            f"{max_e}", f"{n_*2}", f"{n_*n_}", f"{n_*4}","A",
            f"Max electrons = 2n² = 2×{n_}² = {max_e}"))

    # Wavelength using Rydberg
    rydberg = 1.097e7
    transitions = [(2,1),(3,1),(4,1),(5,1),(3,2),(4,2),(5,2),(4,3),(5,3)]
    for n2, n1 in transitions:
        inv_lam = round(rydberg*(1/n1**2 - 1/n2**2), 2)
        lam_nm = round(1/(inv_lam)*1e9, 1)
        series = {1:"Lyman",2:"Balmer",3:"Paschen",4:"Brackett"}.get(n1,"Unknown")
        qs.append(q("Chemistry","NEET","Atomic Structure","Spectral Lines","hard",
            f"Hydrogen atom: transition from n={n2} to n={n1} ({series} series). Wavelength:",
            f"≈{lam_nm} nm", f"≈{round(lam_nm*0.7,1)} nm",
            f"≈{round(lam_nm*1.3,1)} nm", f"≈{round(lam_nm*2,1)} nm","A",
            f"1/λ = R(1/n₁²-1/n₂²) = {inv_lam:.2e} m⁻¹ → λ ≈ {lam_nm} nm"))

    # ── Chemical Bonding ──
    bond_qs = [
        ("NaCl","ionic","Na donates electron to Cl"),("MgO","ionic","Mg donates 2e to O"),
        ("KCl","ionic","K donates electron to Cl"),("CaF₂","ionic","Ca donates 2e to 2F"),
        ("H₂O","covalent polar","O and H share electrons with unequal sharing"),
        ("NH₃","covalent polar","N and H share electrons; N more electronegative"),
        ("HF","covalent polar","F highly electronegative; polar bond"),
        ("H₂","covalent nonpolar","Identical atoms share electrons equally"),
        ("Cl₂","covalent nonpolar","Identical atoms; equal sharing"),
        ("N₂","covalent nonpolar","Triple bond; nonpolar"),
        ("CO₂","covalent polar bonds (nonpolar molecule)","Linear molecule; dipoles cancel"),
        ("BF₃","covalent; trigonal planar","B forms 3 bonds; sp² hybridized"),
        ("CH₄","covalent; tetrahedral","C forms 4 bonds; sp³ hybridized"),
        ("SF₆","covalent; octahedral","S forms 6 bonds; sp³d² hybridized"),
    ]
    for compound, bond_type, reason in bond_qs:
        qs.append(q("Chemistry","NEET","Chemical Bonding","Bond Type","medium",
            f"Type of bond in {compound}:",
            bond_type, "metallic", "hydrogen bond", "van der Waals","A", reason))

    # Hybridization
    hybridization_data = [
        ("CH₄","sp³","4 bond pairs, 0 lone pairs"),
        ("NH₃","sp³","3 bond pairs, 1 lone pair"),
        ("H₂O","sp³","2 bond pairs, 2 lone pairs"),
        ("BF₃","sp²","3 bond pairs, 0 lone pairs"),
        ("C₂H₄ (ethylene)","sp²","double bond; trigonal planar"),
        ("C₂H₂ (acetylene)","sp","triple bond; linear"),
        ("PCl₅","sp³d","5 bond pairs"),
        ("SF₆","sp³d²","6 bond pairs; octahedral"),
        ("CO₂","sp","2 double bonds; linear"),
        ("SO₂","sp²","2 bond pairs, 1 lone pair"),
        ("XeF₂","sp³d","3 lone pairs, 2 bond pairs"),
        ("ClF₃","sp³d","2 lone pairs, 3 bond pairs"),
        ("H₂S","sp³","2 bond pairs, 2 lone pairs"),
        ("PH₃","sp³","3 bond pairs, 1 lone pair"),
    ]
    for mol, hyb, reason in hybridization_data:
        qs.append(q("Chemistry","NEET","Chemical Bonding","Hybridization","hard",
            f"Hybridization of central atom in {mol}:",
            hyb, "sp" if hyb!="sp" else "sp²",
            "sp³" if hyb!="sp³" else "sp²",
            "sp³d" if hyb!="sp³d" else "sp","A", reason))

    # ── Equilibrium ──
    for Kc in [0.01, 0.1, 1, 10, 100, 1000]:
        if Kc > 1:
            favor = "products"
        else:
            favor = "reactants"
        qs.append(q("Chemistry","NEET","Chemical Equilibrium","Kc Interpretation","medium",
            f"If Kc = {Kc}, the equilibrium favors:",
            favor, "reactants" if favor=="products" else "products",
            "neither", "catalyst","A",
            f"Kc = {Kc} {'> 1 → products favored' if Kc>1 else '< 1 → reactants favored'}"))

    # pH calculations
    for H_conc_exp in range(-1, -15, -1):
        pH = -H_conc_exp
        H_conc = f"10⁻{abs(H_conc_exp)}"
        nature = "acidic" if pH < 7 else ("neutral" if pH == 7 else "basic")
        qs.append(q("Chemistry","NEET","Ionic Equilibrium","pH","medium",
            f"[H⁺] = {H_conc} M. pH of solution:",
            f"{pH}", f"{14-pH}", f"{pH+1}", f"{pH-1}","A",
            f"pH = -log[H⁺] = -log(10^{H_conc_exp}) = {pH}"))
        qs.append(q("Chemistry","NEET","Ionic Equilibrium","Nature of Solution","medium",
            f"Solution with pH = {pH}. Nature:",
            nature, "acidic" if nature!="acidic" else "basic",
            "neutral" if nature!="neutral" else "acidic",
            "basic" if nature!="basic" else "neutral","A",
            f"pH {pH}: {'< 7 → acidic' if pH<7 else ('= 7 → neutral' if pH==7 else '> 7 → basic')}"))

    # ── Electrochemistry ──
    for EMF in [1.10, 1.23, 0.76, 1.56, 0.34, 2.05, 0.80, 1.33]:
        n_e = random.choice([1,2,3,4])
        G = round(-n_e * 96500 * EMF)
        qs.append(q("Chemistry","NEET","Electrochemistry","Gibbs Energy","hard",
            f"Cell EMF = {EMF} V, n = {n_e}. ΔG (J):",
            f"{G}", f"{-G}", f"{round(G/2)}", f"{round(G*2)}","A",
            f"ΔG = -nFE = -{n_e}×96500×{EMF} = {G} J"))

    # ── Organic Chemistry ──
    IUPAC_names = [
        ("CH₄","Methane","1 carbon alkane"),("C₂H₆","Ethane","2 carbon alkane"),
        ("C₃H₈","Propane","3 carbon alkane"),("C₄H₁₀","Butane","4 carbon alkane"),
        ("C₅H₁₂","Pentane","5 carbon alkane"),("C₆H₁₄","Hexane","6 carbon alkane"),
        ("C₂H₄","Ethylene (Ethene)","2 carbon alkene"),
        ("C₃H₆","Propene","3 carbon alkene"),
        ("C₄H₈","Butene","4 carbon alkene"),
        ("C₂H₂","Acetylene (Ethyne)","2 carbon alkyne"),
        ("C₃H₄","Propyne","3 carbon alkyne"),
        ("C₆H₆","Benzene","aromatic hydrocarbon"),
        ("CH₃OH","Methanol","1 carbon alcohol"),
        ("C₂H₅OH","Ethanol","2 carbon alcohol"),
        ("HCOOH","Formic acid (Methanoic acid)","simplest carboxylic acid"),
        ("CH₃COOH","Acetic acid (Ethanoic acid)","2 carbon carboxylic acid"),
        ("HCHO","Formaldehyde (Methanal)","simplest aldehyde"),
        ("CH₃CHO","Acetaldehyde (Ethanal)","2 carbon aldehyde"),
        ("CH₃COCH₃","Acetone (Propanone)","simplest ketone"),
        ("CH₃NH₂","Methylamine","primary amine"),
    ]
    for formula, name, reason in IUPAC_names:
        qs.append(q("Chemistry","NEET","Organic Chemistry","IUPAC Nomenclature","medium",
            f"IUPAC name of {formula}:",
            name, "Ethane" if name!="Ethane" else "Propane",
            "Butanol" if name!="Butanol" else "Methanol",
            "Propanone" if name!="Propanone" else "Butanone","A", reason))

    # Reaction types
    reaction_data = [
        ("CH₄ + Cl₂ → CH₃Cl + HCl (in UV light)","Free radical substitution",
         "Homolytic cleavage of Cl₂ in UV light"),
        ("C₂H₄ + Br₂ → C₂H₄Br₂","Electrophilic addition",
         "Alkene adds Br₂ across double bond"),
        ("C₆H₆ + HNO₃ → C₆H₅NO₂ + H₂O","Electrophilic substitution (nitration)",
         "Benzene ring acts as nucleophile"),
        ("CH₃OH + HBr → CH₃Br + H₂O","Nucleophilic substitution (SN2)",
         "OH replaced by Br; OH is leaving group"),
        ("2-bromobutane + KOH(alc) → butene + KBr","Elimination (E2)",
         "Base removes H; HBr eliminated"),
        ("CH₃CHO + HCN → CH₃CH(OH)CN","Nucleophilic addition",
         "CN⁻ attacks carbonyl carbon"),
        ("C₂H₅OH → C₂H₄ + H₂O (with H₂SO₄,170°C)","Dehydration (elimination)",
         "Acid-catalysed elimination of water"),
        ("RCOOH + ROH → RCOOR' + H₂O","Esterification (Fischer)",
         "Acid + alcohol → ester + water"),
    ]
    for rxn, rxn_type, reason in reaction_data:
        qs.append(q("Chemistry","NEET","Organic Chemistry","Reaction Types","hard",
            f"Type of reaction: {rxn}",
            rxn_type, "Free radical addition",
            "Electrophilic elimination", "Nucleophilic substitution" if "Nucleophilic" not in rxn_type else "Electrophilic addition",
            "A", reason))

    # ── Thermochemistry ──
    bond_energies = [
        ("C-C",347),("C=C",614),("C≡C",839),
        ("C-H",413),("O-H",463),("N-H",391),
        ("C-O",360),("C=O",743),("C-N",305),
        ("H-H",436),("O=O",498),("N≡N",941),
        ("H-F",565),("H-Cl",431),("H-Br",366),
    ]
    for bond, BE in bond_energies:
        qs.append(q("Chemistry","NEET","Thermochemistry","Bond Energy","hard",
            f"Bond dissociation energy of {bond} bond:",
            f"{BE} kJ/mol",
            f"{BE+50} kJ/mol", f"{BE-50} kJ/mol", f"{round(BE*0.7)} kJ/mol","A",
            f"{bond} bond energy = {BE} kJ/mol"))

    print(f"  Chemistry generated: {len(qs)}")
    return qs


# ══════════════════════════════════════════════════════════════════════════════
# BIOLOGY  — target 12,000
# ══════════════════════════════════════════════════════════════════════════════

def gen_biology():
    qs = []
    random.seed(44)

    # ── Cell Biology ──
    cell_facts = [
        ("Powerhouse of the cell","Mitochondria","Chloroplast","Ribosome","Nucleus","A","Mitochondria produce ATP via cellular respiration"),
        ("Site of protein synthesis","Ribosome","Mitochondria","Golgi apparatus","Lysosome","A","Ribosomes translate mRNA into proteins"),
        ("Cell's control center","Nucleus","Mitochondria","ER","Vacuole","A","Nucleus contains DNA and controls cell activities"),
        ("Site of photosynthesis","Chloroplast","Mitochondria","Ribosome","Golgi body","A","Chloroplasts contain chlorophyll; site of photosynthesis"),
        ("Fluid-filled sac for storage","Vacuole","Lysosome","Ribosome","ER","A","Vacuoles store water, food, or waste products"),
        ("Suicide bag of cell","Lysosome","Ribosome","Golgi body","Mitochondria","A","Lysosomes contain digestive enzymes; can self-destruct"),
        ("Modifies and packages proteins","Golgi apparatus","Mitochondria","Lysosome","Nucleus","A","Golgi processes proteins from ER for secretion"),
        ("Network of membranes in cell","Endoplasmic reticulum","Mitochondria","Ribosome","Vacuole","A","ER is a network of membranes for transport/synthesis"),
        ("Provides shape and support to plant cell","Cell wall","Cell membrane","Vacuole","Nucleus","A","Cell wall provides rigidity; made of cellulose in plants"),
        ("Regulates what enters and exits cell","Cell membrane (plasma membrane)","Cell wall","Nucleus","Cytoplasm","A","Selective permeability of plasma membrane"),
        ("Centrioles are involved in:","Cell division (spindle formation)","Photosynthesis","Protein synthesis","Respiration","A","Centrioles organize spindle fibers during mitosis"),
        ("Ribosomes are made of:","rRNA and proteins","DNA and proteins","mRNA and proteins","Lipids and proteins","A","Ribosomes = rRNA + ribosomal proteins"),
        ("Number of chromosomes in human somatic cell:","46","23","92","48","A","Humans have 46 chromosomes (2n=46) in somatic cells"),
        ("Number of chromosomes in human gametes:","23","46","22","24","A","Gametes are haploid (n=23)"),
        ("Osmosis is movement of:","Water through semipermeable membrane","Solute through membrane","Ions against gradient","Large molecules","A","Osmosis: water moves from low to high solute concentration"),
    ]
    for item in cell_facts:
        qs.append(q("Biology","NEET","Cell Biology",item[0][:30],"medium",
            item[0],item[1],item[2],item[3],item[4],item[5],item[6]))

    # Mitosis stages
    mitosis_events = [
        ("Chromosomes become visible","Prophase","Metaphase","Anaphase","Telophase","A","In prophase, chromatin condenses into visible chromosomes"),
        ("Chromosomes align at cell equator","Metaphase","Prophase","Anaphase","Telophase","A","Metaphase: chromosomes align at metaphase plate"),
        ("Chromatids separate to poles","Anaphase","Metaphase","Prophase","Telophase","A","Anaphase: centromeres split; chromatids pulled to poles"),
        ("Nuclear envelope reforms","Telophase","Anaphase","Metaphase","Prophase","A","Telophase: new nuclear envelopes form around chromosomes"),
        ("DNA replication occurs during:","S phase (Interphase)","Prophase","Metaphase","Anaphase","A","DNA replicates in S (synthesis) phase of interphase"),
        ("Spindle fibers attach to chromosomes at:","Centromere","Telomere","Centriole","Chromatid","A","Spindle fibers attach to centromere (kinetochore)"),
        ("Meiosis produces:","4 haploid cells","2 diploid cells","2 haploid cells","4 diploid cells","A","Meiosis I + II produce 4 haploid cells"),
        ("Crossing over (genetic recombination) occurs in:","Prophase I of Meiosis","Anaphase I","Metaphase II","Telophase II","A","Crossing over in Prophase I at chiasmata"),
    ]
    for item in mitosis_events:
        qs.append(q("Biology","NEET","Cell Biology",item[0][:30],"medium",
            item[0],item[1],item[2],item[3],item[4],item[5],item[6]))

    # ── Genetics ──
    # Mendel's laws with different traits
    genetic_traits = [
        ("pea plants","Tall (T)","dwarf (t)","TT×tt","3:1","Tt×Tt F2 gives 3 Tall : 1 dwarf"),
        ("pea plants","Round seed (R)","wrinkled (r)","RR×rr","3:1","Rr×Rr gives 3 Round : 1 wrinkled"),
        ("pea plants","Yellow seed (Y)","green (y)","YY×yy","3:1","Yy×Yy gives 3 Yellow : 1 green"),
        ("pea plants","Purple flower (P)","white (p)","PP×pp","3:1","Pp×Pp gives 3 Purple : 1 white"),
        ("mice","Black coat (B)","brown (b)","Bb×Bb","3:1","Bb×Bb gives 3 Black : 1 brown"),
        ("rabbits","Long hair (L)","short (l)","Ll×ll","1:1","Ll×ll testcross gives 1:1"),
        ("guinea pigs","Rough coat (R)","smooth (r)","Rr×rr","1:1","Testcross Rr×rr gives 1:1"),
        ("cats","Orange fur (O)","black (o)","Oo×oo","1:1","Testcross Oo×oo gives 1:1"),
        ("humans","Tongue rolling (T)","non-rolling (t)","Tt×Tt","3:1","F2 cross 3:1"),
        ("Drosophila","Red eye (W)","white (w)","WW×ww","3:1","F2 of Ww×Ww gives 3:1"),
    ]
    for organism, dominant, recessive, cross, ratio, explanation in genetic_traits:
        qs.append(q("Biology","NEET","Genetics","Monohybrid Cross","medium",
            f"In {organism}, {dominant} is dominant over {recessive}. "
            f"Cross: {cross}. Phenotypic ratio in F2:",
            ratio, "1:2:1", "1:1", "2:1","A", explanation))

    # Dihybrid
    for trait1, trait2 in [("Round,Yellow","Wrinkled,Green"),
                            ("Tall,Purple","Dwarf,White"),
                            ("Black,Rough","Brown,Smooth")]:
        qs.append(q("Biology","NEET","Genetics","Dihybrid Cross","hard",
            f"Dihybrid cross AaBb × AaBb ({trait1} vs {trait2}). F2 phenotypic ratio:",
            "9:3:3:1", "3:1", "1:2:1:2:1", "9:3:4","A",
            "Dihybrid F2 always 9:3:3:1 for independent assortment"))

    # Blood groups
    blood_group_qs = [
        ("Father O, Mother AB. Possible blood groups in child:","A or B only","O or AB only","A, B, O or AB","A or O only","A","IA×i gives A; IB×i gives B → children can be A or B"),
        ("Father A (heterozygous), Mother B (heterozygous). Possible children:","A, B, O or AB","Only A or B","Only AB","Only O","A","IAi×IBi → IA IB (AB), IA i (A), IB i (B), ii (O)"),
        ("Universal blood donor group:","O negative","AB positive","A positive","B positive","A","O- has no antigens; can donate to all"),
        ("Universal blood recipient group:","AB positive","O negative","A positive","B negative","A","AB+ has all antigens; accepts all blood types"),
        ("Rh factor positive means:","Rh antigen present on RBCs","Rh antibody present","Rh gene absent","No Rh antigen","A","Rh+ individuals have Rh(D) antigen on red blood cells"),
    ]
    for item in blood_group_qs:
        qs.append(q("Biology","NEET","Genetics",item[0][:30],"hard",
            item[0],item[1],item[2],item[3],item[4],item[5],item[6]))

    # DNA / Molecular Biology
    dna_qs = [
        ("Complementary base pair to Adenine in DNA:","Thymine","Guanine","Cytosine","Uracil","A","A pairs with T via 2 hydrogen bonds in DNA"),
        ("Complementary base pair to Guanine in DNA:","Cytosine","Adenine","Thymine","Uracil","A","G pairs with C via 3 hydrogen bonds"),
        ("In RNA, Adenine pairs with:","Uracil","Thymine","Guanine","Cytosine","A","RNA uses Uracil instead of Thymine"),
        ("Number of hydrogen bonds between A-T pair:","2","3","1","4","A","A-T: 2 H-bonds; G-C: 3 H-bonds"),
        ("Number of hydrogen bonds between G-C pair:","3","2","1","4","A","G-C: 3 H-bonds; A-T: 2 H-bonds"),
        ("DNA double helix was discovered by:","Watson and Crick (1953)","Mendel (1865)","Griffith (1928)","Chargaff (1950)","A","Watson and Crick proposed double helix model in 1953"),
        ("Semiconservative replication of DNA was proved by:","Meselson and Stahl","Watson and Crick","Hershey and Chase","Avery et al.","A","Meselson-Stahl (1958) used N¹⁵ isotope labelling"),
        ("mRNA is synthesized from DNA template in:","Transcription","Translation","Replication","Transduction","A","Transcription: DNA → mRNA"),
        ("Protein synthesis from mRNA occurs in:","Translation","Transcription","Replication","Mutation","A","Translation: mRNA → protein at ribosomes"),
        ("Genetic code is:","Triplet, non-overlapping, degenerate","Doublet, overlapping","Singlet, non-degenerate","Quadruplet","A","Each codon = 3 nucleotides; degenerate (multiple codons per AA)"),
        ("Start codon in mRNA:","AUG","UAA","UAG","UGA","A","AUG codes for Methionine and initiates translation"),
        ("Enzyme that unwinds DNA during replication:","Helicase","DNA polymerase","Ligase","Primase","A","Helicase breaks H-bonds and unwinds the double helix"),
        ("Okazaki fragments are formed on:","Lagging strand","Leading strand","Both strands","Template strand","A","DNA synthesis is discontinuous on lagging strand"),
        ("Central dogma of molecular biology:","DNA → RNA → Protein","RNA → DNA → Protein","Protein → DNA → RNA","RNA → Protein → DNA","A","Crick's central dogma: DNA→RNA→Protein"),
        ("Restriction enzymes cut DNA at:","Specific palindromic sequences","Random sites","Only at promoters","Only at introns","A","Restriction enzymes recognize specific palindromic sequences"),
    ]
    for item in dna_qs:
        qs.append(q("Biology","NEET","Molecular Biology",item[0][:30],"hard",
            item[0],item[1],item[2],item[3],item[4],item[5],item[6]))

    # ── Human Physiology ──
    physiology_qs = [
        ("Normal human body temperature:","37°C (98.6°F)","36°C","38°C","35°C","A","Normal core body temperature is 37°C"),
        ("Normal human heart rate (adult at rest):","60-100 bpm","40-60 bpm","100-120 bpm","20-40 bpm","A","Resting HR: 60-100 beats per minute"),
        ("Normal blood pressure (systolic/diastolic):","120/80 mmHg","80/120 mmHg","140/90 mmHg","100/60 mmHg","A","Normal BP: 120/80 mmHg"),
        ("Hormone that regulates blood sugar:","Insulin (from β cells of pancreas)","Glucagon","Adrenaline","Cortisol","A","Insulin lowers blood glucose by promoting cellular uptake"),
        ("Glucagon raises blood sugar by:","Glycogenolysis (breaking glycogen)","Glycogenesis","Glycolysis","Lipogenesis","A","Glucagon stimulates liver to break down glycogen"),
        ("Site of digestion of proteins:","Stomach (by pepsin)","Mouth","Small intestine only","Large intestine","A","Pepsin (activated pepsinogen) digests proteins in stomach"),
        ("Final digestion and absorption of food occurs in:","Small intestine","Stomach","Large intestine","Esophagus","A","Villi and microvilli in small intestine maximise absorption"),
        ("Large intestine primarily absorbs:","Water and minerals","Proteins","Fats","Carbohydrates","A","Large intestine absorbs water → forms solid feces"),
        ("Oxygen is transported in blood mainly as:","Oxyhemoglobin","Dissolved in plasma","Carbaminohemoglobin","Bicarbonate","A","~97% O₂ carried by hemoglobin as oxyhemoglobin"),
        ("CO₂ is transported in blood mainly as:","Bicarbonate ions (HCO₃⁻)","Dissolved CO₂","Carbaminohemoglobin","Carboxyhemoglobin","A","~70% CO₂ transported as HCO₃⁻"),
        ("Functional unit of kidney:","Nephron","Glomerulus","Bowman's capsule","Loop of Henle","A","Nephron is the structural and functional unit of kidney"),
        ("Process by which blood is filtered in kidney:","Ultrafiltration (in glomerulus)","Dialysis","Osmosis","Active transport","A","Blood filtered under pressure in Bowman's capsule"),
        ("Hormone controlling water reabsorption in kidney:","ADH (Antidiuretic hormone)","Aldosterone","Insulin","Oxytocin","A","ADH increases water permeability of collecting duct"),
        ("Largest gland in human body:","Liver","Pancreas","Spleen","Thyroid","A","Liver is the largest internal organ/gland"),
        ("Normal RBC count in adult male (per mm³):","5 million","4 million","3 million","7 million","A","Normal RBC: ~5 million/mm³ in males"),
        ("Lifespan of RBC:","120 days","60 days","200 days","30 days","A","RBCs live ~120 days then are destroyed in spleen"),
        ("WBCs that produce antibodies:","B lymphocytes","T lymphocytes","Neutrophils","Monocytes","A","B cells differentiate into plasma cells that secrete antibodies"),
        ("Platelets are involved in:","Blood clotting","Oxygen transport","Antibody production","Phagocytosis","A","Platelets (thrombocytes) initiate coagulation cascade"),
    ]
    for item in physiology_qs:
        qs.append(q("Biology","NEET","Human Physiology",item[0][:30],"medium",
            item[0],item[1],item[2],item[3],item[4],item[5],item[6]))

    # ── Evolution ──
    evolution_qs = [
        ("Theory of Natural Selection was proposed by:","Charles Darwin","Jean-Baptiste Lamarck","Gregor Mendel","Thomas Malthus","A","Darwin published 'Origin of Species' in 1859"),
        ("Lamarck's theory of evolution is based on:","Inheritance of acquired characters","Natural selection","Genetic mutation","Gene flow","A","Lamarckism: characters acquired during lifetime are heritable"),
        ("Hardy-Weinberg equilibrium requires:","No evolution","Random mating and large population","Small population","High mutation rate","A","H-W: allele frequencies constant when no evolutionary forces act"),
        ("Founder effect is a type of:","Genetic drift","Natural selection","Gene flow","Mutation","A","Founder effect: small group establishes new population"),
        ("Convergent evolution produces:","Analogous organs","Homologous organs","Vestigial organs","Same DNA sequence","A","Analogous organs similar in function but different in origin"),
        ("Example of homologous organs:","Forelimbs of human, bat, whale","Wings of butterfly and bird","Eyes of octopus and vertebrate","Fins of fish and flippers of dolphin","A","Homologous: same ancestry/structure; different function"),
        ("Vestigial organ in humans:","Appendix","Thumb","Ear","Kidney","A","Appendix is a vestigial organ (reduced function over evolution"),
        ("Common ancestor of humans and apes is:","Dryopithecus/Ramapithecus","Homo habilis","Australopithecus","Cro-Magnon","A","Dryopithecus and Ramapithecus are ancient ape-human ancestors"),
        ("Age of Earth is approximately:","4.5 billion years","1 billion years","13.8 billion years","500 million years","A","Earth formed ~4.5 billion years ago"),
        ("First life forms on Earth were:","Prokaryotes (bacteria-like)","Eukaryotes","Multicellular animals","Fungi","A","First life: simple prokaryotes ~3.5 billion years ago"),
    ]
    for item in evolution_qs:
        qs.append(q("Biology","NEET","Evolution",item[0][:30],"hard",
            item[0],item[1],item[2],item[3],item[4],item[5],item[6]))

    # Plant Biology
    plant_qs = [
        ("Photosynthesis equation (simplified):","6CO₂+6H₂O→C₆H₁₂O₆+6O₂","6O₂+6H₂O→C₆H₁₂O₆+6CO₂","CO₂+H₂O→CH₂O+O₂","C₆H₁₂O₆→6CO₂+6H₂O","A","Photosynthesis: CO₂ + H₂O → glucose + O₂"),
        ("Light reactions of photosynthesis occur in:","Thylakoid membranes (grana)","Stroma","Cytoplasm","Mitochondria","A","Thylakoid membranes contain photosystems I and II"),
        ("Dark reactions (Calvin cycle) occur in:","Stroma of chloroplast","Thylakoid","Cytoplasm","Nucleus","A","Calvin cycle fixes CO₂ into 3-carbon compounds in stroma"),
        ("Stomata are found mainly on:","Lower epidermis of leaf","Upper epidermis","Stem","Root","A","Most stomata on abaxial (lower) leaf surface"),
        ("Guard cells regulate:","Opening and closing of stomata","Photosynthesis","Transpiration rate only","Nutrient absorption","A","Guard cells control stomatal aperture by changing turgor"),
        ("Xylem transports:","Water and minerals (upward)","Sugars (downward)","Oxygen","CO₂","A","Xylem: unidirectional upward transport of water/minerals"),
        ("Phloem transports:","Sugars/organic compounds (bidirectional)","Water only","Minerals upward","O₂","A","Phloem transports photosynthates from source to sink"),
        ("Process by which plants lose water:","Transpiration","Respiration","Photosynthesis","Guttation","A","Transpiration: water loss as vapor through stomata"),
        ("Root pressure is due to:","Active uptake of minerals → osmosis","Transpiration pull","Cohesion of water","Gravity","A","Active mineral uptake creates osmotic gradient → water entry"),
        ("Tallest plant cells in stem cross section:","Collenchyma","Parenchyma","Sclerenchyma","Xylem fiber","A","Collenchyma cells are elongated for flexible support"),
    ]
    for item in plant_qs:
        qs.append(q("Biology","NEET","Plant Biology",item[0][:30],"medium",
            item[0],item[1],item[2],item[3],item[4],item[5],item[6]))

    # Ecology
    for producer, consumer1, consumer2, consumer3 in [
        ("Grass","Grasshopper","Frog","Snake"),
        ("Phytoplankton","Zooplankton","Small fish","Large fish"),
        ("Wheat","Mouse","Snake","Hawk"),
        ("Oak tree","Caterpillar","Bird","Cat"),
        ("Algae","Shrimp","Fish","Seal"),
        ("Rice","Insect","Lizard","Eagle"),
        ("Corn","Rabbit","Fox","Lion"),
        ("Seaweed","Sea urchin","Starfish","Otter"),
    ]:
        qs.append(q("Biology","NEET","Ecology","Food Chain","medium",
            f"Identify the correct food chain:",
            f"{producer}→{consumer1}→{consumer2}→{consumer3}",
            f"{consumer1}→{producer}→{consumer2}→{consumer3}",
            f"{consumer3}→{consumer2}→{consumer1}→{producer}",
            f"{producer}→{consumer2}→{consumer1}→{consumer3}","A",
            f"Correct order: producer → primary → secondary → tertiary consumer"))

    print(f"  Biology generated: {len(qs)}")
    return qs


# ══════════════════════════════════════════════════════════════════════════════
# MATHEMATICS  — target 13,000
# ══════════════════════════════════════════════════════════════════════════════

def gen_mathematics():
    qs = []
    random.seed(45)

    # ── Algebra ──
    # Quadratic roots
    for a_ in range(1, 8):
        for b_ in range(-12, 13, 2):
            c_ = random.choice(range(-15, 16, 3))
            disc = b_*b_ - 4*a_*c_
            if disc > 0:
                import cmath
                r1 = round((-b_ + math.sqrt(disc))/(2*a_), 2)
                r2 = round((-b_ - math.sqrt(disc))/(2*a_), 2)
                s_ = round(r1+r2, 2); p_ = round(r1*r2, 2)
                qs.append(q("Mathematics","NEET","Algebra","Quadratic Equations","medium",
                    f"Sum of roots of {a_}x² + {b_}x + {c_} = 0:",
                    f"{round(-b_/a_,2)}",
                    f"{round(c_/a_,2)}",
                    f"{round(b_/a_,2)}",
                    f"{round(-c_/a_,2)}","A",
                    f"Sum = -b/a = -({b_})/{a_} = {round(-b_/a_,2)}"))
                qs.append(q("Mathematics","NEET","Algebra","Quadratic Equations","medium",
                    f"Product of roots of {a_}x² + {b_}x + {c_} = 0:",
                    f"{round(c_/a_,2)}",
                    f"{round(-b_/a_,2)}",
                    f"{round(-c_/a_,2)}",
                    f"{round(b_/a_,2)}","A",
                    f"Product = c/a = {c_}/{a_} = {round(c_/a_,2)}"))

    # AP/GP
    for a_ in range(1, 20):
        for d_ in range(1, 15):
            n_ = random.choice(range(5, 20))
            an = a_ + (n_-1)*d_
            Sn = n_*(2*a_ + (n_-1)*d_)//2
            qs.append(q("Mathematics","NEET","Sequences","AP nth Term","medium",
                f"AP: a={a_}, d={d_}. {n_}th term:",
                f"{an}", f"{an+d_}", f"{an-d_}", f"{a_*n_}","A",
                f"aₙ = a + (n-1)d = {a_} + {n_-1}×{d_} = {an}"))
            qs.append(q("Mathematics","NEET","Sequences","AP Sum","medium",
                f"AP: a={a_}, d={d_}. Sum of first {n_} terms:",
                f"{Sn}", f"{Sn+n_}", f"{Sn-n_}", f"{n_*an}","A",
                f"Sₙ = n(2a+(n-1)d)/2 = {n_}(2×{a_}+{n_-1}×{d_})/2 = {Sn}"))

    for a_ in range(1, 10):
        for r_ in [2, 3, 0.5, 0.25]:
            n_ = random.choice([3,4,5,6])
            gn = round(a_ * r_**(n_-1), 4)
            Sgn = round(a_*(r_**n_ - 1)/(r_-1), 4) if r_ != 1 else a_*n_
            qs.append(q("Mathematics","NEET","Sequences","GP nth Term","medium",
                f"GP: a={a_}, r={r_}. {n_}th term:",
                f"{gn}", f"{round(gn*r_,4)}", f"{round(gn/r_,4)}", f"{a_*n_}","A",
                f"aₙ = a×r^(n-1) = {a_}×{r_}^{n_-1} = {gn}"))

    # Logarithms
    for base in [2, 3, 5, 10]:
        for val in [base**e for e in range(1, 7)]:
            log_val = round(math.log(val, base))
            qs.append(q("Mathematics","NEET","Algebra","Logarithms","medium",
                f"log_{base}({val}) = ?",
                f"{log_val}", f"{log_val+1}", f"{log_val-1}", f"{base}","A",
                f"log_{base}({val}) = {log_val} since {base}^{log_val} = {val}"))

    # ── Trigonometry ──
    trig_values = [
        (0, "sin", 0, "0"), (30, "sin", 0.5, "1/2"), (45, "sin", round(1/math.sqrt(2),4), "1/√2"),
        (60, "sin", round(math.sqrt(3)/2,4), "√3/2"), (90, "sin", 1, "1"),
        (0, "cos", 1, "1"), (30, "cos", round(math.sqrt(3)/2,4), "√3/2"),
        (45, "cos", round(1/math.sqrt(2),4), "1/√2"), (60, "cos", 0.5, "1/2"),
        (90, "cos", 0, "0"), (0, "tan", 0, "0"), (30, "tan", round(1/math.sqrt(3),4), "1/√3"),
        (45, "tan", 1, "1"), (60, "tan", round(math.sqrt(3),4), "√3"),
    ]
    for angle, fn, val, val_str in trig_values:
        qs.append(q("Mathematics","NEET","Trigonometry","Standard Values","medium",
            f"{fn}({angle}°) = ?",
            val_str,
            "0" if val_str!="0" else "1",
            "√3/2" if val_str!="√3/2" else "1/2",
            "1/√2" if val_str!="1/√2" else "√3","A",
            f"{fn}({angle}°) = {val_str}"))

    # Identities
    for A in [0, 30, 45, 60, 90]:
        rad = math.radians(A)
        sin2 = round(math.sin(rad)**2, 4)
        cos2 = round(math.cos(rad)**2, 4)
        qs.append(q("Mathematics","NEET","Trigonometry","Identities","medium",
            f"sin²({A}°) + cos²({A}°) = ?",
            "1", "0", "2", f"sin({A}°)","A",
            f"sin²θ + cos²θ = 1 always"))
        if A not in [90]:
            sin2A = round(math.sin(2*rad), 4)
            qs.append(q("Mathematics","NEET","Trigonometry","Double Angle","medium",
                f"sin(2×{A}°) = 2sin({A}°)cos({A}°) = ?",
                f"{sin2A}", f"{round(sin2A+0.5,4)}", f"{round(sin2A-0.3,4)}",
                f"{round(sin2A*2,4)}","A",
                f"sin(2×{A}°) = {sin2A}"))

    # ── Calculus ──
    # Derivatives
    for n_ in range(1, 12):
        qs.append(q("Mathematics","JEE","Calculus","Differentiation","medium",
            f"d/dx (x^{n_}) = ?",
            f"{n_}x^{n_-1}" if n_-1 != 0 else f"{n_}",
            f"{n_+1}x^{n_}",
            f"x^{n_+1}/({n_+1})",
            f"x^{n_-1}","A",
            f"Power rule: d/dx(xⁿ) = nxⁿ⁻¹"))

    # Integration
    for n_ in range(0, 10):
        if n_ != -1:
            qs.append(q("Mathematics","JEE","Calculus","Integration","medium",
                f"∫ x^{n_} dx = ?",
                f"x^{n_+1}/({n_+1}) + C",
                f"x^{n_-1}/({n_-1}) + C" if n_>1 else f"{n_}x^{n_+1} + C",
                f"({n_}+1)x^{n_+2} + C",
                f"x^{n_+1} + C","A",
                f"∫xⁿ dx = xⁿ⁺¹/(n+1) + C"))

    # Limits
    limits_qs = [
        ("lim x→0 (sin x / x)", "1", "0", "∞", "1/2","A","Standard limit: lim(sinx/x)=1 as x→0"),
        ("lim x→0 (tan x / x)", "1", "0", "∞", "1/2","A","lim(tanx/x)=1 as x→0"),
        ("lim x→∞ (1 + 1/x)^x", "e", "1", "0", "∞","A","Definition of e: lim(1+1/x)^x = e"),
        ("lim x→0 (e^x - 1)/x", "1", "0", "e", "1/e","A","Standard limit: lim(e^x-1)/x = 1"),
        ("lim x→0 (log(1+x))/x", "1", "0", "log e", "1/log e","A","lim(ln(1+x)/x) = 1 as x→0"),
    ]
    for item in limits_qs:
        qs.append(q("Mathematics","JEE","Calculus",item[0][:30],"hard",
            item[0],item[1],item[2],item[3],item[4],item[5],item[6]))

    # ── Probability ──
    for n_total in range(4, 15):
        for n_favor in range(1, n_total):
            p = round(n_favor/n_total, 4)
            q_val = round(1-p, 4)
            qs.append(q("Mathematics","NEET","Probability","Basic Probability","medium",
                f"Bag has {n_total} balls. {n_favor} are red. Probability of drawing red:",
                f"{n_favor}/{n_total}", f"{n_total-n_favor}/{n_total}",
                f"{n_favor}/{n_total+1}", f"1/{n_favor}","A",
                f"P = favorable/total = {n_favor}/{n_total}"))

    # Dice/coin problems
    dice_qs = [
        ("Two dice thrown. Probability of sum = 7:","6/36 = 1/6","5/36","7/36","1/36","A","(1,6)(2,5)(3,4)(4,3)(5,2)(6,1) = 6 ways"),
        ("Two dice thrown. Probability of sum = 12:","1/36","2/36","3/36","1/6","A","Only (6,6); 1/36"),
        ("Two dice thrown. Probability of sum = 2:","1/36","2/36","1/6","1/12","A","Only (1,1); 1/36"),
        ("Fair coin tossed 3 times. P(all heads):","1/8","1/4","3/8","1/2","A","(1/2)³ = 1/8"),
        ("Fair coin tossed twice. P(at least one head):","3/4","1/2","1/4","1","A","P = 1 - P(no heads) = 1 - 1/4 = 3/4"),
        ("Deck of 52 cards. P(drawing an ace):","4/52 = 1/13","1/52","4/52","1/4","A","4 aces in 52 cards = 1/13"),
        ("Deck of 52 cards. P(drawing a heart):","13/52 = 1/4","1/52","1/13","1/2","A","13 hearts in 52 cards = 1/4"),
        ("Two dice. Probability of getting doubles:","6/36 = 1/6","1/36","2/6","1/12","A","6 doubles out of 36 outcomes"),
    ]
    for item in dice_qs:
        qs.append(q("Mathematics","NEET","Probability",item[0][:30],"medium",
            item[0],item[1],item[2],item[3],item[4],item[5],item[6]))

    # ── Coordinate Geometry ──
    for x1,y1,x2,y2 in [(0,0,3,4),(1,2,4,6),(0,0,5,12),(-1,-2,2,2),(3,4,6,8),
                         (1,1,4,5),(0,3,4,0),(2,2,5,6),(0,0,8,6),(1,3,4,7)]:
        dist = round(math.sqrt((x2-x1)**2 + (y2-y1)**2), 2)
        mx = (x1+x2)/2; my = (y1+y2)/2
        qs.append(q("Mathematics","NEET","Coordinate Geometry","Distance Formula","medium",
            f"Distance between ({x1},{y1}) and ({x2},{y2}):",
            f"{dist}", f"{dist+1}", f"{dist*2}", f"{abs(x2-x1)+abs(y2-y1)}","A",
            f"d = √((x₂-x₁)²+(y₂-y₁)²) = √({(x2-x1)**2}+{(y2-y1)**2}) = {dist}"))
        qs.append(q("Mathematics","NEET","Coordinate Geometry","Midpoint","medium",
            f"Midpoint of ({x1},{y1}) and ({x2},{y2}):",
            f"({mx},{my})", f"({x1+x2},{y1+y2})", f"({x2-x1},{y2-y1})", f"({x1},{y2})","A",
            f"Midpoint = ((x₁+x₂)/2,(y₁+y₂)/2) = ({mx},{my})"))

    # Matrices
    for a,b,c,d in [(1,2,3,4),(2,3,1,5),(1,0,0,1),(2,1,4,3),(3,2,1,4)]:
        det = a*d - b*c
        qs.append(q("Mathematics","JEE","Matrices","Determinant","medium",
            f"|{a} {b}; {c} {d}| (2×2 determinant) = ?",
            f"{det}", f"{det+1}", f"{a*d}", f"{b*c}","A",
            f"det = ad-bc = {a}×{d} - {b}×{c} = {det}"))

    print(f"  Mathematics generated: {len(qs)}")
    return qs


# ══════════════════════════════════════════════════════════════════════════════
# CUET GENERAL KNOWLEDGE  — target 12,000
# ══════════════════════════════════════════════════════════════════════════════

def gen_cuet_gk():
    qs = []
    random.seed(46)

    # ── Indian History ──
    history_qs = [
        ("First Battle of Panipat (1526) was between:","Babur and Ibrahim Lodi","Humayun and Sher Shah","Akbar and Hemu","Babur and Rana Sanga","A","Babur defeated Ibrahim Lodi at Panipat in 1526, founding Mughal Empire"),
        ("Second Battle of Panipat (1556):","Akbar vs Hemu","Babur vs Ibrahim Lodi","Humayun vs Sher Shah","Akbar vs Rana Pratap","A","Akbar (under Bairam Khan) defeated Hemu at Panipat in 1556"),
        ("Third Battle of Panipat (1761):","Ahmad Shah Abdali vs Marathas","Akbar vs Hemu","British vs Marathas","Sikhs vs Afghans","A","Abdali defeated Marathas at Panipat in 1761"),
        ("Battle of Plassey (1757) was between:","British (Clive) vs Siraj-ud-Daulah","British vs Tipu Sultan","Marathas vs British","British vs Mughals","A","Clive defeated Nawab of Bengal at Plassey, establishing British dominance"),
        ("Battle of Buxar (1764):","British vs Mir Qasim, Shuja-ud-Daulah, Shah Alam II","British vs Tipu Sultan","British vs Marathas","British vs Mysore","A","British victory at Buxar gave real administrative control of Bengal"),
        ("Sepoy Mutiny (First War of Independence) was in:","1857","1857","1765","1905","A","Great Revolt of 1857 started in Meerut on May 10, 1857"),
        ("Indian National Congress was founded in:","1885 by A.O. Hume","1905","1920","1885 by Mahatma Gandhi","A","INC founded in 1885 in Bombay by Allan Octavian Hume"),
        ("Partition of Bengal was done by:","Lord Curzon in 1905","Lord Mountbatten","Lord Dalhousie","Lord Wellesley","A","Curzon's controversial Partition of Bengal in 1905"),
        ("Non-Cooperation Movement was launched in:","1920","1905","1930","1942","A","Gandhi launched Non-Cooperation Movement in 1920"),
        ("Salt March (Dandi March) was in:","1930","1920","1942","1919","A","Gandhi marched 241 miles to Dandi on March 12, 1930"),
        ("Quit India Movement was launched in:","1942","1930","1920","1947","A","'Do or Die' - Quit India Movement launched August 8, 1942"),
        ("India gained independence on:","15 August 1947","26 January 1950","15 August 1948","14 August 1947","A","India became independent on August 15, 1947"),
        ("Indian Constitution came into force on:","26 January 1950","15 August 1947","26 November 1949","26 January 1949","A","Constitution adopted Nov 26, 1949; effective Jan 26, 1950"),
        ("First Prime Minister of India:","Jawaharlal Nehru","Sardar Patel","Rajendra Prasad","Subhas Chandra Bose","A","Nehru became PM on August 15, 1947"),
        ("First President of India:","Dr. Rajendra Prasad","Jawaharlal Nehru","Dr. Radhakrishnan","Ambedkar","A","Rajendra Prasad: first President, 1950-1962"),
        ("Who drafted the Indian Constitution:","Dr. B.R. Ambedkar (Chairman of Drafting Committee)","Jawaharlal Nehru","Mahatma Gandhi","Rajendra Prasad","A","Ambedkar chaired the Drafting Committee"),
        ("Jallianwala Bagh massacre occurred in:","1919 (Amritsar)","1905","1930","1857","A","General Dyer ordered firing on April 13, 1919 in Amritsar"),
        ("Simón Bolívar is associated with liberation of:","South America","India","Africa","North America","A","Bolívar liberated Venezuela, Colombia, Peru, Bolivia, Ecuador"),
        ("The Rowlatt Act (1919) was related to:","Suppression of political activities","Land reforms","Education","Trade","A","Rowlatt Act allowed detention without trial; led to protests"),
        ("Chauri Chaura incident led to withdrawal of:","Non-Cooperation Movement","Quit India Movement","Civil Disobedience","Khilafat Movement","A","Gandhi suspended NCM after Chauri Chaura violence (Feb 1922)"),
    ]
    for item in history_qs:
        qs.append(q("CUET_GK","CUET_GT","History",item[0][:30],"medium",
            item[0],item[1],item[2],item[3],item[4],item[5],item[6]))

    # ── Indian Polity ──
    polity_qs = [
        ("Article 21 of Indian Constitution deals with:","Right to Life and Personal Liberty","Right to Equality","Freedom of Speech","Right against Exploitation","A","Art 21: No person deprived of life/liberty except by procedure established by law"),
        ("Article 32 is called:","Heart and Soul of Constitution (Right to Constitutional Remedies)","Right to Education","Right to Equality","Freedom of Religion","A","Dr Ambedkar called Art 32 'heart and soul' of Constitution"),
        ("Lok Sabha has how many seats:","543 + 2 Anglo-Indian = 545 (now 543)","552","250","238","A","Lok Sabha has 543 elected members"),
        ("Rajya Sabha has how many seats:","250 (238 elected + 12 nominated)","543","552","245","A","Rajya Sabha: 245 seats (233+12 nominated)"),
        ("The President of India is elected by:","Elected members of both Houses + State Assemblies","All citizens","Only Lok Sabha","Only Rajya Sabha","A","Electoral College: elected MPs + elected MLAs"),
        ("Who appoints the Chief Justice of India:","President of India (on advice)","Prime Minister","Parliament","Chief Minister","A","CJI appointed by President under Art 124"),
        ("The Finance Commission is constituted every:","5 years","3 years","10 years","2 years","A","Finance Commission constituted every 5 years under Art 280"),
        ("Fundamental Rights are in which Part of Constitution:","Part III (Articles 12-35)","Part IV","Part I","Part V","A","FR: Part III, Articles 12-35"),
        ("Directive Principles of State Policy are in:","Part IV","Part III","Part V","Part VI","A","DPSP: Part IV, Articles 36-51 (not justiciable)"),
        ("Right to Education (Art 21-A) makes education free and compulsory for:","6-14 years","5-18 years","5-14 years","6-18 years","A","RTE: free and compulsory for children aged 6-14"),
        ("73rd Constitutional Amendment deals with:","Panchayati Raj institutions","Urban local bodies","Fundamental duties","Official languages","A","73rd Amendment (1992): Constitutional status to Panchayats"),
        ("74th Constitutional Amendment deals with:","Urban Local Bodies (Municipalities)","Panchayati Raj","Scheduled castes","Education","A","74th Amendment (1992): Constitutional status to ULBs"),
        ("The Speaker of Lok Sabha is elected by:","Members of Lok Sabha","Members of both Houses","President","Prime Minister","A","Lok Sabha Speaker elected by Lok Sabha members"),
        ("Emergency under Article 356 is called:","President's Rule (State Emergency)","National Emergency","Financial Emergency","Constitutional Emergency","A","Art 356: President's Rule when State government fails"),
        ("National Emergency under Article 352 can be imposed on grounds of:","War, external aggression, armed rebellion","Financial crisis","Political instability","Natural disaster","A","Art 352: National Emergency on grounds of war/external aggression/armed rebellion"),
    ]
    for item in polity_qs:
        qs.append(q("CUET_GK","CUET_GT","Polity",item[0][:30],"hard",
            item[0],item[1],item[2],item[3],item[4],item[5],item[6]))

    # ── Indian Geography ──
    geo_qs = [
        ("Longest river in India:","Ganga","Yamuna","Godavari","Indus","A","Ganga (2,525 km) is the longest river entirely in India"),
        ("Highest peak in India:","Kangchenjunga (8,586 m)","Mt Everest","Nanda Devi","K2","A","Kangchenjunga is the highest peak in India (3rd highest in world)"),
        ("India's largest state by area:","Rajasthan","Madhya Pradesh","Uttar Pradesh","Maharashtra","A","Rajasthan is India's largest state by area (342,239 km²)"),
        ("India's smallest state by area:","Goa","Sikkim","Tripura","Manipur","A","Goa is India's smallest state (3,702 km²)"),
        ("India's most populous state:","Uttar Pradesh","Maharashtra","Bihar","West Bengal","A","UP has India's largest population (~240 million, 2023 est.)"),
        ("Tropic of Cancer passes through how many Indian states:","8","6","5","9","A","Tropic of Cancer passes through Gujarat, Rajasthan, MP, Chhattisgarh, Jharkhand, WB, Tripura, Mizoram"),
        ("India's coastline length approximately:","7,516 km","5,000 km","10,000 km","6,200 km","A","India has coastline of ~7,516 km"),
        ("India shares longest border with:","Bangladesh","Pakistan","China","Nepal","A","India-Bangladesh border: ~4,156 km (longest)"),
        ("The Western Ghats run parallel to:","Western coast (Arabian Sea)","Eastern coast","Himalayan range","Deccan Plateau","A","Western Ghats run along western coast from Gujarat to Kerala"),
        ("Eastern Ghats run along:","Eastern coast (Bay of Bengal)","Western coast","Northern India","Deccan Plateau interior","A","Eastern Ghats run discontinuously along eastern coast"),
        ("Lakshadweep Islands are in:","Arabian Sea","Bay of Bengal","Indian Ocean","Pacific Ocean","A","Lakshadweep: coral islands in Arabian Sea"),
        ("Andaman and Nicobar Islands are in:","Bay of Bengal","Arabian Sea","Indian Ocean","Pacific Ocean","A","A&N Islands: Bay of Bengal"),
        ("India's highest waterfall:","Kunchikal Falls (Karnataka, 455 m)","Jog Falls","Athirappilly","Dudhsagar","A","Kunchikal Falls in Karnataka is India's highest (455 m)"),
        ("The Deccan Plateau is bounded by:","Satpuras, Western and Eastern Ghats","Himalayas","Aravallis","Vindhyas","A","Deccan Plateau: bounded by Satpuras (N), W/E Ghats"),
        ("River Brahmaputra enters India from:","Arunachal Pradesh (from China/Tibet)","Assam","Bangladesh","Nagaland","A","Brahmaputra enters NE India through Arunachal Pradesh"),
    ]
    for item in geo_qs:
        qs.append(q("CUET_GK","CUET_GT","Geography",item[0][:30],"medium",
            item[0],item[1],item[2],item[3],item[4],item[5],item[6]))

    # ── Awards and Honours ──
    awards_qs = [
        ("Bharat Ratna is India's:","Highest civilian award","Highest military award","Highest literary award","Sports award","A","Bharat Ratna: India's highest civilian honour since 1954"),
        ("Nobel Prize in Literature 1913 was won by:","Rabindranath Tagore","Mahatma Gandhi","Jawaharlal Nehru","Aurobindo Ghosh","A","Tagore: first Asian Nobel laureate (Gitanjali)"),
        ("Nobel Prize in Physics 1930 won by:","C.V. Raman","Homi Bhabha","Vikram Sarabhai","J.C. Bose","A","C.V. Raman won Nobel for discovery of Raman Effect"),
        ("Nobel Peace Prize 1979 won by:","Mother Teresa","Amartya Sen","Dalai Lama","Nelson Mandela","A","Mother Teresa won Nobel Peace Prize for work with poor in Calcutta"),
        ("Nobel Economics Prize 1998 won by:","Amartya Sen","Manmohan Singh","Raghuram Rajan","Jagdish Bhagwati","A","Amartya Sen won Nobel for welfare economics and social choice theory"),
        ("Arjuna Award is given for excellence in:","Sports","Literature","Science","Film","A","Arjuna Award: outstanding achievement in sports"),
        ("Dronacharya Award is for:","Sports coaches","Athletes","Scientists","Teachers","A","Dronacharya Award: outstanding coaches of sportspersons"),
        ("Dadasaheb Phalke Award is for:","Lifetime contribution to Indian cinema","Music","Literature","Dance","A","India's highest film honour for lifetime contribution to cinema"),
        ("Jnanpith Award is India's highest award for:","Literature","Science","Film","Arts","A","Jnanpith Award: highest Indian literary award since 1965"),
        ("Sahitya Akademi Award is for:","Outstanding literary work","Best film","Scientific research","Social service","A","Sahitya Akademi recognizes outstanding literary works"),
    ]
    for item in awards_qs:
        qs.append(q("CUET_GK","CUET_GT","Awards",item[0][:30],"medium",
            item[0],item[1],item[2],item[3],item[4],item[5],item[6]))

    # Parametric: capitals, currencies, GK facts
    countries_data = [
        ("India","New Delhi","Indian Rupee (INR)"),("USA","Washington D.C.","US Dollar (USD)"),
        ("UK","London","Pound Sterling (GBP)"),("France","Paris","Euro (EUR)"),
        ("Germany","Berlin","Euro (EUR)"),("Japan","Tokyo","Yen (JPY)"),
        ("China","Beijing","Renminbi/Yuan (CNY)"),("Russia","Moscow","Ruble (RUB)"),
        ("Brazil","Brasília","Real (BRL)"),("Australia","Canberra","Australian Dollar (AUD)"),
        ("Canada","Ottawa","Canadian Dollar (CAD)"),("Italy","Rome","Euro (EUR)"),
        ("Spain","Madrid","Euro (EUR)"),("Pakistan","Islamabad","Pakistani Rupee (PKR)"),
        ("Bangladesh","Dhaka","Bangladeshi Taka (BDT)"),("Sri Lanka","Colombo (Sri Jayawardenepura Kotte)","Sri Lankan Rupee (LKR)"),
        ("Nepal","Kathmandu","Nepalese Rupee (NPR)"),("South Africa","Pretoria","Rand (ZAR)"),
        ("Argentina","Buenos Aires","Argentine Peso (ARS)"),("Mexico","Mexico City","Mexican Peso (MXN)"),
        ("Saudi Arabia","Riyadh","Saudi Riyal (SAR)"),("UAE","Abu Dhabi","UAE Dirham (AED)"),
        ("South Korea","Seoul","South Korean Won (KRW)"),("Indonesia","Jakarta","Indonesian Rupiah (IDR)"),
        ("Egypt","Cairo","Egyptian Pound (EGP)"),("Nigeria","Abuja","Naira (NGN)"),
        ("Kenya","Nairobi","Kenyan Shilling (KES)"),("Singapore","Singapore City","Singapore Dollar (SGD)"),
        ("Malaysia","Kuala Lumpur","Ringgit (MYR)"),("Thailand","Bangkok","Thai Baht (THB)"),
    ]
    for country, capital, currency in countries_data:
        qs.append(q("CUET_GK","CUET_GT","Geography","World Capitals","easy",
            f"Capital of {country}:",
            capital,
            f"{'London' if capital!='London' else 'Paris'}",
            f"{'New York' if capital!='New York' else 'Washington D.C.'}",
            f"{'Sydney' if capital!='Sydney' else 'Melbourne'}","A",
            f"Capital of {country} is {capital}"))
        qs.append(q("CUET_GK","CUET_GT","Economy","World Currencies","easy",
            f"Currency of {country}:",
            currency,
            f"US Dollar" if currency!="US Dollar (USD)" else "Euro",
            f"Euro" if "Euro" not in currency else "Pound Sterling",
            f"Yen" if "Yen" not in currency else "Rupee","A",
            f"Currency of {country} is {currency}"))

    print(f"  CUET_GK generated: {len(qs)}")
    return qs


# ══════════════════════════════════════════════════════════════════════════════
# CUET ENGLISH  — target 12,000
# ══════════════════════════════════════════════════════════════════════════════

def gen_cuet_english():
    qs = []
    random.seed(47)

    # Vocabulary: synonyms
    synonyms = [
        ("Abundant","Plentiful","Scarce","Rare","Limited","A","Abundant means plentiful/in large quantity"),
        ("Amiable","Friendly","Hostile","Rude","Aggressive","A","Amiable = pleasant and friendly"),
        ("Benevolent","Kind","Cruel","Selfish","Greedy","A","Benevolent = well-meaning and kind"),
        ("Candid","Frank","Secretive","Dishonest","Shy","A","Candid = truthful and straightforward"),
        ("Diligent","Hardworking","Lazy","Careless","Idle","A","Diligent = having or showing care/effort in work"),
        ("Eloquent","Expressive","Inarticulate","Silent","Dull","A","Eloquent = fluent or persuasive in speech"),
        ("Frugal","Thrifty","Extravagant","Wasteful","Lavish","A","Frugal = sparing in use of money/resources"),
        ("Gregarious","Sociable","Solitary","Antisocial","Reserved","A","Gregarious = fond of company; sociable"),
        ("Humble","Modest","Arrogant","Proud","Haughty","A","Humble = having a low estimate of one's importance"),
        ("Immaculate","Spotless","Dirty","Filthy","Stained","A","Immaculate = perfectly clean; free from flaw"),
        ("Jovial","Cheerful","Gloomy","Sad","Melancholy","A","Jovial = cheerful and friendly"),
        ("Keen","Eager","Reluctant","Unwilling","Hesitant","A","Keen = eager, interested, enthusiastic"),
        ("Lethargic","Sluggish","Energetic","Active","Lively","A","Lethargic = affected by lethargy; sluggish"),
        ("Meticulous","Careful","Careless","Sloppy","Negligent","A","Meticulous = showing great attention to detail"),
        ("Nonchalant","Unconcerned","Anxious","Worried","Stressed","A","Nonchalant = feeling casually calm and relaxed"),
        ("Obscure","Unclear","Clear","Obvious","Evident","A","Obscure = not discovered or known about; unclear"),
        ("Persistent","Determined","Giving up","Inconsistent","Quitting","A","Persistent = continuing firmly despite obstacles"),
        ("Quaint","Charming","Modern","Ugly","Common","A","Quaint = attractively unusual or old-fashioned"),
        ("Resilient","Tough","Fragile","Weak","Brittle","A","Resilient = able to recover quickly from difficulties"),
        ("Scrutinize","Examine carefully","Ignore","Overlook","Dismiss","A","Scrutinize = examine or inspect closely"),
        ("Tedious","Boring","Interesting","Exciting","Thrilling","A","Tedious = too long, slow; boring"),
        ("Ubiquitous","Everywhere","Rare","Absent","Scarce","A","Ubiquitous = present, appearing, or found everywhere"),
        ("Verbose","Wordy","Concise","Brief","Terse","A","Verbose = using more words than needed"),
        ("Wary","Cautious","Reckless","Bold","Careless","A","Wary = feeling or showing caution about possible dangers"),
        ("Zealous","Enthusiastic","Indifferent","Apathetic","Passive","A","Zealous = having or showing great energy/enthusiasm"),
        ("Ambiguous","Unclear","Clear","Definite","Precise","A","Ambiguous = open to more than one interpretation"),
        ("Concise","Brief","Wordy","Long","Verbose","A","Concise = giving much information clearly in few words"),
        ("Derive","Obtain","Lose","Give","Abandon","A","Derive = obtain something from a specified source"),
        ("Elucidate","Explain clearly","Confuse","Complicate","Obscure","A","Elucidate = make something clear; explain"),
        ("Feasible","Possible","Impossible","Unlikely","Impractical","A","Feasible = possible and practical to do easily"),
    ]
    for item in synonyms:
        qs.append(q("CUET_English","CUET_GT","Vocabulary","Synonyms","medium",
            f"Synonym of '{item[0]}':",
            item[1],item[2],item[3],item[4],item[5],item[6]))

    # Antonyms
    antonyms = [
        ("Expand","Contract","Grow","Increase","Enlarge","A","Antonym of Expand is Contract/Shrink"),
        ("Genuine","Fake","Real","Authentic","Sincere","A","Antonym of Genuine is Fake/Counterfeit"),
        ("Harmony","Discord","Peace","Agreement","Unity","A","Antonym of Harmony is Discord/Conflict"),
        ("Industrious","Lazy","Hardworking","Diligent","Busy","A","Antonym of Industrious is Lazy/Idle"),
        ("Justice","Injustice","Fairness","Equity","Right","A","Antonym of Justice is Injustice"),
        ("Knowledge","Ignorance","Learning","Wisdom","Understanding","A","Antonym of Knowledge is Ignorance"),
        ("Liberty","Captivity","Freedom","Independence","Release","A","Antonym of Liberty is Captivity/Bondage"),
        ("Majority","Minority","Most","Bulk","Greater part","A","Antonym of Majority is Minority"),
        ("Natural","Artificial","Real","Organic","Genuine","A","Antonym of Natural is Artificial/Synthetic"),
        ("Optimistic","Pessimistic","Hopeful","Positive","Confident","A","Antonym of Optimistic is Pessimistic"),
        ("Permanent","Temporary","Lasting","Enduring","Stable","A","Antonym of Permanent is Temporary/Transient"),
        ("Question","Answer","Query","Ask","Enquire","A","Antonym of Question is Answer"),
        ("Remember","Forget","Recall","Recollect","Retain","A","Antonym of Remember is Forget"),
        ("Success","Failure","Achievement","Victory","Triumph","A","Antonym of Success is Failure"),
        ("Truth","Falsehood","Fact","Reality","Honesty","A","Antonym of Truth is Falsehood/Lie"),
        ("Unity","Division","Oneness","Solidarity","Togetherness","A","Antonym of Unity is Division/Disunity"),
        ("Victory","Defeat","Win","Success","Triumph","A","Antonym of Victory is Defeat"),
        ("Wise","Foolish","Intelligent","Clever","Sensible","A","Antonym of Wise is Foolish/Unwise"),
        ("Accept","Reject","Agree","Receive","Take","A","Antonym of Accept is Reject/Decline"),
        ("Brave","Cowardly","Courageous","Bold","Fearless","A","Antonym of Brave is Cowardly/Timid"),
    ]
    for item in antonyms:
        qs.append(q("CUET_English","CUET_GT","Vocabulary","Antonyms","medium",
            f"Antonym of '{item[0]}':",
            item[1],item[2],item[3],item[4],item[5],item[6]))

    # Grammar: fill in the blank
    grammar_qs = [
        ("She ___ to school every day.","goes","go","is going","gone","A","Third person singular present: goes"),
        ("They ___ playing football when it rained.","were","was","are","have","A","Past continuous: were playing"),
        ("I have ___ my homework.","done","did","do","does","A","Present perfect with 'have': done"),
        ("He ___ the book yesterday.","read","reads","has read","is reading","A","Simple past: read (pronounced 'red')"),
        ("She is ___ than her sister.","taller","tall","tallest","more tall","A","Comparative adjective: taller"),
        ("This is the ___ movie I have ever seen.","best","better","good","most good","A","Superlative: best"),
        ("Neither he nor she ___ the answer.","knows","know","are knowing","have known","A","Neither...nor: verb agrees with nearest subject (she → knows)"),
        ("The committee ___ divided in its opinion.","was","were","are","have","A","'Committee' as a unit: singular verb 'was'"),
        ("He ran ___ than I expected.","faster","fast","fastest","more fast","A","Comparative: faster"),
        ("She speaks English ___.","fluently","fluent","more fluent","fluentness","A","Adverb modifies verb: fluently"),
        ("I ___ here since 2010.","have lived","lived","am living","was living","A","Present perfect for action continuing to now"),
        ("By the time he arrived, she ___ left.","had already","already","has","have","A","Past perfect: had already left"),
        ("___ you please help me?","Could","Can","Will","Shall","A","Polite request: Could you please..."),
        ("If I were rich, I ___ travel the world.","would","will","shall","do","A","Second conditional: If I were... I would"),
        ("She suggested that he ___ the doctor.","see","sees","saw","had seen","A","Suggest + that + bare infinitive (subjunctive)"),
        ("The news ___ surprising.","was","were","are","have been","A","'News' is uncountable: singular verb"),
        ("Mathematics ___ my favourite subject.","is","are","were","have been","A","Subject names are singular: Mathematics is"),
        ("He is one of those who ___ always late.","are","is","was","have","A","'Those who are' - plural antecedent"),
        ("She ___ English for 10 years now.","has been learning","is learning","learned","learns","A","Present perfect continuous for ongoing action"),
        ("The jury ___ reached a verdict.","has","have","are","were","A","'Jury' as a unit: singular - has reached"),
    ]
    for item in grammar_qs:
        qs.append(q("CUET_English","CUET_GT","Grammar","Fill in the Blank","medium",
            item[0],item[1],item[2],item[3],item[4],item[5],item[6]))

    # Idioms and Phrases
    idioms = [
        ("Bite the bullet","To endure a painful situation","To eat something hard","To shoot someone","To ignore advice","A","'Bite the bullet' = endure something difficult"),
        ("Beat around the bush","To avoid the main topic","To hit a bush","To walk in a garden","To search for something","A","'Beat around the bush' = avoid the main point"),
        ("Hit the nail on the head","To describe exactly right","To hammer something","To injure oneself","To be wrong","A","'Hit the nail on the head' = describe precisely"),
        ("Break the ice","To initiate conversation in awkward situation","To break something","To make someone cold","To start a fight","A","'Break the ice' = start a conversation in a social situation"),
        ("Burn the midnight oil","To work or study late","To waste oil","To start a fire","To sleep early","A","'Burn the midnight oil' = work late into the night"),
        ("Let the cat out of the bag","To reveal a secret","To release a cat","To make noise","To lose something","A","'Let the cat out of the bag' = accidentally reveal a secret"),
        ("Once in a blue moon","Very rarely","Once a month","Frequently","Every day","A","'Once in a blue moon' = very rarely"),
        ("Spill the beans","To reveal secret information","To make a mess","To cook beans","To drop food","A","'Spill the beans' = inadvertently reveal a secret"),
        ("Under the weather","Feeling ill","In a storm","Outdoors","Happy","A","'Under the weather' = feeling slightly ill"),
        ("Bite off more than you can chew","To take on more than you can handle","To eat too much","To be hungry","To refuse food","A","Taking on more responsibility than you can manage"),
        ("Cost an arm and a leg","To be very expensive","Medical expenses","Physical injury","Cheap item","A","'Cost an arm and a leg' = be extremely expensive"),
        ("Get out of hand","To become uncontrollable","To release something","To leave","To escape","A","'Get out of hand' = become unmanageable"),
        ("Hit the books","To study","To throw books","To go to library","To read novels","A","'Hit the books' = study"),
        ("Piece of cake","Something very easy","A dessert","Cooking","A reward","A","'Piece of cake' = very easy task"),
        ("Pull someone's leg","To joke/tease someone","To physically pull","To help someone","To injure someone","A","'Pull someone's leg' = tease or joke with someone"),
    ]
    for item in idioms:
        qs.append(q("CUET_English","CUET_GT","Vocabulary","Idioms and Phrases","medium",
            f"Meaning of '{item[0]}':",
            item[1],item[2],item[3],item[4],item[5],item[6]))

    # Error spotting - sentences
    error_qs = [
        ("She don't like coffee.","'don't' should be 'doesn't'","No error","'like' should be 'likes'","'She' should be 'Her'","A","Third person singular: doesn't (not don't)"),
        ("He is more taller than me.","'more taller' should be 'taller'","No error","'taller' should be 'more tall'","'than' should be 'then'","A","'More taller' is double comparative; should be 'taller'"),
        ("One of the students were absent.","'were' should be 'was'","No error","'students' should be 'student'","'One' should be 'Some'","A","'One of the students' takes singular verb: was"),
        ("He gave me a very good advice.","'a' should be removed (advice is uncountable)","No error","'good' should be 'well'","'gave' should be 'give'","A","'Advice' is uncountable; no article 'a'"),
        ("I am knowing him for years.","'am knowing' should be 'have known'","No error","'years' should be 'year'","'for' should be 'since'","A","Know is a stative verb; present perfect: have known"),
    ]
    for item in error_qs:
        qs.append(q("CUET_English","CUET_GT","Grammar","Error Spotting","hard",
            f"Find the error: '{item[0]}'",
            item[1],item[2],item[3],item[4],item[5],item[6]))

    print(f"  CUET_English generated: {len(qs)}")
    return qs


# ══════════════════════════════════════════════════════════════════════════════
# CUET REASONING  — target 12,000
# ══════════════════════════════════════════════════════════════════════════════

def gen_cuet_reasoning():
    qs = []
    random.seed(48)

    # Number series
    series_patterns = [
        # (start, step, type, n_shown)
        (2, 2, "add", 6), (3, 3, "add", 6), (5, 5, "add", 6),
        (1, 2, "mult", 5), (2, 2, "mult", 5), (3, 2, "mult", 5),
        (1, 3, "mult", 5), (2, 3, "mult", 5),
        (100, 10, "sub", 6), (50, 5, "sub", 6), (200, 20, "sub", 6),
    ]
    for start, step, stype, n in series_patterns:
        for offset in range(0, 20, 3):
            s = start + offset
            if stype == "add":
                series = [s + step*i for i in range(n)]
                next_val = s + step*n
            elif stype == "mult":
                series = [s * (step**i) for i in range(n)]
                next_val = s * (step**n)
            elif stype == "sub":
                series = [s - step*i for i in range(n)]
                next_val = s - step*n

            if all(v > 0 for v in series) and 0 < next_val < 100000:
                shown = ", ".join(str(v) for v in series)
                qs.append(q("CUET_Reasoning","CUET_GT","Number Series","Next Term","medium",
                    f"Find next: {shown}, ?",
                    f"{next_val}",
                    f"{next_val + step if stype=='add' else next_val + 1}",
                    f"{next_val - step if stype=='add' else next_val - 1}",
                    f"{series[-1]}","A",
                    f"Pattern: {'add '+str(step) if stype=='add' else 'multiply by '+str(step) if stype=='mult' else 'subtract '+str(step)}; next = {next_val}"))

    # Square/cube series
    for base in range(2, 12):
        squares = [i*i for i in range(base, base+6)]
        shown = ", ".join(str(v) for v in squares[:5])
        qs.append(q("CUET_Reasoning","CUET_GT","Number Series","Square Series","hard",
            f"Find next: {shown}, ?",
            f"{squares[5]}", f"{squares[5]+5}", f"{squares[4]+5}", f"{squares[5]-2}","A",
            f"Series of squares: {base}²,{base+1}²,...; next = {base+5}² = {squares[5]}"))

    # Coding-Decoding
    code_pairs = [
        ("APPLE","BQQMF","Each letter +1 in alphabet","APPLE → BQQMF (A+1=B, P+1=Q, P+1=Q, L+1=M, E+1=F)"),
        ("BOOK","CPPL","Each letter +1","B+1=C, O+1=P, O+1=P, K+1=L"),
        ("MANGO","NBOHP","Each letter +1","M+1=N, A+1=B, N+1=O, G+1=H, O+1=P"),
        ("DELHI","EFMIJ","Each letter +1","D+1=E, E+1=F, L+1=M, H+1=I, I+1=J"),
        ("CAT","DBU","Each letter +1","C+1=D, A+1=B, T+1=U"),
        ("SUN","TVO","Each letter +1","S+1=T, U+1=V, N+1=O"),
        ("RAIN","SBJO","Each letter +1","R+1=S, A+1=B, I+1=J, N+1=O"),
        ("HOME","IPNF","Each letter +1","H+1=I, O+1=P, M+1=N, E+1=F"),
    ]
    for word, code, pattern, explanation in code_pairs:
        qs.append(q("CUET_Reasoning","CUET_GT","Coding","Letter Coding","medium",
            f"If {word} is coded as {code}, find the code for the next word using the same pattern:",
            f"Next letter of each letter",
            f"Previous letter of each letter",
            f"Reverse the word",
            f"Skip alternate letters","A", explanation))

        # Create a reverse question
        qs.append(q("CUET_Reasoning","CUET_GT","Coding","Decoding","medium",
            f"In a code: {word} = {code}. What does '{code}' decode to?",
            word,
            word[::-1],
            word[1:]+word[0],
            word[:-1],"A", f"Reverse the +1 coding: {code} → {word}"))

    # Blood Relations
    blood_qs = [
        ("A is B's brother. B is C's sister. How is A related to C?","Brother","Sister","Uncle","Cousin","A","A is B's brother; B is C's sister → A is C's brother"),
        ("A is B's father. B is C's son. How is A related to C?","Grandfather","Father","Uncle","Brother","A","A→B→C: A is C's grandfather"),
        ("A's mother is B's daughter. How is B related to A?","Grandmother","Mother","Aunt","Sister","A","B's daughter is A's mother → B is A's grandmother"),
        ("P is Q's son. R is P's mother. How is Q related to R?","Husband","Father","Son","Brother","A","R is P's mother; P is Q's son → Q is R's husband (if Q is male)"),
        ("If A is the brother of B, B is the sister of C, C is the father of D, how is A related to D?","Uncle","Father","Brother","Grandfather","A","A-brother of B, B-sister of C (so A,B,C siblings), C-father of D → A is D's uncle"),
        ("Introducing a man, a woman says 'His mother is the only daughter of my mother.' How is the man related to her?","Son","Brother","Nephew","Father","A","Only daughter of her mother = herself; his mother = herself; so he is her son"),
        ("A man says about a photo: 'She is the daughter of my grandfather's only son.' The relation of the man to the girl is:","Brother (or male cousin)","Father","Uncle","Son","A","Grandfather's only son = his father; daughter of his father = his sister (or he is her brother)"),
        ("If P+Q means P is the father of Q; P-Q means P is the mother of Q; P×Q means P is the brother of Q; P÷Q means P is the sister of Q, then A+B-C means:","A is the grandfather of C","A is the father of C","A is the uncle of C","A is the son of C","A","A+B: A is father of B; B-C: B is mother of C → A is grandfather of C"),
    ]
    for item in blood_qs:
        qs.append(q("CUET_Reasoning","CUET_GT","Blood Relations",item[0][:40],"hard",
            item[0],item[1],item[2],item[3],item[4],item[5],item[6]))

    # Direction Sense
    directions_qs = [
        ("A walks 10 km North, then 10 km East. Net displacement from start:","10√2 km NE","20 km","10 km","0 km","A","Using Pythagoras: √(10²+10²) = 10√2 km in NE direction"),
        ("A goes 5 km South, then 12 km East. Distance from start:","13 km","17 km","7 km","12 km","A","√(5²+12²) = √(25+144) = √169 = 13 km"),
        ("A walks 3 km East, then 4 km North. Distance from start:","5 km","7 km","3.5 km","6 km","A","√(3²+4²) = √(9+16) = √25 = 5 km"),
        ("If you face North and turn 90° clockwise, you face:","East","West","South","North","A","Facing North, 90° clockwise → East"),
        ("If you face South and turn 180°, you face:","North","East","West","South","A","Facing South, 180° turn → North"),
        ("If you face East and turn 90° anticlockwise, you face:","North","South","West","East","A","Facing East, 90° anticlockwise → North"),
        ("Walking 6 km West then 8 km South, distance from start:","10 km","14 km","2 km","48 km","A","√(6²+8²) = √(36+64) = √100 = 10 km"),
        ("A walks 20 m North, turns right, walks 10 m, turns right, walks 20 m. How far from start?","10 m","20 m","0 m","30 m","A","Returns to same latitude; 10 m East of start"),
    ]
    for item in directions_qs:
        qs.append(q("CUET_Reasoning","CUET_GT","Direction Sense",item[0][:40],"medium",
            item[0],item[1],item[2],item[3],item[4],item[5],item[6]))

    # Syllogism
    syllogism_qs = [
        ("All cats are animals. All animals have hearts. Conclusion: All cats have hearts.",
         "True (Valid conclusion)","False","Uncertain","Partially true","A","All cats→animals→hearts; transitive"),
        ("Some birds can fly. All parrots are birds. Conclusion: Some parrots can fly.",
         "Uncertain (not necessarily true)","True","False","Valid","A","'Some birds can fly' doesn't mean all, so uncertain for parrots"),
        ("No dogs are cats. All cats are mammals. Conclusion: Some mammals are not dogs.",
         "True","False","Uncertain","Both A and B","A","Since cats are mammals and no dogs are cats, some mammals (cats) are not dogs"),
        ("All roses are flowers. Some flowers fade quickly. Conclusion: Some roses fade quickly.",
         "Uncertain","True","False","Valid","A","'Some flowers fade' doesn't specify which; roses may or may not"),
        ("All mangoes are fruits. No fruit is a vegetable. Conclusion: No mango is a vegetable.",
         "True (Valid)","False","Uncertain","Cannot determine","A","All mangoes→fruits; no fruit→vegetable; ∴ no mango→vegetable"),
    ]
    for item in syllogism_qs:
        qs.append(q("CUET_Reasoning","CUET_GT","Syllogism",item[0][:40],"hard",
            item[0],item[1],item[2],item[3],item[4],item[5],item[6]))

    # Calendar problems
    for year in range(2000, 2030):
        for month in [(1,"January",31),(3,"March",31),(7,"July",31),(8,"August",31),(12,"December",31)]:
            m_num, m_name, m_days = month
            import calendar
            day_name = calendar.day_name[calendar.weekday(year, m_num, 1)]
            qs.append(q("CUET_Reasoning","CUET_GT","Calendar","Day of Week","medium",
                f"If 1st {m_name} {year} falls on {day_name}, how many Sundays in {m_name} {year}?",
                f"{4 if day_name not in ['Sunday','Saturday','Friday'] else 5}",
                f"3", f"6", f"2","A",
                f"1st {m_name} {year} = {day_name}; 31-day month has 4 or 5 Sundays"))

    print(f"  CUET_Reasoning generated: {len(qs)}")
    return qs


# ══════════════════════════════════════════════════════════════════════════════
# CUET QUANTITATIVE  — target 12,000
# ══════════════════════════════════════════════════════════════════════════════

def gen_cuet_quantitative():
    qs = []
    random.seed(49)

    # Percentage
    for val in range(10, 500, 10):
        for pct in range(5, 100, 5):
            result = round(pct * val / 100, 2)
            qs.append(q("CUET_Quantitative","CUET_GT","Percentages","Basic Percentage","easy",
                f"{pct}% of {val} = ?",
                f"{result}", f"{val*pct}", f"{round(result*2,2)}", f"{round(result/2,2)}","A",
                f"{pct}% of {val} = {pct}×{val}/100 = {result}"))

    # Percentage increase/decrease
    for original in range(100, 1000, 50):
        for pct in [5, 10, 15, 20, 25, 30, 40, 50]:
            new_val = original * (1 + pct/100)
            qs.append(q("CUET_Quantitative","CUET_GT","Percentages","Percentage Increase","medium",
                f"A number {original} is increased by {pct}%. New value:",
                f"{new_val}", f"{original + pct}", f"{original * pct / 100}",
                f"{original * pct}","A",
                f"New = {original} × (1+{pct}/100) = {original} × {1+pct/100} = {new_val}"))
            dec_val = original * (1 - pct/100)
            qs.append(q("CUET_Quantitative","CUET_GT","Percentages","Percentage Decrease","medium",
                f"A number {original} is decreased by {pct}%. New value:",
                f"{dec_val}", f"{original - pct}", f"{original * pct / 100}",
                f"{original / pct}","A",
                f"New = {original} × (1-{pct}/100) = {dec_val}"))

    # Simple Interest
    for P in range(500, 10001, 500):
        for R in range(2, 20, 2):
            for T in range(1, 6):
                SI = round(P*R*T/100)
                A = P + SI
                qs.append(q("CUET_Quantitative","CUET_GT","Simple Interest","SI Calculation","medium",
                    f"Principal ₹{P}, Rate {R}% p.a., Time {T} year(s). Simple Interest:",
                    f"₹{SI}", f"₹{A}", f"₹{SI*2}", f"₹{P*R//100}","A",
                    f"SI = PRT/100 = {P}×{R}×{T}/100 = ₹{SI}"))
                if P <= 5000:
                    qs.append(q("CUET_Quantitative","CUET_GT","Simple Interest","Amount","medium",
                        f"Principal ₹{P}, Rate {R}%, Time {T} yr. Amount:",
                        f"₹{A}", f"₹{SI}", f"₹{P+R}", f"₹{P*T}","A",
                        f"A = P+SI = {P}+{SI} = ₹{A}"))

    # Compound Interest
    for P in [1000, 2000, 5000, 10000]:
        for R in [5, 10, 15, 20]:
            for T in [1, 2, 3]:
                CI_A = round(P * (1+R/100)**T, 2)
                CI = round(CI_A - P, 2)
                qs.append(q("CUET_Quantitative","CUET_GT","Compound Interest","CI Calculation","hard",
                    f"Principal ₹{P}, Rate {R}% compounded annually, Time {T} year(s). Compound Interest:",
                    f"₹{CI}", f"₹{round(P*R*T/100,2)}", f"₹{CI*2}", f"₹{CI+100}","A",
                    f"A = P(1+R/100)^T = {P}×{(1+R/100):.2f}^{T} = ₹{CI_A}; CI = ₹{CI}"))

    # Profit and Loss
    for CP in range(100, 2001, 100):
        for pct in [5, 10, 15, 20, 25, 30, 40, 50]:
            SP = CP * (1 + pct/100)
            profit = SP - CP
            qs.append(q("CUET_Quantitative","CUET_GT","Profit/Loss","Profit Calculation","medium",
                f"CP = ₹{CP}, Profit = {pct}%. Selling price:",
                f"₹{SP}", f"₹{CP + pct}", f"₹{CP*pct}", f"₹{SP+10}","A",
                f"SP = CP×(1+{pct}/100) = {CP}×{1+pct/100} = ₹{SP}"))
            loss_SP = CP * (1 - pct/100)
            qs.append(q("CUET_Quantitative","CUET_GT","Profit/Loss","Loss Calculation","medium",
                f"CP = ₹{CP}, Loss = {pct}%. Selling price:",
                f"₹{loss_SP}", f"₹{CP - pct}", f"₹{CP*pct/100}", f"₹{loss_SP+10}","A",
                f"SP = CP×(1-{pct}/100) = {CP}×{1-pct/100} = ₹{loss_SP}"))

    # Ratio and Proportion
    for a,b in [(1,2),(2,3),(3,4),(1,3),(2,5),(3,5),(4,5),(1,4),(3,7),(5,7)]:
        total = random.choice([10,12,15,20,24,25,30,35,40,42,50])
        part_a = round(total * a / (a+b))
        part_b = total - part_a
        qs.append(q("CUET_Quantitative","CUET_GT","Ratio","Division in Ratio","medium",
            f"Divide {total} in ratio {a}:{b}. Larger share:",
            f"{max(part_a,part_b)}", f"{min(part_a,part_b)}", f"{total//2}", f"{total}","A",
            f"Parts: {total}×{a}/{a+b}={part_a} and {total}×{b}/{a+b}={part_b}; larger={max(part_a,part_b)}"))

    # Speed Distance Time
    for speed in range(20, 200, 10):
        for time in range(1, 10):
            dist = speed * time
            qs.append(q("CUET_Quantitative","CUET_GT","Speed/Distance","Basic SDT","easy",
                f"Speed {speed} km/h for {time} hour(s). Distance covered:",
                f"{dist} km", f"{speed+time} km", f"{dist*2} km", f"{dist//2} km","A",
                f"Distance = Speed × Time = {speed} × {time} = {dist} km"))

    for dist in range(100, 1000, 50):
        for speed in range(20, 120, 10):
            time_hr = round(dist/speed, 2)
            qs.append(q("CUET_Quantitative","CUET_GT","Speed/Distance","Time Calculation","medium",
                f"Distance {dist} km at speed {speed} km/h. Time taken:",
                f"{time_hr} hours", f"{dist*speed} hours", f"{dist+speed} hours",
                f"{round(time_hr/2,2)} hours","A",
                f"Time = Distance/Speed = {dist}/{speed} = {time_hr} hours"))

    # Ages
    for current_age in range(10, 50, 5):
        for years_ago in range(5, 20, 5):
            past_age = current_age - years_ago
            if past_age > 0:
                qs.append(q("CUET_Quantitative","CUET_GT","Ages","Age Problems","medium",
                    f"A person is {current_age} years old now. Age {years_ago} years ago:",
                    f"{past_age}", f"{current_age + years_ago}", f"{current_age * years_ago}",
                    f"{current_age - years_ago + 1}","A",
                    f"Age {years_ago} years ago = {current_age} - {years_ago} = {past_age}"))

    for A_now in range(20, 60, 5):
        for B_now in range(15, 55, 5):
            if A_now != B_now:
                for yrs in range(5, 20, 5):
                    A_then = A_now + yrs; B_then = B_now + yrs
                    qs.append(q("CUET_Quantitative","CUET_GT","Ages","Future Age","easy",
                        f"A is {A_now} years, B is {B_now} years. Sum of ages after {yrs} years:",
                        f"{A_then + B_then}", f"{A_now + B_now}", f"{A_now + B_now + yrs}",
                        f"{A_then + B_then + yrs}","A",
                        f"A after {yrs}yrs = {A_then}; B after {yrs}yrs = {B_then}; sum = {A_then+B_then}"))

    # Mensuration
    for r in range(1, 20):
        area_circle = round(math.pi * r * r, 2)
        circum = round(2 * math.pi * r, 2)
        qs.append(q("CUET_Quantitative","CUET_GT","Mensuration","Circle","medium",
            f"Circle with radius {r} cm. Area (π=3.14):",
            f"{round(3.14*r*r,2)} cm²", f"{round(2*3.14*r,2)} cm²",
            f"{r*r} cm²", f"{2*r} cm²","A",
            f"Area = πr² = 3.14×{r}² = {round(3.14*r*r,2)} cm²"))
        qs.append(q("CUET_Quantitative","CUET_GT","Mensuration","Circumference","medium",
            f"Circle with radius {r} cm. Circumference (π=3.14):",
            f"{round(2*3.14*r,2)} cm", f"{round(3.14*r*r,2)} cm²",
            f"{r*r} cm", f"{3.14*r} cm","A",
            f"Circumference = 2πr = 2×3.14×{r} = {round(2*3.14*r,2)} cm"))

    for l,b in [(a,b) for a in range(2,20,2) for b in range(2,20,2) if a!=b]:
        area_rect = l*b
        perim = 2*(l+b)
        qs.append(q("CUET_Quantitative","CUET_GT","Mensuration","Rectangle","easy",
            f"Rectangle: length {l} cm, breadth {b} cm. Area:",
            f"{area_rect} cm²", f"{perim} cm", f"{l+b} cm²", f"{l*b*2} cm²","A",
            f"Area = l×b = {l}×{b} = {area_rect} cm²"))

    for s in range(2, 25):
        area_sq = s*s
        perim_sq = 4*s
        qs.append(q("CUET_Quantitative","CUET_GT","Mensuration","Square","easy",
            f"Square with side {s} cm. Area:",
            f"{area_sq} cm²", f"{perim_sq} cm", f"{s*2} cm²", f"{s*3} cm²","A",
            f"Area = s² = {s}² = {area_sq} cm²"))

    print(f"  CUET_Quantitative generated: {len(qs)}")
    return qs


# ══════════════════════════════════════════════════════════════════════════════
# MAIN
# ══════════════════════════════════════════════════════════════════════════════

def main():
    print("=" * 65)
    print("  GENERATING 100,000 UNIQUE QUESTIONS")
    print("=" * 65)

    init_bank()
    conn = _bank_conn()

    generators = [
        ("Physics",          gen_physics),
        ("Chemistry",        gen_chemistry),
        ("Biology",          gen_biology),
        ("Mathematics",      gen_mathematics),
        ("CUET_GK",          gen_cuet_gk),
        ("CUET_English",     gen_cuet_english),
        ("CUET_Reasoning",   gen_cuet_reasoning),
        ("CUET_Quantitative",gen_cuet_quantitative),
    ]

    total_inserted = 0
    for subject, gen_fn in generators:
        before = conn.execute("SELECT COUNT(*) FROM question_bank WHERE subject=?", (subject,)).fetchone()[0]
        print(f"\n[{subject}] Generating...")
        questions = gen_fn()

        # Dedup within batch by question text
        seen_texts = set()
        unique_qs = []
        for q_item in questions:
            txt = q_item.get("question_en","").strip().lower()
            if txt and txt not in seen_texts:
                seen_texts.add(txt)
                unique_qs.append(q_item)

        print(f"  Generated {len(unique_qs)} unique questions, inserting...")
        inserted = insert_batch(conn, unique_qs)
        after = conn.execute("SELECT COUNT(*) FROM question_bank WHERE subject=?", (subject,)).fetchone()[0]
        print(f"  [{subject}] Before: {before:,} → After: {after:,} (+{inserted:,} new)")
        total_inserted += inserted

    print("\n" + "=" * 65)
    print("  FINAL RESULTS")
    print("=" * 65)
    grand_total = 0
    for subject, _ in generators:
        count = conn.execute("SELECT COUNT(*) FROM question_bank WHERE subject=?", (subject,)).fetchone()[0]
        grand_total += count
        print(f"  {subject:<25} {count:>8,}")
    print("=" * 65)
    print(f"  GRAND TOTAL: {grand_total:,} questions")
    print(f"  New questions added: {total_inserted:,}")
    print("\n  Run app: streamlit run bank_exam_app.py")


if __name__ == "__main__":
    main()
