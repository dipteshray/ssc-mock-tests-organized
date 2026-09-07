# SSC Mock Tests — Organized Archive

A clean, browsable collection of **every actual SSC mock test** from
[`dipteshray/mock-archive`](https://github.com/dipteshray/mock-archive),
reorganized by exam / year / tier / source with human-readable filenames.

> **What's inside:** 4,839 mock test HTML files (~1 GB), covering SSC CGL,
> CHSL, CPO, Stenographer, Selection Post, JSO exams from 2017–2026.
> Includes actual exam shift papers + full mocks from English Madhyam,
> Oliveboard, RBE, The Pundits, Heisenberg/Testbook, Pinnacle, Yatri,
> SSC Panacea 360 + subject-wise sectionals and PYQs.

---

## What was filtered IN

Only these test types were copied (chapter-wise quizzes and tiny daily
practice quizzes were skipped to keep the repo focused on full-length mocks):

| Type | Files |
|------|-------|
| Actual Exam Shift / PYP (real SSC papers) | ~2,330 |
| Full Mock Test (institution-made) | ~2,126 |
| Sectional Test (subject-wise) | ~667 |
| PYQ Vault / Subject PYQ | ~698 |
| Practice Test (booster) | ~121 |
| **Total copied** | **4,839** |

---

## Folder structure

```
<Exam>/<Year>/<Tier>/<Source>/<clean-filename>.html
<Exam>/<Year>/<Tier>/<Source>/<clean-filename>.caption.txt
```

### Examples

```
SSC_CGL/
├── 2024/
│   ├── Tier-1/
│   │   ├── Actual_Exam_Shifts/
│   │   │   ├── ActualShift_09-SEP-2024_Shift-1_SSC_CGL_2024_Tier-1.html
│   │   │   ├── ActualShift_09-SEP-2024_Shift-2_SSC_CGL_2024_Tier-1.html
│   │   │   └── ...
│   │   ├── EnglishMadhyam/
│   │   │   ├── EnglishMadhyam_FullMock_Test-01_SSC_CGL_2024_Tier-1.html
│   │   │   └── ...
│   │   └── RBE/
│   │       └── RBE_Sectional_Maths_Test-01_SSC_CGL_2024_Tier-1.html
│   └── Tier-2/
│       ├── Actual_Exam_Shifts/
│       └── EnglishMadhyam/
├── 2025/
│   ├── Tier-1/
│   │   ├── Actual_Exam_Shifts/
│   │   ├── EnglishMadhyam/
│   │   ├── Pundits/
│   │   ├── RBE/
│   │   └── Telegram/
│   └── Tier-2/
│       ├── EnglishMadhyam/
│       └── RBE/
└── 2026/  (prep mocks)
    ├── Tier-1/
    └── Tier-2/

SSC_CHSL/        # same structure
SSC_CPO/
SSC_Stenographer/
SSC_Selection_Post/
SSC_JSO/
SSC_MTS/
```

---

## Filename convention

### Actual Exam Shift papers
```
ActualShift_<DATE>_Shift-<N>_SSC_<EXAM>_<YEAR>_<TIER>.html
```
Example: `ActualShift_09-SEP-2024_Shift-2_SSC_CGL_2024_Tier-1.html`

### Institution full mocks
```
<Provider>_FullMock_Test-<NN>_SSC_<Exam>_<Year>_<Tier>.html
```
Example: `EnglishMadhyam_FullMock_Test-05_SSC_CGL_2025_Tier-1.html`

### Sectional tests (subject-wise)
```
<Provider>_Sectional_<Subject>_Test-<NN>_SSC_<Exam>_<Year>_<Tier>.html
```
Example: `RBE_Sectional_Maths_Test-05_SSC_CGL_2026_Tier-1.html`

### Subject PYQs
```
<Provider>_SubjectPYQ_<Subject>_Test-<NN>_SSC_<Exam>_<Year>_<Tier>.html
```

If two files would have the same name (e.g., same mock number from same
provider), a 6-character content-hash suffix is appended to disambiguate:
```
RBE_Sectional_Maths_Test-05_SSC_CGL_2024_Tier-1_043154.html
```

---

## Sources included

| Provider | Clean folder name |
|----------|-------------------|
| English Madhyam Mock | `EnglishMadhyam/` |
| Testbook / Heisenberg | `Heisenberg_Testbook/` |
| RBE (Revolution By Education) | `RBE/` |
| Oliveboard | `Oliveboard/` |
| The Pundits (ProMocks) | `Pundits/` |
| Pinnacle | `Pinnacle/` |
| Yatri | `Yatri/` |
| Mocks Wallah (free) | `MocksWallah/` |
| Telegram (PiroMocks / Pinnacle / Mocks Wallah) | `Telegram/` |
| ProToppers | `ProToppers/` |
| Actual SSC exam shifts | `Actual_Exam_Shifts/` |

---

## Coverage matrix

### SSC CGL (1,770 files)

| Year | Tier-1 Actual Shifts | Tier-1 Mocks | Tier-2 Actual Shifts | Tier-2 Mocks |
|------|---------------------|--------------|---------------------|--------------|
| 2017 | 44 PYQs | – | – | – |
| 2018 | 42 PYQs | – | – | – |
| 2019 | 56 PYQs | – | – | – |
| 2020 | 70 PYQs | – | – | – |
| 2021 | 44 PYQs | – | – | – |
| 2022 | – | – | 6 PYQs | 8 RBE |
| 2023 | 100 PYQs | – | 4 PYQs | 4 RBE |
| 2024 | 258 PYQs | 35 English Madhyam + 38 RBE | 18 PYQs | 17 English Madhyam + 4 RBE |
| 2025 | 265 PYQs | many across 5 providers | 111 English Madhyam | 67 RBE + 30 RBE Live Mocks |
| 2026 | – | many prep mocks | – | 3 Heisenberg Advanced |

### SSC CHSL (~600 files)
2018 → 25, 2019 → 28, 2020 → 35, 2021 → 37, 2022 → 33, 2023 → 41, 2024 → 135

### SSC CPO (~90 files)
2022 → 6, 2023 → 19, 2024 → 34, 2025 → 15

### SSC Stenographer (~120 files)
2022 → 12, 2023 → 8, 2024 → 84, 2025 → 15

### SSC Selection Post (~70 files)
2021 → 8, 2023 → 5, 2024 → 37

---

## Files in this repo

| Path | Purpose |
|------|---------|
| `INDEX.csv` | Spreadsheet mapping new clean filename → original mock-archive path |
| `INDEX.json` | Same as CSV but as JSON |
| `<Exam>/<Year>/<Tier>/<Source>/*.html` | The actual mock test HTML files |
| `<Exam>/<Year>/<Tier>/<Source>/*.caption.txt` | Original Telegram caption (often has shift/date/time info) |

---

## How to use

### Find a specific paper
```bash
# All SSC CGL 2024 Tier-1 actual exam shift papers
ls SSC_CGL/2024/Tier-1/Actual_Exam_Shifts/

# All English Madhyam full mocks for CGL 2025 Tier-2
ls SSC_CGL/2025/Tier-2/EnglishMadhyam/

# All RBE sectionals for CGL 2026 Tier-1
ls SSC_CGL/2026/Tier-1/RBE/
```

### Open a mock test
Just click the `.html` file on GitHub — it renders in the browser.
Or clone the repo and open locally:
```bash
git clone https://github.com/dipteshray/ssc-mock-tests-organized.git
open SSC_CGL/2024/Tier-1/Actual_Exam_Shifts/ActualShift_09-SEP-2024_Shift-2_SSC_CGL_2024_Tier-1.html
```

### Search the index
```python
import csv
with open('INDEX.csv') as f:
    rows = list(csv.DictReader(f))

# All SSC CGL 2024 Tier-1 Shift 2 papers
hits = [r for r in rows
        if r['exam'] == 'SSC CGL'
        and r['year'] == '2024'
        and r['tier'] == 'Tier 1 / Pre'
        and r['shift'] == '2']
for r in hits:
    print(r['new_path'])
```

---

## Companion repo

The full **classification index** (with per-document JSON metadata, evidence,
duplicate detection, SQLite FTS5 search) lives at
[`dipteshray/ssc-mock-archive-index`](https://github.com/dipteshray/ssc-mock-archive-index).

This repo = the actual files. The other repo = the catalog.

---

## License

Mock test HTML files remain the property of their respective Telegram
channels and coaching platforms (English Madhyam Mock, Testbook/Heisenberg,
RBE, Oliveboard, The Pundits, Pinnacle, Yatri, SSC Panacea 360, etc.).
This reorganized collection is provided for personal study purposes only.

Generated 2026-09-08 from `dipteshray/mock-archive` upstream snapshot.
