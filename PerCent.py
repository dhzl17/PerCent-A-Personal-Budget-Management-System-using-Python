#Personal Budget Management System
#IMPORTS
import sqlite3  #database
import time  # To retrieve timestamp in the generate report

#Database Connection
con = sqlite3.connect('PerCent.db')
cur = con.cursor()

#To initialize database tables if they don't exist yet
cur.execute('''CREATE TABLE IF NOT EXISTS user (
                user_id INTEGER PRIMARY KEY AUTOINCREMENT,
                username TEXT NOT NULL UNIQUE, 
                password TEXT NOT NULL,
                email TEXT,
                phone_number TEXT)''')

cur.execute('''CREATE TABLE IF NOT EXISTS category (
                category_id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                type TEXT)''')

cur.execute('''CREATE TABLE IF NOT EXISTS account (
                account_id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER NOT NULL,
                account_type TEXT,
                FOREIGN KEY(user_id) REFERENCES user(user_id))''')

cur.execute('''CREATE TABLE IF NOT EXISTS transactions(
                transaction_id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER NOT NULL,
                category_id INTEGER, 
                account_id INTEGER NOT NULL,
                amount REAL NOT NULL CHECK (amount >= 0), 
                transaction_type TEXT, 
                timestamp TEXT,
                FOREIGN KEY(user_id) REFERENCES user(user_id),
                FOREIGN KEY(category_id) REFERENCES category(category_id),
                FOREIGN KEY(account_id) REFERENCES account(account_id))''')
con.commit()

#CLASSES - About/FAQ/User
#About class for displaying program info
class About:
    @staticmethod
    #THIS FUNCTION IS USED TO DISPLAY INFORMATIONS ABOUT THE PROGRAM
    def display_info():
        print("\n+===========================================================+")
        print("|Program Title: PerCent: A Personal Budget Management System|")
        print("+===========================================================+")
        print("|            Programmer: Denise Hazelyn L. Jumig            |")
        print("| Goal of the Program:                                      |")
        print("|- To help users manage their personal finances.            |")
        print("|- To track income, expenses, and savings.                  |")
        print("| Benefits:                                                 |")
        print("|- Simplifies budgeting by categorizing income and expenses.|")
        print("|- Provides reports on monthly savings and budget status.   |")
        print("|- Helps users make informed financial decisions.           |")
        print("+===========================================================+")

class FAQ:
    @staticmethod
    #====================================FUNCTIONS=====================================
    #THESE FUNCTION CONTAINS FREQUENTLY ASKED QUESTIONS FOR USER GUIDE AND INSTRUCTIONS
    def display_FAQ():
        print("\n+============================================================+")
        print("|                   Frequently Asked Questions               |")
        print("+============================================================+")
        print("                Choose an option for more details:")
        print("[1.] How register an account")
        print("[2.] How to login to your account")
        print("[3.] How to add an income")
        print("[4.] How to add an expense")
        print("[5.] How to generate monthly report")
        print("[6.] How to view about information")
        print("[0.] Exit FAQ")

        choice = input("\nEnter your choice: ")

        if choice == '1':
            print("\n================= FAQ: Register an Account ================")
            print("To register an account, enter a unique username and a password.")
            print("Once registered, you can use these credentials to log in and\nstart tracking your budget.")
        elif choice == '2':
            print("\n================= FAQ: Login to your Account ================")
            print("To log in, enter your registered username and password.")
            print("Once logged in, you can start adding income, expenses,\nand view your monthly report.")
        elif choice == '3':
            print("\n================= FAQ: Add Income ================")
            print("To add income, you need to specify the amount of income.")
            print("Income can be from salary, gift, or any other source of income.")
        elif choice == '4':
            print("\n================= FAQ: Add Expense ================")
            print("To add an expense, choose a category\n(e.g., Food, Transportation, Rent, etc.).")
            print("Enter the amount spent under that category. Make sure\nthe category is valid.")
        elif choice == '5':
            print("\n================= FAQ: Generate Monthly Report ================")
            print("To generate a monthly report, simply choose the 'Generate Report'\noption.")
            print("This will show a summary of your income, expenses, and savings\nfor the current month.")
        elif choice == '6':
            print("\n================= FAQ: About Information ================")
            print("The 'About' section provides information about the program,\nits goals, and benefits.")
            print("It gives the user an overview of what the Personal Budget\nManagement System is designed to do.")
        elif choice == '0':
            print("                          Exiting FAQ.")
        else:
            print("Invalid choice. Please choose a number between 0 and 6.")

#User class for account registration and login
class User:
    #=============================================================FUNCTIONS============================================================
    #THESE FUNCTIONS CONTAINS USER RELATED FUNCTIONALITIES INCLUDING REGISTRATION, LOGIN, ADDING INCOME/EXPENSES AND GENERATING REPORT
    def __init__(self, username, password, email=None, phone_number=None):
        self.username = username
        self.password = password
        self.email = email
        self.phone_number = phone_number
        self.user_id = self.get_user_id()
        self.category = self.get_category()
        self.account = self.get_account()
        self.expense = []

    def get_user_id(self):  #To get user ID based on username
        cur.execute("SELECT user_id FROM user WHERE username=?", (self.username,))
        user = cur.fetchone()
        return user[0] if user else None

    def get_category(self): #Returns categories as a dictionary of ID and name
        cur.execute("SELECT * FROM category")
        return {category[0]: category[1] for category in cur.fetchall()}

    def get_account(self): #Returns user's accounts as a dictionary of ID and account type
        cur.execute("SELECT * FROM account WHERE user_id=?", (self.user_id,))
        return {account[0]: account[2] for account in cur.fetchall()}

    def register(self, username, password, email, phone_number): #Function for user registration
        cur.execute("SELECT * FROM user WHERE username=?", (username,))
        if cur.fetchone():
            print("\n               Username already exists. Try again.")
        else:
            cur.execute("INSERT INTO user (username, password, email, phone_number) VALUES (?, ?, ?, ?)", 
                        (username, password, email, phone_number))
            con.commit()
            print("\n                    You are now registered!")

    def login(self, username, password): #Fucntion for login
        cur.execute("SELECT * FROM user WHERE username=? AND password=?", (username, password))
        if cur.fetchone():
            print("\n+============================================================+")
            print("| Welcome to PerCent, your Personal Budget Management System |")
            print("|             We aim to make your every cent count!          |")
            print("+============================================================+")
            return User(username, password)
        else:
            print("\n                     Invalid credentials.")
            return None

    def update_user_info(self, new_email=None, new_phone_number=None): #Function to update user informations
        if new_email:
            cur.execute("UPDATE user SET email=? WHERE username=?", (new_email, self.username))
            print(f"Email updated to: {new_email}")
        if new_phone_number:
            cur.execute("UPDATE user SET phone_number=? WHERE username=?", (new_phone_number, self.username))
            print(f"Phone number updated to: {new_phone_number}")
        con.commit()

    def update_transactions(self, transaction_id, new_amount=None, new_category=None): #Function to update user transaction records"
        if new_amount:
            cur.execute("UPDATE transactions SET amount=? WHERE id=? AND username=?", (new_amount, transaction_id, self.username))
            print(f"Transaction ID {transaction_id} updated with new amount: {new_amount}")
        if new_category:
            category_id = self.get_category_id_by_name(new_category)
            cur.execute("UPDATE transactions SET category_id=? WHERE id=? AND username=?", (category_id, transaction_id, self.username))
            print(f"Transaction ID {transaction_id} updated with new category: {new_category}")
        con.commit()

    def delete_transactions(self, transaction_id): 
        cur.execute("SELECT * FROM transactions WHERE id=? AND username=?", (transaction_id, self.username))
        if cur.fetchone():  # If the transaction exists
            cur.execute("DELETE FROM transactions WHERE id=? AND username=?", (transaction_id, self.username))
            con.commit()  # Save the changes to the database
            print(f"Transaction ID {transaction_id} has been deleted.")
        else:
            print(f"Transaction ID {transaction_id} not found or does not belong to {self.username}.")


    def select_account(self, account_type): #Function to get account ID based on account type
        for account_id, acc_type in self.account.items():
            if acc_type.lower() == account_type.lower():
                return account_id
        cur.execute("INSERT INTO account (user_id, account_type) VALUES (?, ?)", (self.user_id, account_type))
        con.commit()
        account_id = cur.lastrowid
        self.account[account_id] = account_type
        return account_id

    def get_category_id_by_name(self, category_name): #Function to get category ID by category name
        cur.execute("SELECT category_id FROM category WHERE name=?", (category_name,))
        category = cur.fetchone()
    
        if category is None: 
            # Option to automatically create the category if it doesn't exist
            cur.execute("INSERT INTO category (name, type) VALUES (?, 'expense')", (category_name,)) 
            con.commit()
            return cur.lastrowid  # Return the ID of the newly created category
        else:
            return category[0]

    def add_income(self, amount, account_type, category_name):
        if amount > 0:
            account_id = self.select_account(account_type)
            category_id = self.get_category_id_by_name(category_name)
        
            if category_id is None:
                print(f"Category '{category_name}' not found. Please ensure it exists.")
                return

            cur.execute("INSERT INTO transactions (user_id, category_id, account_id, amount, transaction_type, timestamp) VALUES (?, ?, ?, ?, ?, ?)",
                    (self.user_id, category_id, account_id, amount, 'income', time.ctime()))
            con.commit()
            print(f"Income added: {amount} through {account_type} in category {category_name}\n")
            
        else:
            print("Amount must be a positive number.")

    def add_expense(self, category_name, amount, account_type): #Function to add expense with specified aaccount and category name
        if amount > 0 and category_name:
            account_id = self.select_account(account_type)
            category_id = self.get_category_id_by_name(category_name)
            
            if category_id is None:
                print(f"Category '{category_name}' not found. Please ensure it exists.")
                return
        
            cur.execute("INSERT INTO transactions (user_id, category_id, account_id, amount, transaction_type, timestamp) VALUES (?, ?, ?, ?, ?, ?)",
                    (self.user_id, category_id, account_id, amount, 'expense', time.ctime()))
            con.commit()
            print(f"Expense added: {amount} for {category_name} using {account_type}\n")
        else:
            print("Invalid category or amount.")

    # JOIN method: Fetch transactions with user, category, and account information
    def join_transactions(self):
        query = '''
            SELECT t.transaction_id, t.amount, t.transaction_type, t.timestamp,
                   c.category_id, c.name as category_name, a.account_type
            FROM transactions t
            JOIN category c ON t.category_id = c.category_id
            JOIN account a ON t.account_id = a.account_id
            WHERE t.user_id = ?
            ORDER BY t.timestamp DESC
        '''
        cur.execute(query, (self.user_id,))
        return cur.fetchall()

    def generate_report(self): #Function to generate monthly report of income, expenses and savings
        total_income = 0
        total_expenses = 0
        category_totals = {}
       
        cur.execute("SELECT SUM(amount) FROM transactions WHERE transaction_type = 'income'") # To calculate thee total of income 
        total_income = cur.fetchone()[0] or 0.0  

        cur.execute("SELECT SUM(amount) FROM transactions WHERE transaction_type = 'expense'") #To calculate the expenses
        total_expenses = cur.fetchone()[0] or 0.0  

        cur.execute("SELECT COUNT(*) FROM transactions") # To calculate the total number of transactions in the budget report
        total_transaction = cur.fetchone()[0]  

        cur.execute("SELECT AVG(amount) FROM transactions WHERE transaction_type = 'income'") # To calculate the average income in budget report
        avg_income = cur.fetchone()[0] or 0.0  
        
        print("\n+============================================================+")
        print("|                        Budget Report                       |")
        print("+============================================================+")
        
        transactions = self.join_transactions()
        for transaction in transactions:  #Loop for the transaction calculations
            transaction_id, amount, transaction_type, timestamp, category_id, category_name, account_type = transaction
            
            if transaction_type == "expense":
                category_totals[category_name] = category_totals.get(category_name, 0) + amount
                print(f"Added an Expense of Php {amount:.2f} on {timestamp}")
            else:
                print(f"Added an Income of Php {amount:.2f} on {timestamp}")
        
        print("______________________________________________________________")
        print(f"\nTotal Income: {total_income:.2f}")
        print(f"Total Expenses: {total_expenses:.2f}")
        print(f"Total Transactions: {total_transaction}")
        print(f"Average Income: Php {avg_income:.2f}")
        print("______________________________________________________________")
        print("\n+============================================================+")
        print("|                     Expense by Categories                  |")
        print("+============================================================+")
        
        for category, amount in category_totals.items():
            print(f"{category:} Php {amount:.2f}")
        
        #FOR CALCULATING SAVINGS/BUDGET EXCESS
        remaining_budget = total_income - total_expenses
        if remaining_budget > 0:
            print(f"\nYou have saved: Php {remaining_budget:.2f} this month.")
            print("____________________________________________________________")
        elif remaining_budget < 0:
            print(f"\nYou have exceeded your budget by: Php {-remaining_budget:.2f}.")
            print("____________________________________________________________")
        else:
            print("\nYou have no savings or excess this month.")
            print("____________________________________________________________")


def main(): #Main program flow
    while True:
        print("\n+============================================================+")
        print("|                          Main Menu                         |")
        print("+============================================================+")
        print("                   Please choose an option:                   ")
        print("[1.] Register")
        print("[2.] Login")
        print("[3.] FAQ")
        print("[4.] About")
        print("[5.] Exit")

        choice = input("\nEnter your choice: ")

        if choice == '1':       #Create Option
            print("\n+============================================================+")
            print("|                     Account Registration                   |")
            print("+============================================================+\n")
            username = input("Enter username: ")
            password = input("Enter password: ")
            email = input("Enter email: ")
            phone_number = input("Enter phone number: +63")
            user = User(username, password)
            user.register(username, password, email, phone_number)

        elif choice == '2':     #Read Option
            username = input("Enter username: ")
            password = input("Enter password: ")
            user = User(username, password)
            logged_in_user = user.login(username, password)
            if logged_in_user:
                while True:
                    print("                       Choose an option:")
                    print("[1.] Add Income")
                    print("[2.] Add Expense")
                    print("[3.] Generate Monthly Report")
                    print("[4.] Update Information")
                    print("[5.] Delete Information")
                    print("[6.] Logout")

                    sub_choice = input("\nEnter your choice: ")

                    if sub_choice == '1':           #Create Option
                        amount = float(input("Enter income amount: "))
                        account_type = input("Enter account type (Bank, Cash, Credit): ")
                        category_name = input("Enter income category (Allowance,Salary, etc.): ").strip()
                        logged_in_user.add_income(amount, account_type, category_name)
                    elif sub_choice == '2':         #Create option
                        category_name = input("Enter expense category (Food, Rent, etc.): ").strip()
                        amount = float(input("Enter expense amount: "))
                        account_type = input("Enter account type (Bank, Cash, Credit): ").strip()
                        logged_in_user.add_expense(category_name, amount, account_type)
                    elif sub_choice == '3':         #Read Option
                        logged_in_user.generate_report()
                    elif sub_choice == '4':         #Update options
                        print("Update Options:")
                        print("[1.] Update User Email or Phone Number")
                        print("[2.] Update a Transaction")
                        update_choice = input("Choose what to update: ")
                        if update_choice == '1':
                            new_email = input("Enter new email (leave blank if no change): ")
                            new_phone_number = input("Enter new phone number (leave blank if no change): ")
                            logged_in_user.update_user_info(new_email, new_phone_number)
                        elif update_choice == '2':
                            transaction_id = int(input("Enter Transaction ID to update: "))
                            new_amount = float(input("Enter new amount (leave blank if no change): ") or 0)
                            new_category = input("Enter new category (leave blank if no change): ")
                            logged_in_user.update_transaction(transaction_id, new_amount, new_category)
                    elif sub_choice == '5':         #Delete option
                        print("Delete Options:")
                        print("[1.] Delete a Transaction")
                        delete_choice = input("Choose what to delete: ")
                        if delete_choice == '1':
                            transaction_id = int(input("Enter Transaction ID to delete: "))
                            logged_in_user.delete_transaction(transaction_id)

                    elif sub_choice == '6':
                        print("\n                        Logging Out...")
                        break
                    else:
                        print("Invalid choice. Please try again.")

        elif choice == '3':
            FAQ.display_FAQ()         #To display the FAQ informations
        elif choice == '4':             #To display the about informations
            About.display_info()
        elif choice == '5':             #To exit the program
            print("\n+============================================================+")
            print("|                  Thank you for using Percent.              |")
            print("|             We aim to make your every cent count!          |")
            print("+============================================================+")
            break
        else:
            print("Invalid choice. Please try again.")

if __name__ == '__main__':
    main()
    