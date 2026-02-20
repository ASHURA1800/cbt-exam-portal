"""
apply_all_translations.py
=========================
Applies glossary-based translation to ALL 57,000+ questions in the database.
Works 100% offline — no internet needed.
Translates questions that don't yet have translations in each language.
"""

import sqlite3
import time
import re
from typing import Dict

DB_PATH = "question_bank.db"

LANGS = ["hi", "bn", "ta", "te", "gu", "mr", "kn", "or"]

# ── Full scientific + common word glossary ─────────────────────────────────

GLOSSARY = {
    "hi": {
        # Physics
        "velocity": "वेग", "acceleration": "त्वरण", "force": "बल", "mass": "द्रव्यमान",
        "weight": "भार", "energy": "ऊर्जा", "power": "शक्ति", "work": "कार्य",
        "momentum": "संवेग", "pressure": "दाब", "temperature": "तापमान", "heat": "ऊष्मा",
        "current": "धारा", "voltage": "वोल्टेज", "resistance": "प्रतिरोध",
        "wavelength": "तरंगदैर्ध्य", "frequency": "आवृत्ति", "amplitude": "आयाम",
        "displacement": "विस्थापन", "distance": "दूरी", "time": "समय",
        "speed": "चाल", "gravity": "गुरुत्वाकर्षण", "friction": "घर्षण",
        "electric field": "विद्युत क्षेत्र", "magnetic field": "चुंबकीय क्षेत्र",
        "photon": "फोटोन", "electron": "इलेक्ट्रॉन", "proton": "प्रोटॉन",
        "neutron": "न्यूट्रॉन", "nucleus": "नाभिक", "atom": "परमाणु",
        "molecule": "अणु", "ion": "आयन", "charge": "आवेश",
        "capacitor": "संधारित्र", "conductor": "चालक", "insulator": "कुचालक",
        "lens": "लेंस", "mirror": "दर्पण", "reflection": "परावर्तन",
        "refraction": "अपवर्तन", "diffraction": "विवर्तन",
        "potential energy": "स्थितिज ऊर्जा", "kinetic energy": "गतिज ऊर्जा",
        "Newton": "न्यूटन", "joule": "जूल", "watt": "वाट", "pascal": "पास्कल",
        # Chemistry
        "element": "तत्व", "compound": "यौगिक", "mixture": "मिश्रण",
        "solution": "विलयन", "acid": "अम्ल", "base": "क्षार", "salt": "लवण",
        "oxidation": "ऑक्सीकरण", "reduction": "अपचयन", "catalyst": "उत्प्रेरक",
        "reaction": "अभिक्रिया", "bond": "बंध", "orbital": "कक्षक",
        "valence": "संयोजकता", "mole": "मोल", "concentration": "सांद्रता",
        "solubility": "विलेयता", "entropy": "एन्ट्रॉपी", "enthalpy": "एन्थैल्पी",
        "equilibrium": "साम्य", "polymer": "बहुलक", "isomer": "समावयवी",
        "pH": "pH",
        # Biology
        "cell": "कोशिका", "membrane": "झिल्ली", "enzyme": "एंजाइम",
        "protein": "प्रोटीन", "gene": "जीन", "chromosome": "गुणसूत्र",
        "mitosis": "समसूत्री विभाजन", "meiosis": "अर्धसूत्री विभाजन",
        "photosynthesis": "प्रकाश संश्लेषण", "respiration": "श्वसन",
        "digestion": "पाचन", "evolution": "विकास", "mutation": "उत्परिवर्तन",
        "mitochondria": "माइटोकॉन्ड्रिया", "chloroplast": "क्लोरोप्लास्ट",
        "ribosome": "राइबोसोम", "nephron": "नेफ्रॉन", "neuron": "न्यूरॉन",
        # Maths
        "derivative": "अवकलज", "integral": "समाकल", "matrix": "आव्यूह",
        "vector": "सदिश", "scalar": "अदिश", "probability": "प्रायिकता",
        "trigonometry": "त्रिकोणमिति", "logarithm": "लघुगणक",
        "equation": "समीकरण", "function": "फलन", "limit": "सीमा",
        # Common
        "the": "", "is": "है", "are": "हैं", "and": "और", "or": "या",
        "not": "नहीं", "only": "केवल", "always": "हमेशा",
        "maximum": "अधिकतम", "minimum": "न्यूनतम",
        "increase": "वृद्धि", "decrease": "कमी", "equal": "बराबर",
        "greater": "अधिक", "less": "कम", "zero": "शून्य",
        "positive": "धनात्मक", "negative": "ऋणात्मक",
        "area": "क्षेत्रफल", "volume": "आयतन", "length": "लंबाई",
        "surface": "सतह", "height": "ऊंचाई", "width": "चौड़ाई",
        "initial": "प्रारंभिक", "final": "अंतिम", "total": "कुल",
        "body": "पिंड", "object": "वस्तु", "particle": "कण",
        "direction": "दिशा", "magnitude": "परिमाण",
        "formula": "सूत्र", "law": "नियम", "principle": "सिद्धांत",
        "unit": "इकाई", "dimension": "विमा", "measurement": "माप",
        "calculate": "परिकलन", "find": "ज्ञात करें", "given": "दिया है",
        "A force of": "एक बल", "applied": "लगाया",
        "A body of mass": "एक पिंड जिसका द्रव्यमान",
        "The force": "बल", "The velocity": "वेग", "The acceleration": "त्वरण",
        "starts with": "से शुरू होती है", "travels": "यात्रा करती है",
        "what is": "क्या है", "which": "कौन", "how much": "कितना",
        "per second": "प्रति सेकंड", "per hour": "प्रति घंटा",
        "metre": "मीटर", "kilogram": "किलोग्राम", "second": "सेकंड",
        "Newton's": "न्यूटन का", "Ohm's": "ओम का", "Boyle's": "बॉयल का",
    },
    "bn": {
        "velocity": "বেগ", "acceleration": "ত্বরণ", "force": "বল",
        "mass": "ভর", "weight": "ওজন", "energy": "শক্তি", "power": "ক্ষমতা",
        "work": "কাজ", "momentum": "ভরবেগ", "pressure": "চাপ",
        "temperature": "তাপমাত্রা", "heat": "তাপ", "current": "তড়িৎ প্রবাহ",
        "voltage": "ভোল্টেজ", "resistance": "রোধ", "wavelength": "তরঙ্গদৈর্ঘ্য",
        "frequency": "কম্পাঙ্ক", "amplitude": "বিস্তার",
        "displacement": "সরণ", "distance": "দূরত্ব", "time": "সময়",
        "speed": "দ্রুতি", "gravity": "মাধ্যাকর্ষণ", "friction": "ঘর্ষণ",
        "electron": "ইলেক্ট্রন", "proton": "প্রোটন", "neutron": "নিউট্রন",
        "nucleus": "নিউক্লিয়াস", "atom": "পরমাণু", "molecule": "অণু",
        "ion": "আয়ন", "charge": "আধান", "potential energy": "বিভব শক্তি",
        "kinetic energy": "গতিশক্তি", "element": "মৌল", "compound": "যৌগ",
        "mixture": "মিশ্রণ", "solution": "দ্রবণ", "acid": "অ্যাসিড",
        "base": "ক্ষার", "salt": "লবণ", "oxidation": "জারণ",
        "reduction": "বিজারণ", "catalyst": "অনুঘটক", "reaction": "বিক্রিয়া",
        "bond": "বন্ধন", "mole": "মোল", "concentration": "ঘনমাত্রা",
        "equilibrium": "সাম্যাবস্থা", "cell": "কোষ", "membrane": "ঝিল্লি",
        "enzyme": "এনজাইম", "protein": "প্রোটিন", "gene": "জিন",
        "chromosome": "ক্রোমোজোম", "photosynthesis": "সালোকসংশ্লেষণ",
        "respiration": "শ্বসন", "evolution": "বিবর্তন", "mutation": "মিউটেশন",
        "equation": "সমীকরণ", "probability": "সম্ভাবনা",
        "area": "ক্ষেত্রফল", "volume": "আয়তন", "length": "দৈর্ঘ্য",
        "is": "হয়", "are": "হয়", "and": "এবং", "or": "বা",
        "not": "নয়", "maximum": "সর্বোচ্চ", "minimum": "সর্বনিম্ন",
        "increase": "বৃদ্ধি", "decrease": "হ্রাস", "zero": "শূন্য",
        "body": "বস্তু", "object": "বস্তু", "what is": "কত", "find": "নির্ণয় করুন",
    },
    "ta": {
        "velocity": "திசைவேகம்", "acceleration": "முடுக்கம்", "force": "விசை",
        "mass": "நிறை", "weight": "எடை", "energy": "ஆற்றல்", "power": "திறன்",
        "work": "வேலை", "momentum": "உந்தம்", "pressure": "அழுத்தம்",
        "temperature": "வெப்பநிலை", "heat": "வெப்பம்", "current": "மின்னோட்டம்",
        "voltage": "மின்னழுத்தம்", "resistance": "மின்தடை",
        "wavelength": "அலைநீளம்", "frequency": "அதிர்வெண்", "amplitude": "வீச்சு",
        "displacement": "இடப்பெயர்வு", "distance": "தொலைவு", "time": "நேரம்",
        "speed": "வேகம்", "gravity": "புவியீர்ப்பு", "friction": "உராய்வு",
        "electron": "எலக்ட்ரான்", "proton": "புரோட்டான்", "neutron": "நியூட்ரான்",
        "nucleus": "கரு", "atom": "அணு", "molecule": "மூலக்கூறு",
        "ion": "அயன்", "charge": "மின்னேற்றம்",
        "potential energy": "நிலை ஆற்றல்", "kinetic energy": "இயக்க ஆற்றல்",
        "element": "தனிமம்", "compound": "சேர்மம்", "mixture": "கலவை",
        "solution": "கரைசல்", "acid": "அமிலம்", "base": "காரம்", "salt": "உப்பு",
        "oxidation": "ஆக்சிஜனேற்றம்", "reduction": "ஒடுக்கம்",
        "catalyst": "வினையூக்கி", "reaction": "வினை", "bond": "பிணைப்பு",
        "mole": "மோல்", "concentration": "செறிவு",
        "cell": "செல்", "membrane": "சவ்வு", "enzyme": "நொதி",
        "protein": "புரதம்", "gene": "மரபணு", "chromosome": "குரோமோசோம்",
        "photosynthesis": "ஒளிச்சேர்க்கை", "respiration": "சுவாசம்",
        "evolution": "பரிணாமம்", "mutation": "உருமாற்றம்",
        "equation": "சமன்பாடு", "probability": "நிகழ்தகவு",
        "area": "பரப்பு", "volume": "கனஅளவு", "length": "நீளம்",
        "is": "ஆகும்", "and": "மற்றும்", "or": "அல்லது",
        "not": "இல்லை", "maximum": "அதிகபட்சம்", "minimum": "குறைந்தபட்சம்",
        "increase": "அதிகரிப்பு", "decrease": "குறைவு", "zero": "பூஜ்யம்",
        "body": "பொருள்", "object": "பொருள்", "find": "காண்", "what is": "என்ன",
    },
    "te": {
        "velocity": "వేగం", "acceleration": "త్వరణం", "force": "బలం",
        "mass": "ద్రవ్యరాశి", "weight": "బరువు", "energy": "శక్తి",
        "power": "శక్తి", "work": "పని", "momentum": "ద్రవ్యవేగం",
        "pressure": "పీడనం", "temperature": "ఉష్ణోగ్రత", "heat": "వేడి",
        "current": "విద్యుత్ ప్రవాహం", "voltage": "వోల్టేజ్",
        "resistance": "నిరోధం", "wavelength": "తరంగ దైర్ఘ్యం",
        "frequency": "పౌనఃపున్యం", "amplitude": "వ్యాప్తి",
        "displacement": "స్థానభ్రంశం", "distance": "దూరం", "time": "సమయం",
        "speed": "వేగం", "gravity": "గురుత్వాకర్షణ", "friction": "ఘర్షణ",
        "electron": "ఎలెక్ట్రాన్", "proton": "ప్రోటాన్", "neutron": "న్యూట్రాన్",
        "nucleus": "కేంద్రకం", "atom": "పరమాణువు", "molecule": "అణువు",
        "ion": "అయాన్", "charge": "ఆవేశం",
        "potential energy": "స్థితిజ శక్తి", "kinetic energy": "గతిజ శక్తి",
        "element": "మూలకం", "compound": "సమ్మేళనం", "mixture": "మిశ్రమం",
        "solution": "ద్రావణం", "acid": "ఆమ్లం", "base": "క్షారం", "salt": "లవణం",
        "oxidation": "ఆక్సీకరణ", "reduction": "క్షయకరణం",
        "catalyst": "ఉత్ప్రేరకం", "reaction": "చర్య", "bond": "బంధం",
        "mole": "మోల్", "concentration": "సాంద్రత",
        "cell": "కణం", "membrane": "పొర", "enzyme": "ఎంజైమ్",
        "protein": "ప్రోటీన్", "gene": "జన్యువు", "chromosome": "క్రోమోజోమ్",
        "photosynthesis": "కిరణజన్య సంయోగక్రియ", "respiration": "శ్వాసక్రియ",
        "evolution": "పరిణామం", "mutation": "ఉత్పరివర్తన",
        "equation": "సమీకరణం", "probability": "సంభావ్యత",
        "area": "వైశాల్యం", "volume": "పరిమాణం", "length": "పొడవు",
        "is": "ఉంది", "and": "మరియు", "or": "లేదా",
        "not": "కాదు", "maximum": "గరిష్ట", "minimum": "కనిష్ట",
        "increase": "పెరుగుట", "decrease": "తగ్గుట", "zero": "శూన్యం",
        "body": "వస్తువు", "object": "వస్తువు", "find": "కనుగొనండి",
    },
    "gu": {
        "velocity": "વેગ", "acceleration": "પ્રવેગ", "force": "બળ",
        "mass": "દ્રવ્યમાન", "weight": "વજન", "energy": "ઊર્જા",
        "power": "શક્તિ", "work": "કાર્ય", "momentum": "વેગમાન",
        "pressure": "દબાણ", "temperature": "તાપમાન", "heat": "ઉષ્મા",
        "current": "વિદ્યુત પ્રવાહ", "voltage": "વોલ્ટેજ", "resistance": "અવરોધ",
        "wavelength": "તરંગ લંબાઈ", "frequency": "આવૃત્તિ", "amplitude": "કંપ",
        "displacement": "સ્થાનાંતર", "distance": "અંતર", "time": "સમય",
        "speed": "ઝડપ", "gravity": "ગુરુત્વ", "friction": "ઘર્ષણ",
        "electron": "ઇલેક્ટ્રોન", "proton": "પ્રોટોન", "neutron": "ન્યૂટ્રોન",
        "nucleus": "ન્યૂક્લિયસ", "atom": "પરમાણુ", "molecule": "અણુ",
        "ion": "આયન", "charge": "વિદ્યુતભાર",
        "potential energy": "સ્થિતિ ઊર્જા", "kinetic energy": "ગતિ ઊર્જા",
        "element": "તત્વ", "compound": "સંયોજન", "mixture": "મિશ્રણ",
        "solution": "દ્રાવણ", "acid": "એસિડ", "base": "ક્ષાર", "salt": "મીઠું",
        "oxidation": "ઓક્સિડેશન", "reduction": "રિડક્શન",
        "catalyst": "ઉત્પ્રેરક", "reaction": "પ્રક્રિયા", "bond": "બંધ",
        "mole": "મોલ", "concentration": "સાંદ્રતા",
        "cell": "કોષ", "membrane": "પડદો", "enzyme": "ઉત્સેચક",
        "protein": "પ્રોટીન", "gene": "જનીન", "chromosome": "રંગસૂત્ર",
        "photosynthesis": "પ્રકાશ સંશ્લેષણ", "respiration": "શ્વાસ",
        "evolution": "ઉત્ક્રાંતિ", "mutation": "પરિવર્તન",
        "equation": "સમીકરણ", "probability": "સંભાવના",
        "area": "ક્ષેત્રફળ", "volume": "ઘનફળ", "length": "લંબાઈ",
        "is": "છે", "and": "અને", "or": "અથવા",
        "not": "નહીં", "maximum": "મહત્તમ", "minimum": "ન્યૂનતમ",
        "increase": "વૃદ્ધિ", "decrease": "ઘટાડો", "zero": "શૂન્ય",
        "body": "વસ્તુ", "object": "વસ્તુ", "find": "શોધો", "what is": "શું છે",
        "A force of": "એક બળ", "A body of mass": "એક વસ્તુ જેનું દ્રવ્યમાન",
    },
    "mr": {
        "velocity": "वेग", "acceleration": "त्वरण", "force": "बल",
        "mass": "वस्तुमान", "weight": "वजन", "energy": "ऊर्जा",
        "power": "शक्ती", "work": "काम", "momentum": "संवेग",
        "pressure": "दाब", "temperature": "तापमान", "heat": "उष्णता",
        "current": "विद्युत प्रवाह", "voltage": "व्होल्टेज",
        "resistance": "प्रतिरोध", "wavelength": "तरंगलांबी",
        "frequency": "वारंवारता", "amplitude": "मोठेपणा",
        "displacement": "विस्थापन", "distance": "अंतर", "time": "वेळ",
        "speed": "वेग", "gravity": "गुरुत्वाकर्षण", "friction": "घर्षण",
        "electron": "इलेक्ट्रॉन", "proton": "प्रोटॉन", "neutron": "न्यूट्रॉन",
        "nucleus": "केंद्रक", "atom": "अणू", "molecule": "रेणू",
        "ion": "आयन", "charge": "आवेश",
        "potential energy": "स्थितिज ऊर्जा", "kinetic energy": "गतिज ऊर्जा",
        "element": "मूलद्रव्य", "compound": "संयुग", "mixture": "मिश्रण",
        "solution": "द्राव", "acid": "आम्ल", "base": "आम्लारि", "salt": "क्षार",
        "oxidation": "ऑक्सिडेशन", "reduction": "क्षपण",
        "catalyst": "उत्प्रेरक", "reaction": "अभिक्रिया", "bond": "बंध",
        "mole": "मोल", "concentration": "सांद्रता",
        "cell": "पेशी", "membrane": "पडदा", "enzyme": "विकर",
        "protein": "प्रथिने", "gene": "जनुक", "chromosome": "गुणसूत्र",
        "photosynthesis": "प्रकाशसंश्लेषण", "respiration": "श्वसन",
        "evolution": "उत्क्रांती", "mutation": "उत्परिवर्तन",
        "equation": "समीकरण", "probability": "संभाव्यता",
        "area": "क्षेत्रफळ", "volume": "आयतन", "length": "लांबी",
        "is": "आहे", "and": "आणि", "or": "किंवा",
        "not": "नाही", "maximum": "कमाल", "minimum": "किमान",
        "increase": "वाढ", "decrease": "घट", "zero": "शून्य",
        "body": "वस्तू", "object": "वस्तू", "find": "शोधा", "what is": "काय आहे",
        "A force of": "एक बल", "A body of mass": "एक वस्तू जिचे वस्तुमान",
        "The force applied is": "लावलेले बल",
        "Its final velocity is": "त्याचा अंतिम वेग",
        "potential energy is": "स्थितिज ऊर्जा",
        "Work done is": "केलेले काम",
        "Its power is": "त्याची शक्ती",
    },
    "kn": {
        "velocity": "ವೇಗ", "acceleration": "ತ್ವರಣ", "force": "ಬಲ",
        "mass": "ದ್ರವ್ಯರಾಶಿ", "weight": "ತೂಕ", "energy": "ಶಕ್ತಿ",
        "power": "ಶಕ್ತಿ", "work": "ಕೆಲಸ", "momentum": "ಆವೇಗ",
        "pressure": "ಒತ್ತಡ", "temperature": "ತಾಪಮಾನ", "heat": "ಶಾಖ",
        "current": "ವಿದ್ಯುತ್ ಪ್ರವಾಹ", "voltage": "ವೋಲ್ಟೇಜ್",
        "resistance": "ವಿದ್ಯುತ್ ತಡೆ", "wavelength": "ತರಂಗ ದೈರ್ಘ್ಯ",
        "frequency": "ಆವರ್ತನ", "amplitude": "ವ್ಯಾಪ್ತಿ",
        "displacement": "ಸ್ಥಾನಭ್ರಂಶ", "distance": "ಅಂತರ", "time": "ಸಮಯ",
        "speed": "ವೇಗ", "gravity": "ಗುರುತ್ವ", "friction": "ಘರ್ಷಣ",
        "electron": "ಎಲೆಕ್ಟ್ರಾನ್", "proton": "ಪ್ರೋಟಾನ್", "neutron": "ನ್ಯೂಟ್ರಾನ್",
        "nucleus": "ನ್ಯೂಕ್ಲಿಯಸ್", "atom": "ಪರಮಾಣು", "molecule": "ಅಣು",
        "ion": "ಅಯಾನ್", "charge": "ಆವೇಶ",
        "potential energy": "ಸ್ಥಿತಿಜ ಶಕ್ತಿ", "kinetic energy": "ಗತಿಜ ಶಕ್ತಿ",
        "element": "ಮೂಲ ವಸ್ತು", "compound": "ಸಂಯುಕ್ತ", "mixture": "ಮಿಶ್ರಣ",
        "solution": "ದ್ರಾವಣ", "acid": "ಆಮ್ಲ", "base": "ಕ್ಷಾರ", "salt": "ಲವಣ",
        "oxidation": "ಆಕ್ಸಿಡೇಷನ್", "reduction": "ಅಪಕರ್ಷಣ",
        "catalyst": "ವೇಗವರ್ಧಕ", "reaction": "ರಾಸಾಯನಿಕ ಕ್ರಿಯೆ", "bond": "ಬಂಧ",
        "mole": "ಮೋಲ್", "concentration": "ಸಾಂದ್ರತೆ",
        "cell": "ಕೋಶ", "membrane": "ಪೊರೆ", "enzyme": "ಕಿಣ್ವ",
        "protein": "ಪ್ರೋಟೀನ್", "gene": "ಜೀನ್", "chromosome": "ವರ್ಣತಂತು",
        "photosynthesis": "ದ್ಯುತಿಸಂಶ್ಲೇಷಣೆ", "respiration": "ಉಸಿರಾಟ",
        "evolution": "ವಿಕಾಸ", "mutation": "ರೂಪಾಂತರ",
        "equation": "ಸಮೀಕರಣ", "probability": "ಸಂಭಾವ್ಯತೆ",
        "area": "ವಿಸ್ತೀರ್ಣ", "volume": "ಗಾತ್ರ", "length": "ಉದ್ದ",
        "is": "ಆಗಿದೆ", "and": "ಮತ್ತು", "or": "ಅಥವಾ",
        "not": "ಇಲ್ಲ", "maximum": "ಗರಿಷ್ಠ", "minimum": "ಕನಿಷ್ಠ",
        "increase": "ಹೆಚ್ಚಳ", "decrease": "ಇಳಿಕೆ", "zero": "ಶೂನ್ಯ",
        "body": "ವಸ್ತು", "object": "ವಸ್ತು", "find": "ಕಂಡುಹಿಡಿಯಿರಿ",
    },
    "or": {
        "velocity": "ବେଗ", "acceleration": "ତ୍ୱରଣ", "force": "ବଳ",
        "mass": "ଭର", "weight": "ଓଜନ", "energy": "ଶକ୍ତି",
        "power": "ଶକ୍ତି", "work": "କାର୍ଯ୍ୟ", "momentum": "ସଂବେଗ",
        "pressure": "ଚାପ", "temperature": "ତାପମାତ୍ରା", "heat": "ଉତ୍ତାପ",
        "current": "ବିଦ୍ୟୁତ ପ୍ରବାହ", "voltage": "ଭୋଲ୍ଟେଜ", "resistance": "ପ୍ରତିରୋଧ",
        "wavelength": "ତରଙ୍ଗ ଦୈର୍ଘ୍ୟ", "frequency": "ଆବୃତ୍ତି", "amplitude": "ଆୟାମ",
        "displacement": "ସ୍ଥାନାନ୍ତର", "distance": "ଦୂରତ୍ୱ", "time": "ସମୟ",
        "speed": "ଗତି", "gravity": "ଗୁରୁତ୍ୱ", "friction": "ଘର୍ଷଣ",
        "electron": "ଇଲେକ୍ଟ୍ରନ", "proton": "ପ୍ରୋଟନ", "neutron": "ନ୍ୟୁଟ୍ରନ",
        "nucleus": "ନ୍ୟୁକ୍ଲିୟସ", "atom": "ପରମାଣୁ", "molecule": "ଅଣୁ",
        "ion": "ଆୟନ", "charge": "ଆବେଶ",
        "potential energy": "ସ୍ଥିତିଜ ଶକ୍ତି", "kinetic energy": "ଗତିଜ ଶକ୍ତି",
        "element": "ମୂଳ ଧାତୁ", "compound": "ଯୌଗିକ", "mixture": "ମିଶ୍ରଣ",
        "solution": "ଦ୍ରାବଣ", "acid": "ଅମ୍ଳ", "base": "କ୍ଷାର", "salt": "ଲୁଣ",
        "oxidation": "ଜାରଣ", "reduction": "ବିଜାରଣ",
        "catalyst": "ଅନୁଘଟକ", "reaction": "ରାସାୟନିକ ପ୍ରକ୍ରିୟା", "bond": "ବନ୍ଧ",
        "mole": "ମୋଲ", "concentration": "ସାନ୍ଦ୍ରତା",
        "cell": "କୋଷ", "membrane": "ଝିଲ୍ଲି", "enzyme": "ଏନଜାଇମ",
        "protein": "ପ୍ରୋଟିନ", "gene": "ଜିନ", "chromosome": "ଗୁଣସୂତ୍ର",
        "photosynthesis": "ସଂଶ୍ଲେଷଣ", "respiration": "ଶ୍ୱାସ",
        "evolution": "ବିବର୍ତ୍ତନ", "mutation": "ଉତ୍ପରିବର୍ତ୍ତନ",
        "equation": "ସମୀକରଣ", "probability": "ସମ୍ଭାବ୍ୟତା",
        "area": "କ୍ଷେତ୍ରଫଳ", "volume": "ଘନଫଳ", "length": "ଦୈର୍ଘ୍ୟ",
        "is": "ଅଟେ", "and": "ଏବଂ", "or": "ବା",
        "not": "ନୁହେଁ", "maximum": "ସର୍ବୋଚ୍ଚ", "minimum": "ସର୍ବନିମ୍ନ",
        "increase": "ବୃଦ୍ଧି", "decrease": "ହ୍ରାସ", "zero": "ଶୂନ୍ୟ",
        "body": "ବସ୍ତୁ", "object": "ବସ୍ତୁ", "find": "ଖୋଜ", "what is": "କ'ଣ",
        "A force of": "ଏକ ବଳ", "A body of mass": "ଏକ ବସ୍ତୁ ଯାହାର ଭର",
    },
}


def glossary_translate(text: str, lang: str) -> str:
    """Apply glossary translations preserving numbers and symbols."""
    if not text or lang not in GLOSSARY:
        return text
    
    glossary = GLOSSARY[lang]
    result = text
    
    # Sort by length descending to prevent partial replacements
    sorted_terms = sorted(glossary.items(), key=lambda x: -len(x[0]))
    
    for en_term, native_term in sorted_terms:
        if not native_term or not en_term:
            continue
        # Use word boundary-aware replacement
        pattern = r'\b' + re.escape(en_term) + r'\b'
        try:
            result = re.sub(pattern, native_term, result, flags=re.IGNORECASE)
        except re.error:
            # Fallback for terms that can't be used in regex
            if en_term.lower() in result.lower():
                idx = result.lower().find(en_term.lower())
                result = result[:idx] + native_term + result[idx + len(en_term):]
    
    return result.strip()


def translate_all_questions():
    """Translate ALL untranslated questions using glossary."""
    conn = sqlite3.connect(DB_PATH, timeout=30)
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA journal_mode=WAL")
    conn.execute("PRAGMA synchronous=NORMAL")
    conn.execute("PRAGMA cache_size=-32000")
    
    total = conn.execute("SELECT COUNT(*) FROM question_bank").fetchone()[0]
    print(f"\nTotal questions: {total:,}")
    print("Applying glossary translations to all untranslated questions...\n")
    
    import json
    
    for lang in LANGS:
        untranslated = conn.execute(f"""
            SELECT COUNT(*) FROM question_bank
            WHERE question_{lang} IS NULL OR question_{lang} = ''
        """).fetchone()[0]
        
        if untranslated == 0:
            print(f"✅ {lang}: already fully translated!")
            continue
        
        print(f"Translating {untranslated:,} questions → {lang}...", end=" ", flush=True)
        t0 = time.time()
        
        # Process in batches
        BATCH = 1000
        done = 0
        
        while True:
            rows = conn.execute(f"""
                SELECT qb_id, question_en, option_a_en, option_b_en, option_c_en, option_d_en,
                       translated_langs
                FROM question_bank
                WHERE question_{lang} IS NULL OR question_{lang} = ''
                LIMIT {BATCH}
            """).fetchall()
            
            if not rows:
                break
            
            conn.execute("BEGIN")
            try:
                for row in rows:
                    qb_id = row["qb_id"]
                    q_trans = glossary_translate(row["question_en"], lang)
                    a_trans = glossary_translate(row["option_a_en"], lang)
                    b_trans = glossary_translate(row["option_b_en"], lang)
                    c_trans = glossary_translate(row["option_c_en"], lang)
                    d_trans = glossary_translate(row["option_d_en"], lang)
                    
                    # Update translated_langs JSON
                    try:
                        langs_list = json.loads(row["translated_langs"] or "[]")
                    except Exception:
                        langs_list = []
                    if lang not in langs_list:
                        langs_list.append(lang)
                    
                    conn.execute(f"""
                        UPDATE question_bank
                        SET question_{lang}=?, option_a_{lang}=?, option_b_{lang}=?,
                            option_c_{lang}=?, option_d_{lang}=?, translated_langs=?
                        WHERE qb_id=?
                    """, (q_trans, a_trans, b_trans, c_trans, d_trans,
                          json.dumps(langs_list), qb_id))
                conn.commit()
            except Exception as e:
                conn.rollback()
                print(f"Error: {e}")
                break
            
            done += len(rows)
        
        final = conn.execute(f"""
            SELECT COUNT(*) FROM question_bank
            WHERE question_{lang} IS NOT NULL AND question_{lang} != ''
        """).fetchone()[0]
        pct = round(final / total * 100, 1)
        print(f"{final:,}/{total:,} ({pct}%) — {time.time()-t0:.1f}s")
    
    print("\n" + "="*60)
    print("TRANSLATION COMPLETE — Final Coverage:")
    print("="*60)
    for lang in LANGS:
        count = conn.execute(f"""
            SELECT COUNT(*) FROM question_bank
            WHERE question_{lang} IS NOT NULL AND question_{lang} != ''
        """).fetchone()[0]
        pct = round(count / total * 100, 1)
        status = "✅" if pct >= 99 else "⚠️"
        print(f"  {status} {lang}: {count:,} / {total:,} ({pct}%)")
    
    conn.close()


if __name__ == "__main__":
    translate_all_questions()
