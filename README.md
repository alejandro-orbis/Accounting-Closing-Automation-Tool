# 📊 Accounting Closing Automation

> A Python tool to automate the monthly accounting closing process — no manual Excel formulas required.

[![Python](https://img.shields.io/badge/Python-3.14+-3776AB?style=flat-square&logo=python&logoColor=white)](https://python.org)
[![License: MIT](https://img.shields.io/badge/License-MIT-22c55e?style=flat-square)](LICENSE)
[![Pandas](https://img.shields.io/badge/Pandas-2.x-150458?style=flat-square&logo=pandas&logoColor=white)](https://pandas.pydata.org)
[![OpenPyXL](https://img.shields.io/badge/OpenPyXL-3.x-217346?style=flat-square)](https://openpyxl.readthedocs.io)

---

## What does it do?

Automates the monthly accounting close starting from a CSV exported by any accounting system. It classifies transactions by supplier or keyword, detects duplicates, flags exceptions for manual review, and produces auditable reports ready to deliver.

**The original file is never modified. No macros. No technical knowledge required.**

---

## ✨ Features

| Feature | Description |
|---|---|
| 📥 **CSV import** | Compatible with any accounting system export |
| ✅ **Structure validation** | Checks required columns before processing |
| 🏷️ **Auto-classification** | By supplier name and description keywords |
| 🔍 **Duplicate detection** | Identifies and isolates repeated rows |
| ⚠️ **Exception flagging** | Marks unclassified transactions for manual review |
| 🔒 **Non-destructive** | Original file is never touched |
| 📋 **Full audit trail** | Change log for every classification applied |

---

## 📤 Output files

All files are created in `data/output/`, prefixed with the input filename.

```
data/output/
├── january_adjusted.csv      ← original rows + classification columns added
├── january_exceptions.csv    ← unclassified rows for manual review
├── january_duplicates.csv    ← detected duplicate rows
├── january_change_log.csv    ← full audit trail
└── january_report.xlsx       ← consolidated Excel workbook (all sheets)
```

---

## 🚀 Quick start

### 1. Install dependencies

```bash
pip install pandas openpyxl pyyaml
```

### 2. Export your CSV

Your file must include these columns:

| Column | Description |
|---|---|
| `fecha` | Transaction date |
| `proveedor` | Supplier or vendor name |
| `descripcion` | Line item description |
| `importe` | Transaction amount |
| `cuenta` | Account code |

### 3. Drop the file in the input folder

```
data/input/january.csv
```

### 4. (Optional) Edit your classification rules

Open the CSV files in `data/rules/` and add your own rules — no coding needed.

**`suppliers.csv`** — classify by supplier name:

```csv
supplier_match,category,cost_center
iberdrola,Energy Utilities,HQ
telefónica,Telecommunications,North Branch
```

**`categories.csv`** — classify by keyword in description:

```csv
keyword,category,cost_center
rent,Fixed Costs,Administration
software,Technology,IT
```

### 5. Run the tool

**Windows** — double-click `run.bat`

**Terminal:**

```bash
cd src
python main.py
```

### 6. Check your results

All generated files are in `data/output/`.

---

## 📁 Project structure

```
accounting-closing/
├── data/
│   ├── input/          ← place your CSV files here
│   ├── output/         ← generated reports and logs
│   └── rules/          ← editable classification rules (CSV)
├── src/
│   └── main.py         ← main entry point
├── config/             ← tool configuration
├── run.bat             ← Windows launcher (double-click to run)
└── instructions.txt    ← end-user guide
```

---

## 🛠️ Tech stack

| Library | Purpose |
|---|---|
| [Python 3.14+](https://python.org) | Core language |
| [Pandas](https://pandas.pydata.org) | Data processing and CSV manipulation |
| [OpenPyXL](https://openpyxl.readthedocs.io) | Excel report generation |
| [PyYAML](https://pyyaml.org) | Configuration file parsing |

---

## 📋 Classification rule examples

| Rule type | Trigger | Action |
|---|---|---|
| Supplier match | Supplier contains `"iberdrola"` | Category → `"Energy Utilities"` |
| Keyword match | Description contains `"software"` | Category → `"Technology"` |
| Unknown supplier | No matching rule found | Flagged as exception |
| Missing column | No `"fecha"` column in file | Process stops with error |
| Duplicate row | Identical row detected | Saved to `duplicates.csv` |

---

## 📄 License

MIT License — free for personal and commercial use. See [LICENSE](LICENSE) for details.

---

## 👤 Author

**Alejandro Peralta** — Process Automation Specialist

- GitHub: [@alejandro-orbis](https://github.com/alejandro-orbis)
- LinkedIn: [linkedin.com/in/alejandro-orbis](https://linkedin.com/in/alejandro-orbis)
- Email: [alejandro@orbisautomations.com](mailto:alejandro@orbisautomations.com)

---

*Built to eliminate repetitive closing work — so your team focuses on what actually matters.*
