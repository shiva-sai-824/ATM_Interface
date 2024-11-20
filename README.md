# ATM Interface Project

## Overview
A Python-based ATM (Automated Teller Machine) interface built using Streamlit, providing basic banking functionalities like account creation, login, balance checking, deposits, withdrawals, and transaction history.

## Features
- User Account Management
  - Create new bank accounts
  - Secure PIN-based authentication
  - Unique account number generation

- Banking Transactions
  - Check account balance
  - Deposit funds
  - Withdraw funds
  - View transaction history

- Persistent Data Storage
  - Users data saved in JSON file
  - Transaction history tracking

## Prerequisites
- Python 3.8+
- Streamlit
- Required Python libraries:
  - streamlit
  - datetime
  - random
  - json
  - os

## Installation
1. Clone the repository:
   ```bash
   git clone https://github.com/yourusername/atm-interface.git
   cd atm-interface
   ```

2. Install required dependencies:
   ```bash
   pip install streamlit
   ```

## Running the Application
```bash
streamlit run main.py
```

## Project Structure
- `main.py`: Main Streamlit application
- `users.json`: Stores user account information
- `README.md`: Project documentation

## Security Features
- 4-digit PIN for account access
- Random account number generation
- Local JSON-based data storage

## Limitations
- Data persists only locally
- No advanced encryption
- Single-machine usage

## Contributing
1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## License
Distributed under the MIT License. See `LICENSE` for more information.
