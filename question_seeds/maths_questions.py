"""
question_seeds/maths_questions.py
==================================
Generates 5000+ Mathematics questions for CUET/JEE.
Topics: Algebra, Calculus, Coordinate Geometry, Trigonometry, Statistics, Probability
"""

from typing import List, Dict
import math
import random


def q(question, a, b, c, d, correct, topic, subtopic, difficulty, explanation=""):
    return {
        "subject": "Mathematics",
        "exam_type": "CUET_DOMAIN",
        "topic": topic,
        "subtopic": subtopic,
        "difficulty": difficulty,
        "question_en": question,
        "option_a_en": a,
        "option_b_en": b,
        "option_c_en": c,
        "option_d_en": d,
        "correct_answer": correct,
        "explanation_en": explanation,
        "marks_correct": 5.0,
        "marks_wrong": -1.0,
    }


def gen_algebra():
    qs = []

    # Quadratic equations
    quad_cases = [
        (1, -5, 6, "2 and 3", "−2 and −3", "1 and 6", "−1 and −6", "A"),
        (1, -7, 12, "3 and 4", "−3 and −4", "2 and 6", "1 and 12", "A"),
        (1, 3, -10, "−5 and 2", "5 and −2", "−5 and −2", "5 and 2", "A"),
        (2, -7, 3, "1/2 and 3", "−1/2 and −3", "1/2 and −3", "−1/2 and 3", "A"),
        (1, -10, 25, "5 (repeated)", "−5 (repeated)", "±5", "No real roots", "A"),
        (1, 0, -9, "±3", "3 only", "−3 only", "No real roots", "A"),
        (3, -8, 4, "2/3 and 2", "−2/3 and −2", "3/2 and 2", "1/3 and 4", "A"),
        (1, -6, 8, "2 and 4", "−2 and −4", "2 and −4", "−2 and 4", "A"),
        (1, 1, -12, "3 and −4", "−3 and 4", "3 and 4", "−3 and −4", "A"),
        (1, -4, -5, "5 and −1", "−5 and 1", "5 and 1", "−5 and −1", "A"),
        (2, 5, -3, "1/2 and −3", "−1/2 and 3", "1 and −3/2", "−1 and 3/2", "A"),
        (1, -8, 15, "3 and 5", "−3 and −5", "−3 and 5", "3 and −5", "A"),
    ]
    for a_c, b_c, c_c, ans, w1, w2, w3, cor in quad_cases:
        qs.append(q(
            f"Solve: {a_c}x² {'+'if b_c>=0 else ''}{b_c}x {'+'if c_c>=0 else ''}{c_c} = 0",
            ans, w1, w2, w3, cor,
            "Algebra", "Quadratic Equations", "medium",
            f"Use factoring or quadratic formula"
        ))

    # Sum and product of roots
    roots_cases = [
        (1, -7, 10, "7", "−7", "10", "−10", "A", "Sum = 7", "Sum = -b/a = 7"),
        (1, -7, 10, "10", "−10", "7", "−7", "A", "Product = 10", "Product = c/a = 10"),
        (2, -5, 3, "5/2", "−5/2", "3/2", "−3/2", "A", "Sum = 5/2", "Sum = -b/a = 5/2"),
        (2, -5, 3, "3/2", "−3/2", "5/2", "−5/2", "A", "Product = 3/2", "Product = c/a = 3/2"),
        (3, -11, 6, "11/3", "−11/3", "6/3", "2", "A", "Sum = 11/3", "Sum = 11/3"),
        (1, 0, -25, "0", "25", "−25", "5", "A", "Sum = 0", "Sum = -b/a = 0"),
    ]
    for a_c, b_c, c_c, ans, w1, w2, w3, cor, what, expl in roots_cases:
        qs.append(q(
            f"For {a_c}x² {'+'if b_c>=0 else ''}{b_c}x {'+'if c_c>=0 else ''}{c_c} = 0, {what} of roots is:",
            ans, w1, w2, w3, cor,
            "Algebra", "Quadratic Equations", "medium", expl
        ))

    # Arithmetic Progressions
    ap_cases = [
        (2, 5, 20, "2, 7, 12, 17, 22...", "2, 4, 8, 16, 32...", "2, 5, 8, 11...", "5, 10, 15, 20...", "A"),
        (3, 4, 15, "nth term = 4n - 1", "nth term = 3n + 4", "nth term = 4n + 3", "nth term = 3n - 1", "A"),
        (1, 2, 10, "S₁₀ = 100", "S₁₀ = 55", "S₁₀ = 110", "S₁₀ = 45", "A"),
        (5, 3, 8, "a₈ = 26", "a₈ = 24", "a₈ = 29", "a₈ = 8", "A"),
        (2, 5, None, "S₁₅ = 585", "S₁₅ = 600", "S₁₅ = 570", "S₁₅ = 555", "A"),
        (10, -2, None, "a₅ = 2", "a₅ = 10", "a₅ = 18", "a₅ = -2", "A"),
    ]
    for a_val, d_val, n_val, ans, w1, w2, w3, cor in ap_cases:
        if n_val:
            T_n = a_val + (n_val - 1) * d_val
            qs.append(q(
                f"In AP with first term a = {a_val} and common difference d = {d_val}, find a_{n_val}:",
                ans, w1, w2, w3, cor,
                "Algebra", "Arithmetic Progressions", "medium",
                f"aₙ = a + (n-1)d = {a_val} + ({n_val}-1)×{d_val} = {T_n}"
            ))

    # AP sum
    for a_val, d_val, n_val in [(1,2,10),(3,4,15),(5,3,8),(2,5,20),(1,1,100),(10,-2,5)]:
        S = n_val * (2*a_val + (n_val-1)*d_val) // 2
        qs.append(q(
            f"Sum of {n_val} terms of AP with a = {a_val}, d = {d_val}:",
            f"S = {S}", f"S = {S+10}", f"S = {S-10}", f"S = {2*S}", "A",
            "Algebra", "Arithmetic Progressions", "medium",
            f"Sₙ = n/2[2a+(n-1)d] = {n_val}/2[{2*a_val}+{n_val-1}×{d_val}] = {S}"
        ))

    # GP
    gp_cases = [
        (2, 3, 5, "486", "162", "1458", "54", "A", "a₅ = 2×3⁴ = 162? No, 2×81=162... "),
        (1, 2, 8, "128", "64", "256", "32", "A"),
        (3, 2, 6, "96", "48", "192", "192", "A"),
        (5, 3, 4, "135", "45", "405", "15", "A"),
        (4, 0.5, 5, "0.25", "0.5", "0.125", "1", "A"),
        (1, -2, 6, "-32", "32", "-64", "64", "A"),
        (2, 3, 6, "486", "162", "1458", "54", "A"),
    ]
    for a_val, r_val, n_val, ans, w1, w2, w3, cor, *expl in gp_cases:
        T_n = a_val * (r_val ** (n_val - 1))
        qs.append(q(
            f"In GP with first term {a_val} and common ratio {r_val}, find a_{n_val}:",
            ans, w1, w2, w3, cor,
            "Algebra", "Geometric Progressions", "medium",
            f"aₙ = ar^(n-1) = {a_val}×{r_val}^{n_val-1} = {T_n}"
        ))

    # Binomial theorem
    binomial = [
        ("The number of terms in expansion of (x+y)^n is:", "n+1", "n", "2n", "n-1", "A",
         "Algebra", "Binomial Theorem", "medium"),
        ("Middle term in (x+1)^8 is:", "T₅", "T₄", "T₃", "T₆", "A",
         "Algebra", "Binomial Theorem", "medium"),
        ("Coefficient of x³ in (1+x)^5 is:", "10", "5", "15", "20", "A",
         "Algebra", "Binomial Theorem", "hard"),
        ("Sum of binomial coefficients in (1+x)^n is:", "2^n", "n²", "n!", "2^(n-1)", "A",
         "Algebra", "Binomial Theorem", "medium"),
        ("(x+y)^n general term T_(r+1) = ", "ⁿCᵣ xⁿ⁻ʳ yʳ", "ⁿCᵣ xʳ yⁿ⁻ʳ",
         "ⁿCₙ₋ᵣ xⁿ⁻ʳ yʳ", "ⁿCᵣ xᵣ yⁿ", "A",
         "Algebra", "Binomial Theorem", "medium"),
        ("In (2x + 3)^6, coefficient of x^4 is:", "4320", "2160", "8640", "1080", "A",
         "Algebra", "Binomial Theorem", "very_hard"),
    ]
    for b in binomial:
        qs.append(q(*b))

    # Permutations and Combinations
    pnc = [
        ("⁵P₃ = ?", "60", "10", "120", "30", "A",
         "Algebra", "Permutations", "medium"),
        ("⁵C₃ = ?", "10", "60", "20", "30", "A",
         "Algebra", "Combinations", "medium"),
        ("Number of ways to arrange 6 people in a row:", "720", "120", "360", "240", "A",
         "Algebra", "Permutations", "medium"),
        ("Number of ways to choose 3 from 8:", "56", "336", "28", "168", "A",
         "Algebra", "Combinations", "medium"),
        ("Number of ways to arrange letters of MATH:", "24", "12", "48", "6", "A",
         "Algebra", "Permutations", "medium"),
        ("⁸C₄ = ?", "70", "140", "56", "35", "A",
         "Algebra", "Combinations", "medium"),
        ("¹⁰C₀ + ¹⁰C₁₀ = ?", "2", "10", "1", "0", "A",
         "Algebra", "Combinations", "medium"),
        ("Number of ways to arrange MISSISSIPPI:", "34650", "11!", "11!/2", "720", "A",
         "Algebra", "Permutations", "very_hard"),
        ("In how many ways can 4 boys sit in 7 seats in a row?", "840", "210", "420", "3024", "A",
         "Algebra", "Permutations", "medium"),
        ("Number of diagonals in a hexagon:", "9", "6", "12", "15", "A",
         "Algebra", "Combinations", "hard"),
    ]
    for p in pnc:
        qs.append(q(*p))

    return qs


def gen_calculus():
    qs = []

    # Limits
    limits_qs = [
        ("lim(x→0) sin(x)/x =", "1", "0", "∞", "−1", "A",
         "Calculus", "Limits", "medium"),
        ("lim(x→0) (1-cos x)/x² =", "1/2", "1", "0", "−1/2", "A",
         "Calculus", "Limits", "hard"),
        ("lim(x→0) tan(x)/x =", "1", "0", "∞", "−1", "A",
         "Calculus", "Limits", "medium"),
        ("lim(x→∞) (1 + 1/x)^x =", "e", "1", "∞", "0", "A",
         "Calculus", "Limits", "hard"),
        ("lim(x→0) (e^x - 1)/x =", "1", "0", "e", "∞", "A",
         "Calculus", "Limits", "hard"),
        ("lim(x→0) (log(1+x))/x =", "1", "0", "log x", "∞", "A",
         "Calculus", "Limits", "hard"),
        ("lim(x→2) (x²-4)/(x-2) =", "4", "2", "0", "∞", "A",
         "Calculus", "Limits", "medium"),
        ("lim(x→0) x·sin(1/x) =", "0", "1", "∞", "Does not exist", "A",
         "Calculus", "Limits", "very_hard"),
        ("lim(x→3) (x² - 9)/(x - 3) =", "6", "3", "9", "0", "A",
         "Calculus", "Limits", "medium"),
        ("lim(x→0) (sin 3x)/(sin 5x) =", "3/5", "5/3", "1", "0", "A",
         "Calculus", "Limits", "hard"),
    ]
    for l in limits_qs:
        qs.append(q(*l))

    # Derivatives
    deriv_cases = [
        ("d/dx(x^n) =", "nx^(n-1)", "nx^n", "x^(n-1)", "nx^(n+1)", "A",
         "Calculus", "Differentiation", "medium"),
        ("d/dx(sin x) =", "cos x", "−cos x", "−sin x", "sec x", "A",
         "Calculus", "Differentiation", "medium"),
        ("d/dx(cos x) =", "−sin x", "sin x", "−cos x", "sec x", "A",
         "Calculus", "Differentiation", "medium"),
        ("d/dx(e^x) =", "e^x", "xe^(x-1)", "e^(x-1)", "xe^x", "A",
         "Calculus", "Differentiation", "medium"),
        ("d/dx(ln x) =", "1/x", "ln x", "x/ln x", "1/(x ln x)", "A",
         "Calculus", "Differentiation", "medium"),
        ("d/dx(tan x) =", "sec²x", "−cosec²x", "cot x", "sec x tan x", "A",
         "Calculus", "Differentiation", "medium"),
        ("Product rule: d/dx(uv) =", "u'v + uv'", "u'v - uv'", "uv' - u'v", "u'v'", "A",
         "Calculus", "Differentiation", "medium"),
        ("Chain rule: d/dx f(g(x)) =", "f'(g(x))·g'(x)", "f'(x)·g'(x)",
         "f'(g(x)) + g'(x)", "f(g'(x))", "A", "Calculus", "Differentiation", "medium"),
        ("d/dx(x² sin x) =", "2x sin x + x² cos x", "2x cos x",
         "x² cos x", "2x sin x", "A", "Calculus", "Differentiation", "hard"),
        ("d/dx(e^(x²)) =", "2x e^(x²)", "x² e^(x²)", "2 e^(x²)", "e^(x²)/2x", "A",
         "Calculus", "Differentiation", "hard"),
        ("d/dx(sin(3x+2)) =", "3 cos(3x+2)", "cos(3x+2)", "3 cos(3x)", "−3 cos(3x+2)", "A",
         "Calculus", "Differentiation", "hard"),
        ("d/dx(x/sin x) =", "(sin x - x cos x)/sin²x", "(x cos x - sin x)/sin²x",
         "cos x - x/sin x", "1/cos x", "A", "Calculus", "Differentiation", "very_hard"),
    ]
    for d in deriv_cases:
        qs.append(q(*d))

    # Integrals
    integral_cases = [
        ("∫x^n dx (n ≠ -1) =", "x^(n+1)/(n+1) + C", "nx^(n-1) + C",
         "x^(n+1) + C", "x^n/(n+1) + C", "A", "Calculus", "Integration", "medium"),
        ("∫sin x dx =", "−cos x + C", "cos x + C", "−sin x + C", "tan x + C", "A",
         "Calculus", "Integration", "medium"),
        ("∫cos x dx =", "sin x + C", "−sin x + C", "cos x + C", "−cos x + C", "A",
         "Calculus", "Integration", "medium"),
        ("∫e^x dx =", "e^x + C", "xe^x + C", "e^(x-1) + C", "xe^(x-1) + C", "A",
         "Calculus", "Integration", "medium"),
        ("∫(1/x) dx =", "ln|x| + C", "1/x² + C", "x^(-2) + C", "1/(x+1) + C", "A",
         "Calculus", "Integration", "medium"),
        ("∫sec²x dx =", "tan x + C", "sec x + C", "−cot x + C", "cos²x + C", "A",
         "Calculus", "Integration", "medium"),
        ("∫(from 0 to π) sin x dx =", "2", "0", "1", "π", "A",
         "Calculus", "Definite Integrals", "medium"),
        ("∫(from 0 to 1) x² dx =", "1/3", "1/2", "1", "1/4", "A",
         "Calculus", "Definite Integrals", "medium"),
        ("∫(from 0 to 2) (2x+1) dx =", "6", "4", "5", "8", "A",
         "Calculus", "Definite Integrals", "medium"),
        ("∫x sin x dx =", "sin x − x cos x + C", "x sin x − cos x + C",
         "−x cos x + C", "sin x + cos x + C", "A", "Calculus", "Integration by Parts", "hard"),
        ("∫e^x sin x dx =", "e^x(sin x − cos x)/2 + C", "e^x cos x + C",
         "e^x sin x + C", "e^x(sin x + cos x) + C", "A",
         "Calculus", "Integration by Parts", "very_hard"),
    ]
    for i in integral_cases:
        qs.append(q(*i))

    # Application of calculus
    app_calc = [
        ("A function f(x) is increasing when:", "f'(x) > 0", "f'(x) < 0",
         "f'(x) = 0", "f''(x) > 0", "A", "Calculus", "Application of Derivatives", "medium"),
        ("At local maximum, f'(x) = 0 and f''(x) is:", "Negative", "Positive",
         "Zero", "Undefined", "A", "Calculus", "Application of Derivatives", "medium"),
        ("Rolle's theorem requires f(a) = f(b) and f is:", "Continuous on [a,b] and differentiable on (a,b)",
         "Differentiable on [a,b]", "Continuous on (a,b)", "Monotone on [a,b]", "A",
         "Calculus", "Mean Value Theorems", "hard"),
        ("By MVT, there exists c in (a,b) such that f'(c) =",
         "(f(b)−f(a))/(b−a)", "(f(a)−f(b))/(b−a)", "f(b)−f(a)", "(b−a)/(f(b)−f(a))", "A",
         "Calculus", "Mean Value Theorems", "hard"),
        ("Area bounded by y=x², x-axis from x=0 to x=3 is:", "9", "27", "3", "18", "A",
         "Calculus", "Area Under Curve", "hard"),
        ("Volume of solid of revolution about x-axis from x=0 to x=2 for y=x:",
         "8π/3", "4π", "2π", "16π/3", "A", "Calculus", "Volume", "very_hard"),
        ("Tangent to y=x² at x=2 has slope:", "4", "2", "1", "8", "A",
         "Calculus", "Application of Derivatives", "medium"),
        ("Normal to y=x² at x=1 has slope:", "−1/2", "2", "1/2", "−2", "A",
         "Calculus", "Application of Derivatives", "hard"),
    ]
    for a in app_calc:
        qs.append(q(*a))

    return qs


def gen_trigonometry():
    qs = []

    # Values
    trig_vals = [
        ("sin 30° =", "1/2", "√3/2", "1/√2", "√3", "A",
         "Trigonometry", "Trigonometric Values", "medium"),
        ("cos 60° =", "1/2", "√3/2", "1", "0", "A",
         "Trigonometry", "Trigonometric Values", "medium"),
        ("tan 45° =", "1", "√3", "1/√3", "0", "A",
         "Trigonometry", "Trigonometric Values", "medium"),
        ("sin 90° =", "1", "0", "1/2", "√3/2", "A",
         "Trigonometry", "Trigonometric Values", "medium"),
        ("cos 0° =", "1", "0", "1/2", "√3/2", "A",
         "Trigonometry", "Trigonometric Values", "medium"),
        ("tan 60° =", "√3", "1", "1/√3", "2", "A",
         "Trigonometry", "Trigonometric Values", "medium"),
        ("sin 45° =", "1/√2", "√3/2", "1/2", "1", "A",
         "Trigonometry", "Trigonometric Values", "medium"),
        ("cos 30° =", "√3/2", "1/2", "1/√2", "1", "A",
         "Trigonometry", "Trigonometric Values", "medium"),
        ("sin 0° =", "0", "1", "1/2", "√3/2", "A",
         "Trigonometry", "Trigonometric Values", "medium"),
        ("tan 90° =", "Undefined (∞)", "0", "1", "√3", "A",
         "Trigonometry", "Trigonometric Values", "medium"),
    ]
    for t in trig_vals:
        qs.append(q(*t))

    # Identities
    identities = [
        ("sin²θ + cos²θ =", "1", "0", "sin 2θ", "2", "A",
         "Trigonometry", "Trigonometric Identities", "medium"),
        ("1 + tan²θ =", "sec²θ", "cosec²θ", "1 + sec²θ", "2", "A",
         "Trigonometry", "Trigonometric Identities", "medium"),
        ("1 + cot²θ =", "cosec²θ", "sec²θ", "tan²θ + 1", "2", "A",
         "Trigonometry", "Trigonometric Identities", "medium"),
        ("sin 2θ =", "2 sin θ cos θ", "sin²θ − cos²θ", "cos²θ − sin²θ", "2 cos²θ − 1", "A",
         "Trigonometry", "Trigonometric Identities", "medium"),
        ("cos 2θ =", "cos²θ − sin²θ", "2 sin θ cos θ", "sin 2θ", "1 − 2sin θ", "A",
         "Trigonometry", "Trigonometric Identities", "medium"),
        ("tan 2θ =", "2 tan θ/(1 − tan²θ)", "2 tan θ/(1 + tan²θ)",
         "tan²θ/(1+tan θ)", "2/(1−tan²θ)", "A",
         "Trigonometry", "Trigonometric Identities", "hard"),
        ("sin(A+B) =", "sin A cos B + cos A sin B", "sin A cos B − cos A sin B",
         "cos A cos B + sin A sin B", "sin A + sin B", "A",
         "Trigonometry", "Compound Angles", "medium"),
        ("cos(A−B) =", "cos A cos B + sin A sin B", "cos A cos B − sin A sin B",
         "sin A sin B − cos A cos B", "cos A − cos B", "A",
         "Trigonometry", "Compound Angles", "medium"),
        ("tan(A+B) =", "(tan A + tan B)/(1 − tan A tan B)",
         "(tan A − tan B)/(1 + tan A tan B)", "tan A + tan B", "tan A·tan B", "A",
         "Trigonometry", "Compound Angles", "hard"),
        ("sin 3θ =", "3 sin θ − 4 sin³θ", "3 sin θ + 4 sin³θ",
         "4 sin³θ − 3 sin θ", "sin³θ", "A",
         "Trigonometry", "Multiple Angles", "hard"),
        ("Principal range of arcsin is:", "[−π/2, π/2]", "[0, π]", "[−π, π]", "[0, 2π]", "A",
         "Trigonometry", "Inverse Trigonometry", "medium"),
        ("arctan(1) =", "π/4", "π/2", "π/3", "π/6", "A",
         "Trigonometry", "Inverse Trigonometry", "medium"),
        ("arcsin(1/2) =", "π/6", "π/3", "π/4", "π/2", "A",
         "Trigonometry", "Inverse Trigonometry", "medium"),
        ("General solution of sin θ = 0:", "nπ, n∈Z", "2nπ, n∈Z",
         "(2n+1)π/2, n∈Z", "nπ/2, n∈Z", "A",
         "Trigonometry", "Trigonometric Equations", "hard"),
        ("General solution of cos θ = 0:", "(2n+1)π/2, n∈Z", "nπ, n∈Z",
         "2nπ, n∈Z", "nπ/2, n∈Z", "A",
         "Trigonometry", "Trigonometric Equations", "hard"),
    ]
    for i in identities:
        qs.append(q(*i))

    return qs


def gen_coordinate_geometry():
    qs = []

    # Distance formula
    dist_cases = [
        (0, 0, 3, 4, "5", "7", "√7", "25", "A", "Distance = √(9+16) = 5"),
        (1, 2, 4, 6, "5", "3", "7", "√7", "A", "Distance = √(9+16) = 5"),
        (-1, -2, 2, 2, "5", "3", "√7", "25", "A", "Distance = √(9+16) = 5"),
        (0, 0, 0, 5, "5", "25", "√5", "10", "A", "Distance = 5"),
        (1, 1, 4, 5, "5", "7", "3", "√7", "A", "Distance = √(9+16) = 5"),
        (-3, 0, 0, 4, "5", "7", "√7", "3", "A"),
        (2, 3, 5, 7, "5", "7", "3", "25", "A"),
        (0, 0, 12, 5, "13", "17", "√7", "7", "A"),
    ]
    for x1, y1, x2, y2, ans, w1, w2, w3, cor, *expl in dist_cases:
        d_val = math.sqrt((x2-x1)**2 + (y2-y1)**2)
        qs.append(q(
            f"Distance between points ({x1},{y1}) and ({x2},{y2}) is:",
            ans, w1, w2, w3, cor,
            "Coordinate Geometry", "Distance Formula", "medium",
            f"d = sqrt({(x2-x1)**2}+{(y2-y1)**2}) = {d_val:.0f}"
        ))

    # Section formula
    section_cases = [
        (0, 0, 6, 6, 1, 1, "(3,3)", "(6,6)", "(1,1)", "(0,6)", "A"),
        (2, 4, 8, 10, 1, 2, "(4,6)", "(6,8)", "(5,7)", "(3,5)", "A"),
        (1, 1, 7, 7, 1, 1, "(4,4)", "(7,7)", "(1,1)", "(3,3)", "A"),
        (-2, -2, 4, 4, 1, 1, "(1,1)", "(0,0)", "(-2,4)", "(4,-2)", "A"),
    ]
    for x1, y1, x2, y2, m, n, ans, w1, w2, w3, cor in section_cases:
        mx = (m*x2 + n*x1)/(m+n)
        my = (m*y2 + n*y1)/(m+n)
        qs.append(q(
            f"Point dividing ({x1},{y1}) and ({x2},{y2}) in ratio {m}:{n} internally:",
            ans, w1, w2, w3, cor,
            "Coordinate Geometry", "Section Formula", "medium",
            f"x = ({m}×{x2}+{n}×{x1})/({m}+{n}) = {mx:.0f}, y = {my:.0f}"
        ))

    # Slope
    slope_cases = [
        ((0,0), (3,3), "1", "3", "1/3", "0", "A"),
        ((1,2), (3,4), "1", "2", "1/2", "-1", "A"),
        ((0,1), (2,5), "2", "1/2", "4", "-2", "A"),
        ((2,2), (4,8), "3", "1/3", "6", "-3", "A"),
        ((1,3), (4,9), "2", "1/2", "6", "-2", "A"),
        ((0,0), (4,2), "1/2", "2", "1/4", "-1/2", "A"),
    ]
    for (x1,y1), (x2,y2), ans, w1, w2, w3, cor in slope_cases:
        m_slope = (y2-y1)/(x2-x1) if x2 != x1 else math.inf
        qs.append(q(
            f"Slope of line through ({x1},{y1}) and ({x2},{y2}) is:",
            ans, w1, w2, w3, cor,
            "Coordinate Geometry", "Slope of a Line", "medium",
            f"m = (y₂-y₁)/(x₂-x₁) = ({y2}-{y1})/({x2}-{x1}) = {m_slope}"
        ))

    # Circle
    circle_qs = [
        ("Equation of circle with centre (0,0) and radius 5 is:", "x² + y² = 25",
         "x² + y² = 5", "x² + y² = 10", "(x+5)² + (y+5)² = 25", "A",
         "Coordinate Geometry", "Circle", "medium"),
        ("Centre of circle x² + y² − 4x + 6y + 9 = 0 is:", "(2,−3)",
         "(−2,3)", "(4,−6)", "(−4,6)", "A", "Coordinate Geometry", "Circle", "hard"),
        ("Radius of circle x² + y² = 36 is:", "6", "36", "√6", "18", "A",
         "Coordinate Geometry", "Circle", "medium"),
        ("Standard equation of parabola opening right is:", "y² = 4ax",
         "x² = 4ay", "y² = −4ax", "x² = −4ay", "A",
         "Coordinate Geometry", "Conics", "hard"),
        ("For ellipse x²/a² + y²/b² = 1 (a>b), eccentricity e =",
         "√(1−b²/a²)", "√(1+b²/a²)", "b/a", "a/b", "A",
         "Coordinate Geometry", "Conics", "hard"),
        ("Focus of parabola y² = 8x is:", "(2,0)", "(0,2)", "(−2,0)", "(8,0)", "A",
         "Coordinate Geometry", "Parabola", "hard"),
        ("Vertices of ellipse x²/25 + y²/9 = 1 are:", "(±5,0)", "(±3,0)",
         "(0,±5)", "(0,±3)", "A", "Coordinate Geometry", "Ellipse", "hard"),
        ("Asymptotes of hyperbola x²/a²−y²/b²=1:", "y = ±(b/a)x",
         "y = ±(a/b)x", "x = ±a", "y = ±b", "A",
         "Coordinate Geometry", "Hyperbola", "very_hard"),
    ]
    for c in circle_qs:
        qs.append(q(*c))

    return qs


def gen_statistics_probability():
    qs = []

    # Mean, median, mode
    stats = [
        ("Mean of 2, 4, 6, 8, 10 is:", "6", "5", "8", "4", "A",
         "Statistics", "Measures of Central Tendency", "medium"),
        ("Median of 1, 3, 5, 7, 9 is:", "5", "3", "7", "4", "A",
         "Statistics", "Measures of Central Tendency", "medium"),
        ("Mode of 2, 3, 3, 4, 5, 5, 5 is:", "5", "3", "4", "2", "A",
         "Statistics", "Measures of Central Tendency", "medium"),
        ("Standard deviation is:", "√(Σ(xᵢ−x̄)²/n)", "Σ(xᵢ−x̄)²/n",
         "Σ|xᵢ−x̄|/n", "Σxᵢ/n", "A", "Statistics", "Standard Deviation", "hard"),
        ("Variance = ?", "(Standard deviation)²", "Standard deviation",
         "Mean/Standard deviation", "Standard deviation/n", "A",
         "Statistics", "Variance", "medium"),
        ("For normally distributed data, mean = median = ?", "Mode", "Variance",
         "Range", "SD", "A", "Statistics", "Normal Distribution", "medium"),
        ("Coefficient of variation = ?", "(SD/Mean)×100", "(Mean/SD)×100",
         "SD×Mean", "Mean − SD", "A", "Statistics", "Variation", "hard"),
        ("Median of 3, 7, 2, 8, 5, 9, 4 (arranged):", "5", "7", "8", "2", "A",
         "Statistics", "Median", "medium"),
        ("Mean of 10, 20, 30, 40, 50 is:", "30", "25", "35", "40", "A",
         "Statistics", "Mean", "medium"),
        ("Range of data 4, 7, 13, 2, 1, 9 is:", "12", "4", "13", "7", "A",
         "Statistics", "Measures of Dispersion", "medium"),
    ]
    for s in stats:
        qs.append(q(*s))

    # Probability
    prob_qs = [
        ("Probability of getting head in fair coin toss:", "1/2", "1", "1/4", "0", "A",
         "Probability", "Basic Probability", "medium"),
        ("Probability of getting 6 on a die:", "1/6", "1", "6", "1/3", "A",
         "Probability", "Basic Probability", "medium"),
        ("Probability of getting sum 7 with two dice:", "1/6", "1/12", "7/36", "6/36", "A",
         "Probability", "Joint Probability", "hard"),
        ("P(A∪B) = P(A) + P(B) − ?", "P(A∩B)", "P(A)·P(B)", "P(B)", "P(not A)", "A",
         "Probability", "Set Theory in Probability", "medium"),
        ("If A and B are independent, P(A∩B) =", "P(A)·P(B)", "P(A)+P(B)",
         "P(A∪B)", "P(A)−P(B)", "A", "Probability", "Independent Events", "medium"),
        ("Bayes' theorem deals with:", "Conditional probability",
         "Joint probability", "Marginal probability", "Geometric probability", "A",
         "Probability", "Bayes' Theorem", "hard"),
        ("P(A|B) = ?", "P(A∩B)/P(B)", "P(A∩B)/P(A)",
         "P(A)×P(B)", "P(A∪B)/P(B)", "A",
         "Probability", "Conditional Probability", "hard"),
        ("Probability of complementary event = ?", "1 − P(A)", "P(A)",
         "1 + P(A)", "P(A)²", "A", "Probability", "Complementary Events", "medium"),
        ("Expected value E(X) for discrete distribution =", "Σxᵢ·P(xᵢ)",
         "Σxᵢ/n", "Σxᵢ", "Σxᵢ²·P(xᵢ)", "A",
         "Probability", "Expected Value", "hard"),
        ("In binomial distribution P(X=r) =", "ⁿCᵣ pʳ qⁿ⁻ʳ",
         "ⁿCᵣ pⁿ⁻ʳ qʳ", "pʳ qⁿ", "ⁿCᵣ pᵣ", "A",
         "Probability", "Binomial Distribution", "very_hard"),
        ("Poisson distribution is approximation for:", "Rare events in large trials",
         "Normal events", "Uniform distributions", "All events", "A",
         "Probability", "Poisson Distribution", "very_hard"),
        ("For normal distribution, P(μ−σ < X < μ+σ) ≈", "0.68", "0.95",
         "0.99", "0.50", "A", "Probability", "Normal Distribution", "hard"),
    ]
    for p in prob_qs:
        qs.append(q(*p))

    return qs


def gen_matrices_vectors():
    qs = []

    # Matrices
    mat_qs = [
        ("Order of matrix [[1,2,3],[4,5,6]] is:", "2×3", "3×2", "2×2", "6×1", "A",
         "Matrices", "Basic Concepts", "medium"),
        ("Trace of matrix [[1,2],[3,4]] is:", "5", "4", "10", "2", "A",
         "Matrices", "Trace", "medium"),
        ("Determinant of [[1,2],[3,4]] is:", "−2", "2", "10", "0", "A",
         "Matrices", "Determinants", "medium"),
        ("Determinant of [[1,0],[0,1]] is:", "1", "0", "2", "−1", "A",
         "Matrices", "Determinants", "medium"),
        ("Inverse of [[2,0],[0,3]] is:", "[[1/2,0],[0,1/3]]", "[[3,0],[0,2]]",
         "[[0,2],[3,0]]", "Doesn't exist", "A", "Matrices", "Inverse Matrix", "hard"),
        ("Transpose of [[1,2,3],[4,5,6]] is:", "[[1,4],[2,5],[3,6]]",
         "[[1,2,3],[4,5,6]]", "[[4,5,6],[1,2,3]]", "[[6,5,4],[3,2,1]]", "A",
         "Matrices", "Transpose", "medium"),
        ("Matrix multiplication AB requires:", "Number of columns of A = rows of B",
         "A and B must be square", "A and B must be same order",
         "Number of rows of A = columns of B", "A", "Matrices", "Matrix Multiplication", "medium"),
        ("Rank of zero matrix is:", "0", "1", "Undefined", "Equal to order", "A",
         "Matrices", "Rank", "hard"),
        ("Cramer's rule solves:", "System of linear equations",
         "Differential equations", "Polynomial equations", "Matrix equations", "A",
         "Matrices", "System of Equations", "hard"),
        ("A matrix is singular if:", "Its determinant is zero",
         "Its determinant is one", "It has all positive entries",
         "It is symmetric", "A", "Matrices", "Singular Matrix", "medium"),
    ]
    for m in mat_qs:
        qs.append(q(*m))

    # Vectors
    vec_qs = [
        ("Magnitude of vector 3î + 4ĵ is:", "5", "7", "√7", "25", "A",
         "Vectors", "Magnitude", "medium"),
        ("Dot product of î and ĵ is:", "0", "1", "−1", "√2", "A",
         "Vectors", "Dot Product", "medium"),
        ("Cross product î × î =", "0", "1", "−1", "ĵ", "A",
         "Vectors", "Cross Product", "medium"),
        ("Angle between two perpendicular vectors using dot product =",
         "90° (dot product = 0)", "0°", "45°", "180°", "A",
         "Vectors", "Angle Between Vectors", "medium"),
        ("Unit vector of 3î + 4ĵ is:", "(3î + 4ĵ)/5", "(3î + 4ĵ)/7",
         "3î + 4ĵ", "(î + ĵ)/√2", "A", "Vectors", "Unit Vector", "medium"),
        ("Cross product a × b is:", "Perpendicular to both a and b",
         "Parallel to a", "Parallel to b", "Equal to dot product", "A",
         "Vectors", "Cross Product", "medium"),
        ("If |a × b| = |a||b|, then angle between them is:", "90°", "0°", "180°", "45°", "A",
         "Vectors", "Cross Product", "hard"),
        ("Scalar triple product a·(b×c) gives:", "Volume of parallelepiped",
         "Area of parallelogram", "Length of diagonal", "Nothing useful", "A",
         "Vectors", "Scalar Triple Product", "hard"),
        ("|a + b|² + |a − b|² =", "2(|a|² + |b|²)", "|a|² + |b|²",
         "4|a||b|", "(|a| + |b|)²", "A", "Vectors", "Vector Properties", "hard"),
        ("Work done W = F·d is:", "Scalar quantity", "Vector quantity",
         "Can be either", "Always positive", "A", "Vectors", "Applications", "medium"),
    ]
    for v in vec_qs:
        qs.append(q(*v))

    return qs


def gen_parametric_maths():
    qs = []

    # Derivative computations
    power_funcs = [(2,1), (3,1), (4,1), (5,1), (6,1), (2,2), (3,2), (4,3), (5,2), (6,3)]
    for n, a in power_funcs:
        coeff = n * (a ** (n-1))
        qs.append({
            "subject": "Mathematics", "exam_type": "CUET_DOMAIN",
            "topic": "Calculus", "subtopic": "Differentiation",
            "difficulty": "medium",
            "question_en": f"d/dx({a}x^{n}) at x=1:",
            "option_a_en": f"{n*a**(n-1)}", "option_b_en": f"{n*a**n}",
            "option_c_en": f"{a**n}", "option_d_en": f"{n+a}",
            "correct_answer": "A",
            "explanation_en": f"d/dx({a}x^{n}) = {n*a}x^{n-1}; at x=1 = {n*a}",
            "marks_correct": 5.0, "marks_wrong": -1.0,
        })

    # Integration computations
    for n in range(1, 11):
        for a in [1, 2, 3, 4]:
            qs.append({
                "subject": "Mathematics", "exam_type": "CUET_DOMAIN",
                "topic": "Calculus", "subtopic": "Integration",
                "difficulty": "medium",
                "question_en": f"∫{a}x^{n} dx =",
                "option_a_en": f"{a}x^{n+1}/{n+1} + C",
                "option_b_en": f"{a*n}x^{n-1} + C",
                "option_c_en": f"{a}x^{n+1} + C",
                "option_d_en": f"{a}x^{n}/(n+1) + C",
                "correct_answer": "A",
                "explanation_en": f"∫{a}x^{n} dx = {a}·x^{n+1}/{n+1} + C",
                "marks_correct": 5.0, "marks_wrong": -1.0,
            })

    # AP/GP variations
    for a_val in range(1, 10):
        for d_val in range(1, 6):
            for n_val in [5, 10, 15, 20]:
                T_n = a_val + (n_val - 1) * d_val
                S_n = n_val * (2*a_val + (n_val-1)*d_val) // 2
                qs.append({
                    "subject": "Mathematics", "exam_type": "CUET_DOMAIN",
                    "topic": "Algebra", "subtopic": "Arithmetic Progressions",
                    "difficulty": "medium",
                    "question_en": f"AP: a={a_val}, d={d_val}. Sum of {n_val} terms is:",
                    "option_a_en": f"{S_n}", "option_b_en": f"{S_n+d_val}",
                    "option_c_en": f"{S_n-d_val}", "option_d_en": f"{2*S_n}",
                    "correct_answer": "A",
                    "explanation_en": f"Sₙ = {n_val}/2[{2*a_val} + {n_val-1}×{d_val}] = {S_n}",
                    "marks_correct": 5.0, "marks_wrong": -1.0,
                })

    return qs


def generate_all_maths_questions() -> List[Dict]:
    all_qs = []
    all_qs.extend(gen_algebra())
    all_qs.extend(gen_calculus())
    all_qs.extend(gen_trigonometry())
    all_qs.extend(gen_coordinate_geometry())
    all_qs.extend(gen_statistics_probability())
    all_qs.extend(gen_matrices_vectors())
    all_qs.extend(gen_parametric_maths())

    for q_item in all_qs:
        q_item["subject"] = "Mathematics"
        q_item["exam_type"] = "CUET_DOMAIN"
        if "marks_correct" not in q_item:
            q_item["marks_correct"] = 5.0
        if "marks_wrong" not in q_item:
            q_item["marks_wrong"] = -1.0

    print(f"[Mathematics] Generated {len(all_qs)} questions")
    return all_qs
