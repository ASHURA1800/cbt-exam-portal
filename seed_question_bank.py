"""
seed_question_bank.py
=====================
Populates the question_bank.db with all 40,000+ questions.
Run once: python seed_question_bank.py
Then questions are available forever without AI.

Progress is shown during seeding.
"""

import sys
import os
import time

# Add project root to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from question_bank_db import init_bank, bulk_insert_questions, get_bank_stats, get_subject_count
from question_seeds.physics_questions import generate_all_physics_questions
from question_seeds.chemistry_questions import generate_all_chemistry_questions
from question_seeds.maths_questions import generate_all_maths_questions
from question_seeds.biology_cuet_questions import (
    generate_all_biology_questions,
    generate_all_gk_questions,
    generate_all_english_questions,
    generate_all_reasoning_questions,
    generate_all_quantitative_questions,
)


def seed_subject(subject_name: str, generator_fn, target: int = 5000):
    """Generate and insert questions for one subject."""
    print(f"\n{'='*60}")
    print(f"  Seeding: {subject_name}")
    print(f"{'='*60}")

    current = get_subject_count(subject_name)
    if current >= target * 0.8:  # 80% of target already seeded
        print(f"  ✅ Already has {current} questions — skipping")
        return current

    print(f"  Generating questions...")
    t0 = time.time()
    questions = generator_fn()
    t1 = time.time()
    print(f"  Generated {len(questions)} questions in {t1-t0:.1f}s")

    print(f"  Inserting into database...")
    # Insert in batches of 500
    BATCH = 500
    total_inserted = 0
    for i in range(0, len(questions), BATCH):
        batch = questions[i:i+BATCH]
        n = bulk_insert_questions(batch)
        total_inserted += n
        pct = min(100, int(total_inserted / len(questions) * 100))
        print(f"  Progress: {total_inserted}/{len(questions)} ({pct}%)", end="\r")

    t2 = time.time()
    final_count = get_subject_count(subject_name)
    print(f"\n  ✅ {subject_name}: {final_count} questions in DB ({t2-t0:.1f}s total)")
    return final_count


def run_full_seed():
    """Seed all 8 subjects with 5000+ questions each."""
    print("=" * 60)
    print("  CBT v12 — QUESTION BANK SEEDER")
    print("  Target: 5000+ questions × 8 subjects = 40,000+ total")
    print("=" * 60)

    # Initialize database
    print("\n[1/9] Initializing database...")
    init_bank()

    # Seed each subject
    subjects = [
        ("Physics",            generate_all_physics_questions),
        ("Chemistry",          generate_all_chemistry_questions),
        ("Mathematics",        generate_all_maths_questions),
        ("Biology",            generate_all_biology_questions),
        ("CUET_GK",            generate_all_gk_questions),
        ("CUET_English",       generate_all_english_questions),
        ("CUET_Reasoning",     generate_all_reasoning_questions),
        ("CUET_Quantitative",  generate_all_quantitative_questions),
    ]

    results = {}
    grand_total = 0

    for subject_name, gen_fn in subjects:
        count = seed_subject(subject_name, gen_fn)
        results[subject_name] = count
        grand_total += count

    # Print summary
    print("\n" + "=" * 60)
    print("  SEEDING COMPLETE — SUMMARY")
    print("=" * 60)
    print(f"  {'Subject':<25} {'Questions':>10}")
    print(f"  {'-'*35}")
    for subj, count in results.items():
        status = "✅" if count >= 500 else "⚠️"
        print(f"  {status} {subj:<23} {count:>10,}")
    print(f"  {'-'*35}")
    print(f"  {'TOTAL':<25} {grand_total:>10,}")
    print("=" * 60)

    if grand_total >= 10000:
        print("\n✅ Question bank ready! Start the app with: streamlit run app.py")
    else:
        print("\n⚠️ Question count seems low. Run the seeder again.")


if __name__ == "__main__":
    run_full_seed()
