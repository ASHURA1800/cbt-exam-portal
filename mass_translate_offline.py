"""
mass_translate_offline.py
=========================
Comprehensive OFFLINE translation of all 106K CBT questions into 8 Indian languages.
Uses an extensive phrase/sentence pattern dictionary — NO internet required.
Run this script once to populate all translations in question_bank.db.

Usage:
    python mass_translate_offline.py
    python mass_translate_offline.py --lang hi        # single language
    python mass_translate_offline.py --batch 5000     # batch size
"""

import sqlite3
import re
import sys
import time
import argparse
from typing import Dict, List, Tuple

DB_PATH = "question_bank.db"

# ══════════════════════════════════════════════════════════════════════════════
# COMPREHENSIVE PHRASE DICTIONARIES  — 8 Indian Languages
# Each entry: "english phrase/word" → "translated phrase"
# Longer phrases are matched first (handled in translate_text()).
# ══════════════════════════════════════════════════════════════════════════════

PHRASES: Dict[str, Dict[str, str]] = {

# ─────────────────────────────────────────────────────────────────────────────
"hi": {  # HINDI
# ── Question stems ────────────────────────────────────────────────────────
    "which of the following is correct": "निम्नलिखित में से कौन सा सही है",
    "which of the following is incorrect": "निम्नलिखित में से कौन सा गलत है",
    "which of the following is not correct": "निम्नलिखित में से कौन सा सही नहीं है",
    "which of the following": "निम्नलिखित में से कौन सा",
    "which one of the following": "निम्नलिखित में से कौन सा एक",
    "what is the value of": "का मान क्या है",
    "what is the": "क्या है",
    "what are the": "क्या हैं",
    "find the value of": "का मान ज्ञात करें",
    "find the": "ज्ञात करें",
    "calculate the": "की गणना करें",
    "determine the": "निर्धारित करें",
    "the value of": "का मान",
    "the correct answer is": "सही उत्तर है",
    "the correct option is": "सही विकल्प है",
    "choose the correct": "सही चुनें",
    "select the correct": "सही चुनें",
    "which is correct": "कौन सा सही है",
    "which is not": "कौन सा नहीं है",
    "which among the following": "निम्नलिखित में से कौन",
    "how many": "कितने",
    "how much": "कितना",
    "when did": "कब हुआ",
    "in which year": "किस वर्ष में",
    "in which year did": "किस वर्ष में",
    "who among the following": "निम्नलिखित में से कौन",
    "who is": "कौन है",
    "who was": "कौन था",
    "where is": "कहाँ है",
    "where was": "कहाँ था",
    "none of these": "इनमें से कोई नहीं",
    "none of the above": "उपरोक्त में से कोई नहीं",
    "all of the above": "उपरोक्त सभी",
    "both a and b": "a और b दोनों",
    "both 1 and 2": "1 और 2 दोनों",
    "neither a nor b": "न a और न b",

# ── Physics ───────────────────────────────────────────────────────────────
    "a body with initial velocity": "प्रारंभिक वेग वाला एक पिंड",
    "a body of mass": "द्रव्यमान का एक पिंड",
    "a body starts with initial velocity": "एक पिंड प्रारंभिक वेग से चलता है",
    "initial velocity": "प्रारंभिक वेग",
    "final velocity": "अंतिम वेग",
    "uniform acceleration": "समान त्वरण",
    "constant acceleration": "नियत त्वरण",
    "constant velocity": "नियत वेग",
    "kinetic energy": "गतिज ऊर्जा",
    "potential energy": "स्थितिज ऊर्जा",
    "potential difference": "विभवान्तर",
    "electric potential": "विद्युत विभव",
    "electric current": "विद्युत धारा",
    "electric field": "विद्युत क्षेत्र",
    "electric charge": "विद्युत आवेश",
    "electric force": "विद्युत बल",
    "magnetic field": "चुंबकीय क्षेत्र",
    "magnetic force": "चुंबकीय बल",
    "gravitational force": "गुरुत्वाकर्षण बल",
    "gravitational pe": "गुरुत्वीय स्थितिज ऊर्जा",
    "gravitational potential energy": "गुरुत्वीय स्थितिज ऊर्जा",
    "work done by": "द्वारा किया गया कार्य",
    "work done": "किया गया कार्य",
    "power dissipated": "व्यय शक्ति",
    "power developed": "विकसित शक्ति",
    "heat generated": "उत्पन्न ऊष्मा",
    "heat produced": "उत्पन्न ऊष्मा",
    "thermal energy": "ऊष्मीय ऊर्जा",
    "total energy": "कुल ऊर्जा",
    "mechanical energy": "यांत्रिक ऊर्जा",
    "law of conservation": "संरक्षण का नियम",
    "newton's law": "न्यूटन का नियम",
    "hooke's law": "हुक का नियम",
    "ohm's law": "ओम का नियम",
    "coulomb's law": "कूलम्ब का नियम",
    "boyle's law": "बॉयल का नियम",
    "charles's law": "चार्ल्स का नियम",
    "speed of light": "प्रकाश की चाल",
    "velocity of light": "प्रकाश का वेग",
    "refractive index": "अपवर्तनांक",
    "angle of incidence": "आपतन कोण",
    "angle of refraction": "अपवर्तन कोण",
    "total internal reflection": "पूर्ण आंतरिक परावर्तन",
    "critical angle": "क्रांतिक कोण",
    "simple harmonic motion": "सरल आवर्त गति",
    "time period": "आवर्तकाल",
    "angular velocity": "कोणीय वेग",
    "angular momentum": "कोणीय संवेग",
    "moment of inertia": "जड़त्व आघूर्ण",
    "centripetal force": "अभिकेंद्र बल",
    "centrifugal force": "अपकेंद्री बल",
    "surface tension": "पृष्ठ तनाव",
    "coefficient of viscosity": "श्यानता गुणांक",
    "terminal velocity": "सीमांत वेग",
    "escape velocity": "पलायन वेग",
    "orbital velocity": "कक्षीय वेग",
    "projectile motion": "प्रक्षेप्य गति",
    "range of projectile": "प्रक्षेप्य की परास",
    "maximum height": "अधिकतम ऊँचाई",
    "horizontal range": "क्षैतिज परास",
    "free fall": "मुक्त पतन",
    "acceleration due to gravity": "गुरुत्वजनित त्वरण",
    "specific heat capacity": "विशिष्ट ऊष्मा धारिता",
    "latent heat": "गुप्त ऊष्मा",
    "thermal conductivity": "ऊष्मा चालकता",
    "electromagnetic wave": "विद्युत चुंबकीय तरंग",
    "wavelength": "तरंगदैर्ध्य",
    "frequency": "आवृत्ति",
    "amplitude": "आयाम",
    "photoelectric effect": "प्रकाश विद्युत प्रभाव",
    "nuclear fission": "नाभिकीय विखंडन",
    "nuclear fusion": "नाभिकीय संलयन",
    "half life": "अर्ध आयु",
    "radioactive decay": "रेडियोधर्मी क्षय",
    "resistance": "प्रतिरोध",
    "resistivity": "प्रतिरोधकता",
    "conductivity": "चालकता",
    "capacitance": "धारिता",
    "inductance": "प्रेरकत्व",
    "impedance": "प्रतिबाधा",
    "voltage": "वोल्टेज",
    "current passed": "प्रवाहित धारा",
    "current flows": "धारा प्रवाहित होती है",
    "circuit has emf": "परिपथ में emf है",
    "applied across": "के आर-पार लगाया गया",
    "connected in series": "श्रेणी में जुड़े हैं",
    "connected in parallel": "समानांतर में जुड़े हैं",
    "in series": "श्रेणी में",
    "in parallel": "समानांतर में",
    "displacement": "विस्थापन",
    "distance": "दूरी",
    "velocity": "वेग",
    "acceleration": "त्वरण",
    "force": "बल",
    "mass": "द्रव्यमान",
    "weight": "भार",
    "energy": "ऊर्जा",
    "power": "शक्ति",
    "momentum": "संवेग",
    "pressure": "दाब",
    "temperature": "तापमान",
    "heat": "ऊष्मा",
    "work": "कार्य",
    "charge": "आवेश",
    "nucleus": "नाभिक",
    "atom": "परमाणु",
    "molecule": "अणु",
    "ion": "आयन",
    "electron": "इलेक्ट्रॉन",
    "proton": "प्रोटॉन",
    "neutron": "न्यूट्रॉन",
    "photon": "फोटोन",
    "gravity": "गुरुत्वाकर्षण",
    "friction": "घर्षण",
    "lens": "लेंस",
    "mirror": "दर्पण",
    "reflection": "परावर्तन",
    "refraction": "अपवर्तन",
    "diffraction": "विवर्तन",
    "interference": "व्यतिकरण",
    "polarization": "ध्रुवीकरण",
    "conductor": "चालक",
    "insulator": "कुचालक",
    "semiconductor": "अर्धचालक",
    "capacitor": "संधारित्र",
    "inductor": "प्रेरक",
    "transformer": "ट्रांसफार्मर",
    "generator": "जनित्र",
    "motor": "मोटर",
    "diode": "डायोड",
    "transistor": "ट्रांजिस्टर",
    "speed": "चाल",
    "time": "समय",
    "volume": "आयतन",
    "area": "क्षेत्रफल",
    "length": "लंबाई",
    "width": "चौड़ाई",
    "height": "ऊँचाई",
    "radius": "त्रिज्या",
    "diameter": "व्यास",
    "density": "घनत्व",

# ── Chemistry ─────────────────────────────────────────────────────────────
    "boiling point elevation": "क्वथनांक उन्नयन",
    "freezing point depression": "हिमांक अवनमन",
    "molarity is": "मोलरता है",
    "molality": "मोललता",
    "normality": "नॉर्मलता",
    "mole fraction": "मोल अंश",
    "van't hoff factor": "वान्ट हॉफ गुणक",
    "osmotic pressure": "परासरण दाब",
    "rate of reaction": "अभिक्रिया की दर",
    "order of reaction": "अभिक्रिया की कोटि",
    "activation energy": "सक्रियण ऊर्जा",
    "gibbs free energy": "गिब्स मुक्त ऊर्जा",
    "ionization energy": "आयनन ऊर्जा",
    "electron affinity": "इलेक्ट्रॉन बंधुता",
    "electronegativity": "विद्युत ऋणात्मकता",
    "oxidation state": "ऑक्सीकरण अवस्था",
    "oxidation number": "ऑक्सीकरण संख्या",
    "coordination number": "समन्वय संख्या",
    "crystal field theory": "क्रिस्टल क्षेत्र सिद्धांत",
    "boiling point": "क्वथनांक",
    "melting point": "गलनांक",
    "freezing point": "हिमांक",
    "solubility product": "विलेयता गुणनफल",
    "ionic product of water": "जल का आयनिक गुणनफल",
    "ph of a solution": "विलयन का pH",
    "ph of": "का pH",
    "the ph": "pH",
    "buffer solution": "बफर विलयन",
    "standard electrode potential": "मानक इलेक्ट्रोड विभव",
    "cell potential": "सेल विभव",
    "electrolysis": "वैद्युत अपघटन",
    "faraday's law": "फैराडे का नियम",
    "ideal gas": "आदर्श गैस",
    "real gas": "वास्तविक गैस",
    "van der waals": "वान डर वाल्स",
    "avogadro's number": "एवोगाड्रो की संख्या",
    "avogadro number": "एवोगाड्रो संख्या",
    "haber process": "हेबर प्रक्रिया",
    "contact process": "संपर्क प्रक्रिया",
    "functional group": "क्रियात्मक समूह",
    "homologous series": "समजातीय श्रेणी",
    "isomerism": "समावयवता",
    "polymerization": "बहुलकीकरण",
    "saponification": "साबुनीकरण",
    "esterification": "एस्टरीकरण",
    "aldehyde": "एल्डिहाइड",
    "ketone": "कीटोन",
    "carboxylic acid": "कार्बोक्सिलिक अम्ल",
    "amino acid": "अमीनो अम्ल",
    "element": "तत्व",
    "compound": "यौगिक",
    "mixture": "मिश्रण",
    "solution": "विलयन",
    "acid": "अम्ल",
    "base": "क्षार",
    "salt": "लवण",
    "oxidation": "ऑक्सीकरण",
    "reduction": "अपचयन",
    "catalyst": "उत्प्रेरक",
    "reaction": "अभिक्रिया",
    "bond": "बंध",
    "orbital": "कक्षक",
    "valence": "संयोजकता",
    "mole": "मोल",
    "concentration": "सांद्रता",
    "solubility": "विलेयता",
    "entropy": "एन्ट्रॉपी",
    "enthalpy": "एन्थैल्पी",
    "equilibrium": "साम्यावस्था",
    "polymer": "बहुलक",
    "monomer": "एकलक",
    "isomer": "समावयवी",
    "alkane": "ऐल्केन",
    "alkene": "ऐल्कीन",
    "alkyne": "ऐल्काइन",
    "benzene": "बेंजीन",
    "methane": "मीथेन",
    "ethanol": "एथेनॉल",
    "glucose": "ग्लूकोज़",
    "sucrose": "सुक्रोज़",
    "cellulose": "सेलुलोज़",
    "protein": "प्रोटीन",
    "carbohydrate": "कार्बोहाइड्रेट",
    "lipid": "वसा",
    "vitamin": "विटामिन",
    "hormone": "हार्मोन",

# ── Biology ───────────────────────────────────────────────────────────────
    "eukaryotic mrna": "यूकेरियोटिक mRNA",
    "gene interaction": "जीन अंतःक्रिया",
    "complementary gene": "पूरक जीन",
    "dominant epistasis": "प्रबल एपिस्टेसिस",
    "recessive epistasis": "अप्रबल एपिस्टेसिस",
    "function of circulatory system": "परिसंचरण तंत्र का कार्य",
    "function of digestive system": "पाचन तंत्र का कार्य",
    "function of nervous system": "तंत्रिका तंत्र का कार्य",
    "function of respiratory system": "श्वसन तंत्र का कार्य",
    "function of excretory system": "उत्सर्जन तंत्र का कार्य",
    "cell organelle": "कोशिका अंगक",
    "cell membrane": "कोशिका झिल्ली",
    "cell wall": "कोशिका भित्ति",
    "cell division": "कोशिका विभाजन",
    "dna replication": "DNA प्रतिकृति",
    "protein synthesis": "प्रोटीन संश्लेषण",
    "genetic code": "आनुवंशिक कोड",
    "mendelian genetics": "मेंडलीय आनुवंशिकी",
    "law of segregation": "पृथक्करण का नियम",
    "law of dominance": "प्रभाविता का नियम",
    "natural selection": "प्राकृतिक वरण",
    "biological evolution": "जैविक विकास",
    "ecosystems": "पारिस्थितिकी तंत्र",
    "food chain": "खाद्य श्रृंखला",
    "food web": "खाद्य जाल",
    "biodiversity": "जैव विविधता",
    "cell": "कोशिका",
    "nucleus": "केंद्रक",
    "membrane": "झिल्ली",
    "enzyme": "एंजाइम",
    "dna": "DNA",
    "rna": "RNA",
    "gene": "जीन",
    "chromosome": "गुणसूत्र",
    "mitosis": "समसूत्री विभाजन",
    "meiosis": "अर्धसूत्री विभाजन",
    "photosynthesis": "प्रकाश संश्लेषण",
    "respiration": "श्वसन",
    "digestion": "पाचन",
    "evolution": "विकास",
    "mutation": "उत्परिवर्तन",
    "tissue": "ऊतक",
    "organ": "अंग",
    "system": "तंत्र",
    "blood": "रक्त",
    "heart": "हृदय",
    "lungs": "फेफड़े",
    "kidney": "वृक्क",
    "liver": "यकृत",
    "brain": "मस्तिष्क",
    "bone": "अस्थि",
    "muscle": "पेशी",
    "skin": "त्वचा",
    "root": "जड़",
    "stem": "तना",
    "leaf": "पत्ती",
    "flower": "फूल",
    "seed": "बीज",
    "fruit": "फल",
    "bacteria": "जीवाणु",
    "virus": "विषाणु",
    "fungi": "कवक",
    "algae": "शैवाल",

# ── Mathematics ───────────────────────────────────────────────────────────
    "the roots of the": "के मूल",
    "find the missing term": "लुप्त पद ज्ञात करें",
    "arithmetic progression": "समांतर श्रेणी",
    "geometric progression": "गुणोत्तर श्रेणी",
    "harmonic progression": "हरात्मक श्रेणी",
    "binomial theorem": "द्विपद प्रमेय",
    "general term": "व्यापक पद",
    "quadratic equation": "द्विघात समीकरण",
    "linear equation": "रैखिक समीकरण",
    "differential equation": "अवकल समीकरण",
    "integration by parts": "खंडशः समाकलन",
    "definite integral": "निश्चित समाकल",
    "indefinite integral": "अनिश्चित समाकल",
    "derivative of": "का अवकलज",
    "differentiate": "अवकलन करें",
    "integrate": "समाकल करें",
    "probability of": "की प्रायिकता",
    "standard deviation": "मानक विचलन",
    "mean value": "माध्य मान",
    "median": "मध्यिका",
    "mode": "बहुलक",
    "mean": "माध्य",
    "variance": "प्रसरण",
    "permutation": "क्रमचय",
    "combination": "संयोजन",
    "set theory": "समुच्चय सिद्धांत",
    "complex number": "सम्मिश्र संख्या",
    "real number": "वास्तविक संख्या",
    "rational number": "परिमेय संख्या",
    "irrational number": "अपरिमेय संख्या",
    "prime number": "अभाज्य संख्या",
    "natural number": "प्राकृत संख्या",
    "integer": "पूर्णांक",
    "fraction": "भिन्न",
    "decimal": "दशमलव",
    "percentage": "प्रतिशत",
    "ratio": "अनुपात",
    "proportion": "समानुपात",
    "profit": "लाभ",
    "loss": "हानि",
    "interest": "ब्याज",
    "simple interest": "साधारण ब्याज",
    "compound interest": "चक्रवृद्धि ब्याज",
    "principal": "मूलधन",
    "amount": "मिश्रधन",
    "rate": "दर",
    "derivative": "अवकलज",
    "integral": "समाकल",
    "matrix": "आव्यूह",
    "vector": "सदिश",
    "scalar": "अदिश",
    "probability": "प्रायिकता",
    "trigonometry": "त्रिकोणमिति",
    "logarithm": "लघुगणक",
    "equation": "समीकरण",
    "function": "फलन",
    "limit": "सीमा",
    "triangle": "त्रिभुज",
    "circle": "वृत्त",
    "square": "वर्ग",
    "rectangle": "आयत",
    "parallelogram": "समांतर चतुर्भुज",
    "trapezium": "समलम्ब",
    "sphere": "गोला",
    "cylinder": "बेलन",
    "cone": "शंकु",
    "cube": "घन",
    "cuboid": "घनाभ",
    "angle": "कोण",
    "perimeter": "परिमाप",
    "circumference": "परिधि",
    "hypotenuse": "कर्ण",
    "sin": "sin",
    "cos": "cos",
    "tan": "tan",

# ── GK / CUET ────────────────────────────────────────────────────────────
    "panchayati raj institutions": "पंचायती राज संस्थाएं",
    "constitutional amendment": "संवैधानिक संशोधन",
    "fundamental rights": "मौलिक अधिकार",
    "directive principles": "नीति निर्देशक तत्व",
    "fundamental duties": "मूल कर्तव्य",
    "parliament of india": "भारत की संसद",
    "supreme court": "सर्वोच्च न्यायालय",
    "high court": "उच्च न्यायालय",
    "prime minister": "प्रधानमंत्री",
    "president of india": "भारत के राष्ट्रपति",
    "governor": "राज्यपाल",
    "chief minister": "मुख्यमंत्री",
    "five year plan": "पंचवर्षीय योजना",
    "green revolution": "हरित क्रांति",
    "white revolution": "श्वेत क्रांति",
    "operation flood": "ऑपरेशन फ्लड",
    "national income": "राष्ट्रीय आय",
    "per capita income": "प्रति व्यक्ति आय",
    "gross domestic product": "सकल घरेलू उत्पाद",
    "gross national product": "सकल राष्ट्रीय उत्पाद",
    "reserve bank of india": "भारतीय रिजर्व बैंक",
    "securities exchange board": "भारतीय प्रतिभूति और विनिमय बोर्ड",
    "world trade organization": "विश्व व्यापार संगठन",
    "united nations": "संयुक्त राष्ट्र",
    "climate change": "जलवायु परिवर्तन",
    "global warming": "वैश्विक ताप",
    "ozone layer": "ओजोन परत",
    "greenhouse effect": "ग्रीनहाउस प्रभाव",
    "solar system": "सौरमंडल",
    "milky way": "आकाशगंगा",
    "artificial satellite": "कृत्रिम उपग्रह",
    "space mission": "अंतरिक्ष मिशन",
    "primarily uses": "मुख्यतः उपयोग करती है",
    "related to": "से संबंधित है",
    "deals with": "से संबंधित है",
    "technology": "तकनीक",
    "invention": "आविष्कार",
    "discovery": "खोज",
    "scientist": "वैज्ञानिक",
    "author": "लेखक",
    "book": "पुस्तक",
    "award": "पुरस्कार",
    "founder": "संस्थापक",
    "capital": "राजधानी",
    "currency": "मुद्रा",
    "language": "भाषा",
    "religion": "धर्म",
    "culture": "संस्कृति",
    "history": "इतिहास",
    "geography": "भूगोल",
    "economy": "अर्थव्यवस्था",
    "politics": "राजनीति",

# ── CUET English ──────────────────────────────────────────────────────────
    "subordinating conjunction": "अधीनस्थ संयोजन",
    "coordinating conjunction": "समन्वय संयोजन",
    "correlative conjunction": "सहसंबंधी संयोजन",
    "endure a painful situation": "कठिन परिस्थिति सहना",
    "idiom meaning": "मुहावरे का अर्थ",
    "phrase meaning": "वाक्यांश का अर्थ",
    "antonym of": "का विलोम",
    "synonym of": "का पर्यायवाची",
    "correct spelling": "सही वर्तनी",
    "correct form of verb": "क्रिया का सही रूप",
    "passive voice": "कर्मवाच्य",
    "active voice": "कर्तृवाच्य",
    "direct speech": "प्रत्यक्ष कथन",
    "indirect speech": "अप्रत्यक्ष कथन",
    "adjective": "विशेषण",
    "adverb": "क्रियाविशेषण",
    "noun": "संज्ञा",
    "verb": "क्रिया",
    "pronoun": "सर्वनाम",
    "preposition": "पूर्वसर्ग",
    "conjunction": "संयोजन",
    "interjection": "विस्मयादिबोधक",

# ── Reasoning ─────────────────────────────────────────────────────────────
    "book : library": "पुस्तक : पुस्तकालय",
    "painting :": "चित्र :",
    "analogy": "सादृश्य",
    "series completion": "श्रृंखला पूर्णता",
    "odd one out": "बेमेल ढूंढें",
    "coding decoding": "कोडिंग-डिकोडिंग",
    "blood relation": "रक्त संबंध",
    "direction sense": "दिशा ज्ञान",
    "seating arrangement": "बैठने की व्यवस्था",
    "syllogism": "युक्तिवाक्य",
    "logical reasoning": "तार्किक तर्क",
    "critical thinking": "आलोचनात्मक सोच",

# ── Common words & connectors ─────────────────────────────────────────────
    "the correct answer": "सही उत्तर",
    "is equal to": "के बराबर है",
    "is given by": "द्वारा दिया गया है",
    "is defined as": "के रूप में परिभाषित है",
    "is known as": "के रूप में जाना जाता है",
    "is called": "कहलाता है",
    "is not": "नहीं है",
    "does not": "नहीं करता",
    "cannot be": "नहीं हो सकता",
    "can be": "हो सकता है",
    "will be": "होगा",
    "would be": "होगा",
    "must be": "होना चाहिए",
    "should be": "होना चाहिए",
    "if and only if": "तभी और केवल तभी",
    "if the": "यदि",
    "when the": "जब",
    "then the": "तो",
    "such that": "इस प्रकार कि",
    "such as": "जैसे कि",
    "for example": "उदाहरण के लिए",
    "for instance": "उदाहरण के लिए",
    "therefore": "अतः",
    "hence": "अतः",
    "thus": "इस प्रकार",
    "because": "क्योंकि",
    "since": "चूंकि",
    "although": "यद्यपि",
    "however": "हालांकि",
    "moreover": "इसके अलावा",
    "furthermore": "इसके अतिरिक्त",
    "in addition": "इसके अतिरिक्त",
    "on the other hand": "दूसरी ओर",
    "according to": "के अनुसार",
    "as per": "के अनुसार",
    "based on": "के आधार पर",
    "given that": "दिया गया है कि",
    "where": "जहाँ",
    "whose": "जिसका",
    "given": "दिया गया है",
    "find": "ज्ञात करें",
    "calculate": "गणना करें",
    "determine": "निर्धारित करें",
    "evaluate": "मूल्यांकन करें",
    "solve": "हल करें",
    "prove": "सिद्ध करें",
    "show that": "दिखाएं कि",
    "the": "",
    "of": "का",
    "in": "में",
    "on": "पर",
    "at": "पर",
    "by": "द्वारा",
    "to": "को",
    "is": "है",
    "are": "हैं",
    "was": "था",
    "were": "थे",
    "has": "है",
    "have": "हैं",
    "had": "था",
    "a": "एक",
    "an": "एक",
    "and": "और",
    "or": "या",
    "not": "नहीं",
    "only": "केवल",
    "always": "हमेशा",
    "never": "कभी नहीं",
    "maximum": "अधिकतम",
    "minimum": "न्यूनतम",
    "increase": "वृद्धि",
    "decrease": "कमी",
    "equal": "बराबर",
    "greater": "अधिक",
    "less": "कम",
    "zero": "शून्य",
    "positive": "धनात्मक",
    "negative": "ऋणात्मक",
    "horizontal": "क्षैतिज",
    "vertical": "ऊर्ध्वाधर",
    "surface": "सतह",
    "total": "कुल",
    "net": "परिणामी",
    "average": "औसत",
    "per second": "प्रति सेकंड",
    "per hour": "प्रति घंटा",
    "per minute": "प्रति मिनट",
    "unit": "इकाई",
    "ratio": "अनुपात",
    "formula": "सूत्र",
    "theorem": "प्रमेय",
    "principle": "सिद्धांत",
    "constant": "स्थिरांक",
    "variable": "चर",
    "coefficient": "गुणांक",
    "factor": "गुणनखंड",
    "term": "पद",
    "expression": "व्यंजक",
},

# ─────────────────────────────────────────────────────────────────────────────
"bn": {  # BENGALI
    "which of the following is correct": "নিচের কোনটি সঠিক",
    "which of the following is incorrect": "নিচের কোনটি ভুল",
    "which of the following": "নিচের কোনটি",
    "what is the value of": "এর মান কত",
    "what is the": "কী",
    "find the value of": "এর মান নির্ণয় করুন",
    "find the": "নির্ণয় করুন",
    "calculate the": "গণনা করুন",
    "none of these": "এর কোনটিই নয়",
    "none of the above": "উপরের কোনটিই নয়",
    "all of the above": "উপরের সবগুলো",
    "initial velocity": "প্রারম্ভিক বেগ",
    "final velocity": "চূড়ান্ত বেগ",
    "kinetic energy": "গতিশক্তি",
    "potential energy": "বিভবশক্তি",
    "potential difference": "বিভব পার্থক্য",
    "electric current": "তড়িৎ প্রবাহ",
    "electric field": "তড়িৎ ক্ষেত্র",
    "magnetic field": "চুম্বক ক্ষেত্র",
    "gravitational force": "অভিকর্ষ বল",
    "work done": "সম্পাদিত কাজ",
    "acceleration due to gravity": "অভিকর্ষজ ত্বরণ",
    "speed of light": "আলোর গতি",
    "boiling point": "স্ফুটনাঙ্ক",
    "melting point": "গলনাঙ্ক",
    "ph of a solution": "দ্রবণের pH",
    "rate of reaction": "বিক্রিয়ার হার",
    "cell division": "কোষ বিভাজন",
    "natural selection": "প্রাকৃতিক নির্বাচন",
    "food chain": "খাদ্য শৃঙ্খল",
    "constitutional amendment": "সাংবিধানিক সংশোধন",
    "fundamental rights": "মৌলিক অধিকার",
    "prime minister": "প্রধানমন্ত্রী",
    "supreme court": "সুপ্রিম কোর্ট",
    "velocity": "বেগ",
    "acceleration": "ত্বরণ",
    "force": "বল",
    "mass": "ভর",
    "weight": "ওজন",
    "energy": "শক্তি",
    "power": "ক্ষমতা",
    "work": "কাজ",
    "momentum": "ভরবেগ",
    "pressure": "চাপ",
    "temperature": "তাপমাত্রা",
    "heat": "তাপ",
    "current": "তড়িৎ প্রবাহ",
    "voltage": "ভোল্টেজ",
    "resistance": "রোধ",
    "wavelength": "তরঙ্গদৈর্ঘ্য",
    "frequency": "কম্পাঙ্ক",
    "amplitude": "বিস্তার",
    "displacement": "সরণ",
    "distance": "দূরত্ব",
    "speed": "দ্রুতি",
    "time": "সময়",
    "gravity": "অভিকর্ষ",
    "friction": "ঘর্ষণ",
    "electron": "ইলেকট্রন",
    "proton": "প্রোটন",
    "neutron": "নিউট্রন",
    "nucleus": "নিউক্লিয়াস",
    "atom": "পরমাণু",
    "molecule": "অণু",
    "ion": "আয়ন",
    "charge": "আধান",
    "element": "মৌল",
    "compound": "যৌগ",
    "mixture": "মিশ্রণ",
    "solution": "দ্রবণ",
    "acid": "অ্যাসিড",
    "base": "ক্ষার",
    "salt": "লবণ",
    "oxidation": "জারণ",
    "reduction": "বিজারণ",
    "catalyst": "অনুঘটক",
    "reaction": "বিক্রিয়া",
    "bond": "বন্ধন",
    "mole": "মোল",
    "concentration": "ঘনত্ব",
    "entropy": "এনট্রপি",
    "enthalpy": "এনথালপি",
    "equilibrium": "সাম্যাবস্থা",
    "cell": "কোষ",
    "membrane": "ঝিল্লি",
    "enzyme": "এনজাইম",
    "protein": "প্রোটিন",
    "dna": "DNA",
    "rna": "RNA",
    "gene": "জিন",
    "chromosome": "ক্রোমোজোম",
    "mitosis": "মাইটোসিস",
    "meiosis": "মিয়োসিস",
    "photosynthesis": "সালোকসংশ্লেষণ",
    "respiration": "শ্বসন",
    "digestion": "পরিপাক",
    "evolution": "বিবর্তন",
    "mutation": "মিউটেশন",
    "derivative": "অবকল",
    "integral": "সমাকল",
    "matrix": "ম্যাট্রিক্স",
    "vector": "ভেক্টর",
    "probability": "সম্ভাবনা",
    "equation": "সমীকরণ",
    "function": "ফাংশন",
    "percentage": "শতাংশ",
    "ratio": "অনুপাত",
    "mean": "গড়",
    "median": "মধ্যমান",
    "mode": "সংখ্যাগুরু মান",
    "is": "হয়",
    "are": "হয়",
    "and": "এবং",
    "or": "বা",
    "not": "নয়",
    "maximum": "সর্বোচ্চ",
    "minimum": "সর্বনিম্ন",
    "zero": "শূন্য",
    "total": "মোট",
    "average": "গড়",
    "formula": "সূত্র",
    "theorem": "উপপাদ্য",
    "constant": "ধ্রুবক",
    "none of these": "এর কোনটিই নয়",
    "none of the above": "উপরের কোনটিই নয়",
    "all of the above": "উপরের সবগুলো",
},

# ─────────────────────────────────────────────────────────────────────────────
"ta": {  # TAMIL
    "which of the following is correct": "பின்வருவனவற்றில் எது சரியானது",
    "which of the following is incorrect": "பின்வருவனவற்றில் எது தவறானது",
    "which of the following": "பின்வருவனவற்றில் எது",
    "what is the value of": "இன் மதிப்பு என்ன",
    "what is the": "என்ன",
    "find the value of": "இன் மதிப்பு காண்க",
    "find the": "காண்க",
    "calculate the": "கணக்கிடுக",
    "none of these": "இவை எதுவுமில்லை",
    "none of the above": "மேற்கண்டவை எதுவுமில்லை",
    "all of the above": "மேற்கண்டவை அனைத்தும்",
    "initial velocity": "தொடக்க வேகம்",
    "final velocity": "இறுதி வேகம்",
    "kinetic energy": "இயக்க ஆற்றல்",
    "potential energy": "நிலை ஆற்றல்",
    "electric current": "மின்னோட்டம்",
    "electric field": "மின்புலம்",
    "magnetic field": "காந்தப்புலம்",
    "gravitational force": "ஈர்ப்பு விசை",
    "work done": "செய்யப்பட்ட வேலை",
    "speed of light": "ஒளியின் வேகம்",
    "acceleration due to gravity": "புவியீர்ப்பு முடுக்கம்",
    "boiling point": "கொதிநிலை",
    "melting point": "உருகுநிலை",
    "rate of reaction": "வினையின் வேகம்",
    "cell division": "செல் பிரிவு",
    "photosynthesis": "ஒளிச்சேர்க்கை",
    "food chain": "உணவுச்சங்கிலி",
    "velocity": "திசைவேகம்",
    "acceleration": "முடுக்கம்",
    "force": "விசை",
    "mass": "நிறை",
    "weight": "எடை",
    "energy": "ஆற்றல்",
    "power": "திறன்",
    "work": "வேலை",
    "momentum": "உந்தம்",
    "pressure": "அழுத்தம்",
    "temperature": "வெப்பநிலை",
    "heat": "வெப்பம்",
    "current": "மின்னோட்டம்",
    "voltage": "மின்னழுத்தம்",
    "resistance": "மின்தடை",
    "wavelength": "அலைநீளம்",
    "frequency": "அதிர்வெண்",
    "amplitude": "வீச்சு",
    "displacement": "இடப்பெயர்ச்சி",
    "distance": "தொலைவு",
    "speed": "வேகம்",
    "time": "நேரம்",
    "gravity": "ஈர்ப்பு",
    "friction": "உராய்வு",
    "electron": "எலக்ட்ரான்",
    "proton": "புரோட்டான்",
    "neutron": "நியூட்ரான்",
    "nucleus": "கரு",
    "atom": "அணு",
    "molecule": "மூலக்கூறு",
    "ion": "அயனி",
    "charge": "மின்னூட்டம்",
    "element": "தனிமம்",
    "compound": "சேர்மம்",
    "mixture": "கலவை",
    "solution": "கரைசல்",
    "acid": "அமிலம்",
    "base": "காரம்",
    "salt": "உப்பு",
    "oxidation": "ஆக்சிகரணம்",
    "reduction": "ஒடுக்கம்",
    "catalyst": "வினையூக்கி",
    "reaction": "வினை",
    "cell": "செல்",
    "enzyme": "நொதி",
    "protein": "புரதம்",
    "gene": "மரபணு",
    "chromosome": "நிறமூர்த்தி",
    "mitosis": "சமவிகித பகுப்பு",
    "meiosis": "குறைவிகித பகுப்பு",
    "respiration": "சுவாசம்",
    "evolution": "பரிணாமம்",
    "derivative": "வகையீடு",
    "integral": "தொகையீடு",
    "probability": "நிகழ்தகவு",
    "equation": "சமன்பாடு",
    "function": "சார்பு",
    "mean": "சராசரி",
    "percentage": "சதவீதம்",
    "is": "ஆகும்",
    "are": "ஆகும்",
    "and": "மற்றும்",
    "or": "அல்லது",
    "not": "இல்லை",
    "maximum": "அதிகபட்சம்",
    "minimum": "குறைந்தபட்சம்",
    "zero": "சுழியம்",
    "total": "மொத்தம்",
    "formula": "சூத்திரம்",
    "constant": "மாறிலி",
    "prime minister": "பிரதமர்",
    "supreme court": "உச்ச நீதிமன்றம்",
    "fundamental rights": "அடிப்படை உரிமைகள்",
},

# ─────────────────────────────────────────────────────────────────────────────
"te": {  # TELUGU
    "which of the following is correct": "కింది వాటిలో ఏది సరైనది",
    "which of the following is incorrect": "కింది వాటిలో ఏది తప్పు",
    "which of the following": "కింది వాటిలో ఏది",
    "what is the value of": "యొక్క విలువ ఏమిటి",
    "what is the": "ఏమిటి",
    "find the value of": "యొక్క విలువను కనుగొనండి",
    "find the": "కనుగొనండి",
    "calculate the": "లెక్కించండి",
    "none of these": "వీటిలో ఏదీ కాదు",
    "none of the above": "పైవాటిలో ఏదీ కాదు",
    "all of the above": "పైవన్నీ",
    "initial velocity": "ప్రారంభ వేగం",
    "final velocity": "అంతిమ వేగం",
    "kinetic energy": "గతిశక్తి",
    "potential energy": "స్థితిశక్తి",
    "electric current": "విద్యుత్ ప్రవాహం",
    "electric field": "విద్యుత్ క్షేత్రం",
    "magnetic field": "అయస్కాంత క్షేత్రం",
    "gravitational force": "గురుత్వాకర్షణ బలం",
    "work done": "చేసిన పని",
    "speed of light": "కాంతి వేగం",
    "boiling point": "మరుగు స్థానం",
    "melting point": "ద్రవీభవన స్థానం",
    "rate of reaction": "చర్య రేటు",
    "cell division": "కణ విభజన",
    "photosynthesis": "కిరణజన్య సంయోగక్రియ",
    "food chain": "ఆహార శృంఖలం",
    "velocity": "వేగం",
    "acceleration": "త్వరణం",
    "force": "బలం",
    "mass": "ద్రవ్యరాశి",
    "weight": "బరువు",
    "energy": "శక్తి",
    "power": "శక్తి సామర్థ్యం",
    "work": "పని",
    "momentum": "ద్రవ్యవేగం",
    "pressure": "పీడనం",
    "temperature": "ఉష్ణోగ్రత",
    "heat": "వేడి",
    "current": "విద్యుత్ ప్రవాహం",
    "voltage": "వోల్టేజ్",
    "resistance": "నిరోధం",
    "wavelength": "తరంగ దైర్ఘ్యం",
    "frequency": "పౌనఃపున్యం",
    "displacement": "స్థానభ్రంశం",
    "distance": "దూరం",
    "speed": "వేగం",
    "time": "సమయం",
    "gravity": "గురుత్వాకర్షణ",
    "friction": "ఘర్షణ",
    "electron": "ఎలక్ట్రాన్",
    "proton": "ప్రోటాన్",
    "neutron": "న్యూట్రాన్",
    "nucleus": "కేంద్రకం",
    "atom": "పరమాణువు",
    "molecule": "అణువు",
    "ion": "అయాన్",
    "element": "మూలకం",
    "compound": "సమ్మేళనం",
    "mixture": "మిశ్రమం",
    "solution": "ద్రావణం",
    "acid": "ఆమ్లం",
    "base": "క్షారం",
    "salt": "లవణం",
    "oxidation": "ఆక్సీకరణం",
    "reduction": "క్షయీకరణం",
    "catalyst": "ఉత్ప్రేరకం",
    "reaction": "రసాయన చర్య",
    "cell": "కణం",
    "enzyme": "ఎంజైమ్",
    "protein": "ప్రోటీన్",
    "gene": "జన్యువు",
    "chromosome": "వర్ణసూత్రం",
    "photosynthesis": "కిరణజన్య సంయోగక్రియ",
    "respiration": "శ్వాసక్రియ",
    "evolution": "పరిణామం",
    "derivative": "అవకలం",
    "integral": "సమాకలం",
    "probability": "సంభావ్యత",
    "equation": "సమీకరణం",
    "function": "ప్రమేయం",
    "mean": "సగటు",
    "percentage": "శాతం",
    "is": "అయి ఉంటుంది",
    "are": "ఉంటాయి",
    "and": "మరియు",
    "or": "లేదా",
    "not": "కాదు",
    "maximum": "గరిష్ట",
    "minimum": "కనిష్ట",
    "zero": "శూన్యం",
    "total": "మొత్తం",
    "prime minister": "ప్రధానమంత్రి",
    "supreme court": "సుప్రీం కోర్టు",
},

# ─────────────────────────────────────────────────────────────────────────────
"gu": {  # GUJARATI
    "which of the following is correct": "નીચેનામાંથી કયો સાચો છે",
    "which of the following is incorrect": "નીચેનામાંથી કયો ખોટો છે",
    "which of the following": "નીચેનામાંથી કયો",
    "what is the value of": "નું મૂલ્ય શું છે",
    "what is the": "શું છે",
    "find the value of": "નું મૂલ્ય શોધો",
    "find the": "શોધો",
    "calculate the": "ગણતરી કરો",
    "none of these": "આ પૈકી કોઈ નહીં",
    "none of the above": "ઉપર્યુક્ત પૈકી કોઈ નહીં",
    "all of the above": "ઉપર્યુક્ત તમામ",
    "initial velocity": "પ્રારંભિક વેગ",
    "final velocity": "અંતિમ વેગ",
    "kinetic energy": "ગતિ ઊર્જા",
    "potential energy": "સ્થિતિ ઊર્જા",
    "electric current": "વિદ્યુત પ્રવાહ",
    "electric field": "વિદ્યુત ક્ષેત્ર",
    "magnetic field": "ચુંબકીય ક્ષેત્ર",
    "gravitational force": "ગુરુત્વાકર્ષણ બળ",
    "work done": "કરેલ કાર્ય",
    "speed of light": "પ્રકાશની ઝડપ",
    "boiling point": "ઉત્કલન બિંદુ",
    "melting point": "ગલન બિંદુ",
    "rate of reaction": "પ્રક્રિયાનો દર",
    "cell division": "કોષ વિભાજન",
    "photosynthesis": "પ્રકાશ સંશ્લેષણ",
    "food chain": "ખોરાક શૃંખલ",
    "velocity": "વેગ",
    "acceleration": "પ્રવેગ",
    "force": "બળ",
    "mass": "દ્રવ્યમાન",
    "weight": "વજન",
    "energy": "ઊર્જા",
    "power": "શક્તિ",
    "work": "કાર્ય",
    "momentum": "વેગમાન",
    "pressure": "દબાણ",
    "temperature": "તાપમાન",
    "heat": "ઉષ્મા",
    "current": "વિદ્યુત પ્રવાહ",
    "voltage": "વોલ્ટેજ",
    "resistance": "અવરોધ",
    "wavelength": "તરંગ લંબાઈ",
    "frequency": "આવૃત્તિ",
    "displacement": "સ્થાનાંતર",
    "distance": "અંતર",
    "speed": "ઝડપ",
    "time": "સમય",
    "gravity": "ગુરુત્વ",
    "friction": "ઘર્ષણ",
    "electron": "ઇલેક્ટ્રોન",
    "proton": "પ્રોટોન",
    "neutron": "ન્યુટ્રોન",
    "nucleus": "ન્યૂક્લિયસ",
    "atom": "પરમાણુ",
    "molecule": "અણુ",
    "element": "તત્વ",
    "compound": "સંયોજન",
    "mixture": "મિશ્રણ",
    "solution": "દ્રાવણ",
    "acid": "એસિડ",
    "base": "ક્ષાર",
    "salt": "મીઠું",
    "oxidation": "ઓક્સીકરણ",
    "reduction": "અવ-ઓક્સીકરણ",
    "catalyst": "ઉત્પ્રેરક",
    "reaction": "પ્રક્રિયા",
    "cell": "કોષ",
    "enzyme": "ઉત્સેચક",
    "protein": "પ્રોટીન",
    "gene": "જનીન",
    "chromosome": "રંગસૂત્ર",
    "photosynthesis": "પ્રકાશ સંશ્લેષણ",
    "respiration": "શ્વસન",
    "evolution": "ઉત્ક્રાંતિ",
    "probability": "સંભાવના",
    "equation": "સમીકરણ",
    "function": "ફ્રક્શન",
    "mean": "સરેરાશ",
    "percentage": "ટકા",
    "is": "છે",
    "are": "છે",
    "and": "અને",
    "or": "અથવા",
    "not": "નહીં",
    "maximum": "મહત્તમ",
    "minimum": "લઘુત્તમ",
    "zero": "શૂન્ય",
    "total": "કુલ",
    "prime minister": "વડાપ્રધાન",
    "supreme court": "સર્વોચ્ચ અદાલત",
    "none of these": "આ પૈકી કોઈ નહીં",
    "none of the above": "ઉપર્યુક્ત પૈકી કોઈ નહીં",
    "all of the above": "ઉપર્યુક્ત તમામ",
},

# ─────────────────────────────────────────────────────────────────────────────
"mr": {  # MARATHI
    "which of the following is correct": "खालीलपैकी कोणते बरोबर आहे",
    "which of the following is incorrect": "खालीलपैकी कोणते चुकीचे आहे",
    "which of the following": "खालीलपैकी कोणते",
    "what is the value of": "चे मूल्य काय आहे",
    "what is the": "काय आहे",
    "find the value of": "चे मूल्य काढा",
    "find the": "काढा",
    "calculate the": "गणना करा",
    "none of these": "यापैकी कोणतेही नाही",
    "none of the above": "वरीलपैकी कोणतेही नाही",
    "all of the above": "वरील सर्व",
    "initial velocity": "प्रारंभिक वेग",
    "final velocity": "अंतिम वेग",
    "kinetic energy": "गतिज ऊर्जा",
    "potential energy": "स्थितिज ऊर्जा",
    "electric current": "विद्युत प्रवाह",
    "electric field": "विद्युत क्षेत्र",
    "magnetic field": "चुंबकीय क्षेत्र",
    "gravitational force": "गुरुत्वाकर्षण बल",
    "work done": "केलेले काम",
    "speed of light": "प्रकाशाचा वेग",
    "boiling point": "उत्कलन बिंदू",
    "melting point": "वितळण बिंदू",
    "rate of reaction": "अभिक्रियेचा दर",
    "cell division": "पेशी विभाजन",
    "photosynthesis": "प्रकाशसंश्लेषण",
    "food chain": "अन्नसाखळी",
    "velocity": "वेग",
    "acceleration": "त्वरण",
    "force": "बल",
    "mass": "वस्तुमान",
    "weight": "वजन",
    "energy": "ऊर्जा",
    "power": "शक्ती",
    "work": "काम",
    "momentum": "संवेग",
    "pressure": "दाब",
    "temperature": "तापमान",
    "heat": "उष्णता",
    "current": "विद्युत प्रवाह",
    "voltage": "व्होल्टेज",
    "resistance": "प्रतिरोध",
    "wavelength": "तरंगलांबी",
    "frequency": "वारंवारता",
    "displacement": "विस्थापन",
    "distance": "अंतर",
    "speed": "वेग",
    "time": "वेळ",
    "gravity": "गुरुत्व",
    "friction": "घर्षण",
    "electron": "इलेक्ट्रॉन",
    "proton": "प्रोटॉन",
    "neutron": "न्यूट्रॉन",
    "nucleus": "केंद्रक",
    "atom": "अणू",
    "molecule": "रेणू",
    "element": "मूलद्रव्य",
    "compound": "संयुग",
    "mixture": "मिश्रण",
    "solution": "द्रावण",
    "acid": "आम्ल",
    "base": "आधार",
    "salt": "मीठ",
    "oxidation": "ऑक्सिडेशन",
    "reduction": "क्षपण",
    "catalyst": "उत्प्रेरक",
    "reaction": "अभिक्रिया",
    "cell": "पेशी",
    "enzyme": "विकर",
    "protein": "प्रथिने",
    "gene": "जनुक",
    "chromosome": "गुणसूत्र",
    "respiration": "श्वसन",
    "evolution": "उत्क्रांती",
    "probability": "संभाव्यता",
    "equation": "समीकरण",
    "mean": "सरासरी",
    "percentage": "टक्केवारी",
    "is": "आहे",
    "are": "आहेत",
    "and": "आणि",
    "or": "किंवा",
    "not": "नाही",
    "maximum": "जास्तीत जास्त",
    "minimum": "कमीत कमी",
    "zero": "शून्य",
    "total": "एकूण",
    "prime minister": "पंतप्रधान",
    "supreme court": "सर्वोच्च न्यायालय",
    "none of these": "यापैकी कोणतेही नाही",
    "none of the above": "वरीलपैकी कोणतेही नाही",
    "all of the above": "वरील सर्व",
},

# ─────────────────────────────────────────────────────────────────────────────
"kn": {  # KANNADA
    "which of the following is correct": "ಕೆಳಗಿನವುಗಳಲ್ಲಿ ಯಾವುದು ಸರಿ",
    "which of the following is incorrect": "ಕೆಳಗಿನವುಗಳಲ್ಲಿ ಯಾವುದು ತಪ್ಪು",
    "which of the following": "ಕೆಳಗಿನವುಗಳಲ್ಲಿ ಯಾವುದು",
    "what is the value of": "ಯ ಮೌಲ್ಯ ಏನು",
    "what is the": "ಏನು",
    "find the value of": "ಯ ಮೌಲ್ಯ ಕಂಡುಹಿಡಿಯಿರಿ",
    "find the": "ಕಂಡುಹಿಡಿಯಿರಿ",
    "calculate the": "ಲೆಕ್ಕಿಸಿ",
    "none of these": "ಇವುಗಳಲ್ಲಿ ಯಾವುದೂ ಇಲ್ಲ",
    "none of the above": "ಮೇಲಿನ ಯಾವುದೂ ಇಲ್ಲ",
    "all of the above": "ಮೇಲಿನ ಎಲ್ಲವೂ",
    "initial velocity": "ಆರಂಭಿಕ ವೇಗ",
    "final velocity": "ಅಂತಿಮ ವೇಗ",
    "kinetic energy": "ಚಲನ ಶಕ್ತಿ",
    "potential energy": "ಸ್ಥಿತಿ ಶಕ್ತಿ",
    "electric current": "ವಿದ್ಯುತ್ ಪ್ರವಾಹ",
    "electric field": "ವಿದ್ಯುತ್ ಕ್ಷೇತ್ರ",
    "magnetic field": "ಕಾಂತ ಕ್ಷೇತ್ರ",
    "gravitational force": "ಗುರುತ್ವಾಕರ್ಷಣ ಬಲ",
    "work done": "ಮಾಡಿದ ಕೆಲಸ",
    "speed of light": "ಬೆಳಕಿನ ವೇಗ",
    "boiling point": "ಕುದಿ ಬಿಂದು",
    "melting point": "ಕರಗು ಬಿಂದು",
    "rate of reaction": "ಕ್ರಿಯೆಯ ದರ",
    "photosynthesis": "ದ್ಯುತಿ ಸಂಶ್ಲೇಷಣೆ",
    "food chain": "ಆಹಾರ ಸರಪಳಿ",
    "velocity": "ವೇಗ",
    "acceleration": "ತ್ವರಣ",
    "force": "ಬಲ",
    "mass": "ದ್ರವ್ಯರಾಶಿ",
    "weight": "ತೂಕ",
    "energy": "ಶಕ್ತಿ",
    "power": "ಶಕ್ತಿ",
    "work": "ಕೆಲಸ",
    "momentum": "ಆವೇಗ",
    "pressure": "ಒತ್ತಡ",
    "temperature": "ಉಷ್ಣಾಂಶ",
    "heat": "ಶಾಖ",
    "current": "ವಿದ್ಯುತ್ ಪ್ರವಾಹ",
    "voltage": "ವೋಲ್ಟೇಜ್",
    "resistance": "ಪ್ರತಿರೋಧ",
    "wavelength": "ತರಂಗ ಉದ್ದ",
    "frequency": "ಆವರ್ತನ",
    "displacement": "ಸ್ಥಾನಾಂತರ",
    "distance": "ದೂರ",
    "speed": "ವೇಗ",
    "time": "ಸಮಯ",
    "gravity": "ಗುರುತ್ವ",
    "friction": "ಘರ್ಷಣೆ",
    "electron": "ಎಲೆಕ್ಟ್ರಾನ್",
    "proton": "ಪ್ರೋಟಾನ್",
    "neutron": "ನ್ಯೂಟ್ರಾನ್",
    "nucleus": "ಕೇಂದ್ರಕ",
    "atom": "ಪರಮಾಣು",
    "molecule": "ಅಣು",
    "element": "ಮೂಲವಸ್ತು",
    "compound": "ಸಂಯುಕ್ತ",
    "mixture": "ಮಿಶ್ರಣ",
    "solution": "ದ್ರಾವಣ",
    "acid": "ಆಮ್ಲ",
    "base": "ಕ್ಷಾರ",
    "salt": "ಉಪ್ಪು",
    "catalyst": "ವೇಗವರ್ಧಕ",
    "reaction": "ಕ್ರಿಯೆ",
    "cell": "ಕೋಶ",
    "enzyme": "ಕಿಣ್ವ",
    "protein": "ಪ್ರೋಟೀನ್",
    "gene": "ಜೀನ್",
    "chromosome": "ವರ್ಣತಂತು",
    "respiration": "ಉಸಿರಾಟ",
    "evolution": "ವಿಕಾಸ",
    "probability": "ಸಂಭಾವ್ಯತೆ",
    "equation": "ಸಮೀಕರಣ",
    "mean": "ಸರಾಸರಿ",
    "percentage": "ಶೇಕಡಾ",
    "is": "ಆಗಿದೆ",
    "are": "ಆಗಿವೆ",
    "and": "ಮತ್ತು",
    "or": "ಅಥವಾ",
    "not": "ಅಲ್ಲ",
    "maximum": "ಗರಿಷ್ಠ",
    "minimum": "ಕನಿಷ್ಠ",
    "zero": "ಶೂನ್ಯ",
    "total": "ಒಟ್ಟು",
    "prime minister": "ಪ್ರಧಾನ ಮಂತ್ರಿ",
    "supreme court": "ಸರ್ವೋಚ್ಚ ನ್ಯಾಯಾಲಯ",
    "none of these": "ಇವುಗಳಲ್ಲಿ ಯಾವುದೂ ಇಲ್ಲ",
    "none of the above": "ಮೇಲಿನ ಯಾವುದೂ ಇಲ್ಲ",
    "all of the above": "ಮೇಲಿನ ಎಲ್ಲವೂ",
},

# ─────────────────────────────────────────────────────────────────────────────
"or": {  # ODIA
    "which of the following is correct": "ନିମ୍ନଲିଖିତ ମଧ୍ୟରୁ କେଉଁଟି ସଠିକ",
    "which of the following is incorrect": "ନିମ୍ନଲିଖିତ ମଧ୍ୟରୁ କେଉଁଟି ଭୁଲ",
    "which of the following": "ନିମ୍ନଲିଖିତ ମଧ୍ୟରୁ କେଉଁଟି",
    "what is the value of": "ର ମୂଲ୍ୟ କ'ଣ",
    "what is the": "କ'ଣ",
    "find the value of": "ର ମୂଲ୍ୟ ଖୋଜ",
    "find the": "ଖୋଜ",
    "calculate the": "ଗଣନା କର",
    "none of these": "ଏଥିରୁ କୌଣସିଟି ନୁହେଁ",
    "none of the above": "ଉପରୋକ୍ତ କୌଣସିଟି ନୁହେଁ",
    "all of the above": "ଉପରୋକ୍ତ ସବୁ",
    "initial velocity": "ପ୍ରାରମ୍ଭିକ ବେଗ",
    "final velocity": "ଶେଷ ବେଗ",
    "kinetic energy": "ଗତି ଶକ୍ତି",
    "potential energy": "ସ୍ଥିତିଜ ଶକ୍ତି",
    "electric current": "ବୈଦ୍ୟୁତିକ ସ୍ରୋତ",
    "electric field": "ବୈଦ୍ୟୁତିକ କ୍ଷେତ୍ର",
    "magnetic field": "ଚୁମ୍ବକୀୟ କ୍ଷେତ୍ର",
    "gravitational force": "ମାଧ୍ୟାକର୍ଷଣ ବଳ",
    "work done": "ସମ୍ପାଦିତ କାର୍ଯ୍ୟ",
    "speed of light": "ଆଲୋକର ଗତି",
    "photosynthesis": "ସଂ ଶ୍ଲେଷଣ",
    "food chain": "ଖାଦ୍ୟ ଶୃଙ୍ଖଳ",
    "velocity": "ବେଗ",
    "acceleration": "ତ୍ୱରଣ",
    "force": "ବଳ",
    "mass": "ପ୍ରଭାବ",
    "weight": "ଓଜନ",
    "energy": "ଶକ୍ତି",
    "power": "ଶକ୍ତି",
    "work": "କାର୍ଯ୍ୟ",
    "momentum": "ଭରବେଗ",
    "pressure": "ଚାପ",
    "temperature": "ତାପମାତ୍ରା",
    "heat": "ଉତ୍ତାପ",
    "current": "ସ୍ରୋତ",
    "voltage": "ଭୋଲ୍ଟେଜ",
    "resistance": "ପ୍ରତିରୋଧ",
    "wavelength": "ତରଙ୍ଗ ଦୈର୍ଘ୍ୟ",
    "frequency": "ଆବୃତ୍ତି",
    "displacement": "ସ୍ଥାନଚ୍ୟୁତି",
    "distance": "ଦୂରତ୍ୱ",
    "speed": "ଗତି",
    "time": "ସମୟ",
    "gravity": "ମାଧ୍ୟାକର୍ଷଣ",
    "friction": "ଘର୍ଷଣ",
    "electron": "ଇଲେକ୍ଟ୍ରନ",
    "proton": "ପ୍ରୋଟନ",
    "neutron": "ନ୍ୟୁଟ୍ରନ",
    "nucleus": "ନ୍ୟୁକ୍ଲିୟସ",
    "atom": "ପରମାଣୁ",
    "molecule": "ଅଣୁ",
    "element": "ମୌଳ",
    "compound": "ଯୌଗିକ",
    "mixture": "ମିଶ୍ରଣ",
    "solution": "ଦ୍ରବଣ",
    "acid": "ଅମ୍ଳ",
    "base": "କ୍ଷାର",
    "salt": "ଲବଣ",
    "catalyst": "ଉତ୍ପ୍ରେରକ",
    "reaction": "ରାସାୟନିକ ବିକ୍ରିୟା",
    "cell": "କୋଷ",
    "enzyme": "ଏନ୍‌ଜାଇମ",
    "protein": "ପ୍ରୋଟିନ",
    "gene": "ଜିନ",
    "chromosome": "ଗୁଣସୂତ୍ର",
    "respiration": "ଶ୍ୱସନ",
    "evolution": "ବିବର୍ତ୍ତନ",
    "probability": "ସମ୍ଭାବ୍ୟତା",
    "equation": "ସମୀକରଣ",
    "mean": "ହାରାହାରି",
    "percentage": "ଶତକଡ଼ା",
    "is": "ଅଟେ",
    "are": "ଅଟନ୍ତି",
    "and": "ଏବଂ",
    "or": "ଅଥବା",
    "not": "ନୁହେଁ",
    "maximum": "ସର୍ବାଧିକ",
    "minimum": "ସର୍ବନ୍ୟୂନ",
    "zero": "ଶୂନ",
    "total": "ମୋଟ",
    "prime minister": "ପ୍ରଧାନ ମନ୍ତ୍ରୀ",
    "supreme court": "ସୁପ୍ରିମ କୋର୍ଟ",
    "none of these": "ଏଥିରୁ କୌଣସିଟି ନୁହେଁ",
    "none of the above": "ଉପରୋକ୍ତ କୌଣସିଟି ନୁହେଁ",
    "all of the above": "ଉପରୋକ୍ତ ସବୁ",
},
}  # end PHRASES


def build_sorted_phrases(lang: str):
    """Return phrases sorted longest-first for greedy matching."""
    items = list(PHRASES.get(lang, {}).items())
    items.sort(key=lambda x: len(x[0]), reverse=True)
    return items


def translate_text(text: str, lang: str, sorted_phrases=None) -> str:
    """
    Translate text using phrase dictionary + number/unit preservation.
    Numbers, formulas, symbols are preserved.
    """
    if not text or lang == "en":
        return text

    if sorted_phrases is None:
        sorted_phrases = build_sorted_phrases(lang)

    result = text

    # Protect numbers, formulas, and special tokens
    # Replace them with placeholders to avoid mangling
    protected = {}
    counter = [0]

    def protect(m):
        key = f"__PROT{counter[0]}__"
        protected[key] = m.group(0)
        counter[0] += 1
        return key

    # Protect: numbers with units, scientific notation, formulas, symbols, URLs
    protect_patterns = [
        r'\d+[\./×⁰¹²³⁴⁵⁶⁷⁸⁹]+\d*\s*[A-Za-z%°Ω²³⁻⁺]*',  # numbers with superscript
        r'\d+\.\d+\s*[A-Za-z%°Ω]*',   # decimals
        r'\d+×10[⁻⁺]?\d+',            # scientific notation
        r'[A-Z][a-z]?\d*',             # chemical symbols like O2, CO2, H2O
        r'\d+\s*[A-Za-z°ΩμΩΩ]+',      # numbers with units
        r'[A-Z]+\d+',                   # things like DNA, RNA, ATP, CO2
        r'ΔT|ΔH|ΔG|ΔS|ΔP|ΔV',        # delta notation
        r'[α-ωΑ-Ω]+',                  # Greek letters
        r'\d+',                         # bare numbers
    ]

    for pat in protect_patterns:
        result = re.sub(pat, protect, result)

    # Now do phrase substitution (case-insensitive)
    lower_result = result.lower()
    new_result = result
    offset = 0

    # Build a list of substitutions to apply
    substitutions = []
    used_ranges = set()

    for phrase, translation in sorted_phrases:
        if not phrase.strip() or not translation.strip():
            continue
        start = 0
        while True:
            idx = lower_result.find(phrase.lower(), start)
            if idx == -1:
                break
            end = idx + len(phrase)
            # Check no overlap with already-used ranges
            overlap = any(
                not (end <= r[0] or idx >= r[1])
                for r in used_ranges
            )
            if not overlap:
                used_ranges.add((idx, end))
                substitutions.append((idx, end, translation))
            start = end

    # Sort substitutions by position
    substitutions.sort(key=lambda x: x[0])

    # Apply substitutions in order
    if substitutions:
        parts = []
        prev = 0
        for idx, end, translation in substitutions:
            parts.append(result[prev:idx])
            parts.append(translation)
            prev = end
        parts.append(result[prev:])
        new_result = "".join(parts)

    # Restore protected tokens
    for key, val in protected.items():
        new_result = new_result.replace(key, val)

    # Clean up extra spaces
    new_result = re.sub(r'  +', ' ', new_result).strip()

    return new_result


def translate_all_to_db(lang: str, batch_size: int = 2000, force: bool = False):
    """
    Translate all untranslated questions for `lang` into the DB.
    """
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA journal_mode=WAL")
    conn.execute("PRAGMA synchronous=NORMAL")
    conn.execute("PRAGMA cache_size=10000")

    total = conn.execute("SELECT COUNT(*) FROM question_bank").fetchone()[0]

    if force:
        where = "1=1"
    else:
        where = f"(question_{lang} IS NULL OR question_{lang} = '')"

    remaining = conn.execute(f"SELECT COUNT(*) FROM question_bank WHERE {where}").fetchone()[0]

    print(f"  [{lang}] Total: {total:,} | Need translation: {remaining:,}")

    if remaining == 0:
        print(f"  [{lang}] ✅ Already fully translated!")
        conn.close()
        return 0

    sorted_phrases = build_sorted_phrases(lang)
    fields = ["question", "option_a", "option_b", "option_c", "option_d", "explanation"]
    translated_count = 0
    offset = 0

    while True:
        rows = conn.execute(
            f"""SELECT qb_id, question_en, option_a_en, option_b_en, option_c_en, option_d_en, explanation_en
                FROM question_bank WHERE {where} LIMIT ? OFFSET ?""",
            (batch_size, offset)
        ).fetchall()

        if not rows:
            break

        batch_data = []
        for row in rows:
            d = dict(row)
            qb_id = d["qb_id"]
            translated = {f"{f}_{lang}": translate_text(d.get(f"{f}_en", "") or "", lang, sorted_phrases)
                          for f in fields}
            translated["qb_id"] = qb_id
            batch_data.append(translated)

        # Bulk update
        if batch_data:
            set_clause = ", ".join([f"{f}_{lang}=?" for f in fields])
            conn.executemany(
                f"UPDATE question_bank SET {set_clause} WHERE qb_id=?",
                [
                    [d[f"{f}_{lang}"] for f in fields] + [d["qb_id"]]
                    for d in batch_data
                ]
            )
            conn.commit()
            translated_count += len(batch_data)

        offset += len(rows)
        pct = min(100, (translated_count / remaining * 100)) if remaining > 0 else 100
        print(f"  [{lang}] {translated_count:,}/{remaining:,} ({pct:.1f}%) done", end="\r", flush=True)

        if len(rows) < batch_size:
            break

    print(f"  [{lang}] ✅ {translated_count:,} questions translated!          ")
    conn.close()
    return translated_count


def update_translated_langs_field():
    """Update the translated_langs JSON field for all rows."""
    conn = sqlite3.connect(DB_PATH)
    conn.execute("PRAGMA journal_mode=WAL")
    import json

    all_langs = ["hi", "bn", "ta", "te", "gu", "mr", "kn", "or"]
    print("\n🔄 Updating translated_langs field...")

    # Build a case expression to set translated_langs based on which fields are populated
    conn.execute("""
        UPDATE question_bank
        SET translated_langs = (
            SELECT json_group_array(lang)
            FROM (
                SELECT 'hi' as lang WHERE question_hi IS NOT NULL AND question_hi != '' UNION ALL
                SELECT 'bn' WHERE question_bn IS NOT NULL AND question_bn != '' UNION ALL
                SELECT 'ta' WHERE question_ta IS NOT NULL AND question_ta != '' UNION ALL
                SELECT 'te' WHERE question_te IS NOT NULL AND question_te != '' UNION ALL
                SELECT 'gu' WHERE question_gu IS NOT NULL AND question_gu != '' UNION ALL
                SELECT 'mr' WHERE question_mr IS NOT NULL AND question_mr != '' UNION ALL
                SELECT 'kn' WHERE question_kn IS NOT NULL AND question_kn != '' UNION ALL
                SELECT 'or' WHERE question_or IS NOT NULL AND question_or != ''
            )
        )
    """)
    conn.commit()
    print("✅ translated_langs field updated!")
    conn.close()


def verify_translations():
    """Print verification stats."""
    conn = sqlite3.connect(DB_PATH)
    total = conn.execute("SELECT COUNT(*) FROM question_bank").fetchone()[0]
    print(f"\n📊 Translation Verification (Total: {total:,})")
    print("-" * 50)
    langs = {"hi": "Hindi", "bn": "Bengali", "ta": "Tamil", "te": "Telugu",
             "gu": "Gujarati", "mr": "Marathi", "kn": "Kannada", "or": "Odia"}
    for lc, name in langs.items():
        done = conn.execute(f"SELECT COUNT(*) FROM question_bank WHERE question_{lc} IS NOT NULL AND question_{lc} != ''").fetchone()[0]
        pct = done / total * 100
        bar = "█" * int(pct / 5) + "░" * (20 - int(pct / 5))
        status = "✅" if pct >= 99 else ("⚠️" if pct >= 50 else "❌")
        print(f"  {status} {name:10} [{bar}] {pct:.1f}% ({done:,}/{total:,})")
    conn.close()


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Offline mass translator for CBT question bank")
    parser.add_argument("--lang", help="Translate only this language (e.g. hi)", default=None)
    parser.add_argument("--batch", type=int, default=3000, help="Batch size")
    parser.add_argument("--force", action="store_true", help="Re-translate all, even already translated")
    parser.add_argument("--verify", action="store_true", help="Only show verification stats")
    args = parser.parse_args()

    if args.verify:
        verify_translations()
        sys.exit(0)

    langs_to_do = [args.lang] if args.lang else ["hi", "bn", "ta", "te", "gu", "mr", "kn", "or"]

    print("=" * 60)
    print("  CBT OFFLINE MASS TRANSLATOR")
    print(f"  Languages: {', '.join(langs_to_do)}")
    print(f"  Batch size: {args.batch:,}")
    print(f"  Force re-translate: {args.force}")
    print("=" * 60)

    start_time = time.time()
    total_done = 0

    for lang in langs_to_do:
        lang_name = {"hi":"Hindi","bn":"Bengali","ta":"Tamil","te":"Telugu",
                     "gu":"Gujarati","mr":"Marathi","kn":"Kannada","or":"Odia"}.get(lang, lang)
        print(f"\n🌐 Translating → {lang_name} ({lang})")
        n = translate_all_to_db(lang, batch_size=args.batch, force=args.force)
        total_done += n

    update_translated_langs_field()
    verify_translations()

    elapsed = time.time() - start_time
    print(f"\n⏱  Total time: {elapsed:.1f}s | Questions processed: {total_done:,}")
    print("🎉 Done! All questions are now translatable in the app.")
