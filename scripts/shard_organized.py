#!/usr/bin/env python3
"""
Shard any folder with >500 HTML files into subdirectories.
For Actual_Exam_Shifts: shard by month (e.g., 2024-09-Sep/).
For other folders: shard by first char of filename (a/, b/, c/, ..., 0-9/).
"""
import os
import re
import shutil
from pathlib import Path

ROOT = "/home/z/my-project/ssc-mock-tests-organized"
MAX_FILES = 500  # be conservative, GitHub limit is 1000

def shard_actual_shifts(folder_path):
    """Shard by month: 09-SEP-2024 → 2024-09-SEP/"""
    files = [f for f in os.listdir(folder_path) if os.path.isfile(os.path.join(folder_path, f))]
    if len(files) <= MAX_FILES:
        return 0
    # Group by month from filename pattern: ActualShift_DD-MMM-YYYY_...
    by_month = {}
    for f in files:
        m = re.search(r'(\d{2})-([A-Z]{3})-(\d{4})', f)
        if m:
            key = f"{m.group(3)}-{m.group(1)}-{m.group(2)}"
        else:
            # Use first 6 chars of filename for non-date files
            key = 'other-' + f[:6].upper()
        by_month.setdefault(key, []).append(f)
    # If a single month still exceeds MAX_FILES, further split by shift
    final_groups = {}
    for key, fs in by_month.items():
        if len(fs) > MAX_FILES:
            # Split by shift number
            for f in fs:
                m = re.search(r'Shift-(\d+)', f, re.I)
                if m:
                    shift_key = f"{key}_Shift-{m.group(1)}"
                else:
                    shift_key = f"{key}_{f[:8]}"
                final_groups.setdefault(shift_key, []).append(f)
        else:
            final_groups[key] = fs
    moved = 0
    for key, key_files in final_groups.items():
        sub_dir = os.path.join(folder_path, key.replace('/', '-'))
        os.makedirs(sub_dir, exist_ok=True)
        for f in key_files:
            src = os.path.join(folder_path, f)
            dst = os.path.join(sub_dir, f)
            if os.path.exists(dst):
                continue
            shutil.move(src, dst)
            moved += 1
    return moved

def shard_generic(folder_path):
    """Shard by first 4 chars of filename (more granular than 2)."""
    files = [f for f in os.listdir(folder_path) if os.path.isfile(os.path.join(folder_path, f))]
    if len(files) <= MAX_FILES:
        return 0
    # Try sharding by first 4 chars of filename
    by_shard = {}
    for f in files:
        # Get first 4 alphanumeric chars
        m = re.match(r'([A-Za-z0-9]{4})', f)
        shard = m.group(1).upper() if m else 'other'
        by_shard.setdefault(shard, []).append(f)
    # If a shard still exceeds MAX_FILES, split further by content hash suffix
    final_groups = {}
    for shard, fs in by_shard.items():
        if len(fs) > MAX_FILES:
            # Split by hash suffix (last 6 chars before .html)
            for f in fs:
                m = re.search(r'_([0-9a-f]{6})\.html$', f)
                hash_part = m.group(1) if m else f[-10:-5]
                first = hash_part[0] if hash_part else 'x'
                new_key = f"{shard}-{first}"
                final_groups.setdefault(new_key, []).append(f)
        else:
            final_groups[shard] = fs
    moved = 0
    for shard, shard_files in final_groups.items():
        shard_dir = os.path.join(folder_path, shard)
        os.makedirs(shard_dir, exist_ok=True)
        for f in shard_files:
            src = os.path.join(folder_path, f)
            dst = os.path.join(shard_dir, f)
            if os.path.exists(dst):
                continue
            shutil.move(src, dst)
            moved += 1
    return moved

def main():
    # Walk all directories, find ones with >MAX_FILES files
    big_folders = []
    for root, dirs, files in os.walk(ROOT):
        # Skip .git and scripts
        if '.git' in root or '/scripts' in root:
            continue
        if len(files) > MAX_FILES:
            big_folders.append((root, len(files)))
    print(f"Folders with >{MAX_FILES} files: {len(big_folders)}")
    for r, n in sorted(big_folders, key=lambda x: -x[1]):
        print(f"  {n:5d}  {r}")

    # Shard each
    for folder, _ in big_folders:
        if 'Actual_Exam_Shifts' in folder:
            n = shard_actual_shifts(folder)
        else:
            n = shard_generic(folder)
        print(f"  Sharded {n} files in {os.path.relpath(folder, ROOT)}")

    # Verify
    print("\n=== Verification ===")
    remaining_big = []
    for root, dirs, files in os.walk(ROOT):
        if '.git' in root or '/scripts' in root:
            continue
        if len(files) > MAX_FILES:
            remaining_big.append((root, len(files)))
    if remaining_big:
        print(f"STILL TOO BIG ({len(remaining_big)} folders):")
        for r, n in remaining_big:
            print(f"  {n}  {r}")
    else:
        print(f"All folders now have ≤{MAX_FILES} files ✓")

    # Update INDEX.csv paths
    print("\nUpdating INDEX.csv paths...")
    import csv, json
    # Walk all HTML files now and rebuild mapping by filename
    new_mapping = {}  # filename → new path
    for root, dirs, files in os.walk(ROOT):
        if '.git' in root or '/scripts' in root:
            continue
        for f in files:
            if f.endswith('.html'):
                full = os.path.join(root, f)
                rel = os.path.relpath(full, ROOT)
                new_mapping[f] = rel
    # Update INDEX.csv
    csv_path = os.path.join(ROOT, 'INDEX.csv')
    json_path = os.path.join(ROOT, 'INDEX.json')
    # Read existing
    with open(csv_path, 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        rows = list(reader)
        fieldnames = reader.fieldnames
    # Update each row's new_path
    updated = 0
    for r in rows:
        fn = r['new_filename']
        if fn in new_mapping:
            r['new_path'] = new_mapping[fn]
            updated += 1
    print(f"Updated {updated}/{len(rows)} INDEX rows")
    with open(csv_path, 'w', newline='', encoding='utf-8') as f:
        w = csv.DictWriter(f, fieldnames=fieldnames)
        w.writeheader()
        w.writerows(rows)
    # Update JSON
    with open(json_path, 'r', encoding='utf-8') as f:
        data = json.load(f)
    for r in data['files']:
        fn = r['new_filename']
        if fn in new_mapping:
            r['new_path'] = new_mapping[fn]
    with open(json_path, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=1)

if __name__ == '__main__':
    main()
