# 💸 FinanCLI

**FinanCLI** is a command-line financial management tool designed to help you track, manage, and visualize your accounts and transactions — all from your terminal.

It aims to be:

- 🧾 A personal finance tracker
- 📊 A CLI-based budgeting and reporting tool
- 🔁 A full-featured interface for managing accounts and transactions

---

## 🚀 Features

- ✅ Open, close, deposit, and withdraw from accounts
- ✅ Internal transfers between accounts
- ✅ SQLite-backed data persistence
- ✅ Validation and error handling with helpful messages
- ✅ Modular controller and model architecture
- 🧱 Support for various account types:
  - 🏦 Bank Accounts
  - 💳 Credit Cards
  - 🏬 Store Cards
  - 💰 Loans
  - 🧾 Bills
  - 🔁 Subscriptions
- 📦 CLI entry point with command routing
- 📄 PDF reports and CSV export
- 📋 Budgeting tools and financial summaries
- 📊 Tables using `tabulate`

---

## ⚙️ Requirements

- Python 3.10+
- `sqlite3` (standard library)
- [`tabulate`](https://pypi.org/project/tabulate/)
- [`reportlab`](https://pypi.org/project/reportlab/) (for PDF generation)
- [`pandas`](https://pypi.org/project/pandas/) (for CSV export)

---

## 🧰 Setup

1. Clone the repository:

   ```bash
   git clone https://github.com/your-username/financli.git
   cd financli
   ```

2. Create a virtual environment:

   ```bash
   python -m venv .venv
   source .venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. Install dependencies:

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

## 📁 Project Structure

```
financli/
├── core/
│   ├── controller.py               # Orchestrates actions on accounts
│   ├── db.py                       # Database connection and setup
│   ├── exceptions.py               # Shared error types
│   ├── main.py                     # Entry point for core logic
│   └── utility_service.py          # Provides utility functions for the controller
│
├── features/
│   ├── accounts/
│   │   ├── bank/
│   │   │   ├── exceptions.py       # Domain-specific errors for bank accounts
│   │   │   ├── model.py            # Bank account logic
│   │   │   └── schema.py           # Table schema for SQLite
│   │   ├── credit_card/
│   │   │   ├── exceptions.py       # Domain-specific errors for credit cards
│   │   │   ├── model.py            # Credit card account logic
│   │   │   └── schema.py           # Table schema for SQLite
│   ├── payable/
│   │   ├── bill/
│   │   │   ├── exceptions.py       # Domain-specific errors for bills
│   │   │   ├── model.py            # Bill logic
│   │   │   └── schema.py           # Table schema for SQLite
│   │   └── subscription/
│   │   │   ├── exceptions.py       # Domain-specific errors for subscriptions
│   │   │   ├── model.py            # Subscription logic
│   │   │   └── schema.py           # Table schema for SQLite
│
├── tests/
│   ├── test_bank_model.py          # Unit tests for Bank model
│   ├── test_base_model.py          # Unit tests for Base model
│   ├── test_bill_model.py          # Unit tests for Bill model
│   ├── test_controller.py          # Unit tests for Controller
│   ├── test_credit_card_model.py   # Unit tests for CreditCard model
│   ├── test_db_connectivity.py     # Unit tests for DB connectivity
│   ├── test_store_card_model.py    # Unit tests for StoreCard model
│   └── test_subscription_model.py  # Unit tests for Subscription model
│
├── utils/
│   ├── constants.py                # Constant values
│   ├── helpers.py                  # Error wrappers, etc.
│   ├── model_types.py              # Type definitions for models
│   └── types.py                    # Enum definitions
│
├── run_tests.sh                    # Bash script to run tests
├── main.py                         # Main entry point
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

- [x] Open account
- [x] Close account
- [x] Deposit
- [x] Withdraw
- ✅ All tests passing

#### 🏬 Store Cards

- [x] Open account
- [x] Close account
- [x] Deposit
- [x] Withdraw
- ✅ All tests passing

#### 💰 Loans

- [ ] Open account
- [ ] Close account
- [ ] Deposit

#### 🧾 Bills

- [x] Open account
- [x] Close account
- ✅ All tests passing

#### 🔁 Subscriptions

- [x] Open account
- [x] Close account
- ✅ All tests passing

---

## 📄 Licence

[MIT](LICENSE) — do what you want, just give credit. Built with caffeine & clean code vibes ☕️

---

## ✨ Contributing

FinanCLI is in active development. Contributions are welcome! If you're interested in CLI UX, data visualization, or financial tools — hop in!
