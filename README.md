# GenAI Practicals – Weeks 1 to 5

**Student:** Jaswanth Bhaskar  
**Repository:** GenAI-2520030553-Jaswanthbhaskar

## About This Repository

This repository contains my weekly Generative AI practical implementations. It documents my learning and hands-on experience with Python-based GenAI development, LLM clients, usage logging, tokenization techniques, and token economics.

Each week contains its own implementation and dependencies.

## Repository Structure

```text
GenAI-2520030553-Jaswanthbhaskar/
│
├── week1/
│   ├── .gitignore
│   ├── main.py
│   └── requirements.txt
│
├── week2/
│   ├── llm_client.py
│   ├── main.py
│   ├── requirements.txt
│   └── test_client.py
│
├── week3/
│   ├── llm_client.py
│   ├── main.py
│   ├── requirements.txt
│   ├── test_client.py
│   └── usage_logger.py
│
├── week4/
│   ├── .gitignore
│   ├── requirements.txt
│   └── tokenizer_comparison.py
│
└── week5/
    └── TokenEconomics/
        ├── .gitignore
        ├── .env
        ├── budget.py
        ├── requirements.txt
        └── test_budget.py
```

## Weekly Practicals

### Week 1 – Python Foundations

**Files:** `main.py`, `requirements.txt`

Contains the initial Python practical implementation and its required dependencies.

### Week 2 – LLM Client

**Files:**
- `llm_client.py`
- `main.py`
- `test_client.py`
- `requirements.txt`

Introduces an LLM client implementation with a separate main program and automated tests.

### Week 3 – Usage Logging

**Files:**
- `llm_client.py`
- `main.py`
- `usage_logger.py`
- `test_client.py`
- `requirements.txt`

Extends the earlier LLM client work with a separate usage logging component.

### Week 4 – Tokenizer Lab: Comparison of BPE, WordPiece and SentencePiece

**Main file:** `tokenizer_comparison.py`

This practical compares three tokenization approaches using Hugging Face Transformers.

**Tokenizers and models:**

| Tokenization | Model |
|---|---|
| BPE | GPT-2 |
| WordPiece | Multilingual BERT |
| SentencePiece | XLM-R |

**Languages tested:**
- English
- Telugu
- Hindi

The program compares tokenization results, token IDs, and token counts across the three models.

**Run the program:**

```bash
python tokenizer_comparison.py
```

**Key observation:** GPT-2 produced significantly more tokens for Telugu and Hindi than the multilingual models in the tested examples.

### Week 5 – Token Economics

**Folder:** `week5/TokenEconomics/`

**Main files:**
- `budget.py`
- `test_budget.py`
- `requirements.txt`
- `.env`

This practical implements a reusable Python budgeting tool for estimating the token consumption and API costs of an LLM-powered feature.

**Features:**
- Estimates daily input and output token consumption.
- Calculates daily and monthly API costs.
- Checks Requests Per Minute (RPM) limits.
- Checks Tokens Per Minute (TPM) limits.
- Applies a configurable safety margin.
- Checks daily and monthly budget limits.
- Generates a final `GO` or `REVISE` recommendation.
- Includes automated unit tests.

**Run the budget planner:**

```bash
python budget.py
```

**Run automated tests:**

```bash
python -m unittest -v
```

**Sample results:**

| Metric | Result |
|---|---:|
| Input tokens/day | 2,400,000 |
| Output tokens/day | 600,000 |
| Daily estimated cost | $1.44 |
| Monthly estimated cost | $43.20 |
| Peak RPM with margin | 36 |
| Peak TPM with margin | 54,000 |

The sample configuration produces a `REVISE` recommendation because the monthly budget check includes a 20% safety margin, taking the estimated monthly cost to $51.84 against a $50 budget.

**Testing:** All four automated tests passed.

---

## Technologies Used

- Python
- Hugging Face Transformers
- GPT-2
- Multilingual BERT
- XLM-R
- SentencePiece
- python-dotenv
- Python unittest
- Git and GitHub
- Visual Studio Code

## Running the Practicals

Each practical has its own dependencies and virtual environment.

Navigate to the required week's folder:

```powershell
cd week4
```

Create a virtual environment if one does not already exist:

```powershell
py -m venv .venv
```

Activate it on Windows PowerShell:

```powershell
.\.venv\Scripts\Activate.ps1
```

Install dependencies:

```powershell
python -m pip install -r requirements.txt
```

Run the relevant Python program.

For Week 5, navigate into `week5/TokenEconomics` before running the commands.

## Important Notes

- Each week maintains its own Python virtual environment.
- Install dependencies separately for each practical.
- Configuration files containing private credentials or local settings should not be committed.
- The `.venv` directories are excluded from Git.
- API pricing and provider limits used in Week 5 are illustrative planning assumptions, not guaranteed billing rates.

## Repository

GitHub: https://github.com/jaswanthbhaskar-elite/GenAI-2520030553-Jaswanthbhaskar

---

**Author:** Jaswanth Bhaskar  
**Project:** Generative AI Practical Labs – Weeks 1–5
