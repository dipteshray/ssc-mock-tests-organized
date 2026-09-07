#!/usr/bin/env python3
"""
Copy actual mock-test HTML files from the raw mock-archive into a clean,
browsable folder structure with human-readable filenames.

Filter rules — INCLUDE only:
  - "Actual Exam Shift / PYP"     (real SSC exam papers)
  - "Full Mock Test"              (institution-made full mocks)
  - "Sectional Test"              (subject-wise sectionals — Maths/English/GK/Reasoning)
  - "PYQ Vault / Subject PYQ"     (subject-wise PYQs)
  - "Practice Test"               (booster practice tests)

SKIP:
  - Chapter-wise / Topic-wise    (too granular)
  - Practice Quiz / Daily Practice (small daily quizzes)
  - Vocabulary Quiz
  - Notes / Editorial
  - Unclassified                  (mostly broken/empty)

Output structure:
  <Exam>/<Year>/<Tier>/<Source>/<clean_filename>.html
  <Exam>/<Year>/<Tier>/<Source>/<clean_filename>.caption.txt

Clean filename pattern:
  <Provider>_<TestType>_<Number>_SSC_<Exam>_<Year>_<Tier>_<Shift-or-Date>.html

Examples:
  Actual_ExamShift_09-Sep-2024_Shift-2_SSC_CGL_2024_Tier-1.html
  Oliveboard_FullMock_01_SSC_CGL_2024_Tier-1.html
  EnglishMadhyam_FullMock_05_SSC_CGL_2025_Tier-2.html
  RBE_Math_Sectional_05_SSC_CGL_2026.html
"""
import os
import re
import json
import shutil
import csv
from pathlib import Path

ROOT = "/home/z/my-project/mock-archive"
OUT  = "/home/z/my-project/ssc-mock-tests-organized"
INV  = "/home/z/my-project/ssc-mock-index/inventory/inventory.json"

# Types to include
INCLUDE_TYPES = {
    'Actual Exam Shift / PYP',
    'Full Mock Test',
    'Sectional Test',
    'PYQ Vault / Subject PYQ',
    'Practice Test',
}

# Map exam names to clean folder names
EXAM_FOLDER = {
    'SSC CGL': 'SSC_CGL',
    'SSC CHSL': 'SSC_CHSL',
    'SSC CPO': 'SSC_CPO',
    'SSC MTS': 'SSC_MTS',
    'SSC Stenographer': 'SSC_Stenographer',
    'SSC Selection Post': 'SSC_Selection_Post',
    'SSC JSO': 'SSC_JSO',
    'SSC JE': 'SSC_JE',
    'SSC JHT': 'SSC_JHT',
    'SSC GD Constable': 'SSC_GD_Constable',
    'IBPS': 'IBPS',
    'SBI': 'SBI',
    'RRB NTPC': 'RRB_NTPC',
    'CDS': 'CDS',
    'Unknown': 'Uncategorized',
}

# Map provider to clean folder name
PROVIDER_FOLDER = {
    'English Madhyam Mock': 'EnglishMadhyam',
    'Testbook / Heisenberg': 'Heisenberg_Testbook',
    'RBE': 'RBE',
    'Pinnacle': 'Pinnacle',
    'Oliveboard': 'Oliveboard',
    'The Pundits': 'Pundits',
    'Mocks Wallah': 'MocksWallah',
    'Telegram (PiroMocks / Pinnacle / Mocks Wallah)': 'Telegram',
    'Yatri': 'Yatri',
    'ProToppers': 'ProToppers',
}

# Map tier to clean folder name
def tier_folder(tier_list):
    if not tier_list:
        return 'Unknown_Tier'
    t = tier_list[0]
    if 'Tier 1' in t or 'Pre' in t:
        return 'Tier-1'
    if 'Tier 2' in t or 'Mains' in t:
        return 'Tier-2'
    if 'Tier 3' in t:
        return 'Tier-3'
    return 'Unknown_Tier'

# Map type to clean filename segment
def type_segment(t):
    if t == 'Actual Exam Shift / PYP':
        return 'ActualShift'
    if t == 'Full Mock Test':
        return 'FullMock'
    if t == 'Sectional Test':
        return 'Sectional'
    if t == 'PYQ Vault / Subject PYQ':
        return 'SubjectPYQ'
    if t == 'Practice Test':
        return 'PracticeTest'
    return 'Test'

# Sanitize string for filesystem
def safe(s):
    if not s:
        return ''
    s = str(s)
    # Replace problematic chars
    s = re.sub(r'[/\\:*?"<>|]', '-', s)
    s = re.sub(r'\s+', '_', s.strip())
    s = re.sub(r'_+', '_', s)
    s = s.strip('_-')
    return s[:80]

# Extract mock test number from filename or path
def extract_test_number(text):
    # Look for "Mock - NN" or "Mock NN" or "Mock_NN" or "Test - NN"
    m = re.search(r'(?:Mock|Test)\s*[-_]?\s*(\d+)', text, re.I)
    if m:
        return m.group(1).zfill(2)
    return None

# Extract subject from subjects list (first one)
def subject_segment(subjects):
    if not subjects or subjects == ['General']:
        return ''
    s = subjects[0]
    if 'English' in s:           return 'English'
    if 'Math' in s or 'Quant' in s: return 'Maths'
    if 'Reasoning' in s:         return 'Reasoning'
    if 'GK' in s or 'Awareness' in s: return 'GK'
    if 'Computer' in s:          return 'Computer'
    if 'Hindi' in s:             return 'Hindi'
    return ''

# Build clean filename
def build_filename(r):
    parts = []
    provider = PROVIDER_FOLDER.get(r['provider'], safe(r['provider']) or 'Unknown')
    type_seg = type_segment(r['type'])
    test_num = extract_test_number(r['source_path'] + ' | ' + r['html_title'] + ' | ' + r['caption'])
    subject  = subject_segment(r['subjects'])

    # Actual shift papers get a date-based name
    if r['type'] == 'Actual Exam Shift / PYP':
        if r['date']:
            date_str = safe(r['date']).replace('_', '-')
            parts.append(f"ActualShift_{date_str}")
        else:
            parts.append(f"ActualShift_{test_num or 'PYP'}")
        if r['shift']:
            parts.append(f"Shift-{safe(r['shift'])}")
    else:
        # Institution mock
        parts.append(provider)
        parts.append(type_seg)
        if subject and r['type'] in ('Sectional Test', 'PYQ Vault / Subject PYQ'):
            parts.append(subject)
        if test_num:
            parts.append(f"Test-{test_num}")
        elif r['q_count']:
            parts.append(f"{r['q_count']}Q")

    # Add exam + year + tier suffix
    exam = r['exam'][0] if r['exam'] else 'SSC'
    exam_short = exam.replace('SSC ', '').replace(' ', '') or 'SSC'
    parts.append(f"SSC_{exam_short}" if 'SSC' in exam else exam_short)
    if r['year']:
        parts.append(r['year'])
    parts.append(tier_folder(r['tier']))

    name = '_'.join(str(p) for p in parts if p)
    name = safe(name)
    if not name.endswith('.html'):
        name += '.html'
    return name

# Determine target folder
def build_target_path(r):
    exam = r['exam'][0] if r['exam'] else 'Unknown'
    exam_dir = EXAM_FOLDER.get(exam, safe(exam) or 'Uncategorized')
    year = r['year'] or 'Unknown_Year'
    tier = tier_folder(r['tier'])
    if r['type'] == 'Actual Exam Shift / PYP':
        source_dir = 'Actual_Exam_Shifts'
    else:
        provider = r['provider']
        source_dir = PROVIDER_FOLDER.get(provider, safe(provider) or 'Unknown')
    return os.path.join(exam_dir, year, tier, source_dir)

# Main
def main():
    with open(INV, 'r', encoding='utf-8') as f:
        inventory = json.load(f)
    print(f"Total inventory records: {len(inventory)}")

    # Filter to included types
    selected = [r for r in inventory if r['type'] in INCLUDE_TYPES]
    print(f"Selected for copy (types: {INCLUDE_TYPES}): {len(selected)}")

    # Breakdown
    from collections import Counter
    type_counts = Counter(r['type'] for r in selected)
    print("\nBy type:")
    for t, n in type_counts.most_common():
        print(f"  {n:5d}  {t}")

    # Copy
    os.makedirs(OUT, exist_ok=True)
    index_rows = []
    seen_target_paths = {}  # handle name collisions
    copied = 0
    skipped_no_html = 0
    skipped_too_large = 0
    MAX_FILE_SIZE = 100 * 1024 * 1024  # 100MB GitHub limit

    for i, r in enumerate(selected):
        if i % 500 == 0:
            print(f"  ...processed {i}/{len(selected)} (copied={copied})")
        # Source HTML path
        src_html = os.path.join(ROOT, r['source_path'], r['filename']) if r['filename'] else None
        if not src_html or not os.path.exists(src_html):
            skipped_no_html += 1
            continue
        # Check size
        try:
            size = os.path.getsize(src_html)
            if size > MAX_FILE_SIZE:
                print(f"  SKIP (too large {size//1024//1024}MB): {r['source_path']}")
                skipped_too_large += 1
                continue
        except OSError:
            continue

        # Build target
        target_dir = os.path.join(OUT, build_target_path(r))
        clean_name = build_filename(r)
        target_html = os.path.join(target_dir, clean_name)

        # Handle name collisions by appending short content hash
        if target_html in seen_target_paths:
            short_hash = (r['content_hash'] or r['raw_hash'] or 'x')[:6]
            target_html = target_html[:-5] + f"_{short_hash}.html"
        seen_target_paths[target_html] = True

        # Copy HTML
        os.makedirs(target_dir, exist_ok=True)
        try:
            shutil.copy2(src_html, target_html)
        except Exception as e:
            print(f"  SKIP copy error: {e}")
            continue

        # Also copy caption.txt if exists
        src_cap = os.path.join(ROOT, r['source_path'], 'caption.txt')
        if os.path.exists(src_cap):
            target_cap = target_html[:-5] + '.caption.txt'
            try:
                shutil.copy2(src_cap, target_cap)
            except Exception:
                pass

        # Add to index
        index_rows.append({
            'new_path': os.path.relpath(target_html, OUT),
            'new_filename': clean_name,
            'original_path': r['source_path'],
            'original_filename': r['filename'],
            'exam': '|'.join(r['exam']),
            'tier': '|'.join(r['tier']),
            'year': r['year'] or '',
            'shift': r['shift'] or '',
            'date': r['date'] or '',
            'type': r['type'],
            'provider': r['provider'],
            'subjects': '|'.join(r['subjects']),
            'language': r['language'],
            'q_count': r['q_count'] or '',
            'content_hash': r['content_hash'] or '',
            'file_size_bytes': size,
        })
        copied += 1

    print(f"\n✅ Copied: {copied}")
    print(f"   Skipped (no HTML): {skipped_no_html}")
    print(f"   Skipped (too large): {skipped_too_large}")

    # Write INDEX.csv
    index_csv = os.path.join(OUT, 'INDEX.csv')
    with open(index_csv, 'w', newline='', encoding='utf-8') as f:
        w = csv.DictWriter(f, fieldnames=[
            'new_path','new_filename','original_path','original_filename',
            'exam','tier','year','shift','date','type','provider',
            'subjects','language','q_count','content_hash','file_size_bytes'
        ])
        w.writeheader()
        w.writerows(index_rows)
    print(f"\nINDEX.csv written: {len(index_rows)} rows")

    # Write INDEX.json (structured)
    with open(os.path.join(OUT, 'INDEX.json'), 'w', encoding='utf-8') as f:
        json.dump({
            'total_files': len(index_rows),
            'description': 'Mapping of clean organized filenames to original mock-archive paths.',
            'files': index_rows,
        }, f, ensure_ascii=False, indent=1)

    # Summary stats
    print("\n=== SUMMARY ===")
    exam_year = Counter()
    for r in index_rows:
        exam_year[(r['exam'], r['year'])] += 1
    print("Files per exam × year:")
    for (ex, yr), n in sorted(exam_year.items()):
        print(f"  {n:4d}  {ex:25s}  {yr}")

    # Folder size
    total_size = sum(os.path.getsize(os.path.join(OUT, f['new_path'])) for f in index_rows)
    print(f"\nTotal size: {total_size/1024/1024:.1f} MB ({total_size/1024/1024/1024:.2f} GB)")

if __name__ == '__main__':
    main()
