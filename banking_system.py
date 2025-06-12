import os
from datetime import datetime

# File paths
ACCOUNT_FILE = "account.txt"
TRANSACTION_FILE = "transaction.txt"

# Function to generate a unique account number
def generate_account_number():
    if not os.path.exists(ACCOUNT_FILE) or os.stat(ACCOUNT_FILE).st_size == 0:
        return 1001 
    with open(ACCOUNT_FILE, "r") as file:
        lines = file.readlines()
       
        for line in reversed(lines):
            parts = line.strip().split(",")
            if len(parts) >= 1 and parts[0].isdigit():  
                last_account_number = int(parts[0])
                return last_account_number + 1
    return 1001  

# Function to create a new account
def create_account():
    print("=== Create Account ===")
    username = input("Enter your name: ")
    password = input("Enter a password: ")
    confirm_password = input("Confirm your password: ")

    if password != confirm_password:
        print("Passwords do not match. Try again.")
        return

    # Check if username already exists
    if os.path.exists(ACCOUNT_FILE):
        with open(ACCOUNT_FILE, "r") as file:
            for line in file:
                # Skip improperly formatted lines
                parts = line.strip().split(",")
                if len(parts) != 4:
                    continue
                account_number, existing_username, _, _ = parts
                if existing_username == username:
                    print("Username already exists. Try a different one.")
                    return

    # Generate a unique account number
    account_number = generate_account_number()

    # initial deposit
    while True:
        initial_deposit = input("Enter your initial deposit: ")
        if initial_deposit.isdigit() and int(initial_deposit) >= 0:
            initial_deposit = int(initial_deposit)
            break
        else:
            print("Invalid amount. Please enter a positive number.")

    # Save account details
    with open(ACCOUNT_FILE, "a") as file:
        file.write(f"{account_number},{username},{password},{initial_deposit}\n")
    print(f"Account created successfully! Your account number is {account_number}. (Save this for login)")

# Function to log in using account number
def login():
    print("=== Login ===")
    account_number = input("Enter your account number: ")
    password = input("Enter your password: ")

    # Check credentials
    if os.path.exists(ACCOUNT_FILE):
        with open(ACCOUNT_FILE, "r") as file:
            for line in file:
                # Skip improperly formatted lines
                parts = line.strip().split(",")
                if len(parts) != 4:
                    continue
                existing_account_number, _, existing_password, _ = parts
                if existing_account_number == account_number and existing_password == password:
                    print("Login successful!")
                    return account_number

    print("Invalid account number or password.")
    return None

# Function to deposit money
def deposit(account_number):
    print("=== Deposit Money ===")
    amount = input("Enter the amount to deposit: ")

    if not amount.isdigit() or int(amount) <= 0:
        print("Invalid amount. Please enter a positive number.")
        return

    amount = int(amount)
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")  # Get current date and time

    # Update balance in account file
    updated_lines = []
    with open(ACCOUNT_FILE, "r") as file:
        for line in file:
            # Skip improperly formatted lines
            parts = line.strip().split(",")
            if len(parts) != 4:
                continue
            existing_account_number, username, password, balance = parts
            if existing_account_number == account_number:
                balance = str(int(balance) + amount)
            updated_lines.append(f"{existing_account_number},{username},{password},{balance}\n")

    with open(ACCOUNT_FILE, "w") as file:
        file.writelines(updated_lines)

    # Record the transaction
    with open(TRANSACTION_FILE, "a") as file:
        file.write(f"{account_number},DEPOSIT,{amount},{timestamp}\n")
    print(f"Successfully deposited ${amount} on {timestamp}.")

# Function to view transaction history
def view_transaction_history(account_number):
    print("=== Transaction History ===")
    if not os.path.exists(TRANSACTION_FILE):
        print("No transactions found.")
        return

    found = False
    with open(TRANSACTION_FILE, "r") as file:
        for line in file:
            # Skip improperly formatted lines99
            parts = line.strip().split(",")
            if len(parts) != 4:
                continue
            transaction_account_number, transaction_type, amount, timestamp = parts
            if transaction_account_number == account_number:
                print(f"{timestamp} - {transaction_type}: ${amount}")
                found = True

    if not found:
        print("No transactions found for your account.")

# Main
def user_menu(account_number):
    while True:
        print(f"\n=== Welcome, Account {account_number}! ===")
        print("1. Deposit Money")
        print("2. View Transaction History")
        print("3. Logout")
        choice = input("Enter your choice: ")

        if choice == "1":
            deposit(account_number)
        elif choice == "2":
            view_transaction_history(account_number)
        elif choice == "3":
            print("Logging out...")
            break
        else:
            print("Invalid choice. Please try again.")

if __name__ == "__main__":

    if not os.path.exists(ACCOUNT_FILE) or os.stat(ACCOUNT_FILE).st_size == 0:
        with open(ACCOUNT_FILE, "w") as file:
            file.write("")  
    open(TRANSACTION_FILE, "a").close()
    main()


