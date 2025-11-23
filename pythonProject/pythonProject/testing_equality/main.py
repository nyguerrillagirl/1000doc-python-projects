# This is a sample Python script.

# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.

class BankAccount:
    def __init__(self, acct_id, name, balance):
        self.acct_id = acct_id
        self.name = name
        self.balance = balance

    def __eq__(self, other):
        return (self.acct_id == other.acct_id) and (type(self) == type(other))

class SavingsAccount(BankAccount):
    pass

class CheckingAccount(BankAccount):
    pass






# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    # Create a SavingsAccount
    sa1 = SavingsAccount(1000, "Figgy", 10000)
    sa2 = SavingsAccount(1000, "Figgy", 10000)

    # Create CheckingAccount
    ca1 = CheckingAccount(1000, "Figgy", 10000)

    print("sa1 == ca1 ? ", sa1 == ca1)
    print("type(sa1): ", type(sa1))
    print("type(ca1): ", type(ca1))
    print("sa1 == sa2 ? ", sa1 == sa2)


# See PyCharm help at https://www.jetbrains.com/help/pycharm/
