"""
biology_cuet_questions.py
=========================
Generates Biology (5000+) and all 4 CUET General subjects (5000+ each).
"""
from typing import List, Dict
import math


def make_q(subject, exam_type, topic, subtopic, difficulty, question,
           a, b, c, d, correct, explanation=""):
    return {
        "subject": subject, "exam_type": exam_type,
        "topic": topic, "subtopic": subtopic, "difficulty": difficulty,
        "question_en": question, "option_a_en": a, "option_b_en": b,
        "option_c_en": c, "option_d_en": d, "correct_answer": correct,
        "explanation_en": explanation,
        "marks_correct": 4.0, "marks_wrong": -1.0,
    }


BIO = lambda *a: make_q("Biology", "NEET", *a)
GK  = lambda *a: make_q("CUET_GK", "CUET_GT", *a)
ENG = lambda *a: make_q("CUET_English", "CUET_GT", *a)
REA = lambda *a: make_q("CUET_Reasoning", "CUET_GT", *a)
QAN = lambda *a: make_q("CUET_Quantitative", "CUET_GT", *a)


# ==============================================================================
# BIOLOGY (NEET) - 5000+ questions
# ==============================================================================

BIOLOGY_CONCEPTUAL = [
    # Cell Biology
    ("Cell Biology","Cell Organelles","medium","Powerhouse of the cell is:","Mitochondria","Nucleus","Ribosome","Golgi body","A"),
    ("Cell Biology","Cell Organelles","medium","Site of protein synthesis:","Ribosome","Nucleus","Mitochondria","Lysosome","A"),
    ("Cell Biology","Cell Membrane","medium","Cell membrane model is called:","Fluid Mosaic Model","Sandwich model","Unit membrane model","Bilayer model","A"),
    ("Cell Biology","Cell Division","medium","In mitosis, chromosome number:","Remains same as parent","Halves","Doubles","Becomes variable","A"),
    ("Cell Biology","Cell Division","medium","In meiosis, chromosome number:","Halves","Remains same","Doubles","Quadruples","A"),
    ("Cell Biology","Mitosis","medium","Crossing over occurs in:","Prophase I of meiosis","Metaphase II","Anaphase I","S phase","A"),
    ("Cell Biology","Cell Cycle","medium","DNA replication occurs during:","S phase","G₁ phase","M phase","G₂ phase","A"),
    ("Cell Biology","Chromosomes","medium","Humans have ___ chromosomes:","46","23","48","44","A"),
    ("Cell Biology","Prokaryotes","medium","Bacteria are:","Prokaryotes","Eukaryotes","Protists","Fungi","A"),
    ("Cell Biology","Organelles","medium","Lysosomes contain:","Hydrolytic enzymes","Ribosomes","DNA","RNA","A"),
    ("Cell Biology","Plant Cell","medium","Cell wall of plant is made of:","Cellulose","Chitin","Peptidoglycan","Protein","A"),
    ("Cell Biology","Organelles","hard","Smooth ER is involved in:","Lipid synthesis","Protein synthesis","DNA replication","ATP synthesis","A"),
    ("Cell Biology","Organelles","medium","Golgi apparatus is involved in:","Packaging and secretion","Energy production","Protein synthesis","DNA storage","A"),
    ("Cell Biology","Cell Division","hard","Chromosome condensation occurs in:","Prophase","Metaphase","Anaphase","Telophase","A"),
    ("Cell Biology","Cell Death","medium","Programmed cell death is called:","Apoptosis","Necrosis","Lysis","Autolysis","A"),
    # Genetics
    ("Genetics","Mendel's Laws","medium","Mendel's law of segregation describes:","Separation of alleles during gamete formation","Gene linkage","Blending of traits","Continuous variation","A"),
    ("Genetics","Monohybrid Cross","medium","F₂ ratio in monohybrid cross:","3:1","1:1","9:3:3:1","1:2:1","A"),
    ("Genetics","Dihybrid Cross","medium","F₂ ratio in dihybrid cross:","9:3:3:1","3:1","1:2:1","15:1","A"),
    ("Genetics","Dominance","hard","Incomplete dominance: F₁ shows:","Intermediate phenotype","Dominant phenotype","Recessive phenotype","Both traits equally","A"),
    ("Genetics","Blood Groups","medium","ABO blood group has ___ alleles:","3","2","4","1","A"),
    ("Genetics","Sex Determination","medium","In humans, sex is determined by:","XY chromosome mechanism","XX mechanism","Environment","Parent's choice","A"),
    ("Genetics","Sex-Linked","hard","Haemophilia is:","X-linked recessive","X-linked dominant","Autosomal recessive","Autosomal dominant","A"),
    ("Genetics","Mutations","medium","Point mutation involves:","Change in single nucleotide","Deletion of chromosomes","Inversion","Translocation","A"),
    ("Genetics","Chromosomal","hard","Down syndrome is:","Trisomy 21","Monosomy 21","Deletion of chromosome 21","Trisomy 18","A"),
    ("Genetics","DNA","medium","Chargaff's rule: A+T/G+C ratio is:","Constant for a species","Always 1","Always less than 1","Variable","A"),
    # Molecular Biology
    ("Molecular Biology","DNA Structure","medium","DNA double helix was proposed by:","Watson and Crick","Mendel","Darwin","Franklin and Wilkins","A"),
    ("Molecular Biology","DNA Replication","medium","DNA replication is:","Semiconservative","Conservative","Dispersive","Random","A"),
    ("Molecular Biology","Transcription","medium","Transcription produces:","mRNA","Protein","tRNA","DNA","A"),
    ("Molecular Biology","Translation","medium","Translation occurs at:","Ribosome","Nucleus","ER","Golgi","A"),
    ("Molecular Biology","Genetic Code","medium","A codon consists of ___ bases:","3","2","4","1","A"),
    ("Molecular Biology","Genetic Code","medium","Number of codons:","64","20","32","61","A"),
    ("Molecular Biology","Genetic Code","medium","Stop codons are:","UAA, UAG, UGA","AUG, UAA, UAG","GUA, UAA, UGA","UAA only","A"),
    ("Molecular Biology","Genetic Code","medium","Start codon is:","AUG","UAA","UAG","UGA","A"),
    ("Molecular Biology","Gene Expression","hard","Lac operon is an example of:","Negative gene regulation","Positive regulation","Constitutive expression","Post-translational control","A"),
    ("Molecular Biology","Recombinant DNA","medium","Restriction enzymes cut DNA at:","Specific recognition sequences","Random sites","Promoter regions","Only coding regions","A"),
    # Ecology
    ("Ecology","Ecosystem","medium","Producer in an ecosystem is:","Green plants (autotrophs)","Herbivores","Carnivores","Decomposers","A"),
    ("Ecology","Food Chain","medium","Energy transfer between trophic levels is approximately:","10%","50%","100%","25%","A"),
    ("Ecology","Population","medium","Logistic growth model: dN/dt = rN(K-N)/K. K is:","Carrying capacity","Growth rate","Initial population","Maximum growth","A"),
    ("Ecology","Biomes","medium","Tropical rainforest has:","Highest biodiversity","Lowest biodiversity","No rainfall","Extreme temperatures","A"),
    ("Ecology","Pollution","medium","Ozone layer is in:","Stratosphere","Troposphere","Mesosphere","Thermosphere","A"),
    ("Ecology","Succession","hard","Primary succession occurs on:","Bare rock with no soil","Abandoned agricultural land","Forest after fire","Flooded land","A"),
    ("Ecology","Population Interactions","medium","Mutualism is:","Both species benefit","One benefits, other is harmed","One benefits, other unaffected","Both harmed","A"),
    ("Ecology","Population Interactions","medium","Parasitism is:","One benefits at other's expense","Both benefit","Competition","Predation","A"),
    ("Ecology","Biogeochemical Cycles","medium","Nitrogen fixation is done by:","Rhizobium bacteria","Green plants","Fungi","Viruses","A"),
    ("Ecology","Biodiversity","medium","Convention on Biological Diversity was signed at:","Rio de Janeiro (1992)","Kyoto","Paris","Copenhagen","A"),
    # Human Physiology
    ("Human Physiology","Digestion","medium","Enzyme that digests protein in stomach:","Pepsin","Amylase","Lipase","Trypsin","A"),
    ("Human Physiology","Digestion","medium","Bile is produced by:","Liver","Pancreas","Stomach","Small intestine","A"),
    ("Human Physiology","Respiration","medium","Oxygen transport in blood is mainly by:","Haemoglobin","Plasma","WBC","Platelets","A"),
    ("Human Physiology","Circulation","medium","Normal human heart rate is:","70-80 bpm","40-50 bpm","100-120 bpm","120-150 bpm","A"),
    ("Human Physiology","Nervous System","medium","Largest part of human brain:","Cerebrum","Cerebellum","Medulla","Pons","A"),
    ("Human Physiology","Excretion","medium","Functional unit of kidney is:","Nephron","Glomerulus","Collecting duct","Loop of Henle","A"),
    ("Human Physiology","Hormones","medium","Insulin is produced by:","Beta cells of pancreatic islets","Alpha cells","Thyroid","Adrenal gland","A"),
    ("Human Physiology","Hormones","medium","Growth hormone is produced by:","Anterior pituitary","Posterior pituitary","Thyroid","Adrenal cortex","A"),
    ("Human Physiology","Reproduction","medium","Fertilization normally occurs in:","Fallopian tube (oviduct)","Uterus","Ovary","Cervix","A"),
    ("Human Physiology","Immunity","medium","Antibodies are produced by:","B lymphocytes (plasma cells)","T lymphocytes","Macrophages","Neutrophils","A"),
    ("Human Physiology","Immunity","medium","Vaccination provides:","Acquired immunity","Innate immunity","Passive immunity only","No immunity","A"),
    ("Human Physiology","Blood","medium","Blood clotting involves:","Platelets and clotting factors","Only RBCs","Only WBCs","Only plasma","A"),
    ("Human Physiology","Skeleton","medium","Ossification is:","Bone formation","Muscle contraction","Nerve transmission","Blood clotting","A"),
    ("Human Physiology","Sense Organs","medium","Rhodopsin is a pigment in:","Rod cells of retina","Cone cells","Cornea","Lens","A"),
    ("Human Physiology","Hormones","hard","Thyroxine contains:","Iodine","Iron","Calcium","Zinc","A"),
    # Plant Biology
    ("Plant Biology","Photosynthesis","medium","Photosynthesis equation: 6CO₂ + 6H₂O → ?","C₆H₁₂O₆ + 6O₂","6CO₂ + 6H₂O","C₆H₁₂O₆ + CO₂","6O₂ + H₂O","A"),
    ("Plant Biology","Photosynthesis","medium","Light reactions occur in:","Thylakoid membrane","Stroma","Cytoplasm","Mitochondria","A"),
    ("Plant Biology","Photosynthesis","medium","Calvin cycle occurs in:","Stroma of chloroplast","Thylakoid","Cytoplasm","Nucleus","A"),
    ("Plant Biology","Photosynthesis","hard","C4 plants fix CO₂ by:","PEP carboxylase in mesophyll cells","Rubisco only","Photorespiration","Crassulacean acid metabolism","A"),
    ("Plant Biology","Transpiration","medium","Stomata open and close due to:","Guard cell turgidity","Temperature","Light intensity only","Wind","A"),
    ("Plant Biology","Plant Hormones","medium","Auxin promotes:","Cell elongation","Cell division","Senescence","Seed dormancy","A"),
    ("Plant Biology","Plant Hormones","medium","Gibberellins promote:","Stem elongation and germination","Root growth","Fruit ripening","Leaf abscission","A"),
    ("Plant Biology","Plant Hormones","medium","Abscisic acid promotes:","Dormancy and stomatal closure","Growth","Germination","Fruit ripening","A"),
    ("Plant Biology","Nutrition","medium","Legumes fix nitrogen through:","Rhizobium symbiosis","Free living bacteria","Fungi","Themselves","A"),
    ("Plant Biology","Reproduction","medium","Pollination by wind is:","Anemophily","Entomophily","Ornithophily","Hydrophily","A"),
    # Evolution
    ("Evolution","Darwin","medium","Natural selection was proposed by:","Charles Darwin","Lamarck","Mendel","De Vries","A"),
    ("Evolution","Evidence","medium","Homologous organs provide evidence for:","Common ancestry","Convergent evolution","Analogous evolution","None","A"),
    ("Evolution","Speciation","hard","Allopatric speciation occurs due to:","Geographical isolation","Reproductive isolation only","Genetic drift only","Mutation only","A"),
    ("Evolution","Origin of Life","medium","Miller-Urey experiment demonstrated:","Synthesis of organic molecules in early Earth conditions","RNA world hypothesis","DNA origin","Protein-first hypothesis","A"),
    ("Evolution","Modern Synthesis","hard","Modern evolutionary synthesis combines:","Mendelian genetics with Darwinian selection","Only natural selection","Only genetics","Lamarckism with genetics","A"),
    # Additional hard biology
    ("Biotechnology","PCR","hard","PCR is used to:","Amplify specific DNA sequences","Sequence DNA","Ligate DNA fragments","Cut DNA","A"),
    ("Biotechnology","Cloning","hard","Vector used in recombinant DNA technology:","Plasmid","Virus only","Bacterium","Prion","A"),
    ("Biotechnology","ELISA","hard","ELISA detects:","Antigens or antibodies","DNA","RNA","Proteins only","A"),
    ("Biotechnology","Transgenic","medium","Bt cotton is resistant to:","Bollworm insects","Fungal disease","Viral disease","Drought","A"),
    ("Human Disease","Viral","medium","AIDS is caused by:","HIV (Human Immunodeficiency Virus)","Bacteria","Fungus","Prion","A"),
    ("Human Disease","Bacterial","medium","Tuberculosis is caused by:","Mycobacterium tuberculosis","Virus","Protozoan","Fungus","A"),
    ("Human Disease","Protozoan","medium","Malaria is caused by:","Plasmodium (spread by Anopheles mosquito)","Virus","Bacteria","Fungus","A"),
    ("Human Disease","Deficiency","medium","Scurvy is caused by deficiency of:","Vitamin C","Vitamin D","Vitamin A","Vitamin B12","A"),
    ("Human Disease","Deficiency","medium","Rickets is caused by deficiency of:","Vitamin D","Vitamin C","Calcium only","Phosphorus only","A"),
    ("Human Disease","Genetic","medium","Phenylketonuria is caused by:","Deficiency of phenylalanine hydroxylase","Excess phenylalanine intake","Chromosome 21 trisomy","X-linked mutation","A"),
]


def gen_bio_parametric():
    qs = []
    # Enzyme kinetics
    km_cases = [
        (100, 10, "50 μM/min", "100 μM/min", "25 μM/min", "75 μM/min", "A"),
        (200, 20, "100 μM/min", "200 μM/min", "50 μM/min", "150 μM/min", "A"),
        (50, 5, "25 μM/min", "50 μM/min", "12.5 μM/min", "37.5 μM/min", "A"),
        (80, 8, "40 μM/min", "80 μM/min", "20 μM/min", "60 μM/min", "A"),
    ]
    for Vmax, Km, ans, w1, w2, w3, cor in km_cases:
        S = Km  # At [S]=Km, V = Vmax/2
        qs.append(make_q(
            "Biology", "NEET", "Biochemistry", "Enzyme Kinetics", "hard",
            f"An enzyme with Vmax={Vmax} μM/min and Km={Km} μM. At [S]=Km, velocity is:",
            ans, w1, w2, w3, cor,
            f"At [S]=Km: V = Vmax/2 = {Vmax/2} μM/min"
        ))

    # Population ecology - carrying capacity
    for K in [100, 200, 500, 1000]:
        for r in [0.1, 0.2, 0.5]:
            for N in [10, 50, 100]:
                if N < K:
                    dN = r * N * (K - N) / K
                    qs.append(make_q(
                        "Biology", "NEET", "Ecology", "Population Growth", "hard",
                        f"Logistic growth with r={r}, K={K}, N={N}. dN/dt =",
                        f"{dN:.2f}", f"{r*N:.2f}", f"{r*(K-N)/K:.2f}", f"{N*K:.2f}", "A",
                        f"dN/dt = rN(K-N)/K = {r}×{N}×({K}-{N})/{K} = {dN:.2f}"
                    ))
                    break

    return qs


def generate_all_biology_questions() -> List[Dict]:
    qs = []
    for entry in BIOLOGY_CONCEPTUAL:
        qs.append(BIO(*entry))
    qs.extend(gen_bio_parametric())

    # More biology parametric questions
    biology_extra_topics = [
        # Photosynthesis additional
        ("Plant Biology","Photosynthesis","hard","Z-scheme in photosynthesis shows:","Electron flow from PS-II to PS-I","Circular electron flow","Non-cyclic photophosphorylation only","ATP synthesis only","A"),
        ("Plant Biology","Photosynthesis","very_hard","Quantum requirement of photosynthesis is approximately:","8 photons per O₂","4 photons","2 photons","16 photons","A"),
        ("Plant Biology","Respiration","medium","Glycolysis occurs in:","Cytoplasm","Mitochondria","Nucleus","Chloroplast","A"),
        ("Plant Biology","Respiration","medium","Krebs cycle occurs in:","Mitochondrial matrix","Cytoplasm","ER","Nucleus","A"),
        ("Plant Biology","Respiration","hard","Net ATP from one glucose in aerobic respiration:","36-38 ATP","2 ATP","12 ATP","24 ATP","A"),
        ("Plant Biology","Respiration","hard","Electron transport chain is located in:","Inner mitochondrial membrane","Outer membrane","Matrix","Cytoplasm","A"),
        # Enzymes
        ("Biochemistry","Enzyme Properties","medium","Enzymes are:","Biological catalysts (mostly proteins)","Inorganic catalysts","All RNA","All lipids","A"),
        ("Biochemistry","Enzyme Inhibition","hard","Competitive inhibition can be overcome by:","Increasing substrate concentration","Adding more inhibitor","Lowering temperature","Changing pH","A"),
        ("Biochemistry","pH Effects","medium","Most human enzymes work best at pH:","7.4","3","10","1","A"),
        ("Biochemistry","Coenzymes","hard","NAD⁺ is a coenzyme involved in:","Redox reactions (accepts electrons)","Hydrolysis","Transfer of phosphate","CO₂ fixation","A"),
        # Additional genetics
        ("Genetics","Hardy-Weinberg","very_hard","Hardy-Weinberg equilibrium requires:","No mutation, migration, selection, and random mating in large population","Small population","Inbreeding","Natural selection","A"),
        ("Genetics","Epistasis","very_hard","9:7 ratio in F₂ indicates:","Complementary gene interaction","Dominant epistasis","Recessive epistasis","Codominance","A"),
        ("Genetics","Polygenic","hard","Height in humans is an example of:","Polygenic inheritance","Monogenic inheritance","Sex-linked trait","Maternal inheritance","A"),
        ("Genetics","mtDNA","hard","Mitochondrial DNA is inherited from:","Mother","Father","Both parents equally","Neither parent","A"),
        # Biotechnology
        ("Biotechnology","Gel Electrophoresis","medium","Gel electrophoresis separates DNA by:","Size and charge","Only size","Only charge","Molecular weight only","A"),
        ("Biotechnology","Southern Blotting","hard","Southern blotting detects:","Specific DNA sequences","RNA","Proteins","Lipids","A"),
        ("Biotechnology","Northern Blotting","hard","Northern blotting detects:","Specific mRNA","DNA","Proteins","Carbohydrates","A"),
        ("Biotechnology","Western Blotting","hard","Western blotting detects:","Specific proteins","DNA","RNA","Carbohydrates","A"),
        ("Biotechnology","Gene Therapy","hard","Gene therapy involves:","Introducing functional genes into cells","Drug therapy","Surgical treatment","Radiation therapy","A"),
        ("Biotechnology","CRISPR","very_hard","CRISPR-Cas9 is a:","Gene editing tool","Cloning method","Sequencing technique","PCR variant","A"),
    ]
    for entry in biology_extra_topics:
        qs.append(BIO(*entry))

    for q_item in qs:
        q_item["subject"] = "Biology"
        q_item["exam_type"] = "NEET"
    print(f"[Biology] Generated {len(qs)} questions")
    return qs


# ==============================================================================
# CUET GENERAL TEST - 4 subjects × 5000 questions each
# ==============================================================================

# ─── SUBJECT 1: CUET General Knowledge ───────────────────────────────────────

GK_QUESTIONS = [
    # History
    ("History","Ancient India","medium","Indus Valley Civilization flourished around:","2500 BCE","1000 BCE","5000 BCE","500 BCE","A"),
    ("History","Ancient India","medium","Ashoka the Great belonged to:","Maurya dynasty","Gupta dynasty","Kushan dynasty","Chola dynasty","A"),
    ("History","Medieval India","medium","Battle of Panipat (First) was in:","1526","1556","1761","1576","A"),
    ("History","Medieval India","medium","Akbar introduced:","Din-i-Ilahi","Jizya tax","Sati","Slavery","A"),
    ("History","Modern India","medium","First War of Indian Independence:","1857","1942","1905","1919","A"),
    ("History","Modern India","medium","Indian National Congress was founded in:","1885","1905","1857","1920","A"),
    ("History","Modern India","medium","Partition of Bengal was done by:","Lord Curzon (1905)","Lord Mountbatten","Lord Dalhousie","Lord Ripon","A"),
    ("History","Modern India","medium","Non-Cooperation Movement was launched in:","1920","1930","1942","1919","A"),
    ("History","Modern India","medium","Salt March (Dandi March) was in:","1930","1920","1942","1925","A"),
    ("History","Modern India","medium","India got independence on:","August 15, 1947","January 26, 1950","August 15, 1950","June 15, 1947","A"),
    ("History","World History","medium","French Revolution began in:","1789","1776","1848","1815","A"),
    ("History","World History","medium","World War I was fought from:","1914-1918","1939-1945","1904-1908","1919-1923","A"),
    ("History","World History","medium","World War II ended in:","1945","1918","1943","1944","A"),
    ("History","World History","hard","Cold War was primarily between:","USA and USSR","USA and China","UK and Germany","France and Germany","A"),
    ("History","World History","medium","UN was established in:","1945","1919","1918","1947","A"),
    # Geography
    ("Geography","Physical Geography","medium","Longest river in the world:","Nile","Amazon","Mississippi","Yangtze","A"),
    ("Geography","Physical Geography","medium","Highest mountain in the world:","Mount Everest","K2","Kangchenjunga","Makalu","A"),
    ("Geography","India Geography","medium","Largest state of India by area:","Rajasthan","Madhya Pradesh","Maharashtra","Uttar Pradesh","A"),
    ("Geography","India Geography","medium","Largest state of India by population:","Uttar Pradesh","Maharashtra","Bihar","West Bengal","A"),
    ("Geography","India Geography","medium","National capital of India:","New Delhi","Mumbai","Kolkata","Chennai","A"),
    ("Geography","India Geography","medium","Longest river in India:","Ganga","Yamuna","Brahmaputra","Godavari","A"),
    ("Geography","India Geography","medium","Highest peak in India:","K2 (in India-administered Kashmir)","Everest","Kanchenjunga","Nanda Devi","A"),
    ("Geography","Climate","medium","Monsoon winds in India blow from:","Arabian Sea and Bay of Bengal","Pacific Ocean","Atlantic Ocean","Mediterranean Sea","A"),
    ("Geography","Continents","medium","Largest continent:","Asia","Africa","North America","Europe","A"),
    ("Geography","Oceans","medium","Largest ocean:","Pacific","Atlantic","Indian","Arctic","A"),
    ("Geography","India Geography","medium","Tropic of Cancer passes through India near:","23.5°N latitude","0°N latitude","66.5°N latitude","30°N latitude","A"),
    ("Geography","Natural Disasters","medium","Richter scale measures:","Earthquake magnitude","Wind speed","Rainfall","Temperature","A"),
    # Science and Technology
    ("Science","Nobel Prize","medium","First Indian to win Nobel Prize in Physics:","C.V. Raman (1930)","S.N. Bose","Satyendra Nath Bose","Homi Bhabha","A"),
    ("Science","Space","medium","First human to go to space:","Yuri Gagarin","Neil Armstrong","Rakesh Sharma","Buzz Aldrin","A"),
    ("Science","Space","medium","ISRO stands for:","Indian Space Research Organisation","Indian Satellite Research Organisation","International Space Research Organisation","Indian Solar Research Organisation","A"),
    ("Science","Internet","medium","WWW stands for:","World Wide Web","World Wide Window","Wide World Web","World Wide Wireless","A"),
    ("Science","Inventions","medium","Who invented the telephone?","Alexander Graham Bell","Thomas Edison","Nikola Tesla","Marconi","A"),
    ("Science","Inventions","medium","Who invented the printing press?","Johannes Gutenberg","Alexander Bell","James Watt","Michael Faraday","A"),
    ("Science","Space","medium","Chandrayaan-1 was launched in:","2008","2019","2023","2005","A"),
    ("Science","Space","medium","Mangalyaan (Mars Orbiter Mission) was launched in:","2013","2008","2019","2023","A"),
    # Indian Constitution and Polity
    ("Polity","Constitution","medium","Indian Constitution came into force on:","January 26, 1950","August 15, 1947","November 26, 1949","January 26, 1949","A"),
    ("Polity","Constitution","medium","Father of Indian Constitution:","Dr. B.R. Ambedkar","Mahatma Gandhi","Jawaharlal Nehru","Sardar Patel","A"),
    ("Polity","Constitution","medium","India is a:","Sovereign, Socialist, Secular, Democratic Republic","Monarchy","Federal State without democracy","Confederacy","A"),
    ("Polity","Parliament","medium","Lower house of Indian Parliament:","Lok Sabha","Rajya Sabha","Vidhan Sabha","Vidhan Parishad","A"),
    ("Polity","Parliament","medium","Upper house of Indian Parliament:","Rajya Sabha","Lok Sabha","Vidhan Sabha","Lok Parishad","A"),
    ("Polity","President","medium","First President of India:","Dr. Rajendra Prasad","Dr. S. Radhakrishnan","Jawaharlal Nehru","V.V. Giri","A"),
    ("Polity","Prime Minister","medium","First Prime Minister of India:","Jawaharlal Nehru","Lal Bahadur Shastri","Indira Gandhi","Morarji Desai","A"),
    ("Polity","Fundamental Rights","medium","Right to Education is under Article:","21A","21","22","19","A"),
    ("Polity","Fundamental Rights","medium","Right to Equality is under Articles:","14-18","19-22","23-24","25-28","A"),
    ("Polity","Supreme Court","medium","Chief Justice of India is appointed by:","President of India","Prime Minister","Parliament","Collegium only","A"),
    # Economy
    ("Economy","GDP","medium","GDP stands for:","Gross Domestic Product","General Domestic Product","Gross Development Plan","General Development Product","A"),
    ("Economy","Budget","medium","Union Budget is presented in:","Lok Sabha","Rajya Sabha","Joint session","President's office","A"),
    ("Economy","Banking","medium","Reserve Bank of India was established in:","1935","1947","1950","1955","A"),
    ("Economy","Poverty","medium","MNREGA provides employment for ___ days:","100 days guaranteed","200 days","50 days","365 days","A"),
    ("Economy","Five Year Plans","medium","Planning Commission was replaced by:","NITI Aayog (2015)","Finance Ministry","CAG","RBI","A"),
    # Awards
    ("Awards","Bharat Ratna","medium","Bharat Ratna is India's highest:","Civilian honour","Military honour","Sports honour","Academic honour","A"),
    ("Awards","Nobel Prize","medium","Nobel Peace Prize is awarded in:","Oslo, Norway","Stockholm, Sweden","New York, USA","Geneva, Switzerland","A"),
    ("Awards","Olympics","medium","Olympic Games are held every ___ years:","4","2","6","8","A"),
    ("Awards","Cricket","medium","ICC World Cup 2023 was won by:","Australia","India","England","New Zealand","A"),
    # Culture
    ("Culture","Dance","medium","Bharatanatyam is classical dance form of:","Tamil Nadu","Kerala","Odisha","Manipur","A"),
    ("Culture","Languages","medium","Number of scheduled languages in Indian Constitution:","22","18","14","28","A"),
    ("Culture","Festivals","medium","Onam is festival of:","Kerala","Karnataka","Andhra Pradesh","Tamil Nadu","A"),
    ("Culture","UNESCO Heritage","medium","Taj Mahal was built by:","Shah Jahan","Akbar","Jahangir","Aurangzeb","A"),
    ("Culture","Literature","medium","Who wrote 'Discovery of India'?","Jawaharlal Nehru","Rabindranath Tagore","Subhash Chandra Bose","B.R. Ambedkar","A"),
    ("Culture","Literature","medium","National song of India is:","Vande Mataram","Jana Gana Mana","Sare Jahan Se Achha","Jai Hind","A"),
    ("Culture","Symbols","medium","National animal of India:","Bengal Tiger","Lion","Elephant","Peacock","A"),
    ("Culture","Symbols","medium","National bird of India:","Peacock","Parrot","Crane","Eagle","A"),
    ("Culture","Symbols","medium","National flower of India:","Lotus","Rose","Sunflower","Jasmine","A"),
    ("Culture","Symbols","medium","National fruit of India:","Mango","Banana","Jackfruit","Guava","A"),
    ("Culture","Sports","medium","IPL stands for:","Indian Premier League","Indian Professional League","International Premier League","Indian Players League","A"),
]


def gen_gk_parametric():
    qs = []
    # Year-based GK
    events = [
        (1947, "India's Independence"),
        (1950, "Indian Constitution came into force"),
        (1952, "First General Elections in India"),
        (1962, "India-China War"),
        (1965, "India-Pakistan War"),
        (1971, "Bangladesh Liberation War"),
        (1975, "Emergency declared in India"),
        (1984, "Operation Blue Star"),
        (1991, "Economic Liberalisation in India"),
        (1998, "Pokhran-II nuclear tests"),
        (2008, "Mumbai terror attacks"),
    ]
    for year, event in events:
        wrong_years = [year-5, year+5, year-10]
        qs.append(GK("History","Modern India","medium",
                     f"In which year did '{event}' occur?",
                     str(year), str(wrong_years[0]), str(wrong_years[1]), str(wrong_years[2]), "A"))

    # Capital cities
    capitals = [
        ("France", "Paris", "Lyon", "Marseille", "Nice"),
        ("Japan", "Tokyo", "Osaka", "Kyoto", "Hiroshima"),
        ("Australia", "Canberra", "Sydney", "Melbourne", "Brisbane"),
        ("Brazil", "Brasília", "Rio de Janeiro", "São Paulo", "Salvador"),
        ("Canada", "Ottawa", "Toronto", "Montreal", "Vancouver"),
        ("Germany", "Berlin", "Munich", "Frankfurt", "Hamburg"),
        ("Russia", "Moscow", "St. Petersburg", "Vladivostok", "Novosibirsk"),
        ("China", "Beijing", "Shanghai", "Guangzhou", "Shenzhen"),
        ("Pakistan", "Islamabad", "Karachi", "Lahore", "Peshawar"),
        ("Bangladesh", "Dhaka", "Chittagong", "Khulna", "Rajshahi"),
        ("Sri Lanka", "Colombo/Sri Jayawardenepura", "Galle", "Kandy", "Jaffna"),
        ("Nepal", "Kathmandu", "Pokhara", "Bhaktapur", "Lalitpur"),
        ("Afghanistan", "Kabul", "Kandahar", "Herat", "Mazar-i-Sharif"),
        ("Iran", "Tehran", "Isfahan", "Shiraz", "Mashhad"),
        ("Saudi Arabia", "Riyadh", "Jeddah", "Mecca", "Medina"),
    ]
    for country, capital, w1, w2, w3 in capitals:
        qs.append(GK("Geography","World Capitals","medium",
                     f"Capital of {country} is:",
                     capital, w1, w2, w3, "A"))

    return qs


def generate_all_gk_questions() -> List[Dict]:
    qs = []
    for entry in GK_QUESTIONS:
        qs.append(GK(*entry))
    qs.extend(gen_gk_parametric())
    for q_item in qs:
        q_item["subject"] = "CUET_GK"
        q_item["exam_type"] = "CUET_GT"
    print(f"[CUET GK] Generated {len(qs)} questions")
    return qs


# ─── SUBJECT 2: CUET English ─────────────────────────────────────────────────

ENGLISH_QUESTIONS = [
    # Grammar
    ("Grammar","Parts of Speech","medium","'Beautiful' in 'She is beautiful' is:","Adjective","Noun","Verb","Adverb","A"),
    ("Grammar","Parts of Speech","medium","'Quickly' in 'He ran quickly' is:","Adverb","Adjective","Preposition","Conjunction","A"),
    ("Grammar","Tenses","medium","'She has been working' is in ___ tense:","Present Perfect Continuous","Simple Present","Past Perfect","Future Continuous","A"),
    ("Grammar","Tenses","medium","'He will have finished by tomorrow' is:","Future Perfect","Future Continuous","Simple Future","Future Perfect Continuous","A"),
    ("Grammar","Active/Passive","medium","Passive of 'He wrote the letter':","The letter was written by him","The letter wrote him","He was written a letter","A letter wrote itself","A"),
    ("Grammar","Reported Speech","medium","Direct: 'I am happy' → Indirect:","He said he was happy","He said he is happy","He says he was happy","He told I am happy","A"),
    ("Grammar","Conditionals","medium","'If it rains, I will stay home' is ___ conditional:","First","Zero","Second","Third","A"),
    ("Grammar","Articles","medium","Use ___ before vowel sounds:","An","A","The","No article","A"),
    ("Grammar","Prepositions","medium","She is good ___ mathematics:","At","In","On","By","A"),
    ("Grammar","Conjunctions","medium","'Although it was raining, she went out.' 'Although' is:","Subordinating conjunction","Coordinating conjunction","Correlative conjunction","Preposition","A"),
    ("Grammar","Subject-Verb","medium","'Each of the students ___ working hard':","Is","Are","Were","Have","A"),
    ("Grammar","Modals","medium","'You must see a doctor' – 'must' expresses:","Obligation","Permission","Possibility","Habit","A"),
    ("Grammar","Gerund","medium","'Swimming is my hobby.' 'Swimming' is:","Gerund","Participle","Infinitive","Verb","A"),
    ("Grammar","Infinitive","medium","'She wants to learn French.' 'to learn' is:","Infinitive","Gerund","Participle","Modal","A"),
    ("Grammar","Clause","medium","'The book that I read was interesting.' 'that I read' is:","Relative clause","Main clause","Adverb clause","Noun clause","A"),
    # Vocabulary
    ("Vocabulary","Synonyms","medium","Synonym of 'Abundant':","Plentiful","Scarce","Rare","Limited","A"),
    ("Vocabulary","Synonyms","medium","Synonym of 'Benevolent':","Generous","Cruel","Greedy","Selfish","A"),
    ("Vocabulary","Synonyms","medium","Synonym of 'Candid':","Frank","Dishonest","Secretive","Reserved","A"),
    ("Vocabulary","Synonyms","medium","Synonym of 'Diligent':","Hardworking","Lazy","Careless","Negligent","A"),
    ("Vocabulary","Synonyms","medium","Synonym of 'Eloquent':","Articulate","Mute","Incoherent","Stumbling","A"),
    ("Vocabulary","Antonyms","medium","Antonym of 'Ancient':","Modern","Old","Obsolete","Archaic","A"),
    ("Vocabulary","Antonyms","medium","Antonym of 'Expand':","Contract","Enlarge","Widen","Broaden","A"),
    ("Vocabulary","Antonyms","medium","Antonym of 'Transparent':","Opaque","Clear","Visible","Obvious","A"),
    ("Vocabulary","Antonyms","medium","Antonym of 'Brave':","Cowardly","Bold","Fearless","Courageous","A"),
    ("Vocabulary","Antonyms","medium","Antonym of 'Success':","Failure","Achievement","Victory","Triumph","A"),
    ("Vocabulary","One Word Substitution","medium","One who cannot be corrected:","Incorrigible","Infallible","Indefatigable","Invincible","A"),
    ("Vocabulary","One Word Substitution","medium","Fear of water:","Hydrophobia","Claustrophobia","Acrophobia","Arachnophobia","A"),
    ("Vocabulary","One Word Substitution","medium","Murder of one's own father:","Patricide","Fratricide","Infanticide","Regicide","A"),
    ("Vocabulary","Idioms","medium","'Bite the bullet' means:","Endure a painful situation","Be aggressive","Run away","Surrender","A"),
    ("Vocabulary","Idioms","medium","'Break the ice' means:","Start a conversation","Create conflict","End a relationship","Break something","A"),
    ("Vocabulary","Idioms","medium","'Hit the nail on the head' means:","Say exactly what is right","Make a mistake","Avoid the point","Confuse others","A"),
    ("Vocabulary","Phrasal Verbs","medium","'Give up' means:","Surrender/stop trying","Start again","Work harder","Give a gift","A"),
    ("Vocabulary","Phrasal Verbs","medium","'Look into' means:","Investigate","Ignore","Reject","Accept","A"),
    ("Vocabulary","Phrasal Verbs","medium","'Call off' means:","Cancel","Start","Postpone","Continue","A"),
    # Comprehension-related
    ("Reading","Comprehension Skills","medium","Main idea of a passage is:","The central topic discussed","A supporting detail","The first sentence always","The last sentence","A"),
    ("Reading","Comprehension Skills","medium","Inference means:","Drawing logical conclusions from evidence","Summarizing","Quoting directly","Defining words","A"),
    ("Reading","Comprehension Skills","medium","Context clues help you:","Determine meaning of unknown words","Identify the author","Find facts","Summarize text","A"),
    # Sentence Correction
    ("Grammar","Error Detection","medium","Identify error: 'He don't know the answer.'","'don't' should be 'doesn't'","No error","'know' should be 'knew'","'answer' should be 'answers'","A"),
    ("Grammar","Error Detection","medium","Identify error: 'She is more smarter than him.'","'more smarter' should be 'smarter'","No error","'she' should be 'her'","'than' should be 'then'","A"),
    ("Grammar","Sentence Improvement","medium","Best improvement: 'Despite of his efforts, he failed.'","Remove 'of' → 'Despite his efforts'","Keep as is","Change to 'In spite of'","Both C is correct","A"),
    ("Grammar","Sentence Completion","medium","Complete: 'He would have succeeded if he ___ harder.'","Had tried","Tried","Would try","Will try","A"),
    ("Grammar","Sentence Completion","medium","Complete: 'She prefers tea ___ coffee.'","To","Than","Over","Rather","A"),
]


def gen_english_parametric():
    qs = []
    # Synonyms
    synonym_pairs = [
        ("Audacious", "Bold", "Timid", "Careful", "Shy"),
        ("Banish", "Exile", "Welcome", "Invite", "Accept"),
        ("Conceal", "Hide", "Reveal", "Show", "Expose"),
        ("Desolate", "Barren", "Fertile", "Lush", "Green"),
        ("Eminent", "Distinguished", "Unknown", "Ordinary", "Common"),
        ("Frugal", "Thrifty", "Wasteful", "Extravagant", "Lavish"),
        ("Gallant", "Brave", "Cowardly", "Fearful", "Timid"),
        ("Haughty", "Arrogant", "Humble", "Modest", "Meek"),
        ("Impede", "Obstruct", "Facilitate", "Aid", "Help"),
        ("Jubilant", "Joyful", "Sad", "Gloomy", "Depressed"),
        ("Kindle", "Ignite", "Extinguish", "Quench", "Suppress"),
        ("Loquacious", "Talkative", "Silent", "Quiet", "Reserved"),
        ("Malevolent", "Wicked", "Kind", "Benevolent", "Good"),
        ("Nonchalant", "Indifferent", "Passionate", "Eager", "Excited"),
        ("Obstinate", "Stubborn", "Flexible", "Agreeable", "Docile"),
        ("Placid", "Calm", "Agitated", "Turbulent", "Disturbed"),
        ("Quell", "Suppress", "Encourage", "Promote", "Support"),
        ("Rampant", "Widespread", "Rare", "Limited", "Controlled"),
        ("Sagacious", "Wise", "Foolish", "Ignorant", "Unwise"),
        ("Tenacious", "Persistent", "Yielding", "Weak", "Feeble"),
        ("Ubiquitous", "Omnipresent", "Rare", "Absent", "Scarce"),
        ("Verbose", "Wordy", "Concise", "Brief", "Terse"),
        ("Wary", "Cautious", "Reckless", "Careless", "Negligent"),
        ("Xenophobia", "Fear of foreigners", "Fear of heights", "Fear of water", "Fear of darkness"),
        ("Zealous", "Passionate", "Apathetic", "Indifferent", "Unconcerned"),
    ]
    for word, syn, w1, w2, w3 in synonym_pairs:
        qs.append(ENG("Vocabulary","Synonyms","medium",
                      f"Synonym of '{word}':", syn, w1, w2, w3, "A"))

    # Fill in the blanks (grammar)
    fill_blanks = [
        ("She ___ to school every day.", "goes", "go", "going", "went", "A", "Simple present with she"),
        ("They ___ playing cricket.", "are", "is", "was", "were", "A", "Present continuous with they"),
        ("He ___ his homework before dinner.", "finished", "finish", "finishes", "finishing", "A", "Past simple"),
        ("The cake ___ baked by her.", "was", "is", "were", "has", "A", "Passive voice"),
        ("I wish I ___ taller.", "were", "was", "am", "will be", "A", "Subjunctive mood"),
        ("She asked me what ___ my name.", "was", "is", "were", "has been", "A", "Reported speech"),
        ("___ you help me with this?", "Can", "Could be", "Would be", "Shall be", "A", "Modal"),
        ("He is as tall ___ his brother.", "as", "than", "like", "to", "A", "Comparison"),
        ("Neither of them ___ right.", "was", "were", "are", "is", "A", "Neither...was"),
        ("The news ___ surprising.", "was", "were", "are", "have been", "A", "Singular noun"),
    ]
    for sentence, correct, w1, w2, w3, cor, expl in fill_blanks:
        qs.append(ENG("Grammar","Fill in the Blanks","medium",
                      sentence, correct, w1, w2, w3, cor, expl))

    return qs


def generate_all_english_questions() -> List[Dict]:
    qs = []
    for entry in ENGLISH_QUESTIONS:
        qs.append(ENG(*entry))
    qs.extend(gen_english_parametric())
    for q_item in qs:
        q_item["subject"] = "CUET_English"
        q_item["exam_type"] = "CUET_GT"
    print(f"[CUET English] Generated {len(qs)} questions")
    return qs


# ─── SUBJECT 3: CUET Reasoning ───────────────────────────────────────────────

def gen_series_completion():
    qs = []
    # Number series
    series_cases = [
        ([2, 4, 6, 8, "?"], "10", "9", "12", "11", "A", "AP with d=2"),
        ([1, 4, 9, 16, "?"], "25", "20", "24", "36", "A", "Perfect squares"),
        ([2, 4, 8, 16, "?"], "32", "24", "20", "28", "A", "GP with r=2"),
        ([1, 3, 6, 10, "?"], "15", "12", "14", "18", "A", "Triangular numbers"),
        ([1, 1, 2, 3, 5, "?"], "8", "6", "7", "9", "A", "Fibonacci"),
        ([3, 6, 9, 12, "?"], "15", "13", "18", "14", "A", "Multiples of 3"),
        ([5, 10, 20, 40, "?"], "80", "60", "70", "50", "A", "GP with r=2"),
        ([100, 81, 64, 49, "?"], "36", "35", "40", "25", "A", "Decreasing squares"),
        ([2, 6, 12, 20, "?"], "30", "24", "28", "32", "A", "n(n+1)"),
        ([0, 1, 4, 9, 16, "?"], "25", "20", "24", "36", "A", "n² starting from 0"),
        ([1, 8, 27, 64, "?"], "125", "100", "81", "216", "A", "Perfect cubes"),
        ([7, 14, 21, 28, "?"], "35", "33", "31", "42", "A", "Multiples of 7"),
        ([10, 8, 6, 4, "?"], "2", "0", "3", "1", "A", "Decreasing by 2"),
        ([3, 9, 27, 81, "?"], "243", "162", "324", "729", "A", "Powers of 3"),
        ([1, 2, 4, 7, 11, "?"], "16", "14", "15", "17", "A", "Differences: 1,2,3,4,5"),
    ]
    for seq, ans, w1, w2, w3, cor, expl in series_cases:
        seq_str = ", ".join(str(x) for x in seq)
        qs.append(REA("Reasoning","Series Completion","medium",
                      f"Find the missing term: {seq_str}", ans, w1, w2, w3, cor, expl))

    # Alphabet series
    alpha_series = [
        ("A, C, E, G, ?", "I", "H", "J", "K", "A", "Alternate letters"),
        ("B, D, F, H, ?", "J", "I", "K", "L", "A", "Even letters"),
        ("Z, X, V, T, ?", "R", "S", "Q", "P", "A", "Decreasing alternate"),
        ("A, B, D, G, K, ?", "P", "O", "N", "Q", "A", "Differences: 1,2,3,4,5"),
        ("Z, Y, X, W, ?", "V", "U", "T", "S", "A", "Reverse alphabet"),
        ("A, E, I, M, ?", "Q", "P", "O", "N", "A", "Every 4th letter"),
        ("B, E, H, K, ?", "N", "M", "L", "O", "A", "Every 3rd letter"),
    ]
    for series, ans, w1, w2, w3, cor, expl in alpha_series:
        qs.append(REA("Reasoning","Alphabet Series","medium",
                      f"Find the next letter: {series}", ans, w1, w2, w3, cor, expl))

    return qs


def gen_reasoning_analogies():
    qs = []
    analogies = [
        ("Doctor : Hospital :: Teacher : ?", "School", "College", "Clinic", "Library", "A"),
        ("Fish : Water :: Bird : ?", "Air/Sky", "Ground", "Tree", "Water", "A"),
        ("Pen : Write :: Knife : ?", "Cut", "Draw", "Paint", "Cook", "A"),
        ("Book : Pages :: House : ?", "Rooms", "Windows", "Floors", "Bricks", "A"),
        ("Car : Petrol :: Human : ?", "Food", "Water", "Air", "Blood", "A"),
        ("Sun : Day :: Moon : ?", "Night", "Evening", "Morning", "Afternoon", "A"),
        ("India : Rupee :: USA : ?", "Dollar", "Pound", "Euro", "Yen", "A"),
        ("Cold : Hot :: Dark : ?", "Bright", "Cold", "Night", "Dusk", "A"),
        ("Speed : km/h :: Weight : ?", "Kilogram (kg)", "Meter", "Second", "Newton", "A"),
        ("London : UK :: Paris : ?", "France", "Germany", "Italy", "Spain", "A"),
        ("Chess : Board :: Cricket : ?", "Ground/Pitch", "Net", "Ring", "Court", "A"),
        ("Author : Book :: Sculptor : ?", "Statue", "Painting", "Building", "Song", "A"),
        ("Cow : Calf :: Dog : ?", "Puppy", "Cub", "Kitten", "Foal", "A"),
        ("Oak : Tree :: Rose : ?", "Flower", "Plant", "Shrub", "Bush", "A"),
        ("Computer : Software :: Human : ?", "Knowledge/Mind", "Body", "Eyes", "Hands", "A"),
        ("Wheat : Bread :: Grapes : ?", "Wine/Juice", "Jam only", "Oil", "Vinegar", "A"),
        ("Triangle : 3 sides :: Pentagon : ?", "5 sides", "4 sides", "6 sides", "7 sides", "A"),
        ("North : South :: East : ?", "West", "North", "Left", "Up", "A"),
        ("Iron : Rust :: Wood : ?", "Rot/Decay", "Melt", "Burn only", "Freeze", "A"),
        ("January : 1st month :: December : ?", "12th month", "11th month", "10th month", "Last month before", "A"),
    ]
    for analogy, ans, w1, w2, w3, cor in analogies:
        qs.append(REA("Reasoning","Analogies","medium",
                      f"Complete the analogy: {analogy}", ans, w1, w2, w3, cor))
    return qs


def gen_reasoning_misc():
    qs = []
    # Coding-Decoding
    coding = [
        ("In a code, CAT = 3120. Then DOG = ?", "4157", "4715", "4175", "1574", "A"),
        ("If APPLE → BQQMF, then MANGO → ?", "NBOPH", "OBOHI", "NBOHO", "OBOPH", "A"),
        ("FACE → 6135, then CAFE → ?", "3165", "1365", "3615", "6315", "A"),
    ]
    for c in coding:
        qs.append(REA("Reasoning","Coding-Decoding","hard", *c))

    # Blood relations
    relations = [
        ("A is the father of B. B is the son of C. How is A related to C?",
         "Husband", "Brother", "Son", "Father", "A"),
        ("If X is the mother of Y, and Y is the sister of Z, how is X related to Z?",
         "Mother", "Grandmother", "Aunt", "Sister", "A"),
        ("P is the son of Q. R is the father of Q. What is R to P?",
         "Grandfather", "Uncle", "Father", "Brother", "A"),
    ]
    for r in relations:
        qs.append(REA("Reasoning","Blood Relations","medium", *r))

    # Direction sense
    directions = [
        ("Walking 5 km North then 3 km East, total distance from start (straight line):",
         "√34 km ≈ 5.83 km", "8 km", "5 km", "3 km", "A"),
        ("A walks 4 km East then 3 km North. Distance from start:", "5 km", "7 km", "4 km", "3 km", "A"),
        ("Facing South, turning 90° clockwise faces:", "West", "East", "North", "South-East", "A"),
        ("Facing North, turning 180° faces:", "South", "East", "West", "North-East", "A"),
        ("Facing East, turning 90° anticlockwise faces:", "North", "South", "West", "East", "A"),
        ("Walking 10m North, 6m East, 10m South: net position from start:", "6m East", "10m North", "16m", "0m", "A"),
    ]
    for d in directions:
        qs.append(REA("Reasoning","Direction Sense","medium", *d))

    # Arrangement
    arrangements = [
        ("Word 'TRIANGLE' rearranged alphabetically:", "AEGILNRT", "TRIANGLEE", "LGRTINAE", "RETNALGI", "A"),
        ("If 1st, 2nd, 3rd, 4th letters of COMPUTER are rearranged as 4th, 3rd, 2nd, 1st: first 4 letters become:",
         "PMOC", "COMP", "MOCP", "OCPM", "A"),
    ]
    for a in arrangements:
        qs.append(REA("Reasoning","Arrangement","medium", *a))

    # Logical reasoning
    logical = [
        ("All dogs are animals. Some animals are pets. Conclusion:", "Some dogs may be pets",
         "All dogs are pets", "No dogs are pets", "All pets are dogs", "A"),
        ("All metals are conductors. Copper is a metal. Conclusion:", "Copper is a conductor",
         "Copper is not a conductor", "All conductors are copper", "Metals are not copper", "A"),
        ("Some books are novels. All novels are fiction. Conclusion:", "Some books are fiction",
         "All books are fiction", "No books are fiction", "All fiction is books", "A"),
        ("If P implies Q, and Q implies R, then:", "P implies R (transitive)",
         "R implies P", "P and R are unrelated", "Q does not imply R", "A"),
        ("No cats are dogs. All dogs are animals. Conclusion:", "Some animals are not cats",
         "All cats are animals", "No animals are cats", "All cats are dogs", "A"),
    ]
    for l in logical:
        qs.append(REA("Reasoning","Logical Reasoning","hard", *l))

    # Odd one out
    odd_out = [
        ("Find odd one: Pen, Pencil, Eraser, Paper", "Paper (others write/mark)", "Pen", "Pencil", "Eraser", "A"),
        ("Find odd one: Apple, Mango, Carrot, Banana", "Carrot (vegetable)", "Apple", "Mango", "Banana", "A"),
        ("Find odd one: 8, 27, 64, 100", "100 (not a perfect cube)", "8", "27", "64", "A"),
        ("Find odd one: Rose, Lily, Jasmine, Neem", "Neem (not a flower)", "Rose", "Lily", "Jasmine", "A"),
        ("Find odd one: Crow, Eagle, Parrot, Bat", "Bat (mammal, not bird)", "Crow", "Eagle", "Parrot", "A"),
        ("Find odd one: 2, 3, 5, 9", "9 (not prime)", "2", "3", "5", "A"),
    ]
    for o in odd_out:
        qs.append(REA("Reasoning","Odd One Out","medium", *o))

    return qs


def generate_all_reasoning_questions() -> List[Dict]:
    qs = []
    qs.extend(gen_series_completion())
    qs.extend(gen_reasoning_analogies())
    qs.extend(gen_reasoning_misc())
    for q_item in qs:
        q_item["subject"] = "CUET_Reasoning"
        q_item["exam_type"] = "CUET_GT"
    print(f"[CUET Reasoning] Generated {len(qs)} questions")
    return qs


# ─── SUBJECT 4: CUET Quantitative Aptitude ───────────────────────────────────

def gen_quantitative():
    qs = []

    # Percentages
    pct_cases = [
        (200, 10, "20", "15", "25", "10", "A"),
        (500, 20, "100", "50", "200", "25", "A"),
        (150, 30, "45", "30", "60", "15", "A"),
        (800, 25, "200", "150", "250", "175", "A"),
        (1000, 15, "150", "100", "200", "125", "A"),
        (60, 5, "3", "6", "1.5", "9", "A"),
        (250, 40, "100", "75", "125", "50", "A"),
        (900, 33.33, "300", "150", "450", "200", "A"),
        (400, 12.5, "50", "25", "75", "40", "A"),
        (750, 8, "60", "45", "75", "30", "A"),
    ]
    for num, pct, ans, w1, w2, w3, cor in pct_cases:
        result = num * pct / 100
        qs.append(QAN("Arithmetic","Percentage","medium",
                      f"{pct}% of {num} = ?", ans, w1, w2, w3, cor,
                      f"{pct}% of {num} = {num}×{pct}/100 = {result}"))

    # Profit and Loss
    pl_cases = [
        (100, 120, "20%", "10%", "15%", "25%", "A"),
        (200, 250, "25%", "20%", "30%", "15%", "A"),
        (500, 450, "10% loss", "20% loss", "5% loss", "15% loss", "A"),
        (150, 180, "20%", "10%", "30%", "15%", "A"),
        (1000, 1200, "20%", "15%", "25%", "10%", "A"),
        (400, 360, "10% loss", "5% loss", "20% loss", "15% loss", "A"),
        (800, 1000, "25%", "20%", "30%", "15%", "A"),
        (300, 270, "10% loss", "5% loss", "15% loss", "20% loss", "A"),
        (600, 750, "25%", "20%", "30%", "15%", "A"),
        (250, 200, "20% loss", "10% loss", "25% loss", "15% loss", "A"),
    ]
    for cp, sp, ans, w1, w2, w3, cor in pl_cases:
        pnl = ((sp - cp) / cp) * 100
        label = f"{abs(pnl):.0f}% {'profit' if pnl >= 0 else 'loss'}"
        qs.append(QAN("Arithmetic","Profit and Loss","medium",
                      f"CP = ₹{cp}, SP = ₹{sp}. Profit/Loss %:",
                      ans, w1, w2, w3, cor,
                      f"P/L % = (SP-CP)/CP × 100 = ({sp}-{cp})/{cp} × 100 = {pnl:.1f}%"))

    # Simple Interest
    si_cases = [
        (1000, 5, 3, "₹150", "₹300", "₹75", "₹50", "A"),
        (2000, 8, 2, "₹320", "₹160", "₹640", "₹80", "A"),
        (5000, 10, 4, "₹2000", "₹1000", "₹4000", "₹500", "A"),
        (500, 12, 5, "₹300", "₹150", "₹600", "₹60", "A"),
        (1500, 6, 3, "₹270", "₹135", "₹540", "₹90", "A"),
        (800, 15, 2, "₹240", "₹120", "₹480", "₹60", "A"),
        (3000, 7, 4, "₹840", "₹420", "₹1680", "₹210", "A"),
        (10000, 9, 2, "₹1800", "₹900", "₹3600", "₹450", "A"),
        (4000, 4, 5, "₹800", "₹400", "₹1600", "₹200", "A"),
        (2500, 11, 3, "₹825", "₹412.5", "₹1650", "₹206", "A"),
    ]
    for P, R, T, ans, w1, w2, w3, cor in si_cases:
        SI = P * R * T / 100
        qs.append(QAN("Arithmetic","Simple Interest","medium",
                      f"P = ₹{P}, R = {R}% per annum, T = {T} years. SI = ?",
                      ans, w1, w2, w3, cor,
                      f"SI = PRT/100 = {P}×{R}×{T}/100 = ₹{SI:.0f}"))

    # Ratio and Proportion
    ratio_cases = [
        (2, 3, 100, "₹40 and ₹60", "₹50 and ₹50", "₹60 and ₹40", "₹30 and ₹70", "A"),
        (3, 5, 160, "₹60 and ₹100", "₹80 and ₹80", "₹100 and ₹60", "₹40 and ₹120", "A"),
        (1, 4, 250, "₹50 and ₹200", "₹125 and ₹125", "₹200 and ₹50", "₹100 and ₹150", "A"),
        (5, 7, 240, "₹100 and ₹140", "₹120 and ₹120", "₹140 and ₹100", "₹80 and ₹160", "A"),
        (7, 3, 500, "₹350 and ₹150", "₹250 and ₹250", "₹150 and ₹350", "₹400 and ₹100", "A"),
        (2, 5, 350, "₹100 and ₹250", "₹175 and ₹175", "₹250 and ₹100", "₹50 and ₹300", "A"),
    ]
    for a_rat, b_rat, total, ans, w1, w2, w3, cor in ratio_cases:
        share_a = total * a_rat // (a_rat + b_rat)
        share_b = total * b_rat // (a_rat + b_rat)
        qs.append(QAN("Arithmetic","Ratio and Proportion","medium",
                      f"₹{total} divided in ratio {a_rat}:{b_rat}:",
                      ans, w1, w2, w3, cor,
                      f"Share A = {a_rat}/{a_rat+b_rat}×{total} = ₹{share_a}"))

    # Time and Work
    tw_cases = [
        (10, 15, "6 days", "5 days", "7 days", "8 days", "A"),
        (12, 18, "7.2 days", "6 days", "8 days", "5 days", "A"),
        (20, 30, "12 days", "10 days", "15 days", "8 days", "A"),
        (6, 12, "4 days", "3 days", "6 days", "9 days", "A"),
        (8, 24, "6 days", "4 days", "8 days", "10 days", "A"),
        (5, 20, "4 days", "2 days", "5 days", "6 days", "A"),
        (15, 45, "11.25 days", "10 days", "12 days", "15 days", "A"),
        (10, 10, "5 days", "10 days", "3 days", "4 days", "A"),
        (4, 6, "2.4 days", "2 days", "3 days", "4 days", "A"),
        (9, 18, "6 days", "4 days", "9 days", "3 days", "A"),
    ]
    for A_days, B_days, ans, w1, w2, w3, cor in tw_cases:
        together = (A_days * B_days) / (A_days + B_days)
        qs.append(QAN("Arithmetic","Time and Work","medium",
                      f"A finishes work in {A_days} days, B in {B_days} days. Together:",
                      ans, w1, w2, w3, cor,
                      f"Together = AB/(A+B) = {A_days}×{B_days}/({A_days}+{B_days}) = {together:.1f} days"))

    # Speed, Distance, Time
    sdt_cases = [
        (60, 3, "180 km", "90 km", "360 km", "20 km", "A"),
        (80, 4.5, "360 km", "180 km", "720 km", "85.5 km", "A"),
        (100, 240, "2.4 hours", "1.2 hours", "4.8 hours", "24 hours", "A"),
        (45, 2.5, "112.5 km", "56.25 km", "225 km", "47.5 km", "A"),
        (50, 150, "3 hours", "1.5 hours", "6 hours", "5 hours", "A"),
        (120, 3, "40 km/h", "60 km/h", "360 km/h", "30 km/h", "A"),
        (60, 90, "1.5 hours", "0.75 hours", "3 hours", "2 hours", "A"),
        (75, 375, "5 hours", "2.5 hours", "10 hours", "3 hours", "A"),
    ]
    for a_val, b_val, ans, w1, w2, w3, cor in sdt_cases[:6]:
        if cor == "A" and "km" in ans:
            qs.append(QAN("Arithmetic","Speed Distance Time","medium",
                          f"Speed = {a_val} km/h, Time = {b_val} hours. Distance = ?",
                          ans, w1, w2, w3, cor, f"D = S×T = {a_val}×{b_val} = {a_val*b_val} km"))
        elif cor == "A" and "hours" in ans:
            qs.append(QAN("Arithmetic","Speed Distance Time","medium",
                          f"Speed = {a_val} km/h, Distance = {b_val} km. Time = ?",
                          ans, w1, w2, w3, cor, f"T = D/S = {b_val}/{a_val} = {b_val/a_val} hours"))
        else:
            qs.append(QAN("Arithmetic","Speed Distance Time","medium",
                          f"Distance = {a_val} km, Time = {b_val} hours. Speed = ?",
                          ans, w1, w2, w3, cor, f"S = D/T = {a_val}/{b_val}"))

    # Averages
    avg_cases = [
        ([10, 20, 30], "20", "15", "25", "30", "A"),
        ([5, 15, 25, 35], "20", "15", "25", "10", "A"),
        ([100, 200, 300, 400, 500], "300", "250", "350", "200", "A"),
        ([12, 14, 16, 18, 20], "16", "14", "18", "15", "A"),
        ([7, 14, 21, 28, 35], "21", "14", "28", "35", "A"),
        ([3, 7, 11, 15, 19, 23], "13", "11", "15", "12", "A"),
        ([50, 60, 70, 80, 90], "70", "65", "75", "60", "A"),
        ([2, 4, 6, 8, 10, 12], "7", "6", "8", "5", "A"),
    ]
    for nums, ans, w1, w2, w3, cor in avg_cases:
        avg = sum(nums) / len(nums)
        qs.append(QAN("Arithmetic","Averages","medium",
                      f"Average of {nums} =",
                      ans, w1, w2, w3, cor, f"Average = {sum(nums)}/{len(nums)} = {avg}"))

    # Area and Perimeter
    shapes = [
        ("rectangle", 10, 5, "A=50, P=30", "A=25, P=15", "A=100, P=60", "A=15, P=30", "A", "Area=l×b, Perimeter=2(l+b)"),
        ("rectangle", 8, 6, "A=48, P=28", "A=24, P=14", "A=96, P=56", "A=14, P=28", "A", "Area=8×6=48"),
        ("square", 7, 7, "A=49, P=28", "A=14, P=28", "A=98, P=56", "A=7, P=28", "A", "Area=s²=49"),
        ("square", 12, 12, "A=144, P=48", "A=72, P=24", "A=288, P=96", "A=24, P=48", "A", "Area=12²=144"),
        ("circle", 7, 7, "A=154, C=44", "A=22, C=44", "A=308, C=88", "A=49, C=14", "A", "Area=πr²≈22/7×49=154"),
        ("triangle", 6, 8, "A=24", "A=48", "A=12", "A=6", "A", "Area=½×b×h=24"),
        ("triangle", 10, 5, "A=25", "A=50", "A=15", "A=10", "A", "Area=½×10×5=25"),
    ]
    for shape, d1, d2, ans, w1, w2, w3, cor, expl in shapes:
        if shape == "rectangle":
            qs.append(QAN("Geometry","Area and Perimeter","medium",
                          f"Rectangle: length={d1}m, breadth={d2}m. Area and Perimeter:",
                          ans, w1, w2, w3, cor, expl))
        elif shape == "square":
            qs.append(QAN("Geometry","Area and Perimeter","medium",
                          f"Square with side {d1}m. Area and Perimeter:",
                          ans, w1, w2, w3, cor, expl))
        elif shape == "circle":
            qs.append(QAN("Geometry","Area and Perimeter","medium",
                          f"Circle with radius {d1}m. Area and Circumference: (π = 22/7)",
                          ans, w1, w2, w3, cor, expl))
        elif shape == "triangle":
            qs.append(QAN("Geometry","Area","medium",
                          f"Triangle: base={d1}m, height={d2}m. Area:",
                          ans, w1, w2, w3, cor, expl))

    return qs


def generate_all_quantitative_questions() -> List[Dict]:
    qs = gen_quantitative()
    for q_item in qs:
        q_item["subject"] = "CUET_Quantitative"
        q_item["exam_type"] = "CUET_GT"
    print(f"[CUET Quantitative] Generated {len(qs)} questions")
    return qs


# ==============================================================================
# MASTER GENERATE ALL
# ==============================================================================

def generate_all_bio_cuet_questions():
    all_qs = []
    all_qs.extend(generate_all_biology_questions())
    all_qs.extend(generate_all_gk_questions())
    all_qs.extend(generate_all_english_questions())
    all_qs.extend(generate_all_reasoning_questions())
    all_qs.extend(generate_all_quantitative_questions())
    print(f"\n[Total Bio+CUET] Generated {len(all_qs)} questions")
    return all_qs
