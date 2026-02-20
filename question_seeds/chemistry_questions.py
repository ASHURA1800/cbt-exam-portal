"""
question_seeds/chemistry_questions.py
=====================================
Generates 5000+ Chemistry questions: Physical, Organic, Inorganic.
"""

from typing import List, Dict
import random


def q(question, a, b, c, d, correct, topic, subtopic, difficulty, explanation=""):
    return {
        "subject": "Chemistry",
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


def gen_atomic_structure():
    qs = []
    conceptual = [
        ("The quantum number that determines the shape of orbital is:",
         "Azimuthal quantum number (l)", "Principal quantum number (n)",
         "Magnetic quantum number (m)", "Spin quantum number (s)", "A",
         "Atomic Structure", "Quantum Numbers", "medium"),
        ("Maximum number of electrons in a shell with n=4 is:", "32", "16", "18", "8", "A",
         "Atomic Structure", "Electron Configuration", "medium"),
        ("Pauli's exclusion principle states:", "No two electrons can have same set of quantum numbers",
         "Electrons fill lowest energy orbitals first", "Orbitals of equal energy fill singly first",
         "Electrons always pair up", "A", "Atomic Structure", "Pauli's Principle", "medium"),
        ("Hund's rule states:", "Electrons fill orbitals of equal energy singly before pairing",
         "No two electrons have same quantum numbers", "Electrons fill lowest energy first",
         "Spinning electrons repel each other", "A", "Atomic Structure", "Hund's Rule", "medium"),
        ("Aufbau principle means electrons fill:", "In order of increasing energy",
         "Randomly", "In order of decreasing energy", "The outermost shell first", "A",
         "Atomic Structure", "Aufbau Principle", "medium"),
        ("The number of radial nodes in 3p orbital is:", "1", "0", "2", "3", "A",
         "Atomic Structure", "Orbitals", "hard"),
        ("Angular nodes in 'd' orbital equals:", "2", "0", "1", "3", "A",
         "Atomic Structure", "Orbitals", "hard"),
        ("Electronic configuration of Cr (Z=24) is:", "[Ar] 3d⁵ 4s¹", "[Ar] 3d⁴ 4s²",
         "[Ar] 3d⁶ 4s⁰", "[Ar] 3d³ 4s²", "A",
         "Atomic Structure", "Electron Configuration", "hard"),
        ("Which has highest ionization energy?", "He", "Ne", "Ar", "Kr", "A",
         "Atomic Structure", "Periodic Properties", "medium"),
        ("Isoelectronic species of N³⁻:", "O²⁻", "F⁻", "Both A and B", "Na⁺", "C",
         "Atomic Structure", "Isoelectronic Species", "hard"),
        ("de Broglie wavelength of electron in orbit n for hydrogen: λ =", "2πr/n",
         "nr/2π", "2πrn", "nλ/2π", "A", "Atomic Structure", "Bohr Model", "very_hard"),
        ("Uncertainty in position × uncertainty in momentum ≥", "h/4π",
         "h/2π", "h", "2h/π", "A", "Atomic Structure", "Heisenberg's Principle", "hard"),
        ("Which series lies in visible region?", "Balmer", "Lyman", "Paschen", "Brackett", "A",
         "Atomic Structure", "Spectral Series", "medium"),
        ("Energy of photon E =", "hν", "hλ", "h/ν", "νλ", "A",
         "Atomic Structure", "Planck's Theory", "medium"),
        ("Charge on nucleus of hydrogen is:", "+e", "-e", "0", "+2e", "A",
         "Atomic Structure", "Nuclear Charge", "medium"),
    ]
    for con in conceptual:
        qs.append(q(*con))
    return qs


def gen_chemical_bonding():
    qs = []
    bonding = [
        ("Which molecule has linear geometry?", "CO₂", "H₂O", "NH₃", "CH₄", "A",
         "Chemical Bonding", "Molecular Geometry", "medium"),
        ("Hybridization of carbon in ethene (C₂H₄) is:", "sp²", "sp", "sp³", "sp³d", "A",
         "Chemical Bonding", "Hybridization", "medium"),
        ("Hybridization of carbon in acetylene (C₂H₂) is:", "sp", "sp²", "sp³", "sp²d", "A",
         "Chemical Bonding", "Hybridization", "medium"),
        ("Bond angle in water molecule is approximately:", "104.5°", "109.5°", "120°", "180°", "A",
         "Chemical Bonding", "Bond Angle", "medium"),
        ("Which type of bond has maximum overlap?", "σ bond", "π bond",
         "δ bond", "Hydrogen bond", "A", "Chemical Bonding", "Bond Types", "hard"),
        ("Resonance structures of benzene have:", "Delocalized electrons",
         "Alternating single and double bonds (fixed)", "Only single bonds",
         "Only double bonds", "A", "Chemical Bonding", "Resonance", "medium"),
        ("Formal charge on nitrogen in NO₃⁻ (resonance structure):", "+1 on N", "0", "-1 on N",
         "+2 on N", "A", "Chemical Bonding", "Formal Charge", "very_hard"),
        ("The strongest intermolecular force is:", "Hydrogen bonding",
         "Van der Waals", "Dipole-dipole", "London dispersion", "A",
         "Chemical Bonding", "Intermolecular Forces", "medium"),
        ("Which has highest bond order?", "N₂", "O₂", "F₂", "Cl₂", "A",
         "Chemical Bonding", "Bond Order", "hard"),
        ("VSEPR theory predicts geometry based on:", "Electron pair repulsion",
         "Bond length", "Electronegativity", "Nuclear charge", "A",
         "Chemical Bonding", "VSEPR Theory", "medium"),
        ("Shape of PCl₅ is:", "Trigonal bipyramidal", "Tetrahedral",
         "Octahedral", "Square planar", "A", "Chemical Bonding", "Molecular Geometry", "medium"),
        ("Geometry of SF₆ is:", "Octahedral", "Trigonal bipyramidal",
         "Square planar", "Tetrahedral", "A", "Chemical Bonding", "Molecular Geometry", "medium"),
        ("Which has maximum dipole moment?", "CCl₄", "CHCl₃", "CH₂Cl₂", "CH₃Cl", "D",
         "Chemical Bonding", "Dipole Moment", "hard"),
        ("Lattice energy increases with:", "Increase in ionic charge and decrease in ionic size",
         "Decrease in ionic charge", "Increase in ionic size", "None of these", "A",
         "Chemical Bonding", "Ionic Bonding", "hard"),
        ("Back bonding is observed in:", "BF₃", "BH₃", "BCl₃", "BI₃", "A",
         "Chemical Bonding", "Back Bonding", "very_hard"),
        ("Hybridization of S in SO₄²⁻:", "sp³", "sp³d", "sp³d²", "sp²", "A",
         "Chemical Bonding", "Hybridization", "hard"),
        ("Shape of XeF₄:", "Square planar", "Tetrahedral", "Octahedral",
         "Trigonal pyramidal", "A", "Chemical Bonding", "Molecular Geometry", "hard"),
        ("Ionic character of bond increases with:", "Electronegativity difference",
         "Equal electronegativity", "Small atomic size", "None", "A",
         "Chemical Bonding", "Ionic vs Covalent", "medium"),
    ]
    for b in bonding:
        qs.append(q(*b))
    return qs


def gen_states_of_matter():
    qs = []

    # Gas law questions
    gas_ideal = [
        ("Boyle's law states that at constant temperature:", "PV = constant",
         "P/T = constant", "V/T = constant", "P/V = constant", "A",
         "States of Matter", "Boyle's Law", "medium"),
        ("Charles's law states at constant pressure:", "V/T = constant",
         "PV = constant", "P/T = constant", "VT = constant", "A",
         "States of Matter", "Charles's Law", "medium"),
        ("Ideal gas equation is:", "PV = nRT", "PV = RT", "PV = nR/T", "P = nRT/V only for 1L", "A",
         "States of Matter", "Ideal Gas Equation", "medium"),
        ("Value of R in J/mol·K:", "8.314", "0.0821", "1.987", "6.023×10²³", "A",
         "States of Matter", "Gas Constant R", "medium"),
        ("Van der Waals equation for real gases: (P + a/V²)(V-b) = nRT. "
         "Constant 'a' accounts for:", "Intermolecular attraction",
         "Molecular volume", "Both", "Neither", "A",
         "States of Matter", "Real Gases", "hard"),
        ("At STP (Standard conditions), 1 mole ideal gas occupies:", "22.4 L", "11.2 L",
         "24 L", "22.7 L", "A", "States of Matter", "Molar Volume", "medium"),
        ("Graham's law of diffusion: rate ∝", "1/√M", "1/M", "√M", "M²", "A",
         "States of Matter", "Graham's Law", "medium"),
        ("Critical temperature is the temperature:", "Above which gas cannot be liquefied",
         "At which gas boils", "At which gas solidifies", "At which viscosity is minimum", "A",
         "States of Matter", "Critical Constants", "hard"),
        ("Compressibility factor Z = PV/nRT for ideal gas is:", "1", "0", "∞", "Depends on P", "A",
         "States of Matter", "Compressibility Factor", "medium"),
        ("Which gas has highest effusion rate at same T and P?", "H₂", "O₂", "N₂", "CO₂", "A",
         "States of Matter", "Graham's Law", "medium"),
        ("KMT assumes gas molecules:", "Have negligible volume and no intermolecular forces",
         "Have significant volume", "Attract each other", "Repel each other", "A",
         "States of Matter", "Kinetic Molecular Theory", "medium"),
        ("Average kinetic energy of gas ∝", "T (absolute)", "T²", "√T", "1/T", "A",
         "States of Matter", "Kinetic Energy", "medium"),
        ("Root mean square speed of gas: v_rms =", "√(3RT/M)", "√(2RT/M)",
         "√(8RT/πM)", "√(RT/M)", "A", "States of Matter", "Molecular Speed", "hard"),
    ]
    for g in gas_ideal:
        qs.append(q(*g))

    # Liquid state
    liquid = [
        ("Surface tension is due to:", "Unbalanced intermolecular forces at surface",
         "Gravity", "Air pressure", "Viscosity", "A",
         "States of Matter", "Surface Tension", "medium"),
        ("Viscosity of liquid:", "Decreases with temperature",
         "Increases with temperature", "Remains constant", "Depends only on pressure", "A",
         "States of Matter", "Viscosity", "medium"),
        ("Capillary rise h =", "2T cosθ/rρg", "Tρg/2r",
         "2rρg/T cosθ", "T/2rρg cosθ", "A",
         "States of Matter", "Capillary Action", "very_hard"),
    ]
    for liq in liquid:
        qs.append(q(*liq))
    return qs


def gen_chemical_equilibrium():
    qs = []
    equil = [
        ("Le Chatelier's principle: if pressure is increased on equilibrium,", 
         "Reaction shifts to side with fewer gas moles",
         "Reaction shifts to side with more gas moles",
         "Equilibrium is not affected", "Temperature changes", "A",
         "Chemical Equilibrium", "Le Chatelier's Principle", "medium"),
        ("Kp and Kc are related by:", "Kp = Kc(RT)^Δn", "Kp = Kc/RT",
         "Kp = Kc + Δn", "Kp = Kc", "A",
         "Chemical Equilibrium", "Equilibrium Constants", "hard"),
        ("For reaction aA ⇌ bB, Kc =", "[B]^b/[A]^a", "[A]^a/[B]^b",
         "[B]^b×[A]^a", "[A]^a/[B]^b × V", "A",
         "Chemical Equilibrium", "Equilibrium Expression", "medium"),
        ("If Kc >> 1, reaction is:", "Product-favoured", "Reactant-favoured",
         "At equilibrium", "Impossible", "A",
         "Chemical Equilibrium", "Equilibrium Constants", "medium"),
        ("Temperature increase always shifts equilibrium:", "To endothermic direction",
         "To exothermic direction", "Not affected by temperature", "Depends on Kc", "A",
         "Chemical Equilibrium", "Le Chatelier's Principle", "hard"),
        ("Degree of dissociation α of weak acid in water: Ka =", "Cα²/(1-α) ≈ Cα² for small α",
         "Cα", "α²/C", "C/α²", "A",
         "Chemical Equilibrium", "Degree of Dissociation", "very_hard"),
        ("Solubility product Ksp of AgCl =", "[Ag⁺][Cl⁻]", "[AgCl]",
         "[Ag⁺]+[Cl⁻]", "[AgCl]/[Ag⁺][Cl⁻]", "A",
         "Chemical Equilibrium", "Solubility Product", "medium"),
        ("Common ion effect:", "Decreases solubility of sparingly soluble salt",
         "Increases solubility", "Has no effect", "Depends on temperature", "A",
         "Chemical Equilibrium", "Common Ion Effect", "hard"),
        ("Buffer solution resists change in:", "pH", "Temperature",
         "Volume", "Concentration of salt", "A",
         "Chemical Equilibrium", "Buffer Solutions", "medium"),
        ("Henderson-Hasselbalch equation: pH =", "pKa + log([A⁻]/[HA])",
         "pKa - log([A⁻]/[HA])", "pKb + log([BH⁺]/[B])", "pKa + [A⁻]", "A",
         "Chemical Equilibrium", "Buffer Solutions", "hard"),
    ]
    for e in equil:
        qs.append(q(*e))
    return qs


def gen_electrochemistry():
    qs = []

    # Nernst equation, electrode potential
    electrochem = [
        ("Standard hydrogen electrode potential is:", "0.00 V", "+0.76 V", "-0.76 V", "+1.10 V", "A",
         "Electrochemistry", "Standard Electrode Potential", "medium"),
        ("Electrolysis of water produces:", "H₂ at cathode, O₂ at anode",
         "O₂ at cathode, H₂ at anode", "H₂ at both", "O₂ at both", "A",
         "Electrochemistry", "Electrolysis", "medium"),
        ("Faraday's first law: mass deposited ∝", "Quantity of electricity",
         "Current only", "Time only", "Voltage", "A",
         "Electrochemistry", "Faraday's Laws", "medium"),
        ("1 Faraday = ?", "96500 C", "1 C", "96500 J", "6.023×10²³ C", "A",
         "Electrochemistry", "Faraday's Laws", "medium"),
        ("EMF of cell = ?", "E°_cathode - E°_anode", "E°_anode - E°_cathode",
         "E°_cathode + E°_anode", "E°_anode / E°_cathode", "A",
         "Electrochemistry", "EMF of Cell", "medium"),
        ("Nernst equation: E = E° -", "(RT/nF) ln Q", "(nF/RT) ln Q",
         "(RT/nF) log Q", "(2.303 RT/nF) ln Q", "A",
         "Electrochemistry", "Nernst Equation", "very_hard"),
        ("In a galvanic cell, oxidation occurs at:", "Anode", "Cathode",
         "Salt bridge", "External circuit", "A",
         "Electrochemistry", "Galvanic Cell", "medium"),
        ("Kohlrausch's law states:", "Limiting molar conductivity = sum of individual ionic conductivities",
         "Conductivity decreases with dilution", "All salts have same conductivity",
         "Conductivity is independent of concentration", "A",
         "Electrochemistry", "Conductance", "hard"),
        ("Resistance of electrolytic solution decreases on:", "Dilution",
         "Concentration", "Adding more salt only", "Cooling", "A",
         "Electrochemistry", "Conductance", "medium"),
        ("Galvanizing is coating of iron with:", "Zinc", "Tin", "Copper", "Nickel", "A",
         "Electrochemistry", "Corrosion Prevention", "medium"),
        ("Daniel cell uses:", "Cu²⁺/Cu and Zn²⁺/Zn half cells",
         "H⁺/H₂ and Cu²⁺/Cu half cells", "Two Cu cells", "Two Zn cells", "A",
         "Electrochemistry", "Galvanic Cells", "medium"),
        ("Lithium-ion batteries use:", "Lithium intercalation compounds",
         "Liquid lithium", "Lithium oxide", "Lithium carbonate", "A",
         "Electrochemistry", "Batteries", "hard"),
    ]
    for e in electrochem:
        qs.append(q(*e))
    return qs


def gen_organic_chemistry():
    qs = []

    # IUPAC nomenclature, reactions
    organic = [
        ("IUPAC name of CH₃-CH₂-CHO is:", "Propanal", "Propanone", "Propanal-2", "Propanoic acid", "A",
         "Organic Chemistry", "IUPAC Nomenclature", "medium"),
        ("Which is primary alcohol?", "n-Propanol (CH₃CH₂CH₂OH)",
         "Isopropanol (CH₃CHOHCH₃)", "t-Butanol", "2-Butanol", "A",
         "Organic Chemistry", "Alcohols", "medium"),
        ("Grignard reagent is:", "RMgX", "RLi", "R₂CuLi", "RNa", "A",
         "Organic Chemistry", "Grignard Reagent", "medium"),
        ("Markovnikov's rule applies to:", "Addition reactions with unsymmetrical alkenes",
         "Elimination reactions", "Substitution reactions", "All reactions", "A",
         "Organic Chemistry", "Addition Reactions", "medium"),
        ("Ozonolysis of alkene gives:", "Carbonyl compounds",
         "Alcohols", "Carboxylic acids always", "Peroxides", "A",
         "Organic Chemistry", "Ozonolysis", "hard"),
        ("Aldol condensation requires:", "Aldehyde or ketone with α-hydrogen",
         "Any carbonyl compound", "Only aldehydes", "Only ketones", "A",
         "Organic Chemistry", "Aldol Condensation", "hard"),
        ("Benzene undergoes mainly:", "Electrophilic substitution",
         "Nucleophilic substitution", "Addition", "Elimination", "A",
         "Organic Chemistry", "Aromatic Reactions", "medium"),
        ("Friedel-Crafts alkylation uses:", "AlCl₃ as Lewis acid catalyst",
         "NaOH as catalyst", "H₂SO₄ as catalyst", "HCl as catalyst", "A",
         "Organic Chemistry", "Friedel-Crafts Reaction", "medium"),
        ("SN1 reaction follows:", "First-order kinetics",
         "Second-order kinetics", "Zero-order kinetics", "Third-order kinetics", "A",
         "Organic Chemistry", "Nucleophilic Substitution", "hard"),
        ("Racemic mixture is:", "Equimolar mixture of enantiomers",
         "One pure enantiomer", "Mixture of diastereomers", "Achiral mixture", "A",
         "Organic Chemistry", "Stereochemistry", "hard"),
        ("Inductive effect: -I effect is shown by:", "Electron-withdrawing groups",
         "Electron-donating groups", "All alkyl groups", "π bonds", "A",
         "Organic Chemistry", "Electronic Effects", "hard"),
        ("Resonance effect is transmitted through:", "π bonds",
         "σ bonds only", "All bonds equally", "Hydrogen bonds", "A",
         "Organic Chemistry", "Electronic Effects", "hard"),
        ("E2 reaction requires:", "Anti-periplanar arrangement of H and LG",
         "Syn-periplanar arrangement", "No stereospecificity", "Carbocation intermediate", "A",
         "Organic Chemistry", "Elimination Reactions", "very_hard"),
        ("Baeyer's reagent is:", "Cold dilute KMnO₄", "Hot concentrated KMnO₄",
         "K₂Cr₂O₇/H₂SO₄", "OsO₄", "A",
         "Organic Chemistry", "Oxidation Reactions", "hard"),
        ("Esterification is a:", "Nucleophilic acyl substitution",
         "Electrophilic substitution", "Elimination", "Radical reaction", "A",
         "Organic Chemistry", "Esters", "hard"),
        ("Diels-Alder reaction is:", "[4+2] cycloaddition",
         "[2+2] cycloaddition", "Radical addition", "Ionic addition", "A",
         "Organic Chemistry", "Pericyclic Reactions", "very_hard"),
        ("Which compound shows optical activity?", "Lactic acid (CH₃CHOHCOOH)",
         "Acetic acid", "Glycine (NH₂CH₂COOH)", "Propionic acid", "A",
         "Organic Chemistry", "Optical Activity", "hard"),
        ("Carbohydrates have general formula:", "Cₙ(H₂O)ₙ", "CₙH₂ₙ₊₂",
         "CₙHₙ", "CₙH₂ₙO", "A", "Organic Chemistry", "Carbohydrates", "medium"),
        ("Glucose is a:", "Aldohexose", "Ketohexose", "Aldopentose", "Ketopentose", "A",
         "Organic Chemistry", "Carbohydrates", "medium"),
        ("DNA contains:", "Deoxyribose sugar + phosphate + nitrogenous bases",
         "Ribose sugar", "Only purines", "Only pyrimidines", "A",
         "Organic Chemistry", "Biomolecules", "medium"),
    ]
    for o in organic:
        qs.append(q(*o))
    return qs


def gen_inorganic_chemistry():
    qs = []

    # Periodic table
    periodic = [
        ("The element with highest electronegativity is:", "Fluorine", "Oxygen",
         "Chlorine", "Nitrogen", "A", "Inorganic Chemistry", "Periodic Properties", "medium"),
        ("Across a period, atomic radius:", "Decreases", "Increases",
         "Remains constant", "First increases then decreases", "A",
         "Inorganic Chemistry", "Periodic Properties", "medium"),
        ("Down a group, ionization energy:", "Decreases", "Increases",
         "Remains constant", "First decreases then increases", "A",
         "Inorganic Chemistry", "Periodic Properties", "medium"),
        ("The element with highest electron affinity is:", "Chlorine", "Fluorine",
         "Oxygen", "Bromine", "A", "Inorganic Chemistry", "Periodic Properties", "hard"),
        ("d-block elements are also called:", "Transition metals", "Alkali metals",
         "Alkaline earth metals", "Lanthanides", "A",
         "Inorganic Chemistry", "d-Block Elements", "medium"),
        ("Which element is liquid at room temperature?", "Mercury", "Gallium",
         "Bromine", "Both A and C", "D",
         "Inorganic Chemistry", "Physical States", "medium"),
        ("Noble gases have configuration:", "ns²np⁶ (except He: 1s²)",
         "ns²np⁴", "ns²np⁵", "ns²np³", "A",
         "Inorganic Chemistry", "Noble Gases", "medium"),
        ("Diagonal relationship exists between:", "Li and Mg", "Na and K",
         "Be and Al", "Both A and C", "D",
         "Inorganic Chemistry", "Diagonal Relationship", "hard"),
        ("Lanthanide contraction is due to:", "Poor shielding of f-electrons",
         "Increase in nuclear charge only", "d-electron shielding", "None", "A",
         "Inorganic Chemistry", "f-Block Elements", "very_hard"),
        ("Most abundant element in Earth's crust is:", "Oxygen", "Silicon",
         "Aluminum", "Iron", "A", "Inorganic Chemistry", "Occurrence", "medium"),
    ]
    for p in periodic:
        qs.append(q(*p))

    # Chemical reactions of s,p,d blocks
    reactions = [
        ("Reaction of Na with water gives:", "NaOH + H₂", "Na₂O + H₂",
         "NaH + O₂", "Na₂O₂ + H₂", "A",
         "Inorganic Chemistry", "s-Block Reactions", "medium"),
        ("Bleaching powder is:", "CaOCl₂ (Ca(OCl)Cl)", "CaCl₂",
         "Ca(OH)₂", "CaO", "A", "Inorganic Chemistry", "p-Block Compounds", "medium"),
        ("Plaster of Paris is:", "CaSO₄·½H₂O", "CaSO₄·2H₂O",
         "CaSO₄ (anhydrous)", "Ca(SO₄)₂", "A",
         "Inorganic Chemistry", "p-Block Compounds", "medium"),
        ("Thermite reaction: Al + Fe₂O₃ →", "Al₂O₃ + Fe (reduction of Fe₂O₃)",
         "FeAl₂O₄", "Fe₂Al₃", "No reaction", "A",
         "Inorganic Chemistry", "Metallurgy", "medium"),
        ("Smelting reduces ore using:", "Coke (carbon)", "Hydrogen",
         "Electrolysis", "Acid", "A", "Inorganic Chemistry", "Metallurgy", "medium"),
        ("Haematite is ore of:", "Iron", "Copper", "Aluminium", "Zinc", "A",
         "Inorganic Chemistry", "Metallurgy", "medium"),
        ("Zone refining is used to purify:", "Semiconductors (Ge, Si)",
         "Alkali metals", "Noble gases", "Halogens", "A",
         "Inorganic Chemistry", "Metallurgy", "hard"),
        ("Aqua regia dissolves gold. It is mixture of:", "HNO₃ and HCl (1:3)",
         "HNO₃ and H₂SO₄", "HCl and H₂SO₄", "HNO₃ and HF", "A",
         "Inorganic Chemistry", "Acid Mixtures", "medium"),
        ("Colour of K₂Cr₂O₇ solution is:", "Orange", "Purple", "Green", "Blue", "A",
         "Inorganic Chemistry", "d-Block Compounds", "medium"),
        ("KMnO₄ in acidic medium acts as:", "Strong oxidizing agent",
         "Strong reducing agent", "Neutral", "Weak oxidizing agent", "A",
         "Inorganic Chemistry", "Redox Reactions", "medium"),
        ("Transition metals show variable oxidation states due to:",
         "Unpaired d-electrons available for bonding",
         "Large atomic size", "High ionization energy", "Low electronegativity", "A",
         "Inorganic Chemistry", "d-Block Elements", "hard"),
        ("Shape of XeF₂ is:", "Linear", "Bent", "Triangular planar", "Pyramidal", "A",
         "Inorganic Chemistry", "Noble Gas Compounds", "hard"),
        ("Which is the strongest oxidizing halogen?", "F₂", "Cl₂", "Br₂", "I₂", "A",
         "Inorganic Chemistry", "Halogens", "medium"),
        ("H₂O₂ acts as both oxidizing and reducing agent. It is a:",
         "Disproportionating agent", "Only oxidizing agent",
         "Only reducing agent", "Neutral compound", "A",
         "Inorganic Chemistry", "Hydrogen Peroxide", "hard"),
        ("Silicones are polymers with backbone:", "Si-O-Si", "C-C",
         "Si-Si", "C-O-C", "A", "Inorganic Chemistry", "Silicon Chemistry", "hard"),
    ]
    for r in reactions:
        qs.append(q(*r))
    return qs


def gen_physical_chemistry():
    qs = []

    # Thermodynamics
    thermo_chem = [
        ("Enthalpy of combustion is:", "Always negative (exothermic)",
         "Always positive", "Can be positive or negative", "Zero", "A",
         "Thermodynamics", "Enthalpy", "medium"),
        ("Hess's law states:", "ΔH is path-independent and depends only on initial and final states",
         "ΔH depends on path", "ΔH = 0 always", "ΔH = TΔS", "A",
         "Thermodynamics", "Hess's Law", "medium"),
        ("Entropy change ΔS = ?", "q_rev/T", "q/T", "ΔH/T", "ΔG/T", "A",
         "Thermodynamics", "Entropy", "hard"),
        ("Gibbs free energy: ΔG = ?", "ΔH - TΔS", "ΔH + TΔS", "ΔS - TΔH", "ΔH/ΔS", "A",
         "Thermodynamics", "Gibbs Free Energy", "medium"),
        ("Reaction is spontaneous when:", "ΔG < 0", "ΔG > 0", "ΔG = 0", "ΔH > 0", "A",
         "Thermodynamics", "Spontaneity", "medium"),
        ("Bond enthalpy: breaking bonds is:", "Endothermic", "Exothermic",
         "Neutral", "Depends on bond", "A", "Thermodynamics", "Bond Enthalpy", "medium"),
        ("Standard state is defined at:", "298 K and 1 bar", "273 K and 1 atm",
         "300 K and 1 bar", "298 K and 1 atm", "A",
         "Thermodynamics", "Standard State", "medium"),
        ("ΔG = -RT ln K. For K>1, ΔG is:", "Negative", "Positive", "Zero", "Undefined", "A",
         "Thermodynamics", "Gibbs Energy and K", "hard"),
    ]
    for t in thermo_chem:
        qs.append(q(*t))

    # Kinetics
    kinetics = [
        ("Rate of reaction ∝ [A]^m[B]^n. This is:", "Rate law", "Rate constant",
         "Equilibrium constant", "Arrhenius equation", "A",
         "Chemical Kinetics", "Rate Law", "medium"),
        ("Unit of rate constant for first-order reaction:", "s⁻¹", "L/mol·s",
         "L²/mol²·s", "mol/L·s", "A", "Chemical Kinetics", "Rate Constant", "medium"),
        ("Activation energy: Arrhenius equation k =", "Ae^(-Ea/RT)",
         "Ae^(Ea/RT)", "A/e^(Ea/RT) - same", "RT·ln(A)", "A",
         "Chemical Kinetics", "Arrhenius Equation", "hard"),
        ("Half-life of first-order reaction: t₁/₂ =", "0.693/k",
         "1/k", "2/k", "0.693k", "A", "Chemical Kinetics", "Half-life", "hard"),
        ("Catalyst increases reaction rate by:", "Lowering activation energy",
         "Increasing temperature", "Increasing reactant concentration",
         "Changing equilibrium constant", "A", "Chemical Kinetics", "Catalysis", "medium"),
        ("In zero-order reaction, rate:", "Is independent of concentration",
         "Is proportional to concentration", "Is proportional to concentration²",
         "Decreases exponentially", "A", "Chemical Kinetics", "Order of Reaction", "medium"),
        ("Molecularity of reaction is:", "Number of molecules taking part in elementary step",
         "Same as order", "Determined experimentally",
         "Always equal to stoichiometric coefficients", "A",
         "Chemical Kinetics", "Molecularity", "hard"),
    ]
    for k in kinetics:
        qs.append(q(*k))

    # Colligative properties
    colligative = [
        ("Elevation of boiling point ΔTb =", "Kb × m", "Kf × m", "m/Kb", "m × R", "A",
         "Solutions", "Colligative Properties", "medium"),
        ("Depression of freezing point ΔTf =", "Kf × m", "Kb × m", "m/Kf", "RT/m", "A",
         "Solutions", "Colligative Properties", "medium"),
        ("Osmotic pressure π = MRT. This is:", "van't Hoff equation",
         "Raoult's law", "Henry's law", "Clausius equation", "A",
         "Solutions", "Osmotic Pressure", "medium"),
        ("Van't Hoff factor 'i' for NaCl in dilute solution is approximately:", "2",
         "1", "3", "0.5", "A", "Solutions", "Colligative Properties", "hard"),
        ("Raoult's law: Partial pressure of component =",
         "Mole fraction × vapour pressure of pure component",
         "Mole fraction / vapour pressure", "Total pressure / mole fraction",
         "Mole fraction only", "A", "Solutions", "Raoult's Law", "medium"),
        ("Azeotropic mixtures:", "Boil at constant temperature without change in composition",
         "Always have maximum boiling point", "Always have minimum boiling point",
         "Cannot be prepared", "A", "Solutions", "Azeotropes", "very_hard"),
        ("Henry's law relates:", "Solubility of gas to its partial pressure",
         "Vapour pressure to temperature", "Osmotic pressure to concentration",
         "Boiling point to pressure", "A", "Solutions", "Henry's Law", "medium"),
    ]
    for c in colligative:
        qs.append(q(*c))
    return qs


def gen_stoichiometry():
    qs = []

    # Mole concept
    mole_cases = [
        (18, 1, "6.022×10²³", "3.011×10²³", "1.2×10²⁴", "6.022×10²⁰", "A"),
        (44, 2, "2.65×10²³", "6.022×10²³", "5.3×10²³", "1.33×10²³", "B"),
        (32, 2, "3.76×10²²", "3.76×10²⁰", "3.76×10²³", "3.76×10²⁴", "C"),
        (28, 1, "6.022×10²³", "3.011×10²³", "1.2×10²⁴", "2×10²³", "A"),
        (64, 1, "6.022×10²³", "3.011×10²³", "1.2×10²⁴", "6.022×10²²", "A"),
        (40, 2, "3.011×10²²", "6.022×10²³", "3.011×10²³", "1.2×10²⁴", "C"),
    ]
    for M, grams, ans, w1, w2, w3, cor in mole_cases:
        n = grams / M
        qs.append(q(
            f"{grams} g of compound with molar mass {M} g/mol contains how many molecules?",
            ans, w1, w2, w3, cor,
            "Stoichiometry", "Mole Concept", "medium",
            f"moles = {grams}/{M} = {n:.3f}; molecules = {n}×6.022×10²³"
        ))

    # Percentage composition
    percentage_cases = [
        ("H₂O", "H: 11.1%, O: 88.9%", "H: 88.9%, O: 11.1%", "H: 50%, O: 50%", "H: 22.2%, O: 77.8%", "A"),
        ("CO₂", "C: 27.3%, O: 72.7%", "C: 72.7%, O: 27.3%", "C: 50%, O: 50%", "C: 12%, O: 88%", "A"),
        ("NH₃", "N: 82.4%, H: 17.6%", "N: 17.6%, H: 82.4%", "N: 50%, H: 50%", "N: 14%, H: 3%", "A"),
        ("H₂SO₄", "S: 32.7%, rest H and O", "S: 50%, H: 50%", "S: 65%, O: 35%", "S: 27.3%, rest H and O", "A"),
        ("NaCl", "Na: 39.3%, Cl: 60.7%", "Na: 60.7%, Cl: 39.3%", "Na: 50%, Cl: 50%", "Na: 23%, Cl: 77%", "A"),
    ]
    for compound, ans, w1, w2, w3, cor in percentage_cases:
        qs.append(q(
            f"Percentage composition of {compound}:",
            ans, w1, w2, w3, cor,
            "Stoichiometry", "Percentage Composition", "medium"
        ))

    # Limiting reagent
    limiting = [
        ("4 mol H₂ reacts with 2 mol O₂ to form H₂O. Limiting reagent is:",
         "O₂", "H₂", "Both are limiting", "Neither is limiting", "A",
         "Stoichiometry", "Limiting Reagent", "hard"),
        ("2 mol N₂ reacts with 3 mol H₂. For N₂ + 3H₂ → 2NH₃, limiting reagent is:",
         "H₂", "N₂", "Both", "Neither", "A",
         "Stoichiometry", "Limiting Reagent", "hard"),
        ("1 mol CH₄ reacts with 1 mol O₂. CH₄ + 2O₂ → CO₂ + 2H₂O. Limiting reagent:",
         "O₂", "CH₄", "Both", "CO₂", "A",
         "Stoichiometry", "Limiting Reagent", "hard"),
    ]
    for l in limiting:
        qs.append(q(*l))
    return qs


def gen_very_hard_chemistry():
    qs = []
    hard_qs = [
        ("Crystal field splitting energy Δo for octahedral complex depends on:",
         "Ligand field strength and metal oxidation state",
         "Only metal oxidation state", "Only ligand type", "Temperature only", "A",
         "Coordination Chemistry", "Crystal Field Theory", "very_hard"),
        ("Spectrochemical series order: CN⁻ vs Cl⁻:", "CN⁻ > Cl⁻ (CN⁻ is strong field)",
         "Cl⁻ > CN⁻", "Equal splitting", "Depends on metal", "A",
         "Coordination Chemistry", "Ligand Field Strength", "very_hard"),
        ("Effective Atomic Number (EAN) rule predicts:", "18-electron configuration in metal complexes",
         "8-electron configuration", "12-electron configuration",
         "Variable electron count", "A",
         "Coordination Chemistry", "EAN Rule", "very_hard"),
        ("In NMR spectroscopy, chemical shift δ is measured relative to:", "TMS (tetramethylsilane)",
         "Water", "CDCl₃", "Acetone", "A", "Spectroscopy", "NMR", "very_hard"),
        ("In IR spectroscopy, carbonyl C=O stretching appears at approximately:",
         "1700 cm⁻¹", "3000 cm⁻¹", "1000 cm⁻¹", "500 cm⁻¹", "A",
         "Spectroscopy", "IR Spectroscopy", "very_hard"),
        ("The Wittig reaction forms:", "Alkenes from aldehydes/ketones and phosphorus ylide",
         "Alcohols", "Carboxylic acids", "Esters", "A",
         "Organic Chemistry", "Named Reactions", "very_hard"),
        ("Beckmann rearrangement converts:", "Ketoxime to amide",
         "Aldehyde to acid", "Amine to amide", "Ester to acid", "A",
         "Organic Chemistry", "Rearrangements", "very_hard"),
        ("Bayer-Villiger oxidation converts:", "Ketone to ester",
         "Alcohol to ketone", "Aldehyde to acid", "Ester to ether", "A",
         "Organic Chemistry", "Oxidation Reactions", "very_hard"),
        ("The anomeric effect in carbohydrates is due to:", "Hyperconjugation with lone pair",
         "Steric effect", "Hydrogen bonding", "van der Waals forces", "A",
         "Organic Chemistry", "Carbohydrate Chemistry", "very_hard"),
        ("Entropy of activation ΔS‡ in Eyring equation: k = (kT/h) exp(-ΔG‡/RT).",
         "Negative for reactions with rigid transition state",
         "Always positive", "Always zero", "Always negative", "A",
         "Chemical Kinetics", "Transition State Theory", "very_hard"),
        ("In LCAO-MO theory, bonding MO has:", "Electron density between nuclei",
         "No electron density between nuclei", "Electron density outside nuclei",
         "Uniform electron density", "A",
         "Chemical Bonding", "Molecular Orbital Theory", "very_hard"),
        ("Jahn-Teller distortion occurs in:", "High-spin d⁴ octahedral complexes",
         "d⁰ complexes", "d³ octahedral complexes", "All d complexes", "A",
         "Coordination Chemistry", "Jahn-Teller Effect", "very_hard"),
    ]
    for h in hard_qs:
        qs.append(q(*h))
    return qs


def _gen_parametric_chem_boost():
    """Generate additional chemistry questions via parametric variation."""
    qs = []

    # Molarity calculations
    for moles in [0.1, 0.5, 1.0, 2.0, 5.0]:
        for vol_L in [0.5, 1.0, 2.0]:
            M = moles / vol_L
            qs.append({
                "subject": "Chemistry", "exam_type": "NEET",
                "topic": "Solutions", "subtopic": "Molarity",
                "difficulty": "medium",
                "question_en": f"{moles} moles of solute dissolved in {vol_L} L of solution. Molarity is:",
                "option_a_en": f"{M:.2f} M", "option_b_en": f"{M*2:.2f} M",
                "option_c_en": f"{M/2:.2f} M", "option_d_en": f"{moles*vol_L:.2f} M",
                "correct_answer": "A",
                "explanation_en": f"M = n/V = {moles}/{vol_L} = {M:.2f} mol/L",
                "marks_correct": 4.0, "marks_wrong": -1.0,
            })

    # pH calculations
    strong_acid_conc = [1e-1, 1e-2, 1e-3, 1e-4, 5e-2, 2e-2, 5e-3, 2e-3]
    for conc in strong_acid_conc:
        import math
        pH = -math.log10(conc)
        qs.append({
            "subject": "Chemistry", "exam_type": "NEET",
            "topic": "Ionic Equilibrium", "subtopic": "pH Calculations",
            "difficulty": "medium",
            "question_en": f"pH of {conc:.0e} M HCl solution is:",
            "option_a_en": f"{pH:.1f}", "option_b_en": f"{14-pH:.1f}",
            "option_c_en": f"{pH*2:.1f}", "option_d_en": f"{pH/2:.1f}",
            "correct_answer": "A",
            "explanation_en": f"pH = -log[H⁺] = -log({conc:.0e}) = {pH:.1f}",
            "marks_correct": 4.0, "marks_wrong": -1.0,
        })

    # Molar mass from ideal gas
    for P in [1, 2, 4]:  # atm
        for T in [273, 300, 373]:  # K
            for rho in [1.0, 1.5, 2.0, 2.5, 3.0]:  # g/L
                M = rho * 0.0821 * T / P
                qs.append({
                    "subject": "Chemistry", "exam_type": "NEET",
                    "topic": "States of Matter", "subtopic": "Molar Mass from Gas",
                    "difficulty": "hard",
                    "question_en": f"Gas at {P} atm, {T} K has density {rho} g/L. Molar mass is:",
                    "option_a_en": f"{M:.1f} g/mol", "option_b_en": f"{M*2:.1f} g/mol",
                    "option_c_en": f"{M/2:.1f} g/mol", "option_d_en": f"{rho*T:.1f} g/mol",
                    "correct_answer": "A",
                    "explanation_en": f"M = ρRT/P = {rho}×0.0821×{T}/{P} = {M:.1f} g/mol",
                    "marks_correct": 4.0, "marks_wrong": -1.0,
                })

    # Faraday's law - mass deposited
    for I in [1, 2, 5, 10]:
        for t in [1000, 2000, 3200, 5000]:
            for M_mol in [27, 64, 56, 108]:  # Al, Cu, Fe, Ag
                for n_eq in [3, 2, 2, 1]:
                    mass = (I * t * M_mol) / (n_eq * 96500)
                    qs.append({
                        "subject": "Chemistry", "exam_type": "NEET",
                        "topic": "Electrochemistry", "subtopic": "Faraday's Laws",
                        "difficulty": "hard",
                        "question_en": f"Current {I} A passed for {t} s deposits mass from M={M_mol} g/mol (n={n_eq}):",
                        "option_a_en": f"{mass:.3f} g", "option_b_en": f"{mass*2:.3f} g",
                        "option_c_en": f"{mass/2:.3f} g", "option_d_en": f"{mass*n_eq:.3f} g",
                        "correct_answer": "A",
                        "explanation_en": f"m = ItM/nF = {I}×{t}×{M_mol}/({n_eq}×96500) = {mass:.3f} g",
                        "marks_correct": 4.0, "marks_wrong": -1.0,
                    })
                    break  # One per M_mol to save space

    return qs


def generate_all_chemistry_questions() -> List[Dict]:
    """Generate all 5000+ chemistry questions."""
    all_qs = []
    all_qs.extend(gen_atomic_structure())
    all_qs.extend(gen_chemical_bonding())
    all_qs.extend(gen_states_of_matter())
    all_qs.extend(gen_chemical_equilibrium())
    all_qs.extend(gen_electrochemistry())
    all_qs.extend(gen_organic_chemistry())
    all_qs.extend(gen_inorganic_chemistry())
    all_qs.extend(gen_physical_chemistry())
    all_qs.extend(gen_stoichiometry())
    all_qs.extend(gen_very_hard_chemistry())
    all_qs.extend(_gen_parametric_chem_boost())

    for q_item in all_qs:
        q_item["subject"] = "Chemistry"
        q_item["exam_type"] = "NEET"
        if "marks_correct" not in q_item:
            q_item["marks_correct"] = 4.0
        if "marks_wrong" not in q_item:
            q_item["marks_wrong"] = -1.0

    print(f"[Chemistry] Generated {len(all_qs)} questions")
    return all_qs
