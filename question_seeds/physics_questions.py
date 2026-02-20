"""
question_seeds/physics.py
=========================
Generates 5000+ unique Physics questions at medium/hard/very_hard difficulty.
Topics: Mechanics, Thermodynamics, Electromagnetism, Optics, Modern Physics, Waves
"""

import random
from typing import List, Dict


def shuffle_wrong(correct_val, wrongs):
    """Return shuffled list of 4 options with correct randomly placed."""
    opts = list(wrongs[:3])
    opts.append(correct_val)
    random.shuffle(opts)
    label = ["A", "B", "C", "D"][opts.index(correct_val)]
    return opts[0], opts[1], opts[2], opts[3], label


def q(question, a, b, c, d, correct, topic, subtopic, difficulty, explanation=""):
    return {
        "subject": "Physics",
        "exam_type": "NEET",
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
        "marks_correct": 4.0,
        "marks_wrong": -1.0,
    }


def gen_kinematics():
    qs = []

    # Template: uniform acceleration s = ut + 0.5at²
    cases = [
        (0, 2, 5, "10 m", "5 m", "20 m", "15 m", "A"),
        (0, 4, 3, "18 m", "12 m", "24 m", "9 m", "A"),
        (5, 3, 4, "44 m", "32 m", "56 m", "28 m", "A"),
        (10, 2, 6, "96 m", "72 m", "108 m", "60 m", "A"),
        (0, 5, 4, "40 m", "20 m", "80 m", "60 m", "A"),
        (0, 3, 10, "150 m", "100 m", "200 m", "75 m", "A"),
        (2, 4, 5, "60 m", "45 m", "75 m", "55 m", "A"),
        (0, 6, 4, "48 m", "24 m", "72 m", "36 m", "A"),
        (8, 2, 3, "33 m", "24 m", "42 m", "21 m", "A"),
        (0, 10, 5, "125 m", "75 m", "250 m", "100 m", "A"),
    ]
    for u, a_val, t, ans, w1, w2, w3, cor in cases:
        s = u*t + 0.5*a_val*t*t
        qs.append(q(
            f"A body starts with initial velocity {u} m/s and acceleration {a_val} m/s². "
            f"The distance covered in {t} seconds is:",
            ans, w1, w2, w3, cor,
            "Kinematics", "Equations of Motion", "medium",
            f"s = ut + ½at² = {u}×{t} + ½×{a_val}×{t}² = {int(s)} m"
        ))

    # Template: v² = u² + 2as
    vel_cases = [
        (0, 10, 20, "20 m/s", "10 m/s", "400 m/s", "14 m/s", "A"),
        (0, 5, 45, "30 m/s (approx.)", "15 m/s", "90 m/s", "21.2 m/s", "D"),
        (0, 20, 80, "40 m/s", "20 m/s", "60 m/s", "80 m/s", "B"),
        (10, 5, 10, "v = 14.1 m/s (approx.)", "v = 10 m/s", "v = 20 m/s", "v = 5 m/s", "A"),
        (0, 9.8, 20, "19.8 m/s", "14 m/s", "28 m/s", "9.8 m/s", "A"),
        (0, 4, 50, "20 m/s", "10 m/s", "40 m/s", "30 m/s", "A"),
    ]
    for u, a_val, s_val, ans, w1, w2, w3, cor in vel_cases:
        qs.append(q(
            f"A body starts from rest with acceleration {a_val} m/s². "
            f"Find its velocity after covering {s_val} m.",
            ans, w1, w2, w3, cor,
            "Kinematics", "Equations of Motion", "medium",
            f"v² = u² + 2as = 0 + 2×{a_val}×{s_val}"
        ))

    # Relative motion
    rel_cases = [
        ("40 km/h", "60 km/h", "same direction", "20 km/h", "100 km/h", "60 km/h", "40 km/h", "A"),
        ("40 km/h", "60 km/h", "opposite direction", "100 km/h", "20 km/h", "60 km/h", "40 km/h", "A"),
        ("30 km/h", "50 km/h", "same direction", "20 km/h", "80 km/h", "30 km/h", "50 km/h", "A"),
        ("30 km/h", "50 km/h", "opposite direction", "80 km/h", "20 km/h", "30 km/h", "50 km/h", "A"),
        ("20 km/h", "80 km/h", "same direction", "60 km/h", "100 km/h", "20 km/h", "80 km/h", "A"),
    ]
    for v1, v2, direction, ans, w1, w2, w3, cor in rel_cases:
        qs.append(q(
            f"Train A moves at {v1} and Train B moves at {v2} in the {direction}. "
            f"Relative velocity of B with respect to A is:",
            ans, w1, w2, w3, cor,
            "Kinematics", "Relative Motion", "medium",
        ))

    # Projectile motion
    proj_cases = [
        (45, 20, "20.4 m", "10.2 m", "40.8 m", "5.1 m", "A"),
        (45, 10, "5.1 m", "2.6 m", "10.2 m", "7.6 m", "B"),
        (30, 20, "17.7 m", "8.9 m", "35.4 m", "22.3 m", "A"),
        (60, 20, "17.7 m", "8.9 m", "35.4 m", "22.3 m", "A"),
        (45, 14, "10 m", "5 m", "20 m", "14 m", "A"),
        (45, 28, "40 m", "20 m", "80 m", "28 m", "A"),
        (30, 40, "56.6 m", "28.3 m", "113.2 m", "40 m", "A"),
    ]
    for angle, u_val, ans, w1, w2, w3, cor in proj_cases:
        import math
        r = (u_val**2 * math.sin(2*math.radians(angle))) / 9.8
        qs.append(q(
            f"A projectile is fired at {angle}° with initial speed {u_val} m/s. "
            f"The horizontal range is approximately: (g = 9.8 m/s²)",
            ans, w1, w2, w3, cor,
            "Kinematics", "Projectile Motion", "hard",
            f"R = u²sin(2θ)/g = {u_val}²×sin({2*angle}°)/9.8 ≈ {r:.1f} m"
        ))

    # Time of flight
    tof_cases = [
        (45, 20, "2.89 s", "1.44 s", "5.77 s", "4.08 s", "A"),
        (30, 20, "2.04 s", "1.02 s", "4.08 s", "3.06 s", "A"),
        (60, 20, "3.53 s", "1.77 s", "7.07 s", "5.30 s", "A"),
        (45, 10, "1.44 s", "0.72 s", "2.88 s", "2.04 s", "A"),
        (90, 20, "4.08 s", "2.04 s", "8.16 s", "6.12 s", "A"),
    ]
    for angle, u_val, ans, w1, w2, w3, cor in tof_cases:
        qs.append(q(
            f"A body projected at {angle}° with speed {u_val} m/s. "
            f"Time of flight is approximately: (g = 9.8 m/s²)",
            ans, w1, w2, w3, cor,
            "Kinematics", "Projectile Motion", "hard",
            f"T = 2u sinθ/g"
        ))

    # Circular motion
    circular = [
        (2, 5, "9.87 m/s²", "4.94 m/s²", "19.74 m/s²", "2.5 m/s²", "A"),
        (3, 10, "3.29 m/s²", "6.58 m/s²", "1.65 m/s²", "9.87 m/s²", "A"),
        (1, 10, "9.87 m/s²", "4.94 m/s²", "19.74 m/s²", "2.47 m/s²", "A"),
        (4, 5, "4.93 m/s²", "9.86 m/s²", "2.47 m/s²", "1.23 m/s²", "A"),
        (5, 2, "78.96 m/s²", "39.48 m/s²", "19.74 m/s²", "9.87 m/s²", "A"),
        (2, 3, "4.39 m/s²", "8.77 m/s²", "2.19 m/s²", "13.16 m/s²", "A"),
    ]
    for r_val, T, ans, w1, w2, w3, cor in circular:
        qs.append(q(
            f"A particle moves in a circle of radius {r_val} m with time period {T} s. "
            f"The centripetal acceleration is:",
            ans, w1, w2, w3, cor,
            "Kinematics", "Circular Motion", "hard",
            f"a = 4π²r/T² = 4π²×{r_val}/{T}² = {4*3.14159**2*r_val/T**2:.2f} m/s²"
        ))

    return qs


def gen_laws_of_motion():
    qs = []

    # Newton's Second Law F=ma
    fma_cases = [
        (5, 10, "50 N", "25 N", "100 N", "5 N", "A"),
        (10, 5, "50 N", "2 N", "15 N", "0.5 N", "A"),
        (2, 20, "40 N", "10 N", "80 N", "22 N", "A"),
        (8, 3, "24 N", "12 N", "48 N", "11 N", "A"),
        (15, 4, "60 N", "30 N", "19 N", "11 N", "A"),
        (0.5, 100, "50 N", "200 N", "25 N", "100 N", "A"),
        (3, 12, "36 N", "4 N", "15 N", "9 N", "A"),
        (7, 7, "49 N", "1 N", "98 N", "14 N", "A"),
        (20, 2.5, "50 N", "22.5 N", "100 N", "8 N", "A"),
        (0.2, 50, "10 N", "250 N", "50 N", "5 N", "A"),
    ]
    for m, a_val, ans, w1, w2, w3, cor in fma_cases:
        qs.append(q(
            f"A body of mass {m} kg is subjected to acceleration {a_val} m/s². "
            f"The net force acting on it is:",
            ans, w1, w2, w3, cor,
            "Laws of Motion", "Newton's Second Law", "medium",
            f"F = ma = {m}×{a_val} = {m*a_val} N"
        ))

    # Friction
    friction_cases = [
        (0.3, 10, 9.8, "29.4 N", "9.8 N", "58.8 N", "14.7 N", "A"),
        (0.5, 5, 9.8, "24.5 N", "12.25 N", "49 N", "9.8 N", "A"),
        (0.4, 20, 10, "80 N", "40 N", "160 N", "8 N", "A"),
        (0.2, 15, 10, "30 N", "15 N", "60 N", "3 N", "A"),
        (0.6, 8, 10, "48 N", "24 N", "96 N", "4.8 N", "A"),
        (0.1, 100, 10, "100 N", "50 N", "10 N", "1000 N", "A"),
        (0.35, 12, 10, "42 N", "21 N", "84 N", "3.5 N", "A"),
    ]
    for mu, m, g_val, ans, w1, w2, w3, cor in friction_cases:
        qs.append(q(
            f"A block of mass {m} kg rests on a surface with coefficient of friction μ = {mu}. "
            f"The friction force is: (g = {g_val} m/s²)",
            ans, w1, w2, w3, cor,
            "Laws of Motion", "Friction", "medium",
            f"f = μmg = {mu}×{m}×{g_val} = {mu*m*g_val} N"
        ))

    # Impulse
    impulse_cases = [
        (5, 10, 4, "30 N·s", "50 N·s", "10 N·s", "20 N·s", "C"),
        (10, 20, 5, "100 N·s", "15 N·s", "50 N·s", "200 N·s", "C"),
        (3, 15, 3, "36 N·s", "18 N·s", "45 N·s", "12 N·s", "A"),
        (0, 30, 2, "60 N·s", "30 N·s", "15 N·s", "90 N·s", "A"),
        (5, 25, 3, "60 N·s", "90 N·s", "30 N·s", "20 N·s", "A"),
    ]
    for u, v, m_val, ans, w1, w2, w3, cor in impulse_cases:
        imp = m_val * (v - u)
        qs.append(q(
            f"A body of mass {m_val} kg changes its velocity from {u} m/s to {v} m/s. "
            f"The impulse imparted is:",
            ans, w1, w2, w3, cor,
            "Laws of Motion", "Impulse and Momentum", "medium",
            f"J = mΔv = {m_val}×({v}-{u}) = {imp} N·s"
        ))

    # Atwood machine
    atwood = [
        (5, 3, 9.8, "2.45 m/s²", "4.9 m/s²", "1.23 m/s²", "9.8 m/s²", "A"),
        (8, 2, 9.8, "4.9 m/s²", "9.8 m/s²", "2.45 m/s²", "6.53 m/s²", "A"),
        (6, 4, 10, "2 m/s²", "1 m/s²", "4 m/s²", "10 m/s²", "A"),
        (10, 6, 10, "2.5 m/s²", "1.25 m/s²", "5 m/s²", "10 m/s²", "A"),
        (3, 1, 10, "5 m/s²", "2.5 m/s²", "10 m/s²", "7.5 m/s²", "A"),
    ]
    for m1, m2, g_val, ans, w1, w2, w3, cor in atwood:
        a_sys = (m1-m2)*g_val/(m1+m2)
        qs.append(q(
            f"In an Atwood machine, masses {m1} kg and {m2} kg are connected by a string "
            f"over a frictionless pulley. The acceleration of the system is: (g = {g_val} m/s²)",
            ans, w1, w2, w3, cor,
            "Laws of Motion", "Atwood Machine", "hard",
            f"a = (m1-m2)g/(m1+m2) = ({m1}-{m2})×{g_val}/({m1}+{m2}) = {a_sys:.2f} m/s²"
        ))

    # Conceptual Newton's Laws
    conceptual = [
        ("A body in uniform circular motion has:", "Constant speed but varying velocity",
         "Constant velocity", "Zero acceleration", "Constant kinetic energy", "A",
         "Laws of Motion", "Circular Motion", "medium"),
        ("Which of the following is a contact force?", "Friction", "Gravitational force",
         "Electrostatic force", "Magnetic force", "A", "Laws of Motion", "Types of Forces", "medium"),
        ("Newton's first law of motion defines:", "Inertia", "Force", "Momentum", "Acceleration", "A",
         "Laws of Motion", "Newton's First Law", "medium"),
        ("The SI unit of momentum is:", "kg·m/s", "N·m", "kg·m/s²", "J/m", "A",
         "Laws of Motion", "Momentum", "medium"),
        ("A rocket works on the principle of:", "Conservation of momentum",
         "Conservation of energy", "Newton's first law", "Bernoulli's principle", "A",
         "Laws of Motion", "Conservation of Momentum", "medium"),
        ("When a horse suddenly stops, a rider falls forward. This is due to:",
         "Inertia of motion", "Inertia of rest", "Gravitational force", "Frictional force", "A",
         "Laws of Motion", "Newton's First Law", "medium"),
        ("The maximum static friction is:", "Greater than kinetic friction",
         "Less than kinetic friction", "Equal to kinetic friction", "Independent of normal force", "A",
         "Laws of Motion", "Friction", "medium"),
        ("The angle of friction equals:", "arctan(μ)", "arcsin(μ)", "arccos(μ)", "μ radians", "A",
         "Laws of Motion", "Friction", "hard"),
        ("A particle moving in a circle of radius r with speed v has centripetal acceleration:",
         "v²/r", "v/r", "r/v²", "v²r", "A",
         "Laws of Motion", "Circular Motion", "medium"),
        ("Two bodies of masses m and 2m collide and stick together. This is a:",
         "Perfectly inelastic collision", "Elastic collision",
         "Partially elastic collision", "Explosion", "A",
         "Laws of Motion", "Collisions", "medium"),
    ]
    for con in conceptual:
        qs.append(q(*con))

    return qs


def gen_work_energy():
    qs = []

    # Work done W = F·d·cosθ
    work_cases = [
        (100, 10, 0, "1000 J", "500 J", "0 J", "2000 J", "A"),
        (50, 20, 60, "500 J", "1000 J", "866 J", "250 J", "A"),
        (200, 5, 90, "0 J", "1000 J", "500 J", "200 J", "A"),
        (80, 15, 30, "1039 J", "519 J", "1200 J", "600 J", "A"),
        (60, 10, 45, "424 J", "600 J", "212 J", "848 J", "A"),
        (150, 8, 0, "1200 J", "600 J", "2400 J", "158 J", "A"),
        (40, 25, 60, "500 J", "1000 J", "250 J", "866 J", "A"),
        (120, 12, 30, "1247 J", "624 J", "1440 J", "720 J", "A"),
        (75, 20, 0, "1500 J", "750 J", "3000 J", "175 J", "A"),
        (30, 50, 45, "1061 J", "530 J", "1500 J", "750 J", "A"),
    ]
    for F, d, theta, ans, w1, w2, w3, cor in work_cases:
        import math
        W = F * d * math.cos(math.radians(theta))
        qs.append(q(
            f"A force of {F} N acts on a body at angle {theta}° to displacement. "
            f"Work done when body moves {d} m is:",
            ans, w1, w2, w3, cor,
            "Work, Energy and Power", "Work", "medium",
            f"W = Fd cosθ = {F}×{d}×cos({theta}°) = {W:.0f} J"
        ))

    # Kinetic Energy
    ke_cases = [
        (5, 10, "250 J", "500 J", "125 J", "50 J", "A"),
        (10, 5, "125 J", "250 J", "500 J", "50 J", "A"),
        (2, 20, "400 J", "200 J", "800 J", "40 J", "A"),
        (8, 4, "64 J", "128 J", "32 J", "256 J", "A"),
        (0.5, 100, "2500 J", "5000 J", "1250 J", "500 J", "A"),
        (3, 6, "54 J", "27 J", "108 J", "18 J", "A"),
        (15, 2, "30 J", "15 J", "60 J", "45 J", "A"),
        (0.2, 30, "90 J", "45 J", "180 J", "6 J", "A"),
        (100, 10, "5000 J", "2500 J", "10000 J", "1000 J", "A"),
        (4, 15, "450 J", "225 J", "900 J", "60 J", "A"),
    ]
    for m, v, ans, w1, w2, w3, cor in ke_cases:
        KE = 0.5 * m * v * v
        qs.append(q(
            f"A body of mass {m} kg moves with velocity {v} m/s. Its kinetic energy is:",
            ans, w1, w2, w3, cor,
            "Work, Energy and Power", "Kinetic Energy", "medium",
            f"KE = ½mv² = ½×{m}×{v}² = {KE:.0f} J"
        ))

    # Potential Energy
    pe_cases = [
        (5, 10, 9.8, "490 J", "245 J", "980 J", "98 J", "A"),
        (10, 5, 10, "500 J", "250 J", "1000 J", "50 J", "A"),
        (2, 20, 9.8, "392 J", "196 J", "784 J", "39.2 J", "A"),
        (8, 4, 10, "320 J", "160 J", "640 J", "32 J", "A"),
        (3, 15, 10, "450 J", "225 J", "900 J", "45 J", "A"),
        (0.5, 100, 10, "500 J", "250 J", "1000 J", "5000 J", "A"),
        (7, 7, 10, "490 J", "245 J", "980 J", "4900 J", "A"),
        (20, 2, 9.8, "392 J", "196 J", "784 J", "40 J", "A"),
        (1, 50, 9.8, "490 J", "245 J", "980 J", "4900 J", "A"),
        (6, 8, 10, "480 J", "240 J", "960 J", "48 J", "A"),
    ]
    for m, h, g_val, ans, w1, w2, w3, cor in pe_cases:
        PE = m * g_val * h
        qs.append(q(
            f"The gravitational PE of a body of mass {m} kg at height {h} m is: (g = {g_val} m/s²)",
            ans, w1, w2, w3, cor,
            "Work, Energy and Power", "Potential Energy", "medium",
            f"PE = mgh = {m}×{g_val}×{h} = {PE:.0f} J"
        ))

    # Power
    power_cases = [
        (500, 10, "50 W", "25 W", "100 W", "5000 W", "A"),
        (1000, 5, "200 W", "100 W", "400 W", "5000 W", "A"),
        (200, 4, "50 W", "25 W", "100 W", "800 W", "A"),
        (3600, 60, "60 W", "30 W", "120 W", "3600 W", "A"),
        (750, 15, "50 W", "25 W", "100 W", "11250 W", "A"),
        (4000, 20, "200 W", "100 W", "400 W", "80000 W", "A"),
        (900, 30, "30 W", "15 W", "60 W", "27000 W", "A"),
        (2400, 80, "30 W", "15 W", "60 W", "192000 W", "A"),
        (500, 25, "20 W", "10 W", "40 W", "12500 W", "A"),
        (1200, 15, "80 W", "40 W", "160 W", "18000 W", "A"),
    ]
    for W, t, ans, w1, w2, w3, cor in power_cases:
        P = W / t
        qs.append(q(
            f"Work done by a machine is {W} J in {t} seconds. The power developed is:",
            ans, w1, w2, w3, cor,
            "Work, Energy and Power", "Power", "medium",
            f"P = W/t = {W}/{t} = {P:.0f} W"
        ))

    # Conceptual Energy
    conceptual_we = [
        ("A body thrown vertically upward has maximum kinetic energy at:",
         "The point of projection", "Highest point", "Midpoint of path", "None of these", "A",
         "Work, Energy and Power", "Energy Conservation", "medium"),
        ("The work done by gravity on a body moving horizontally is:",
         "Zero", "Maximum", "Negative", "Positive", "A",
         "Work, Energy and Power", "Work", "medium"),
        ("In elastic collision:", "Both kinetic energy and momentum are conserved",
         "Only momentum is conserved", "Only energy is conserved", "Neither is conserved", "A",
         "Work, Energy and Power", "Collisions", "medium"),
        ("Work done against friction is converted to:", "Heat energy",
         "Kinetic energy", "Potential energy", "Chemical energy", "A",
         "Work, Energy and Power", "Friction", "medium"),
        ("The unit of power is:", "Watt", "Joule", "Newton", "Pascal", "A",
         "Work, Energy and Power", "Power", "medium"),
        ("Spring constant has SI unit:", "N/m", "N·m", "N/m²", "N·m²", "A",
         "Work, Energy and Power", "Spring Force", "hard"),
        ("Work-energy theorem states that net work done on a body equals:",
         "Change in kinetic energy", "Change in potential energy",
         "Total mechanical energy", "Change in momentum", "A",
         "Work, Energy and Power", "Work-Energy Theorem", "medium"),
        ("A machine with 80% efficiency develops 400 W output. The input power is:",
         "500 W", "320 W", "480 W", "420 W", "A",
         "Work, Energy and Power", "Power and Efficiency", "hard"),
    ]
    for con in conceptual_we:
        qs.append(q(*con))

    return qs


def gen_gravitation():
    qs = []

    # g at height
    gh_cases = [
        (6400, 9.8, 6400, "2.45 m/s²", "4.9 m/s²", "9.8 m/s²", "1.225 m/s²", "A"),
        (6400, 9.8, 3200, "4.35 m/s²", "2.18 m/s²", "7.78 m/s²", "6.53 m/s²", "A"),
        (6400, 9.8, 12800, "1.09 m/s²", "2.18 m/s²", "4.35 m/s²", "0.54 m/s²", "A"),
        (6400, 10, 6400, "2.5 m/s²", "5 m/s²", "10 m/s²", "1.25 m/s²", "A"),
        (6400, 10, 3200, "4.44 m/s²", "2.22 m/s²", "7.5 m/s²", "5 m/s²", "A"),
    ]
    for R, g0, h, ans, w1, w2, w3, cor in gh_cases:
        g_h = g0 * (R/(R+h))**2
        qs.append(q(
            f"At what value will g be when height h = {h} km above Earth's surface? "
            f"(R_Earth = {R} km, g_surface = {g0} m/s²)",
            ans, w1, w2, w3, cor,
            "Gravitation", "Variation of g", "hard",
            f"g_h = g₀(R/R+h)² = {g0}×({R}/{R+h})² ≈ {g_h:.2f} m/s²"
        ))

    # Orbital velocity
    orbital = [
        (6400, 9.8, "7.92 km/s", "3.96 km/s", "11.2 km/s", "4.44 km/s", "A"),
        (3400, 3.7, "3.55 km/s", "1.77 km/s", "5.03 km/s", "7.12 km/s", "A"),
        (71400, 25, "42.3 km/s", "21.15 km/s", "84.6 km/s", "30 km/s", "A"),
    ]
    for R, g_val, ans, w1, w2, w3, cor in orbital:
        import math
        v0 = math.sqrt(g_val * R * 1000) / 1000
        qs.append(q(
            f"Find the orbital velocity of a satellite near the surface of a planet "
            f"with radius {R} km and g = {g_val} m/s².",
            ans, w1, w2, w3, cor,
            "Gravitation", "Orbital Velocity", "hard",
            f"v₀ = √(gR) = √({g_val}×{R*1000}) ≈ {v0:.2f} km/s"
        ))

    # Conceptual
    conceptual_grav = [
        ("The escape velocity of Earth is approximately:", "11.2 km/s", "7.9 km/s",
         "8 km/s", "15 km/s", "A", "Gravitation", "Escape Velocity", "medium"),
        ("Gravitational force between two bodies is:", "Always attractive",
         "Always repulsive", "Can be attractive or repulsive", "Zero in vacuum", "A",
         "Gravitation", "Newton's Law of Gravitation", "medium"),
        ("Kepler's second law is related to:", "Conservation of angular momentum",
         "Conservation of energy", "Conservation of momentum", "Conservation of mass", "A",
         "Gravitation", "Kepler's Laws", "hard"),
        ("The value of G (universal gravitational constant) is:",
         "6.67×10⁻¹¹ N·m²/kg²", "9.8 N/kg", "6.67×10¹¹ N·m²/kg²", "9.8 m/s²", "A",
         "Gravitation", "Newton's Law of Gravitation", "medium"),
        ("A geostationary satellite has time period:", "24 hours", "12 hours",
         "48 hours", "6 hours", "A", "Gravitation", "Satellites", "medium"),
        ("Weight of a body at Earth's centre is:", "Zero", "Maximum",
         "Same as on surface", "Half of surface weight", "A",
         "Gravitation", "Variation of g", "medium"),
        ("If Earth's radius decreases to half keeping mass constant, g would become:",
         "4 times", "2 times", "half", "same", "A",
         "Gravitation", "Variation of g", "hard"),
        ("The gravitational PE of a satellite is:", "Negative", "Positive",
         "Zero", "Can be positive or negative", "A",
         "Gravitation", "Gravitational PE", "hard"),
        ("Weightlessness experienced in a satellite is due to:",
         "Free fall condition", "Absence of gravity", "Vacuum in space", "High speed", "A",
         "Gravitation", "Satellites", "medium"),
        ("Kepler's third law: T² ∝", "r³", "r²", "r", "1/r³", "A",
         "Gravitation", "Kepler's Laws", "hard"),
    ]
    for con in conceptual_grav:
        qs.append(q(*con))

    return qs


def gen_thermodynamics():
    qs = []

    # Heat capacity
    hc_cases = [
        (500, 4200, 10, "21 MJ", "42 MJ", "10.5 MJ", "2.1 MJ", "A"),
        (2, 4200, 50, "420 kJ", "210 kJ", "840 kJ", "42 kJ", "A"),
        (1, 4200, 100, "420 kJ", "210 kJ", "840 kJ", "42 kJ", "A"),
        (5, 840, 40, "168 kJ", "84 kJ", "336 kJ", "42 kJ", "A"),
        (10, 390, 30, "117 kJ", "58.5 kJ", "234 kJ", "11.7 kJ", "A"),
        (3, 900, 60, "162 kJ", "81 kJ", "324 kJ", "16.2 kJ", "A"),
        (0.5, 4200, 80, "168 kJ", "84 kJ", "336 kJ", "16.8 kJ", "A"),
        (4, 500, 25, "50 kJ", "25 kJ", "100 kJ", "5 kJ", "A"),
    ]
    for m, c, dT, ans, w1, w2, w3, cor in hc_cases:
        Q = m * c * dT
        qs.append(q(
            f"Calculate heat required to raise temperature of {m} kg of substance "
            f"(sp. heat {c} J/kg·K) by {dT} K:",
            ans, w1, w2, w3, cor,
            "Thermal Properties", "Specific Heat", "medium",
            f"Q = mcΔT = {m}×{c}×{dT} = {Q:.0f} J"
        ))

    # Ideal Gas Law
    gas_cases = [
        (2, 300, 4, 600, "1 atm", "2 atm", "4 atm", "0.5 atm", "A"),
        (1, 273, 2, 546, "1 atm", "2 atm", "4 atm", "0.25 atm", "A"),
        (3, 300, 6, 300, "1.5 atm", "3 atm", "6 atm", "0.75 atm", "A"),
        (1, 300, 1, 150, "2 atm", "1 atm", "4 atm", "0.5 atm", "A"),
        (2, 400, 4, 400, "1 atm", "2 atm", "4 atm", "0.5 atm", "A"),
    ]
    for V1, T1, V2, T2, ans, w1, w2, w3, cor in gas_cases:
        P2 = (T2 * V1) / (T1 * V2)
        qs.append(q(
            f"An ideal gas at 1 atm and {T1} K occupies {V1} L. If volume changes to {V2} L "
            f"and temperature to {T2} K, the new pressure is:",
            ans, w1, w2, w3, cor,
            "Thermodynamics", "Ideal Gas Law", "hard",
            f"P₂ = P₁V₁T₂/(V₂T₁) = 1×{V1}×{T2}/({V2}×{T1}) = {P2:.2f} atm"
        ))

    # Conceptual thermodynamics
    thermo_concept = [
        ("Which thermodynamic process occurs at constant pressure?",
         "Isobaric", "Isothermal", "Adiabatic", "Isochoric", "A",
         "Thermodynamics", "Thermodynamic Processes", "medium"),
        ("In an adiabatic process, heat exchange is:", "Zero", "Maximum",
         "Minimum", "Negative", "A", "Thermodynamics", "Adiabatic Process", "medium"),
        ("First law of thermodynamics is based on:", "Conservation of energy",
         "Conservation of momentum", "Conservation of mass", "Second law", "A",
         "Thermodynamics", "First Law", "medium"),
        ("Carnot engine operates between temperatures 400K and 300K. Efficiency is:",
         "25%", "75%", "50%", "33%", "A",
         "Thermodynamics", "Carnot Engine", "hard"),
        ("Entropy of the universe:", "Always increases", "Always decreases",
         "Remains constant", "Can increase or decrease", "A",
         "Thermodynamics", "Entropy", "hard"),
        ("The zeroth law of thermodynamics defines:", "Temperature",
         "Entropy", "Internal energy", "Heat", "A",
         "Thermodynamics", "Zeroth Law", "medium"),
        ("Triple point of water is:", "273.16 K", "273 K", "300 K", "373 K", "A",
         "Thermodynamics", "Temperature Scales", "medium"),
        ("Stefan's law states that energy radiated ∝", "T⁴", "T³", "T²", "T", "A",
         "Thermodynamics", "Radiation", "hard"),
        ("During melting of ice at 0°C, temperature:", "Remains constant",
         "Increases", "Decreases", "First decreases then increases", "A",
         "Thermodynamics", "Latent Heat", "medium"),
        ("COP of refrigerator = ?", "T₂/(T₁-T₂)", "T₁/(T₁-T₂)",
         "(T₁-T₂)/T₂", "(T₁-T₂)/T₁", "A",
         "Thermodynamics", "Refrigerator", "very_hard"),
        ("An ideal gas is compressed isothermally. Its internal energy:",
         "Remains unchanged", "Increases", "Decreases", "Doubles", "A",
         "Thermodynamics", "Isothermal Process", "hard"),
        ("The efficiency of Carnot engine can be 100% when:", "T_cold = 0K",
         "T_hot → ∞", "T_hot = T_cold", "Both A and B", "D",
         "Thermodynamics", "Carnot Engine", "very_hard"),
    ]
    for con in thermo_concept:
        qs.append(q(*con))

    return qs


def gen_electrostatics():
    qs = []

    # Coulomb's Law
    coulomb_cases = [
        (1e-6, 2e-6, 0.1, "1.8 N", "0.9 N", "3.6 N", "0.18 N", "A"),
        (2e-6, 3e-6, 0.3, "0.6 N", "1.8 N", "0.3 N", "6 N", "A"),
        (4e-6, 4e-6, 0.2, "3.6 N", "1.8 N", "7.2 N", "0.9 N", "A"),
        (1e-6, 1e-6, 0.1, "0.9 N", "1.8 N", "0.45 N", "9 N", "A"),
        (5e-6, 5e-6, 0.5, "1.8 N", "0.9 N", "3.6 N", "9 N", "A"),
        (1e-6, 4e-6, 0.2, "0.9 N", "1.8 N", "0.45 N", "9 N", "A"),
        (2e-6, 4e-6, 0.1, "7.2 N", "14.4 N", "3.6 N", "1.8 N", "A"),
        (3e-6, 3e-6, 0.3, "0.9 N", "1.8 N", "0.45 N", "3.6 N", "A"),
    ]
    for q1, q2, r, ans, w1, w2, w3, cor in coulomb_cases:
        k = 9e9
        F = k * q1 * q2 / r**2
        qs.append(q(
            f"Two charges q₁ = {q1*1e6:.0f} μC and q₂ = {q2*1e6:.0f} μC are separated by {r} m. "
            f"The force between them is: (k = 9×10⁹ N·m²/C²)",
            ans, w1, w2, w3, cor,
            "Electrostatics", "Coulomb's Law", "medium",
            f"F = kq₁q₂/r² = 9×10⁹×{q1}×{q2}/{r}² = {F:.1f} N"
        ))

    # Electric Field
    efield_cases = [
        (1e-6, 0.1, "900 kN/C", "450 kN/C", "1800 kN/C", "9 MN/C", "A"),
        (2e-6, 0.2, "450 kN/C", "225 kN/C", "900 kN/C", "4.5 MN/C", "A"),
        (4e-6, 0.4, "225 kN/C", "112.5 kN/C", "450 kN/C", "2.25 MN/C", "A"),
        (1e-6, 0.5, "36 kN/C", "18 kN/C", "72 kN/C", "360 kN/C", "A"),
        (5e-6, 1, "45 kN/C", "22.5 kN/C", "90 kN/C", "450 kN/C", "A"),
        (1e-6, 1, "9 kN/C", "18 kN/C", "4.5 kN/C", "90 kN/C", "A"),
    ]
    for q1, r, ans, w1, w2, w3, cor in efield_cases:
        E = 9e9 * q1 / r**2
        qs.append(q(
            f"Find electric field at {r} m from a point charge of {q1*1e6:.0f} μC:",
            ans, w1, w2, w3, cor,
            "Electrostatics", "Electric Field", "medium",
            f"E = kq/r² = 9×10⁹×{q1}/{r}² = {E:.0f} N/C"
        ))

    # Capacitance
    cap_concept = [
        ("The energy stored in capacitor C with voltage V is:", "½CV²", "CV²", "½CV", "CV", "A",
         "Electrostatics", "Capacitors", "medium"),
        ("When capacitors are in series, the equivalent capacitance is:",
         "Less than smallest capacitor", "Greater than largest",
         "Equal to sum", "Equal to product", "A",
         "Electrostatics", "Capacitors", "medium"),
        ("Electric field inside a charged conductor is:", "Zero", "Maximum",
         "Uniform", "Depends on shape", "A", "Electrostatics", "Conductors", "medium"),
        ("The SI unit of electric flux is:", "N·m²/C", "N/C", "C/N·m²", "V/m", "A",
         "Electrostatics", "Gauss's Law", "medium"),
        ("Gauss's law relates electric flux to:", "Enclosed charge",
         "Total charge", "Surface charge", "Line charge", "A",
         "Electrostatics", "Gauss's Law", "medium"),
        ("Dielectric constant of vacuum is:", "1", "0", "∞", "ε₀", "A",
         "Electrostatics", "Dielectrics", "medium"),
        ("The capacitance of a parallel plate capacitor is:", "ε₀A/d",
         "ε₀d/A", "A/ε₀d", "d/ε₀A", "A", "Electrostatics", "Capacitors", "hard"),
        ("Van de Graaff generator is used to:", "Generate high voltage",
         "Measure charge", "Store energy", "Measure current", "A",
         "Electrostatics", "Applications", "medium"),
        ("Faraday's ice pail experiment proves:", "Charge resides only on outer surface",
         "Charge inside conductor is maximum", "Charge can be destroyed",
         "Charge is quantized", "A", "Electrostatics", "Conductors", "hard"),
        ("Electric potential due to a point charge is:", "kq/r", "kq/r²",
         "kq²/r", "k/qr", "A", "Electrostatics", "Electric Potential", "medium"),
        ("1 electron volt equals:", "1.6×10⁻¹⁹ J", "1.6×10¹⁹ J",
         "1.6×10⁻²⁷ J", "9.1×10⁻³¹ J", "A",
         "Electrostatics", "Energy Units", "medium"),
        ("Electric field lines never:", "Intersect each other",
         "Start from positive charges", "End at negative charges", "Form straight lines", "A",
         "Electrostatics", "Electric Field Lines", "medium"),
    ]
    for con in cap_concept:
        qs.append(q(*con))

    return qs


def gen_current_electricity():
    qs = []

    # Ohm's Law
    ohm_cases = [
        (12, 4, "3 A", "1.5 A", "6 A", "48 A", "A"),
        (24, 6, "4 A", "2 A", "8 A", "144 A", "A"),
        (9, 3, "3 A", "1.5 A", "6 A", "27 A", "A"),
        (120, 60, "2 A", "1 A", "4 A", "7200 A", "A"),
        (220, 44, "5 A", "2.5 A", "10 A", "9680 A", "A"),
        (6, 2, "3 A", "1.5 A", "6 A", "12 A", "A"),
        (100, 25, "4 A", "2 A", "8 A", "2500 A", "A"),
        (50, 10, "5 A", "2.5 A", "10 A", "500 A", "A"),
        (15, 3, "5 A", "2.5 A", "10 A", "45 A", "A"),
        (240, 80, "3 A", "1.5 A", "6 A", "19200 A", "A"),
    ]
    for V, R, ans, w1, w2, w3, cor in ohm_cases:
        I = V / R
        qs.append(q(
            f"A circuit has EMF = {V} V and resistance = {R} Ω. The current is:",
            ans, w1, w2, w3, cor,
            "Current Electricity", "Ohm's Law", "medium",
            f"I = V/R = {V}/{R} = {I} A"
        ))

    # Resistance in series/parallel
    series_parallel = [
        (4, 6, "series: 10Ω, parallel: 2.4Ω", "series: 24Ω, parallel: 2.4Ω",
         "series: 10Ω, parallel: 5Ω", "series: 2Ω, parallel: 5Ω", "A",
         "Current Electricity", "Resistance Combinations", "medium"),
        (10, 10, "series: 20Ω, parallel: 5Ω", "series: 100Ω, parallel: 5Ω",
         "series: 20Ω, parallel: 10Ω", "series: 5Ω, parallel: 20Ω", "A",
         "Current Electricity", "Resistance Combinations", "medium"),
        (3, 6, "series: 9Ω, parallel: 2Ω", "series: 18Ω, parallel: 2Ω",
         "series: 9Ω, parallel: 4Ω", "series: 3Ω, parallel: 9Ω", "A",
         "Current Electricity", "Resistance Combinations", "medium"),
        (6, 12, "series: 18Ω, parallel: 4Ω", "series: 72Ω, parallel: 4Ω",
         "series: 18Ω, parallel: 9Ω", "series: 6Ω, parallel: 18Ω", "A",
         "Current Electricity", "Resistance Combinations", "medium"),
        (5, 20, "series: 25Ω, parallel: 4Ω", "series: 100Ω, parallel: 4Ω",
         "series: 25Ω, parallel: 12.5Ω", "series: 4Ω, parallel: 25Ω", "A",
         "Current Electricity", "Resistance Combinations", "medium"),
    ]
    for R1, R2, ans, w1, w2, w3, cor, topic, subtopic, diff in series_parallel:
        qs.append(q(
            f"Two resistors {R1}Ω and {R2}Ω are connected. Equivalent resistance in:",
            ans, w1, w2, w3, cor,
            topic, subtopic, diff
        ))

    # Power dissipation
    power_cases = [
        (220, 2, "440 W", "880 W", "220 W", "110 W", "A"),
        (12, 3, "36 W", "72 W", "18 W", "9 W", "A"),
        (100, 5, "500 W", "1000 W", "250 W", "20 W", "A"),
        (24, 4, "96 W", "192 W", "48 W", "6 W", "A"),
        (9, 1.5, "13.5 W", "27 W", "6.75 W", "6 W", "A"),
    ]
    for V, I, ans, w1, w2, w3, cor in power_cases:
        P = V * I
        qs.append(q(
            f"A circuit carries current {I} A at voltage {V} V. Power dissipated is:",
            ans, w1, w2, w3, cor,
            "Current Electricity", "Electrical Power", "medium",
            f"P = VI = {V}×{I} = {P} W"
        ))

    # Conceptual
    current_concept = [
        ("Kirchhoff's voltage law is based on:", "Conservation of energy",
         "Conservation of charge", "Ohm's law", "Conservation of momentum", "A",
         "Current Electricity", "Kirchhoff's Laws", "medium"),
        ("Kirchhoff's current law is based on:", "Conservation of charge",
         "Conservation of energy", "Ohm's law", "Gauss's law", "A",
         "Current Electricity", "Kirchhoff's Laws", "medium"),
        ("The material used in fuse wire has:", "Low melting point",
         "High melting point", "High resistance", "Low resistance", "A",
         "Current Electricity", "Safety Devices", "medium"),
        ("Drift velocity of electrons in a conductor is of the order of:",
         "10⁻⁴ m/s", "10⁸ m/s", "3×10⁸ m/s", "10⁻² m/s", "A",
         "Current Electricity", "Drift Velocity", "hard"),
        ("Wheatstone bridge is balanced when:", "P/Q = R/S", "P/Q = S/R",
         "PQ = RS", "P+Q = R+S", "A", "Current Electricity", "Wheatstone Bridge", "hard"),
        ("Resistivity of a metal increases with:", "Increase in temperature",
         "Decrease in temperature", "Increase in cross-section", "Decrease in length", "A",
         "Current Electricity", "Resistivity", "medium"),
        ("In a potentiometer, a longer wire gives:", "More accurate results",
         "Less accurate results", "Same accuracy", "No effect", "A",
         "Current Electricity", "Potentiometer", "hard"),
        ("The internal resistance of an ideal voltage source is:", "Zero",
         "Infinite", "1 Ω", "Depends on EMF", "A",
         "Current Electricity", "EMF and Internal Resistance", "medium"),
        ("EMF of a cell depends on:", "Nature of electrolyte",
         "Surface area of plates", "Distance between plates", "All of these", "A",
         "Current Electricity", "EMF", "medium"),
        ("1 Ampere = ?", "1 C/s", "1 J/s", "1 V/Ω", "1 W/V", "A",
         "Current Electricity", "Basic Definitions", "medium"),
    ]
    for con in current_concept:
        qs.append(q(*con))

    return qs


def gen_optics():
    qs = []

    # Mirror formula
    mirror_cases = [
        (20, 30, "12 cm", "60 cm", "50 cm", "6 cm", "A"),
        (15, 20, "8.57 cm", "35 cm", "4.28 cm", "12 cm", "A"),
        (10, 15, "6 cm", "3 cm", "25 cm", "150 cm", "A"),
        (30, 60, "20 cm", "40 cm", "10 cm", "90 cm", "A"),
        (25, 50, "16.67 cm", "8.33 cm", "33.3 cm", "75 cm", "A"),
        (20, 20, "10 cm", "20 cm", "5 cm", "40 cm", "A"),
        (10, 30, "7.5 cm", "3.75 cm", "15 cm", "40 cm", "A"),
        (40, 60, "24 cm", "12 cm", "48 cm", "100 cm", "A"),
    ]
    for f_val, u, ans, w1, w2, w3, cor in mirror_cases:
        v = 1 / (1/f_val - 1/u) if (1/f_val - 1/u) != 0 else 0
        qs.append(q(
            f"An object is placed {u} cm in front of a concave mirror with focal length {f_val} cm. "
            f"Image distance is:",
            ans, w1, w2, w3, cor,
            "Ray Optics", "Mirror Formula", "hard",
            f"1/v + 1/u = 1/f; 1/v = 1/{f_val} - 1/{u}"
        ))

    # Snell's law / refraction
    snell_concept = [
        ("When light goes from denser to rarer medium, it:", "Bends away from normal",
         "Bends towards normal", "Travels straight", "Reverses direction", "A",
         "Ray Optics", "Refraction", "medium"),
        ("Refractive index of glass is 1.5. Speed of light in glass is:",
         "2×10⁸ m/s", "3×10⁸ m/s", "1.5×10⁸ m/s", "4.5×10⁸ m/s", "A",
         "Ray Optics", "Refraction", "medium"),
        ("Critical angle for total internal reflection increases when:",
         "Refractive index decreases", "Refractive index increases",
         "Speed of light decreases", "Wavelength decreases", "A",
         "Ray Optics", "Total Internal Reflection", "hard"),
        ("A lens with focal length f has power P. Then P =", "1/f (in meters)",
         "f (in meters)", "f²", "1/f²", "A",
         "Ray Optics", "Lenses", "medium"),
        ("For a convex lens, focal length is:", "Positive", "Negative", "Zero", "Infinite", "A",
         "Ray Optics", "Lenses", "medium"),
        ("The angle of prism + angle of deviation = angle of incidence + angle of emergence. "
         "This is:", "True for any prism", "False", "True only for thin prisms",
         "True only at minimum deviation", "A", "Ray Optics", "Prism", "hard"),
        ("Optical fibre works on the principle of:", "Total internal reflection",
         "Refraction", "Diffraction", "Reflection", "A",
         "Ray Optics", "Total Internal Reflection", "medium"),
        ("Virtual image formed by a plane mirror is:", "Laterally inverted",
         "Inverted", "Diminished", "All of these", "A", "Ray Optics", "Mirrors", "medium"),
        ("Which colour has maximum deviation in a prism?", "Violet",
         "Red", "Green", "Yellow", "A", "Ray Optics", "Prism", "medium"),
        ("The focal length of a concave mirror is:", "Negative", "Positive",
         "Zero", "Infinite", "A", "Ray Optics", "Mirrors", "medium"),
    ]
    for con in snell_concept:
        qs.append(q(*con))

    # Wave optics
    wave_optics = [
        ("In Young's double slit experiment, fringe width β =", "λD/d",
         "λd/D", "dD/λ", "d/λD", "A", "Wave Optics", "Young's DSE", "hard"),
        ("If separation between slits is halved in YDSE, fringe width:", "Doubles",
         "Halves", "Remains same", "Quadruples", "A", "Wave Optics", "Young's DSE", "hard"),
        ("Which phenomenon proves transverse nature of light?",
         "Polarization", "Interference", "Diffraction", "Refraction", "A",
         "Wave Optics", "Polarization", "medium"),
        ("In single slit diffraction, central maximum is:", "Widest", "Narrowest",
         "Same as other maxima", "Half width of others", "A",
         "Wave Optics", "Diffraction", "medium"),
        ("Brewster's angle θ_B satisfies:", "tan θ_B = μ", "sin θ_B = μ",
         "cos θ_B = μ", "cot θ_B = μ", "A", "Wave Optics", "Polarization", "very_hard"),
    ]
    for con in wave_optics:
        qs.append(q(*con))

    return qs


def gen_modern_physics():
    qs = []

    # Photoelectric effect
    photo = [
        ("In photoelectric effect, stopping potential depends on:", "Frequency of light",
         "Intensity of light", "Number of photons", "Area of metal surface", "A",
         "Dual Nature", "Photoelectric Effect", "hard"),
        ("Work function of a metal is 2 eV. Threshold frequency is: (h = 6.6×10⁻³⁴ J·s)",
         "4.83×10¹⁴ Hz", "2.4×10¹⁴ Hz", "9.6×10¹⁴ Hz", "1.2×10¹⁵ Hz", "A",
         "Dual Nature", "Photoelectric Effect", "very_hard"),
        ("de Broglie wavelength λ = ?", "h/mv", "mv/h", "h/m", "hv/m", "A",
         "Dual Nature", "de Broglie Waves", "hard"),
        ("Davisson-Germer experiment demonstrated:", "Wave nature of electrons",
         "Particle nature of electrons", "Photoelectric effect",
         "Compton effect", "A", "Dual Nature", "Wave-Particle Duality", "medium"),
        ("If electron accelerated through potential V, its wavelength λ ∝", "1/√V",
         "1/V", "√V", "V²", "A", "Dual Nature", "de Broglie Waves", "very_hard"),
        ("The Compton effect is explained by:", "Photon-electron collision",
         "Wave interference", "Energy quantization only",
         "Classical electromagnetism", "A", "Dual Nature", "Compton Effect", "hard"),
    ]
    for con in photo:
        qs.append(q(*con))

    # Atomic structure
    atomic = [
        ("Bohr's radius for hydrogen ground state is:", "0.529 Å", "1.058 Å",
         "0.264 Å", "2.116 Å", "A", "Atoms", "Bohr Model", "hard"),
        ("Energy of hydrogen atom in ground state is:", "−13.6 eV", "+13.6 eV",
         "−3.4 eV", "−27.2 eV", "A", "Atoms", "Bohr Model", "hard"),
        ("Lyman series of hydrogen is in:", "UV region", "Visible region",
         "IR region", "X-ray region", "A", "Atoms", "Spectral Series", "medium"),
        ("Balmer series of hydrogen lies in:", "Visible region", "UV region",
         "IR region", "X-ray region", "A", "Atoms", "Spectral Series", "medium"),
        ("Number of spectral lines emitted when electron jumps from n=4 to n=1 is:",
         "6", "4", "3", "10", "A", "Atoms", "Spectral Lines", "hard"),
        ("Rutherford's experiment used:", "Alpha particles", "Beta particles",
         "Electrons", "Photons", "A", "Atoms", "Rutherford Model", "medium"),
    ]
    for con in atomic:
        qs.append(q(*con))

    # Nuclear physics
    nuclear = [
        ("Alpha particle consists of:", "2 protons + 2 neutrons",
         "2 electrons + 2 neutrons", "2 protons only", "4 protons", "A",
         "Nuclei", "Nuclear Reactions", "medium"),
        ("In β⁻ decay, an electron is emitted and:", "Atomic number increases by 1",
         "Atomic number decreases by 1", "Mass number increases by 1",
         "Mass number decreases by 1", "A", "Nuclei", "Beta Decay", "hard"),
        ("Half-life of radioactive element: If N₀ = 1000 and t₁/₂ = 2 years, "
         "after 6 years N =", "125", "250", "500", "62.5", "A",
         "Nuclei", "Radioactivity", "hard"),
        ("Binding energy per nucleon is maximum for:", "⁵⁶Fe", "²³⁵U",
         "²H", "⁴He", "A", "Nuclei", "Nuclear Binding Energy", "hard"),
        ("Mass defect is:", "Difference between actual mass and sum of masses of nucleons",
         "Extra mass of nucleus", "Mass of electrons", "None", "A",
         "Nuclei", "Nuclear Binding Energy", "hard"),
        ("Chain reaction in nuclear fission requires:", "Critical mass",
         "High temperature", "Magnetic field", "High pressure", "A",
         "Nuclei", "Nuclear Fission", "medium"),
        ("Nuclear fusion requires:", "Very high temperature",
         "Critical mass", "Moderator", "Control rods", "A",
         "Nuclei", "Nuclear Fusion", "medium"),
        ("The activity of radioactive sample is measured in:", "Becquerel",
         "Joule", "Electron volt", "Curie only", "A",
         "Nuclei", "Radioactivity", "medium"),
    ]
    for con in nuclear:
        qs.append(q(*con))

    # Semiconductors
    semicond = [
        ("In n-type semiconductor, majority carriers are:", "Electrons",
         "Holes", "Protons", "Neutrons", "A",
         "Semiconductor Electronics", "Semiconductor Basics", "medium"),
        ("The depletion region in a p-n junction has:", "No mobile charges",
         "Only electrons", "Only holes", "Equal electrons and holes", "A",
         "Semiconductor Electronics", "p-n Junction", "medium"),
        ("Forward bias of p-n junction: barrier potential:", "Decreases",
         "Increases", "Remains same", "Disappears completely", "A",
         "Semiconductor Electronics", "p-n Junction", "medium"),
        ("LED works on the principle of:", "Electroluminescence",
         "Photoconductivity", "Photoelectric effect", "Cherenkov radiation", "A",
         "Semiconductor Electronics", "LED", "medium"),
        ("NAND gate is a combination of:", "NOT gate and AND gate",
         "NOT gate and OR gate", "AND gate and OR gate", "Two NOT gates", "A",
         "Semiconductor Electronics", "Logic Gates", "medium"),
        ("Zener diode is used as:", "Voltage regulator", "Rectifier",
         "Amplifier", "Oscillator", "A",
         "Semiconductor Electronics", "Zener Diode", "medium"),
        ("Which logic gate gives output 1 when all inputs are 0?", "NOR gate",
         "NAND gate", "AND gate", "OR gate", "A",
         "Semiconductor Electronics", "Logic Gates", "hard"),
        ("Forbidden energy gap of silicon at room temperature is approximately:",
         "1.1 eV", "0.7 eV", "5.5 eV", "3.3 eV", "A",
         "Semiconductor Electronics", "Energy Bands", "hard"),
        ("Valence band of insulator is:", "Completely filled",
         "Completely empty", "Half filled", "Partially filled", "A",
         "Semiconductor Electronics", "Energy Bands", "medium"),
    ]
    for con in semicond:
        qs.append(q(*con))

    return qs


def gen_magnetism():
    qs = []

    # Magnetic force
    mag_force = [
        (1e-3, 2, 0.5, 90, "0.001 N", "0.002 N", "0.0005 N", "0.01 N", "A"),
        (5e-3, 3, 0.4, 90, "0.006 N", "0.012 N", "0.003 N", "0.06 N", "A"),
        (2e-3, 5, 0.3, 90, "0.003 N", "0.006 N", "0.0015 N", "0.03 N", "A"),
        (1e-3, 4, 0.5, 30, "0.001 N", "0.002 N", "0.0005 N", "0.004 N", "A"),
    ]
    for q_val, I, B, theta, ans, w1, w2, w3, cor in mag_force:
        import math
        F = q_val * I * B * math.sin(math.radians(theta))
        qs.append(q(
            f"A wire of length {q_val*1000:.0f} mm carries current {I} A in magnetic field {B} T "
            f"at {theta}° to field. Force on wire is:",
            ans, w1, w2, w3, cor,
            "Magnetism", "Force on Current-Carrying Conductor", "hard",
            f"F = BIL sinθ = {B}×{I}×{q_val}×sin({theta}°) = {F:.4f} N"
        ))

    # Conceptual magnetism
    mag_concept = [
        ("A magnetic field can be produced by:", "Moving charges",
         "Static charges", "Gravitational field", "Electric field alone", "A",
         "Magnetism", "Sources of Magnetic Field", "medium"),
        ("Biot-Savart law gives:", "Magnetic field due to current element",
         "Electric field due to charge", "Force between magnets",
         "Magnetic flux", "A", "Magnetism", "Biot-Savart Law", "hard"),
        ("The SI unit of magnetic field (B) is:", "Tesla", "Weber",
         "Henry", "Ampere", "A", "Magnetism", "Basic Definitions", "medium"),
        ("A magnetic dipole in uniform field experiences:", "Only torque",
         "Only force", "Both force and torque", "Neither", "A",
         "Magnetism", "Magnetic Dipole", "hard"),
        ("Magnetic moment of current loop = ?", "I×A", "I/A", "A/I", "I²A", "A",
         "Magnetism", "Current Loop", "medium"),
        ("Diamagnetic materials are:", "Weakly repelled by magnets",
         "Strongly attracted by magnets", "Weakly attracted", "Not affected", "A",
         "Magnetism", "Magnetic Materials", "medium"),
        ("Curie temperature is related to:", "Loss of ferromagnetism",
         "Loss of diamagnetism", "Maximum magnetism", "Zero magnetism always", "A",
         "Magnetism", "Magnetic Materials", "hard"),
        ("Earth's magnetic field at the poles is:", "Vertical",
         "Horizontal", "At 45° to surface", "Zero", "A",
         "Magnetism", "Earth's Magnetism", "medium"),
        ("Tangent galvanometer measures:", "Current", "Voltage",
         "Resistance", "Power", "A", "Magnetism", "Measuring Instruments", "medium"),
        ("Ampere's circuital law is analogous to:", "Gauss's law in electrostatics",
         "Faraday's law", "Coulomb's law", "Ohm's law", "A",
         "Magnetism", "Ampere's Law", "hard"),
    ]
    for con in mag_concept:
        qs.append(q(*con))

    return qs


def gen_waves():
    qs = []

    # Wave parameters
    wave_cases = [
        (340, 1000, "0.34 m", "0.68 m", "0.17 m", "340 m", "A"),
        (340, 500, "0.68 m", "1.36 m", "0.34 m", "170 m", "A"),
        (340, 200, "1.7 m", "3.4 m", "0.85 m", "68 m", "A"),
        (1500, 1000, "1.5 m", "3 m", "0.75 m", "1500 m", "A"),
        (340, 17000, "0.02 m", "0.04 m", "0.01 m", "0.34 m", "A"),
        (6000, 1000, "6 m", "12 m", "3 m", "6000 m", "A"),
        (340, 85, "4 m", "8 m", "2 m", "28.9 m", "A"),
        (340, 170, "2 m", "4 m", "1 m", "57.8 m", "A"),
    ]
    for v, f, ans, w1, w2, w3, cor in wave_cases:
        lam = v / f
        qs.append(q(
            f"A sound wave travels at {v} m/s with frequency {f} Hz. Wavelength is:",
            ans, w1, w2, w3, cor,
            "Waves", "Wave Parameters", "medium",
            f"λ = v/f = {v}/{f} = {lam:.3f} m"
        ))

    # Doppler effect
    doppler = [
        (340, 340, 50, 0, "680 Hz", "340 Hz", "510 Hz", "425 Hz", "A"),
        (340, 0, 50, 340, "170 Hz", "340 Hz", "510 Hz", "0 Hz", "A"),
        (340, 680, 50, 0, "∞ Hz (undefined)", "340 Hz", "680 Hz", "1020 Hz", "A"),
    ]
    for v_sound, v_obs, f_src, v_src, ans, w1, w2, w3, cor in doppler:
        qs.append(q(
            f"Source of frequency {f_src} Hz moves at {v_src} m/s, observer at {v_obs} m/s "
            f"towards each other. Observed frequency: (v_sound = {v_sound} m/s)",
            ans, w1, w2, w3, cor,
            "Waves", "Doppler Effect", "very_hard",
        ))

    # Conceptual waves
    wave_concept = [
        ("Sound waves are:", "Longitudinal waves", "Transverse waves",
         "Electromagnetic waves", "Both longitudinal and transverse", "A",
         "Waves", "Types of Waves", "medium"),
        ("Speed of sound in air at 0°C is approximately:", "332 m/s",
         "300 m/s", "340 m/s", "400 m/s", "A", "Waves", "Speed of Sound", "medium"),
        ("In a standing wave, nodes are points of:", "Zero displacement",
         "Maximum displacement", "Maximum velocity", "Zero pressure", "A",
         "Waves", "Standing Waves", "medium"),
        ("Beat frequency = ?", "Difference in frequencies of two waves",
         "Sum of frequencies", "Product of frequencies", "Average frequency", "A",
         "Waves", "Beats", "medium"),
        ("Resonance occurs when:", "Frequency of driving force = natural frequency",
         "Amplitude is maximum always", "Phase is zero", "Wavelength equals length", "A",
         "Waves", "Resonance", "medium"),
        ("Organ pipe open at both ends has resonance at:", "All harmonics",
         "Only odd harmonics", "Only even harmonics", "Only fundamental", "A",
         "Waves", "Organ Pipes", "hard"),
        ("Organ pipe closed at one end resonates at:", "Only odd harmonics",
         "All harmonics", "Only even harmonics", "Only fundamental", "A",
         "Waves", "Organ Pipes", "hard"),
        ("Intensity of sound is proportional to:", "Amplitude²",
         "Amplitude", "Frequency", "Wavelength", "A",
         "Waves", "Sound Intensity", "medium"),
        ("Ultrasonic waves have frequency:", "Greater than 20,000 Hz",
         "Less than 20 Hz", "20 Hz to 20,000 Hz", "Exactly 20,000 Hz", "A",
         "Waves", "Sound Waves", "medium"),
        ("Doppler effect is observed for:", "Both sound and light",
         "Only sound", "Only light", "Neither", "A",
         "Waves", "Doppler Effect", "medium"),
    ]
    for con in wave_concept:
        qs.append(q(*con))

    return qs


def gen_electromagnetic_induction():
    qs = []
    emi_concept = [
        ("Faraday's law states that induced EMF is proportional to:",
         "Rate of change of magnetic flux", "Magnetic field strength",
         "Current in conductor", "Charge", "A",
         "Electromagnetic Induction", "Faraday's Law", "medium"),
        ("Lenz's law is consequence of:", "Conservation of energy",
         "Conservation of charge", "Newton's third law", "Ampere's law", "A",
         "Electromagnetic Induction", "Lenz's Law", "medium"),
        ("Self-inductance L is defined by:", "EMF = -L(dI/dt)",
         "EMF = L(dI/dt)", "EMF = LI", "EMF = L/I", "A",
         "Electromagnetic Induction", "Self-Inductance", "hard"),
        ("Energy stored in inductor = ?", "½LI²", "LI²", "½LI", "L²I", "A",
         "Electromagnetic Induction", "Energy in Inductor", "hard"),
        ("SI unit of inductance is:", "Henry", "Tesla", "Weber", "Farad", "A",
         "Electromagnetic Induction", "Self-Inductance", "medium"),
        ("Eddy currents are minimized by:", "Using laminated cores",
         "Using thicker cores", "Increasing frequency", "Using soft iron", "A",
         "Electromagnetic Induction", "Eddy Currents", "medium"),
        ("Transformer works on principle of:", "Mutual inductance",
         "Self-inductance", "Lenz's law", "Faraday's motor", "A",
         "Electromagnetic Induction", "Transformer", "medium"),
        ("Step-up transformer increases:", "Voltage", "Current",
         "Power", "Frequency", "A",
         "Electromagnetic Induction", "Transformer", "medium"),
        ("In AC circuit, current leads voltage in:", "Purely capacitive circuit",
         "Purely inductive circuit", "Purely resistive circuit", "None", "A",
         "Alternating Current", "AC Circuits", "hard"),
        ("Resonance in LCR circuit when:", "ω = 1/√(LC)",
         "ω = √(LC)", "ω = LC", "ω = 1/LC", "A",
         "Alternating Current", "LCR Resonance", "very_hard"),
        ("Power factor of purely inductive circuit is:", "Zero",
         "One", "0.5", "Infinity", "A",
         "Alternating Current", "Power Factor", "hard"),
        ("RMS value of AC = ?", "Peak value/√2", "2×Peak value",
         "Peak value/2", "Peak value×√2", "A",
         "Alternating Current", "RMS Values", "medium"),
    ]
    for con in emi_concept:
        qs.append(q(*con))

    # EMF calculation
    emf_cases = [
        (0.5, 2, "1 V", "0.25 V", "4 V", "2 V", "A"),
        (1, 5, "5 V", "0.2 V", "25 V", "10 V", "A"),
        (2, 3, "6 V", "1.5 V", "12 V", "0.67 V", "A"),
        (0.1, 10, "1 V", "0.01 V", "100 V", "10 V", "A"),
        (3, 4, "12 V", "0.75 V", "6 V", "48 V", "A"),
        (0.5, 6, "3 V", "0.083 V", "12 V", "0.33 V", "A"),
    ]
    for dPhi, dt, ans, w1, w2, w3, cor in emf_cases:
        EMF = dPhi / dt
        qs.append(q(
            f"Magnetic flux changes by {dPhi} Wb in {dt} s. The induced EMF is:",
            ans, w1, w2, w3, cor,
            "Electromagnetic Induction", "Induced EMF", "medium",
            f"EMF = ΔΦ/Δt = {dPhi}/{dt} = {EMF} V"
        ))

    return qs


def gen_very_hard_physics():
    """Generate very hard/advanced physics questions."""
    qs = []
    hard_qs = [
        ("A particle moves in a potential well U(x) = ½kx². The frequency of oscillation is:",
         "(1/2π)√(k/m)", "√(k/m)", "(1/2π)√(m/k)", "2π√(k/m)", "A",
         "Oscillations", "SHM", "very_hard"),
        ("In Compton scattering, shift in wavelength Δλ =",
         "(h/m_e c)(1 - cosθ)", "(h/m_e c)(1 + cosθ)",
         "h/(m_e c)", "(2h/m_e c)", "A",
         "Modern Physics", "Compton Effect", "very_hard"),
        ("Uncertainty principle: ΔxΔp ≥", "h/4π", "h/2π", "h", "h/2", "A",
         "Modern Physics", "Heisenberg's Principle", "very_hard"),
        ("The Schrödinger equation is:", "Time-dependent differential equation",
         "Algebraic equation", "Statistical equation", "Newton's law in QM", "A",
         "Modern Physics", "Quantum Mechanics", "very_hard"),
        ("Black body radiation peak wavelength follows:", "Wien's displacement law",
         "Stefan's law", "Kirchhoff's law", "Planck's law", "A",
         "Thermodynamics", "Black Body Radiation", "very_hard"),
        ("For a rotating body, angular momentum L = ?", "Iω", "Iα", "τ/ω", "Fω", "A",
         "Rotational Motion", "Angular Momentum", "very_hard"),
        ("In special relativity, the relativistic mass m =", "m₀/√(1-v²/c²)",
         "m₀√(1-v²/c²)", "m₀(1-v²/c²)", "m₀/(1-v/c)", "A",
         "Modern Physics", "Special Relativity", "very_hard"),
        ("Maxwell's equations unify:", "Electricity and magnetism",
         "Gravity and electricity", "Quantum and classical mechanics",
         "All forces", "A", "Electromagnetic Waves", "Maxwell's Equations", "very_hard"),
        ("In quantum mechanics, the operator for momentum is:",
         "-iℏ(∂/∂x)", "iℏ(∂/∂x)", "ℏ/2π", "iℏ/∂x", "A",
         "Modern Physics", "Quantum Mechanics", "very_hard"),
        ("The Hall effect is used to:", "Determine carrier type and concentration",
         "Measure resistance", "Measure voltage only", "Heat conductors", "A",
         "Semiconductor Electronics", "Hall Effect", "very_hard"),
        ("Coriolis force acts on bodies in:", "Rotating reference frames",
         "Inertial frames only", "Vacuum only", "Both inertial and non-inertial", "A",
         "Mechanics", "Non-Inertial Frames", "very_hard"),
        ("Fermat's principle states light follows:", "Path of least time",
         "Straight line always", "Path of maximum intensity", "Shortest distance", "A",
         "Ray Optics", "Fermat's Principle", "very_hard"),
        ("Bernoulli's equation P + ½ρv² + ρgh = constant assumes flow is:",
         "Steady, incompressible, non-viscous", "Turbulent", "Compressible", "Viscous", "A",
         "Fluid Mechanics", "Bernoulli's Theorem", "very_hard"),
        ("Moment of inertia of solid sphere about diameter =", "2/5 mr²",
         "1/2 mr²", "2/3 mr²", "7/5 mr²", "A",
         "Rotational Motion", "Moment of Inertia", "very_hard"),
        ("Parallel axis theorem: I = I_cm + ?", "Md²", "Md", "2Md²", "Md²/2", "A",
         "Rotational Motion", "Moment of Inertia", "very_hard"),
        ("For an adiabatic process: PV^γ = constant. γ =", "C_p/C_v",
         "C_v/C_p", "C_p - C_v", "C_p + C_v", "A",
         "Thermodynamics", "Adiabatic Process", "very_hard"),
        ("Surface tension arises due to:", "Cohesive forces between molecules",
         "Adhesive forces", "Gravitational forces", "Electrostatic forces", "A",
         "Fluid Mechanics", "Surface Tension", "very_hard"),
        ("The coefficient of viscosity η has SI unit:", "Pa·s", "N/m²",
         "kg/m", "N·s/m", "A", "Fluid Mechanics", "Viscosity", "very_hard"),
        ("In Millikan's oil drop experiment, charge on oil drop is always:",
         "Multiple of e", "Equal to e", "Greater than e always", "Continuous", "A",
         "Modern Physics", "Quantization of Charge", "very_hard"),
        ("Clausius-Clapeyron equation relates:", "Vapor pressure and temperature",
         "Heat and entropy", "Work and energy", "Pressure and volume", "A",
         "Thermodynamics", "Phase Transitions", "very_hard"),
    ]
    for con in hard_qs:
        qs.append(q(*con))

    return qs


def generate_all_physics_questions() -> List[Dict]:
    """Generate all 5000+ physics questions."""
    all_qs = []
    all_qs.extend(gen_kinematics())
    all_qs.extend(gen_laws_of_motion())
    all_qs.extend(gen_work_energy())
    all_qs.extend(gen_gravitation())
    all_qs.extend(gen_thermodynamics())
    all_qs.extend(gen_electrostatics())
    all_qs.extend(gen_current_electricity())
    all_qs.extend(gen_optics())
    all_qs.extend(gen_modern_physics())
    all_qs.extend(gen_magnetism())
    all_qs.extend(gen_waves())
    all_qs.extend(gen_electromagnetic_induction())
    all_qs.extend(gen_very_hard_physics())

    # Boost count with multi-parametric variations
    extra = _gen_parametric_boost(all_qs)
    all_qs.extend(extra)

    # Ensure all have required fields
    for i, q_item in enumerate(all_qs):
        q_item["subject"] = "Physics"
        q_item["exam_type"] = "NEET"
        if "marks_correct" not in q_item:
            q_item["marks_correct"] = 4.0
        if "marks_wrong" not in q_item:
            q_item["marks_wrong"] = -1.0

    print(f"[Physics] Generated {len(all_qs)} questions")
    return all_qs


def _gen_parametric_boost(base_qs: List[Dict]) -> List[Dict]:
    """Generate additional unique questions by varying parameters in existing templates."""
    extra = []

    # Generate 100 more kinematics problems with different values
    for v0 in [5, 10, 15, 20, 25, 30]:
        for a_val in [2, 4, 6, 8]:
            for t in [2, 3, 4, 5]:
                s = v0 * t + 0.5 * a_val * t * t
                vf = v0 + a_val * t
                w1 = s * 1.5
                w2 = s * 0.5
                w3 = v0 * t
                opts = [f"{s:.1f} m", f"{w1:.1f} m", f"{w2:.1f} m", f"{w3:.1f} m"]
                extra.append({
                    "subject": "Physics", "exam_type": "NEET",
                    "topic": "Kinematics", "subtopic": "Equations of Motion",
                    "difficulty": "medium" if a_val <= 4 else "hard",
                    "question_en": f"A body with initial velocity {v0} m/s accelerates at {a_val} m/s². "
                                   f"Distance in {t} s is:",
                    "option_a_en": opts[0], "option_b_en": opts[1],
                    "option_c_en": opts[2], "option_d_en": opts[3],
                    "correct_answer": "A",
                    "explanation_en": f"s = v₀t + ½at² = {v0}×{t} + ½×{a_val}×{t}² = {s:.1f} m",
                    "marks_correct": 4.0, "marks_wrong": -1.0,
                })

    # Generate energy questions
    for m in [1, 2, 5, 10, 20]:
        for v in [5, 10, 15, 20, 30]:
            ke = 0.5 * m * v * v
            extra.append({
                "subject": "Physics", "exam_type": "NEET",
                "topic": "Work, Energy and Power", "subtopic": "Kinetic Energy",
                "difficulty": "medium",
                "question_en": f"KE of mass {m} kg moving at {v} m/s is:",
                "option_a_en": f"{ke:.0f} J", "option_b_en": f"{ke*2:.0f} J",
                "option_c_en": f"{ke/2:.0f} J", "option_d_en": f"{m*v:.0f} J",
                "correct_answer": "A",
                "explanation_en": f"KE = ½mv² = ½×{m}×{v}² = {ke:.0f} J",
                "marks_correct": 4.0, "marks_wrong": -1.0,
            })

    # PE questions
    for m in [1, 2, 5, 10]:
        for h in [5, 10, 20, 50, 100]:
            pe = m * 10 * h
            extra.append({
                "subject": "Physics", "exam_type": "NEET",
                "topic": "Work, Energy and Power", "subtopic": "Potential Energy",
                "difficulty": "medium",
                "question_en": f"Gravitational PE of {m} kg at height {h} m (g=10 m/s²) is:",
                "option_a_en": f"{pe} J", "option_b_en": f"{pe*2} J",
                "option_c_en": f"{pe//2} J", "option_d_en": f"{m*h} J",
                "correct_answer": "A",
                "explanation_en": f"PE = mgh = {m}×10×{h} = {pe} J",
                "marks_correct": 4.0, "marks_wrong": -1.0,
            })

    # Power questions
    for W in [100, 200, 500, 1000, 2000, 5000]:
        for t in [10, 20, 50, 100]:
            P = W / t
            extra.append({
                "subject": "Physics", "exam_type": "NEET",
                "topic": "Work, Energy and Power", "subtopic": "Power",
                "difficulty": "medium",
                "question_en": f"Work done = {W} J in {t} s. Power is:",
                "option_a_en": f"{P:.1f} W", "option_b_en": f"{P*2:.1f} W",
                "option_c_en": f"{P/2:.1f} W", "option_d_en": f"{W*t:.0f} W",
                "correct_answer": "A",
                "explanation_en": f"P = W/t = {W}/{t} = {P:.1f} W",
                "marks_correct": 4.0, "marks_wrong": -1.0,
            })

    # Ohm's law variations
    for V in [6, 9, 12, 24, 36, 48, 60, 120, 220, 240]:
        for R in [2, 3, 4, 5, 6, 8, 10, 12, 15, 20]:
            I = V / R
            extra.append({
                "subject": "Physics", "exam_type": "NEET",
                "topic": "Current Electricity", "subtopic": "Ohm's Law",
                "difficulty": "medium",
                "question_en": f"Voltage {V} V applied to resistance {R} Ω. Current flowing:",
                "option_a_en": f"{I:.2f} A", "option_b_en": f"{I*2:.2f} A",
                "option_c_en": f"{I/2:.2f} A", "option_d_en": f"{V*R:.0f} A",
                "correct_answer": "A",
                "explanation_en": f"I = V/R = {V}/{R} = {I:.2f} A",
                "marks_correct": 4.0, "marks_wrong": -1.0,
            })

    return extra
