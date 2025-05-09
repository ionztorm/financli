# FinanCLI

**FinanCLI** is a command-line financial management tool designed to help you track, manage, and visualize your accounts and transactions — all from your terminal.

It aims to be:

- A personal finance tracker
- A CLI-based budgeting and reporting tool
- A full-featured interface for managing accounts and transactions

---

## Features

- Open, close, deposit, and withdraw from accounts
- Internal transfers between accounts
- SQLite-backed data persistence
- Validation and error handling with helpful messages
- Modular controller and model architecture
- Support for various account types:
  - Bank Accounts
  - Credit Cards
  - Store Cards
  - Loans
  - Bills
  - Subscriptions
- CLI entry point with command routing
- PDF reports and CSV export
- Budgeting tools and financial summaries
- Tables using `tabulate`

---

## Requirements

- Python 3.10+
- `sqlite3` (standard library)
- [`tabulate`](https://pypi.org/project/tabulate/)
- [`reportlab`](https://pypi.org/project/reportlab/) (for PDF generation)
- [`InquirerPy`](https://pypi.org/project/InquirerPy/) (for interactive CLI prompts)

---

## Setup

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

## Running Tests

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

## Project Structure

```
financli/
├── core/
│   ├── __init__.py                  # Package initializer
│   ├── base_model.py                # Base model for inheritance
│   ├── cli/                         # CLI-related scripts
│   │   ├── __init__.py              # Package initializer for CLI
│   │   ├── close.py                 # Close operation script
│   │   ├── open.py                  # Open operation script
│   │   ├── transaction.py           # Transaction operations
│   │   ├── update.py                # Update operations
│   │   ├── imports.py               # Import JSON or CSV
│   │   └── export.py                # Export to JSON, CSV, or TXT
│   ├── controller.py                # Orchestrates actions on accounts
│   ├── data/                        # Database and related files
│   │   └── financli.db              # SQLite database file
│   ├── db.py                        # Database connection and setup
│   ├── exceptions/                  # Exception handling
│   ├── exceptions.py                # Shared error types
│   ├── main.py                      # Entry point for core logic
│   ├── transaction_service.py       # Transaction-related functions
│   ├── utility_service.py           # Utility functions for controller
│   └── utils/                       # Utility-related files
│       ├── __init__.py              # Package initializer for utils
│       ├── constants.py             # Constant values
│       ├── helpers.py               # Helper functions and error wrappers
│       ├── model_types.py           # Type definitions for models
│       └── types.py                 # Enum definitions
├── data/                            # Database storage folder
│   └── financli.db                  # SQLite database file
├── features/
│   ├── accounts/                    # Account-related features
│   │   ├── __init__.py              # Package initializer for accounts
│   │   ├── bank/                    # Bank account features
│   │   │   ├── exceptions.py       # Domain-specific errors for bank accounts
│   │   │   ├── model.py            # Bank account logic
│   │   │   └── schema.py           # Table schema for SQLite
│   │   ├── credit_card/             # Credit card account features
│   │   │   ├── exceptions.py       # Domain-specific errors for credit cards
│   │   │   ├── model.py            # Credit card account logic
│   │   │   └── schema.py           # Table schema for SQLite
│   │   ├── exceptions.py           # Domain-specific errors for accounts
│   │   ├── model.py                # Common account logic
│   │   └── schema.py               # Common table schema for SQLite
│   ├── banks/                       # Bank-related features
│   │   └── tests/                   # Tests for bank features
│   │       └── test_bank.py         # Bank feature tests
│   ├── payable/                     # Payable-related features
│   │   ├── __init__.py              # Package initializer for payable
│   │   ├── bill/                    # Bill-related features
│   │   │   ├── exceptions.py       # Domain-specific errors for bills
│   │   │   ├── model.py            # Bill logic
│   │   │   └── schema.py           # Table schema for SQLite
│   │   ├── exceptions.py           # Domain-specific errors for payable
│   │   └── subscription/           # Subscription-related features
│   │       ├── exceptions.py       # Domain-specific errors for subscriptions
│   │       ├── model.py            # Subscription logic
│   │       └── schema.py           # Table schema for SQLite
│   ├── transactions/                # Transaction-related features
│   │   ├── exceptions.py           # Domain-specific errors for transactions
│   │   ├── model.py                # Transaction logic
│   │   └── schema.py               # Table schema for SQLite
│   └── tests/                       # Tests for features
│       ├── test_bank_model.py       # Unit tests for Bank model
│       ├── test_base_model.py       # Unit tests for Base model
│       ├── test_bill_model.py       # Unit tests for Bill model
│       ├── test_controller.py       # Unit tests for Controller
│       ├── test_credit_card_model.py# Unit tests for CreditCard model
│       ├── test_db_connectivity.py  # Unit tests for DB connectivity
│       ├── test_store_card_model.py # Unit tests for StoreCard model
│       └── test_subscription_model.py# Unit tests for Subscription model
├── LICENSE                          # License for the project
├── main.py                          # Main entry point
├── plan.md                          # Project planning and roadmap
├── README.md                        # Project documentation
├── run_tests.sh                     # Bash script to run tests
├── test.db                          # Test database file
└── tui/                             # Text-based UI files
```

---

## Roadmap

### Core Features

- [x] Deposit / Withdraw / Transfer
- [x] Validation and exception handling
- [x] Test coverage for core features
- [x] CLI command interface
- [x] CSV exports
- [x] JSON exports
- [ ] PDF exports
- [ ] Reporting and summaries

### Account Type Support

#### Bank Accounts

- [x] Open account
- [x] Close account
- [x] Deposit
- [x] Withdraw
- [x] Update
- All tests passing

#### Credit Cards

- [x] Open account
- [x] Close account
- [x] Deposit
- [x] Withdraw
- [x] Update
- All tests passing

#### Store Cards

- [x] Open account
- [x] Close account
- [x] Deposit
- [x] Withdraw
- [x] Update
- All tests passing

#### Loans

- [x] Open account
- [x] Close account
- [x] Deposit
- [x] Update

#### Bills

- [x] Open account
- [x] Close account
- [x] Update
- All tests passing

#### Subscriptions

- [x] Open account
- [x] Close account
- [x] Update
- All tests passing

### Transactions

- [x] Log transaction
- [ ] Edit transaction
- [ ] Delete transaction

---

## Licence

[MIT](LICENSE) — do what you want, just give credit. Built with caffeine & clean code vibes

---

## Contributing

FinanCLI is in active development. Contributions are welcome! If you're interested in CLI UX, data visualization, or financial tools — hop in!
