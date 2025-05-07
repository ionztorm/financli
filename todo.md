# Todo

## Models

- [ ] add 'update()' method to Bank, Credit Card, Store Card, Bill, and Subscription models. This should allow users to make ammendments to accounts:

  - [x] Accounts
  - [x] Bank
    - [x] Model
    - [x] Tests
  - [x] Credit Card
    - [x] Model
    - [x] Tests
  - [x] Store Card
    - [x] Model
    - [x] Tests
  - [ ] Loans
    - [ ] Model
    - [ ] Tests
  - [ ] Pay Only
  - [ ] Subscriptions
    - [ ] Model
    - [ ] Tests
  - [ ] Bills
    - [ ] Model
    - [ ] Tests

- [ ] add 'edit()' to Transactions, in case a user makes a mistake when logging. This should consider that adjustments to the payment amount, or the source or destination accounts will require balance corrections.

- [ ] implement 'list()' on Controller to allow listing based on selected account types.

## CLI

- [ ] implement 'list' CLI parser. `list --account-type`. Include InquirerPy functionality for account type selection if subparser is not used.
- [ ] implement 'report' CLI parser `report --report-type`. Include InquirerPy functionality for report type selection if subparser is not used.

## Reporting

- [ ] implement exporting in CSV format
- [ ] implement PDF reporting
- [ ] implement CLI transaction filtering
