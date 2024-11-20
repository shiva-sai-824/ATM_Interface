import streamlit as st
import datetime
import random
import json
import os

class User:
    def __init__(self, name, account_number, pin, balance=1000):
        self.name = name
        self.account_number = account_number
        self.pin = pin
        self.balance = balance
        self.transaction_history = []

    def record_transaction(self, transaction_type, amount):
        timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        transaction = {
            "type": transaction_type,
            "amount": amount,
            "timestamp": timestamp
        }
        self.transaction_history.append(transaction)

class ATM:
    def __init__(self):
        self.users = {}
        self.load_users()

    def load_users(self):
        if os.path.exists('users.json'):
            with open('users.json', 'r') as f:
                user_data = json.load(f)
                for data in user_data:
                    user = User(data['name'], data['account_number'], data['pin'], data['balance'])
                    user.transaction_history = data.get('transaction_history', [])
                    self.users[user.account_number] = user

    def save_users(self):
        user_data = [{
            'name': user.name,
            'account_number': user.account_number,
            'pin': user.pin,
            'balance': user.balance,
            'transaction_history': user.transaction_history
        } for user in self.users.values()]
        
        with open('users.json', 'w') as f:
            json.dump(user_data, f, indent=4)

    def create_account(self, name, pin):
        account_number = str(random.randint(10000000, 99999999))
        while account_number in self.users:
            account_number = str(random.randint(10000000, 99999999))
        
        user = User(name, account_number, pin)
        self.users[account_number] = user
        self.save_users()
        return account_number

    def authenticate(self, account_number, pin):
        user = self.users.get(account_number)
        return user and user.pin == pin

    def check_balance(self, account_number):
        user = self.users.get(account_number)
        return user.balance

    def deposit(self, account_number, amount):
        user = self.users.get(account_number)
        if amount > 0:
            user.balance += amount
            user.record_transaction("DEPOSIT", amount)
            self.save_users()
            return True
        return False

    def withdraw(self, account_number, amount):
        user = self.users.get(account_number)
        if 0 < amount <= user.balance:
            user.balance -= amount
            user.record_transaction("WITHDRAWAL", amount)
            self.save_users()
            return True
        return False

    def get_transaction_history(self, account_number):
        user = self.users.get(account_number)
        return user.transaction_history

def reset_session_state():
    for key in list(st.session_state.keys()):
        del st.session_state[key]

def main():
    st.title("🏦 ATM Interface")
    
    # Initialize ATM
    if 'atm' not in st.session_state:
        st.session_state.atm = ATM()
    
    # Navigation
    if not st.session_state.get('logged_in', False):
        menu = ["Login", "Create Account"]
        choice = st.sidebar.selectbox("Navigation", menu)
        
        if choice == "Create Account":
            st.subheader("Create New Account")
            name = st.text_input("Enter Name")
            pin = st.text_input("Enter 4-digit PIN", type="password")
            
            if st.button("Create Account"):
                if len(pin) == 4 and pin.isdigit():
                    account_number = st.session_state.atm.create_account(name, pin)
                    st.success(f"Account created! Your account number is: {account_number}")
                else:
                    st.error("PIN must be 4 digits")
        
        elif choice == "Login":
            st.subheader("Login")
            account_number = st.text_input("Enter Account Number")
            pin = st.text_input("Enter PIN", type="password")
            
            if st.button("Login"):
                if st.session_state.atm.authenticate(account_number, pin):
                    st.session_state.account_number = account_number
                    st.session_state.logged_in = True
                    st.rerun()
                else:
                    st.error("Invalid Account Number or PIN")
    
    if st.session_state.get('logged_in', False):
        st.sidebar.title("Banking Menu")
        
        # Balance Display
        balance = st.session_state.atm.check_balance(st.session_state.account_number)
        st.sidebar.success(f"Current Balance: ${balance}")
        
        # Transaction Options
        transaction_type = st.sidebar.radio("Select Transaction", 
                                            ["Check Balance", "Deposit", "Withdraw", "Transaction History"])
        
        if transaction_type == "Check Balance":
            st.subheader("Balance Information")
            st.success(f"Your current balance is: ${balance}")
        
        elif transaction_type == "Deposit":
            st.subheader("Deposit Funds")
            amount = st.number_input("Enter Deposit Amount", min_value=0.0, step=10.0)
            if st.button("Deposit"):
                if st.session_state.atm.deposit(st.session_state.account_number, amount):
                    st.success(f"Deposited ${amount}")
                else:
                    st.error("Invalid Deposit Amount")
        
        elif transaction_type == "Withdraw":
            st.subheader("Withdraw Funds")
            amount = st.number_input("Enter Withdrawal Amount", min_value=0.0, step=10.0)
            if st.button("Withdraw"):
                if st.session_state.atm.withdraw(st.session_state.account_number, amount):
                    st.success(f"Withdrawn ${amount}")
                else:
                    st.error("Insufficient Funds")
        
        elif transaction_type == "Transaction History":
            st.subheader("Transaction History")
            history = st.session_state.atm.get_transaction_history(st.session_state.account_number)
            if history:
                for transaction in history:
                    st.write(f"**{transaction['type']}**: ${transaction['amount']} on {transaction['timestamp']}")
            else:
                st.info("No transaction history available.")
        
        # Logout
        if st.sidebar.button("Logout"):
            reset_session_state()
            st.rerun()

if __name__ == "__main__":
    main()
