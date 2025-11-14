import os
# Updated Account class with encapsulation for transactions and history
class Account:
    __nbAccounts = 0

    def __init__(self, acc_id=None, balance=0.0, owner=None):
        Account.__nbAccounts += 1
        self.__code = Account.__nbAccounts
        self.id = acc_id if acc_id is not None else f"ACC{self.__code}"
        self.balance = float(balance)
        self.history = [f"Created with {self.balance:.2f}"]
        self.__owner = owner

    def get_code(self): return self.__code
    def get_balance(self): return self.balance
    def get_owner(self): return self.__owner

    def deposit(self, amt):
        if amt <= 0:
            raise ValueError("Amount must be positive")
        self.balance += amt
        self.history.append(f"Deposit {amt:.2f}")

    def withdraw(self, amt):
        if amt <= 0:
            raise ValueError("Amount must be positive")
        if amt > self.balance:
            raise ValueError("Insufficient balance")
        self.balance -= amt
        self.history.append(f"Withdraw {amt:.2f}")

    def record_transfer_out(self, amt, target):
        self.balance -= amt
        self.history.append(f"Transfer out {amt:.2f} to {target}")

    def record_transfer_in(self, amt, source):
        self.balance += amt
        self.history.append(f"Transfer in {amt:.2f} from {source}")

    def display(self):
        print(f"Account Code: {self.__code}, ID: {self.id}, Balance: {self.balance:.2f}")
    
    @staticmethod
    def displayNbAccounts():
        print("Total accounts created:", Account.__nbAccounts)

# Updated Client class
class Client:
    def __init__(self, cin, first, last, tel=""):
        self.cin = cin
        self.first = first
        self.last = last
        self.tel = tel
        self.accounts = []

    def add_account(self, acc):
        self.accounts.append(acc)

    def display(self):
        print(f"CIN: {self.cin}, Name: {self.first} {self.last}, Tel: {self.tel}")

# Bank class to connect the work and manage clients and accounts
class Bank:
    def __init__(self):
        self.clients = []

    def find_client(self, cin):
        return next((c for c in self.clients if c.cin == cin), None)
# to order account selection and numerate them
    def _select_account(self, client, prompt="Select account number: "):
        if not client.accounts:
            print("No accounts.")
            return None
        for i, a in enumerate(client.accounts, 1):
            print(f"{i}. {a.id} - {a.balance:.2f}")
        try:
            sel = int(input(prompt).strip())
            if 1 <= sel <= len(client.accounts):
                return client.accounts[sel - 1]
        except ValueError:
            pass
        print("Invalid selection.")
        return None
# this is the create account function where new clients can create their account
    def create_account(self):
        cin = input("Client CIN: ").strip()
        client = self.find_client(cin)
        if not client:
            print("New client. Enter details:")
            first = input("First name: ").strip()
            last = input("Last name: ").strip()
            tel = input("Telephone: ").strip()
            client = Client(cin, first, last, tel)
            self.clients.append(client)
        acc_id = input("Account ID: ").strip()
        try:
            bal = float(input("Initial balance (default 0): ").strip() or 0)
        except ValueError:
            print("Invalid amount.")
            return
        acc = Account(acc_id, bal, owner=client)
        client.add_account(acc)
        print(f"Account {acc_id} created for {client.cin} with {acc.balance:.2f}")
# this is the login function where client can access their account
    def login(self):
        cin = input("Client CIN: ").strip()
        client = self.find_client(cin)
        if not client:
            print("Client not found.")
            return
        acc = self._select_account(client)
        if not acc:
            return
        self._session(client, acc)
# i've added session management for client operations just to make it more complete and professional
    def _session(self, client, acc):
        while True:
            os.system('cls' if os.name == 'nt' else 'clear')
            print("\n1 Deposit\n2 Withdraw\n3 Transfer\n4 History\n5 Logout\n")
            choice = input("Choice: ").strip()
            if choice == "1":
                try:
                    amt = float(input("Amount to deposit: ").strip())
                except ValueError:
                    print("Invalid amount.")
                    input("Press Enter to continue...")
                    continue
                if amt <= 0:
                    print("Must be positive.")
                    input("Press Enter to continue...")
                    continue
                acc.deposit(amt)
                print(f"New balance: {acc.balance:.2f}")
                input("Press Enter to continue...")
            elif choice == "2":
                try:
                    amt = float(input("Amount to withdraw: ").strip())
                except ValueError:
                    print("Invalid amount.")
                    input("Press Enter to continue...")
                    continue
                if amt <= 0:
                    print("Must be positive.")
                    input("Press Enter to continue...")
                    continue
                if amt > acc.balance:
                    print("Insufficient funds.")
                    input("Press Enter to continue...")
                    continue
                acc.withdraw(amt)
                print(f"New balance: {acc.balance:.2f}")
                input("Press Enter to continue...")
            elif choice == "3":
                tgt_cin = input("Target CIN: ").strip()
                tgt_client = self.find_client(tgt_cin)
                if not tgt_client:
                    print("Target client not found.")
                    input("Press Enter to continue...")
                    continue
                tgt = self._select_account(tgt_client, "Select target account number: ")
                if not tgt:
                    input("Press Enter to continue...")
                    continue
                try:
                    amt = float(input("Amount to transfer: ").strip())
                except ValueError:
                    print("Invalid amount.")
                    input("Press Enter to continue...")
                    continue
                if amt <= 0:
                    print("Must be positive.")
                    input("Press Enter to continue...")
                    continue
                if amt > acc.balance:
                    print("Insufficient funds.")
                    input("Press Enter to continue...")
                    continue
                acc.record_transfer_out(amt, f"{tgt_client.cin}:{tgt.id}")
                tgt.record_transfer_in(amt, f"{client.cin}:{acc.id}")
                print(f"Transferred {amt:.2f}. Source balance: {acc.balance:.2f}")
                input("Press Enter to continue...")
            elif choice == "4":
                print(f"History for {acc.id}:")
                for h in acc.history:
                    print("-", h)
                input("Press Enter to continue...")
            elif choice == "5":
                print("Logged out.")
                input("Press Enter to continue...")
                break
            else:
                print("Invalid choice.")
                input("Press Enter to continue...")
# to list all clients
    def list_clients(self):
        if not self.clients:
            print("No clients.")
            return
        for c in self.clients:
            print(f"{c.cin}: {c.first} {c.last} - {c.tel} ({len(c.accounts)} accounts)")
# Main program to run the banking system
def main():
    bank = Bank()
    menu = "\n1 Create Account\n2 Login\n3 List Clients\n4 Exit\n"
    while True:
        os.system('cls')
        print(menu)
        choice = input("Choice: ").strip()
        if choice == "1":
            bank.create_account()
            input("Press Enter to continue...")
        elif choice == "2":
            bank.login()
            input("Press Enter to continue...")
        elif choice == "3":
            bank.list_clients()
            input("Press Enter to continue...")
        elif choice == "4":
            print("Bye")
            break
        else:
            continue

main()
# i've updated the Account and Client classes to use encapsulation for sensitive attributes.
# i've used help of AIto write syntax but i coded logic , functions , defs and structure myself