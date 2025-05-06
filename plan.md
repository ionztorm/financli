# Planning

## Architecture

-   **Base Model**

    -   Provides common database interaction methods (create, read, update, delete).
    -   Handles basic validation.
    -   Defines abstract methods for account-specific logic.

-   **Account Models (Bank, CreditCard, StoreCard, Bill, Subscription)**

    -   Inherit from Base Model.
    -   Implement account-specific validation and logic.
    -   Define relationships between accounts and transactions.
    -   Handle domain-specific error wrapping.
    -   Compare withdrawals against balances, taking into account overdrafts and credit limits.
    -   Compare deposits to credit cards & store cards against balance to ensure accounts don't go into debit.
    -   Ensure payments to bills and subscriptions are not greater than or less than monthly charges.

-   **Controller**

    -   Orchestrates actions between the CLI layer and the models.
    -   Handles data validation and error handling.
    -   Manages database transactions.
    -   Selects appropriate models based on user input.
    -   Uses `utility_service.py` for common tasks.

-   **CLI Layer (main.py)**

    -   Accepts user input and passes it to the Controller.
    -   Displays output to the user.
    -   Handles command-line argument parsing.

-   **Database (db.py)**

    -   Manages the SQLite database connection.
    -   Provides methods for executing SQL queries.
    -   Handles database setup and migrations.

-   **Utility Service (utility_service.py)**

    -   Provides utility functions for the controller, such as formatting data and generating reports.

-   **Exceptions (exceptions.py, features/\*/exceptions.py)**
    -   Defines custom exception classes for the application.
    -   Provides a consistent way to handle errors.
    -   Domain specific error wrapping.

## CLI Data Structure

### Data Structure from CLI - transactions

```py
DATA = {
    "transaction_type",        # all transactions
    "source_id",               # all transactions
    "source_type",             # all transactions
    "amount",                  # all transactions
    "destination_id",          # transfers
    "destination_type",        # transfers
}
```

### Data Structure from CLI - open()

```py
DATA = {
    "account_type",            # all
    "provider",                # all
    "alias",                   # bank
    "balance",                 # all
    "limiter",                 # bank, credit card, store card
    "monthly_charge",          # bill, subscription
}
```

### Data Structure from CLI - close() list() - id optional for list

```py
DATA = {
    "account_type",            # all
    "account_id"               # close(), list() if getting 1 record
}
```
