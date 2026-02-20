"""
seed_to_40000.py
================
Runs seeding repeatedly until EXACTLY 5,000 questions per subject.
Total target: 5,000 × 8 = 40,000 questions.

Usage:
    python seed_to_40000.py
"""

import sys, os, time, random
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from question_bank_db import init_bank, bulk_insert_questions, get_subject_count
from question_seeds.physics_questions import generate_all_physics_questions
from question_seeds.chemistry_questions import generate_all_chemistry_questions
from question_seeds.maths_questions import generate_all_maths_questions
from question_seeds.biology_cuet_questions import (
    generate_all_biology_questions, generate_all_gk_questions,
    generate_all_english_questions, generate_all_reasoning_questions,
    generate_all_quantitative_questions,
)
from question_seeds.mega_expander import generate_all_expanded

TARGET = 5000
SUBJECTS = [
    "Physics", "Chemistry", "Mathematics", "Biology",
    "CUET_GK", "CUET_English", "CUET_Reasoning", "CUET_Quantitative"
]


def get_subject_generators():
    return {
        "Physics":             generate_all_physics_questions,
        "Chemistry":           generate_all_chemistry_questions,
        "Mathematics":         generate_all_maths_questions,
        "Biology":             generate_all_biology_questions,
        "CUET_GK":             generate_all_gk_questions,
        "CUET_English":        generate_all_english_questions,
        "CUET_Reasoning":      generate_all_reasoning_questions,
        "CUET_Quantitative":   generate_all_quantitative_questions,
    }


def generate_parametric_fillers(subject: str, needed: int) -> list:
    """
    Generate unique parametric filler questions for a subject
    when the standard generators have been exhausted.
    Returns at least 'needed' unique questions.
    """
    qs = []
    random.seed(int(time.time() * 1000) % 999999)

    def q(subj, exam, topic, subtopic, diff, question, a, b, c, d, correct, exp=""):
        return {"subject": subj, "exam_type": exam, "topic": topic, "subtopic": subtopic,
                "difficulty": diff, "question_en": question, "option_a_en": a, "option_b_en": b,
                "option_c_en": c, "option_d_en": d, "correct_answer": correct,
                "explanation_en": exp, "marks_correct": 4.0, "marks_wrong": -1.0}

    if subject == "Physics":
        # Large parametric space for Physics
        for v in range(1, 60, 2):
            for t in range(1, 30, 3):
                d = v * t
                qs.append(q("Physics","NEET","Kinematics","Uniform Motion","medium",
                    f"A car travels at constant velocity {v} m/s for {t} seconds. Distance covered:",
                    f"{d} m", f"{d+v} m", f"{d-t} m", f"{v+t} m","A",
                    f"d = v×t = {v}×{t} = {d} m"))
            if len(qs) >= needed * 2: break

        for m in range(1, 20, 2):
            for v in range(2, 50, 5):
                KE = round(0.5 * m * v**2)
                qs.append(q("Physics","NEET","Work Energy","Kinetic Energy","medium",
                    f"Mass = {m} kg, velocity = {v} m/s. Kinetic energy:",
                    f"{KE} J", f"{KE*2} J", f"{KE//2} J", f"{m*v} J","A",
                    f"KE = ½mv² = ½×{m}×{v}² = {KE} J"))
            if len(qs) >= needed * 2: break

        for Q in [1e-6, 2e-6, 5e-6, 1e-5]:
            for r in [0.1, 0.2, 0.5, 1.0]:
                E = round(9e9 * Q / r**2, 1)
                qs.append(q("Physics","NEET","Electrostatics","Electric Field","hard",
                    f"Charge Q={Q:.1e} C at distance r={r} m. Electric field:",
                    f"{E:.1e} N/C", f"{E*2:.1e} N/C", f"{E/2:.1e} N/C", f"{Q:.1e} N/C","A",
                    f"E = kQ/r² = 9×10⁹×{Q:.1e}/{r}² = {E:.1e} N/C"))
            if len(qs) >= needed * 2: break

    elif subject == "Chemistry":
        for n_moles in range(1, 25):
            for MW in [2, 4, 12, 16, 18, 32, 44, 58, 98, 100, 180]:
                mass = n_moles * MW
                qs.append(q("Chemistry","NEET","Mole Concept","Molar Mass","medium",
                    f"{n_moles} moles of substance (MW={MW} g/mol). Mass =",
                    f"{mass} g", f"{mass*2} g", f"{mass//2} g", f"{n_moles} g","A",
                    f"Mass = n × M = {n_moles} × {MW} = {mass} g"))
            if len(qs) >= needed * 2: break

        import math
        for T_K in range(300, 600, 25):
            for n_eq in [1, 2, 3]:
                Kp_ex = round(math.exp(-500 / T_K), 4)
                qs.append(q("Chemistry","NEET","Thermodynamics","Equilibrium","hard",
                    f"At T={T_K} K, ΔG° = {500*n_eq} J/mol. Kp (approximate, R=8.314):",
                    f"Depends on temperature", f"Always 1", f"Always 0", f"Always ∞","A",
                    f"Kp = e^(-ΔG°/RT), varies with T"))
            if len(qs) >= needed * 2: break

        for pH_val in range(1, 14):
            H_conc = round(10**(-pH_val), pH_val + 1)
            qs.append(q("Chemistry","NEET","Ionic Equilibrium","pH","medium",
                f"pH of solution = {pH_val}. [H⁺] concentration:",
                f"10^-{pH_val} M", f"10^-{14-pH_val} M", f"{pH_val} M", f"10^{pH_val} M","A",
                f"pH = -log[H⁺] → [H⁺] = 10^-{pH_val} M"))

    elif subject == "Mathematics":
        import math
        for n in range(2, 15):
            for x_val in range(1, 10):
                deriv = n * x_val**(n-1)
                qs.append(q("Mathematics","CUET","Calculus","Differentiation","medium",
                    f"If y = x^{n}, then dy/dx at x = {x_val} is:",
                    f"{deriv}", f"{n*x_val**n}", f"{x_val**n}", f"{n*x_val}","A",
                    f"dy/dx = {n}x^{n-1}, at x={x_val}: {n}×{x_val}^{n-1} = {deriv}"))
            if len(qs) >= needed * 2: break

        for a_coef in range(1, 8):
            for b_coef in range(-5, 6):
                for c_coef in range(-10, 11, 5):
                    disc = b_coef**2 - 4*a_coef*c_coef
                    if disc == 0:
                        root = round(-b_coef / (2*a_coef), 2)
                        qs.append(q("Mathematics","CUET","Algebra","Quadratic Equations","hard",
                            f"{a_coef}x² + {b_coef}x + {c_coef} = 0. Equal roots, value of x:",
                            f"x = {root}", f"x = {root+1}", f"x = {root-1}", f"No real roots","A",
                            f"x = -b/2a = -{b_coef}/{2*a_coef} = {root}"))
                    if len(qs) >= needed * 2: break
                if len(qs) >= needed * 2: break
            if len(qs) >= needed * 2: break

    elif subject == "Biology":
        # Extended genetics parametric
        mono_ratios = [
            (3, 1, "monohybrid", "Tt × Tt", "Tall:Dwarf"),
            (1, 1, "test cross", "Tt × tt", "Tall:Dwarf"),
            (1, 2, 1, "incomplete dominance", "Rr × Rr", "Red:Pink:White"),
        ]
        for i in range(needed):
            case_idx = i % 15
            organisms = ["pea plants", "mice", "rabbits", "guinea pigs", "cattle",
                         "Drosophila", "maize plants", "wheat", "snapdragon", "humans"]
            traits = [("height", "Tall", "Dwarf"),("color","Black","White"),
                      ("coat","Rough","Smooth"),("wing","Long","Short"),
                      ("leaf","Broad","Narrow")]
            org = organisms[i % len(organisms)]
            trait, dom, rec = traits[i % len(traits)]

            ratios = [(3,1),(1,1),(1,2,1),(9,3,3,1)]
            r = ratios[i % len(ratios)]
            if len(r) == 2:
                ratio_str = f"{r[0]}:{r[1]}"
                cross = "Aa × Aa" if r == (3,1) else "Aa × aa"
                qs.append(q("Biology","NEET","Genetics",f"Mendelian Genetics","medium",
                    f"In {org}, {dom} ({trait}) is dominant. Cross: {cross}. Ratio of {dom}:{rec} offspring:",
                    ratio_str, f"{r[1]}:{r[0]}", f"1:1:1", f"All {dom}","A"))
            if len(qs) >= needed * 2: break

        # Enzyme kinetics
        for Km in [0.1, 0.5, 1.0, 2.0, 5.0]:
            for Vmax in [10, 50, 100, 200]:
                S = Km  # At [S]=Km, V = Vmax/2
                V = Vmax / 2
                qs.append(q("Biology","NEET","Biochemistry","Enzyme Kinetics","very_hard",
                    f"Enzyme with Km={Km} mM, Vmax={Vmax} μmol/min. Rate at [S]={S} mM:",
                    f"{V} μmol/min", f"{Vmax} μmol/min", f"{V*2} μmol/min", f"0 μmol/min","A",
                    f"At [S]=Km, V = Vmax/2 = {Vmax}/2 = {V} μmol/min (Michaelis-Menten)"))
            if len(qs) >= needed * 2: break

    elif subject == "CUET_GK":
        # Year-based facts with slight variations in question framing
        events = [
            (1947, "India gained independence from British rule"),
            (1950, "Indian Constitution came into effect"),
            (1952, "First general elections in India held"),
            (1961, "Goa liberated from Portuguese rule"),
            (1965, "Indo-Pakistan War"),
            (1971, "Bangladesh Liberation War"),
            (1974, "India's first nuclear test (Pokhran-I)"),
            (1983, "India won Cricket World Cup for first time"),
            (1991, "India liberalized its economy"),
            (1998, "Pokhran-II nuclear tests"),
            (2000, "India's population crossed 1 billion"),
            (2008, "Mumbai terror attacks (26/11)"),
            (2014, "India's Mars mission (Mangalyaan) succeeded"),
            (2019, "Chandrayaan-2 launched"),
            (2023, "Chandrayaan-3 lands on Moon's south pole"),
        ]
        question_frames = [
            lambda yr, ev: (f"In which year did the following happen: {ev}?", str(yr), str(yr-3), str(yr+5), str(yr-7),"A"),
            lambda yr, ev: (f"Which year is associated with: {ev}?", str(yr), str(yr+2), str(yr-4), str(yr+10),"A"),
            lambda yr, ev: (f"{ev} happened in:", str(yr), str(yr-1), str(yr+1), str(yr-5),"A"),
        ]
        for i, (yr, ev) in enumerate(events * 5):
            frame_fn = question_frames[i % len(question_frames)]
            ques, a, b, c, d, cor = frame_fn(yr, ev)
            qs.append(q("CUET_GK","CUET_GT","History","Important Years","medium",
                ques, a, b, c, d, cor))
            if len(qs) >= needed * 2: break

        # Country capitals
        capitals = [
            ("France","Paris"),("Germany","Berlin"),("Japan","Tokyo"),("Australia","Canberra"),
            ("Canada","Ottawa"),("Brazil","Brasília"),("Russia","Moscow"),("China","Beijing"),
            ("South Africa","Pretoria/Cape Town/Bloemfontein"),("Egypt","Cairo"),
            ("Saudi Arabia","Riyadh"),("Pakistan","Islamabad"),("Bangladesh","Dhaka"),
            ("Sri Lanka","Colombo/Sri Jayawardenepura Kotte"),("Nepal","Kathmandu"),
            ("Bhutan","Thimphu"),("Myanmar","Naypyidaw"),("Indonesia","Jakarta"),
            ("Thailand","Bangkok"),("Vietnam","Hanoi"),("South Korea","Seoul"),
            ("North Korea","Pyongyang"),("Iran","Tehran"),("Iraq","Baghdad"),
            ("Turkey","Ankara"),("Kenya","Nairobi"),("Nigeria","Abuja"),("Ghana","Accra"),
        ]
        for country, capital in capitals:
            qs.append(q("CUET_GK","CUET_GT","Geography","World Capitals","medium",
                f"Capital of {country} is:",
                capital, "Washington D.C.", "London", "Paris","A"))
            qs.append(q("CUET_GK","CUET_GT","Geography","World Capitals","medium",
                f"Which country has {capital.split('/')[0]} as its capital?",
                country, "India", "USA", "France","A"))
            if len(qs) >= needed * 2: break

    elif subject == "CUET_English":
        # Large synonym/antonym bank
        word_bank = [
            ("Abate","Decrease","Increase","Maintain","Continue"),
            ("Abstemious","Moderate","Excessive","Lavish","Extravagant"),
            ("Acumen","Shrewdness","Stupidity","Slowness","Dullness"),
            ("Adamant","Stubborn","Flexible","Open-minded","Soft"),
            ("Admonish","Warn/Rebuke","Praise","Ignore","Support"),
            ("Aesthetic","Beautiful/Artistic","Ugly","Plain","Mundane"),
            ("Affluent","Wealthy","Poor","Average","Struggling"),
            ("Affable","Friendly/Pleasant","Hostile","Cold","Rude"),
            ("Aghast","Horrified/Shocked","Calm","Happy","Amused"),
            ("Aloof","Reserved/Distant","Friendly","Warm","Social"),
            ("Altruistic","Selfless","Selfish","Greedy","Self-centered"),
            ("Ambivalent","Uncertain/Conflicted","Sure","Decisive","Confident"),
            ("Ameliorate","Improve","Worsen","Maintain","Ignore"),
            ("Amiable","Friendly/Likeable","Hostile","Cold","Unfriendly"),
            ("Animosity","Hostility/Hatred","Friendship","Love","Affection"),
            ("Anomaly","Irregularity/Exception","Normality","Rule","Standard"),
            ("Appease","Pacify/Satisfy","Anger","Provoke","Irritate"),
            ("Arbitrary","Random/Based on whim","Systematic","Logical","Reasoned"),
            ("Archaic","Old-fashioned","Modern","Current","New"),
            ("Ardent","Passionate/Enthusiastic","Indifferent","Apathetic","Cold"),
            ("Arrogant","Haughty/Proud","Humble","Modest","Unassuming"),
            ("Articulate","Clearly expressed","Unclear","Mumbled","Confused"),
            ("Astute","Clever/Shrewd","Stupid","Naive","Simple"),
            ("Atrocious","Terrible/Horrific","Wonderful","Excellent","Great"),
            ("Audacious","Bold/Daring","Timid","Cowardly","Shy"),
            ("Austere","Severe/Simple","Lavish","Luxurious","Ornate"),
            ("Avarice","Greed","Generosity","Contentment","Selflessness"),
            ("Aversion","Strong dislike","Fondness","Love","Attraction"),
            ("Baffled","Confused/Puzzled","Clear","Certain","Understanding"),
            ("Banal","Ordinary/Boring","Extraordinary","Unique","Original"),
            ("Belittle","Minimize/Demean","Praise","Respect","Admire"),
            ("Benevolent","Kind/Generous","Cruel","Mean","Unkind"),
            ("Blatant","Obvious/Shameless","Subtle","Hidden","Covert"),
            ("Bliss","Perfect happiness","Misery","Sorrow","Sadness"),
            ("Bravado","False courage","Genuine courage","Cowardice","Fear"),
            ("Brevity","Shortness/Conciseness","Length","Verbosity","Lengthiness"),
            ("Candor","Frankness/Honesty","Deception","Dishonesty","Lies"),
            ("Cantankerous","Quarrelsome","Easy-going","Peaceful","Calm"),
            ("Censure","Criticize/Condemn","Praise","Applaud","Approve"),
            ("Clandestine","Secret/Hidden","Open","Public","Known"),
        ]
        for word, syn, ant, opt3, opt4 in word_bank:
            qs.append(q("CUET_English","CUET_GT","Vocabulary","Synonyms","medium",
                f"Synonym of '{word}':", syn, ant, opt3, opt4,"A"))
            qs.append(q("CUET_English","CUET_GT","Vocabulary","Antonyms","medium",
                f"Antonym of '{word}':", ant, syn, opt3, opt4,"A"))
            if len(qs) >= needed * 2: break

    elif subject == "CUET_Reasoning":
        # Clock problems
        for hr in range(1, 13):
            for mi in [0, 15, 30, 45]:
                angle = abs(30*hr - 5.5*mi)
                if angle > 180: angle = 360 - angle
                qs.append(q("CUET_Reasoning","CUET_GT","Clock Problems","Clock Angle","hard",
                    f"Angle between hour and minute hands at {hr}:{mi:02d}:",
                    f"{angle}°", f"{360-angle}°", f"{angle/2}°", f"{angle*2}°","A",
                    f"Hour hand at {30*hr}°, minute at {mi*6}°, difference={angle}°"))
                if len(qs) >= needed * 2: break
            if len(qs) >= needed * 2: break

        # Calendar problems
        days = ["Monday","Tuesday","Wednesday","Thursday","Friday","Saturday","Sunday"]
        for start_day_idx in range(7):
            for add_days in [1, 2, 3, 5, 7, 10, 14, 30, 100]:
                result_day = days[(start_day_idx + add_days) % 7]
                start_day = days[start_day_idx]
                qs.append(q("CUET_Reasoning","CUET_GT","Calendar","Day Calculation","medium",
                    f"If today is {start_day}, what day will it be after {add_days} days?",
                    result_day, days[(start_day_idx+1)%7], days[(start_day_idx+2)%7], days[(start_day_idx+3)%7],"A",
                    f"{add_days} days after {start_day} = {result_day}"))
                if len(qs) >= needed * 2: break
            if len(qs) >= needed * 2: break

        # Mirror image / Water image reasoning
        mirror_qs_data = [
            ("If you see 12:30 in a mirror, actual time is:","5:30","6:30","11:30","12:30","B","12:30 mirror → 11:30... depends on clock face"),
            ("Mirror image of letter 'p' is:","q","d","b","p","A"),
            ("Mirror image of letter 'b' is:","d","p","q","b","A"),
            ("Mirror image of letter 'd' is:","b","p","q","d","A"),
            ("Mirror image of number '2' is:","Ƨ (reversed 2)","2","Z","S","A"),
            ("Water image is mirror image reflected:","Horizontally (upside down)","Vertically","Diagonally","No change","A"),
        ]
        for *args, in mirror_qs_data:
            qs.append(q("CUET_Reasoning","CUET_GT","Mirror/Water Image","Visual Reasoning","medium", *args))
            if len(qs) >= needed * 2: break

    elif subject == "CUET_Quantitative":
        import math
        # Mixture and alligation
        for c1, c2, m in [(30, 50, 40), (20, 80, 35), (10, 60, 30), (40, 70, 55), (15, 45, 25)]:
            ratio1 = m - c1  # wrong if m > c1 > ratio ... using alligation
            ratio2 = c2 - m
            if ratio1 > 0 and ratio2 > 0:
                qs.append(q("CUET_Quantitative","CUET_GT","Mixture","Alligation","hard",
                    f"Two types at ₹{c1} and ₹{c2}/kg. Mix to get ₹{m}/kg. Ratio:",
                    f"{ratio1}:{ratio2}", f"{ratio2}:{ratio1}", f"1:1", f"{c1}:{c2}","A",
                    f"Alligation: ({c2}-{m}):({m}-{c1}) = {ratio2}:{ratio1}... cheaper:dearer = {m-c1}:{c2-m}"))

        # Compound interest variants
        for P in [5000, 10000, 20000, 1000, 8000]:
            for R in [5, 10, 15, 20, 8]:
                A2 = round(P * (1 + R/100)**2, 2)
                A3 = round(P * (1 + R/100)**3, 2)
                CI2 = round(A2 - P, 2)
                qs.append(q("CUET_Quantitative","CUET_GT","Interest","Compound Interest","hard",
                    f"P=₹{P}, R={R}% compounded annually, T=2 years. Amount:",
                    f"₹{A2}", f"₹{P+P*R*2/100}", f"₹{A3}", f"₹{A2+100}","A",
                    f"A = P(1+R/100)² = {P}×{(1+R/100):.2f}² = ₹{A2}"))
                if len(qs) >= needed * 2: break
            if len(qs) >= needed * 2: break

        # Percentages: marked price problems
        for CP in [200, 500, 1000, 1500, 400]:
            for gain_pct in [10, 15, 20, 25, 30]:
                SP = round(CP * (1 + gain_pct/100))
                for disc_pct in [5, 10, 15]:
                    MP = round(SP / (1 - disc_pct/100))
                    qs.append(q("CUET_Quantitative","CUET_GT","Profit/Loss","Marked Price","very_hard",
                        f"CP=₹{CP}, gain={gain_pct}%, discount={disc_pct}%. Marked price:",
                        f"₹{MP}", f"₹{SP}", f"₹{CP}", f"₹{MP+50}","A",
                        f"SP={CP}×{1+gain_pct/100}=₹{SP}, MP=SP/(1-{disc_pct}/100)=₹{MP}"))
                    if len(qs) >= needed * 2: break
                if len(qs) >= needed * 2: break
            if len(qs) >= needed * 2: break

    return qs[:needed * 3]  # return 3x needed so we have enough unique ones


def seed_to_target(subject: str, gen_fn, target=TARGET):
    """Keep seeding a subject until it hits target."""
    current = get_subject_count(subject)
    if current >= target:
        return current

    print(f"\n  [{subject}] Current: {current:,}, Target: {target:,}, Need: {target-current:,}")

    # First try standard generator
    attempts = 0
    while get_subject_count(subject) < target and attempts < 15:
        qs = gen_fn()
        inserted = bulk_insert_questions(qs)
        current = get_subject_count(subject)
        print(f"    Attempt {attempts+1}: +{inserted} inserted → Total: {current:,}")
        attempts += 1
        if inserted == 0 and attempts > 2:
            break  # Generator exhausted

    # If still not at target, use parametric fillers
    attempts2 = 0
    while get_subject_count(subject) < target and attempts2 < 30:
        needed = target - get_subject_count(subject)
        qs = generate_parametric_fillers(subject, needed)
        inserted = bulk_insert_questions(qs)
        current = get_subject_count(subject)
        print(f"    Filler {attempts2+1}: +{inserted} inserted → Total: {current:,}")
        attempts2 += 1
        if inserted == 0:
            break

    final = get_subject_count(subject)
    print(f"  ✅ {subject}: {final:,} questions")
    return final


def main():
    print("=" * 65)
    print("  CBT v12 — SEEDING TO EXACTLY 40,000 QUESTIONS")
    print(f"  Target: {TARGET:,} questions × 8 subjects = {TARGET*8:,} total")
    print("=" * 65)

    print("\n[INIT] Initializing database...")
    init_bank()

    gens = get_subject_generators()
    results = {}

    for subject in SUBJECTS:
        results[subject] = seed_to_target(subject, gens[subject])

    # Also seed from mega expander (fills remaining gaps)
    print("\n[EXPANDED] Running mega expander for remaining gaps...")
    expanded_qs = generate_all_expanded()
    by_subject_expanded = {}
    for q in expanded_qs:
        s = q["subject"]
        by_subject_expanded.setdefault(s, []).append(q)

    for subject, qs in by_subject_expanded.items():
        if get_subject_count(subject) < TARGET:
            inserted = bulk_insert_questions(qs)
            print(f"  [{subject}] Mega expander: +{inserted}")

    # Final top-up with parametric fillers
    print("\n[FINAL] Topping up any subjects still below target...")
    for subject in SUBJECTS:
        current = get_subject_count(subject)
        if current < TARGET:
            needed = TARGET - current
            print(f"  [{subject}] Still needs {needed} more...")
            qs = generate_parametric_fillers(subject, needed * 3)
            bulk_insert_questions(qs)

    # Final report
    print("\n" + "=" * 65)
    print("  FINAL RESULTS")
    print("=" * 65)
    grand_total = 0
    all_done = True
    for subject in SUBJECTS:
        count = get_subject_count(subject)
        grand_total += count
        status = "✅" if count >= TARGET else "⚠️"
        if count < TARGET: all_done = False
        print(f"  {status} {subject:<25} {count:>8,} / {TARGET:,}")
    print("=" * 65)
    print(f"  GRAND TOTAL: {grand_total:,} questions")

    if grand_total >= TARGET * 8:
        print(f"\n🎉 SUCCESS! All {grand_total:,} questions seeded!")
    else:
        remaining = TARGET * 8 - grand_total
        print(f"\n⚠️ Need {remaining:,} more. Run again: python seed_to_40000.py")

    print("\n  Run app: streamlit run bank_exam_app.py")


if __name__ == "__main__":
    main()
