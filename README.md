# 💸 FinanCLI

**FinanCLI** is a command-line financial management tool designed to help you track, manage, and visualise your accounts and transactions — all from your terminal.

It aims to be:

- 🧾 A personal finance tracker
- 📊 A CLI-based budgeting and reporting tool
- 🔁 A full-featured interface for managing accounts and transactions

---

## 🚀 Features (in progress)

- ✅ Open, close, deposit, and withdraw from accounts
- ✅ Internal transfers between accounts
- ✅ SQLite-backed data persistence
- ✅ Validation and error handling with helpful messages
- ✅ Modular controller and model architecture
- 🧪 Unit tests for all major operations
- 🧱 Support for various account types:
  - 🏦 Bank Accounts
  - 💳 Credit Cards
  - 🏬 Store Cards
  - 💰 Loans
  - 🧾 Bills
  - 🔁 Subscriptions

Coming soon:

- 📦 CLI entry point with command routing
- 🧵 Interactive REPL and TUI (Text User Interface)
- 📄 PDF reports and CSV export
- 📋 Budgeting tools and financial summaries
- 📊 Pretty tables using `tabulate`

---

## ⚙️ Requirements

- Python 3.10+
- `sqlite3` (standard library)
- [`tabulate`](https://pypi.org/project/tabulate/) (planned)
- Future: PDF and CSV libraries (TBD)

---

## 🧰 Setup

1. Clone the repository:

   ```bash
   git clone https://github.com/your-username/financli.git
   cd financli
   ```

2. Create a virtual environment:

   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. Install dependencies (when `requirements.txt` is added):
   ```bash
   pip install -r requirements.txt
   ```

---

## 🧪 Running Tests

You can run the full test suite using the provided script:

```bash
./run_tests.sh
```

If you get a permission error, make it executable first:

```bash
chmod +x run_tests.sh
```

Alternatively, you can run tests manually with:

```bash
python -m unittest discover tests
```

---

## 📁 Project Structure (WIP)

```
financli/
├── core/
│   ├── controller.py       # Orchestrates actions on accounts
│   ├── exceptions.py       # Shared error types
│
├── features/
│   └── bank/
│       ├── model.py        # Bank account logic
│       ├── schema.py       # Table schema for SQLite
│       ├── exceptions.py   # Domain-specific errors
│
├── tests/
│   └── test_controller.py  # Unit tests for Controller
│
├── utils/
│   ├── helpers.py          # Error wrappers, etc.
│   ├── constants.py
│   └── types.py
│
├── run_tests.sh            # Bash script to run tests
└── README.md
```

---

## 🛣️ Roadmap

### ✅ Core Features

- [x] Deposit / Withdraw / Transfer
- [x] Validation and exception handling
- [x] Test coverage for core features
- [ ] CLI command interface
- [ ] TUI with curses or Textual
- [ ] CSV and PDF exports
- [ ] Reporting and summaries
- [ ] Budget tracking and projections

### 🧱 Account Type Support

#### 🏦 Bank Accounts

- [x] Open account
- [x] Close account
- [x] Deposit
- [x] Withdraw
- ✅ All tests passing

#### 💳 Credit Cards

- [ ] Open account
- [ ] Close account
- [ ] Deposit
- [ ] Withdraw

#### 🏬 Store Cards

- [ ] Open account
- [ ] Close account
- [ ] Deposit
- [ ] Withdraw

#### 💰 Loans

- [ ] Open account
- [ ] Close account
- [ ] Deposit
- [ ] Withdraw

#### 🧾 Bills

- [ ] Open account
- [ ] Close account
- [ ] Deposit
- [ ] Withdraw

#### 🔁 Subscriptions

- [ ] Open account
- [ ] Close account
- [ ] Deposit
- [ ] Withdraw

---

## 📄 Licence

[MIT](LICENSE) — do what you want, just give credit.  
Built with caffeine & clean code vibes ☕️

---

## ✨ Contributing

FinanCLI is in active development. Contributions are welcome as features stabilise! If you're interested in CLI UX, data visualisation, or financial tools — hop in!
