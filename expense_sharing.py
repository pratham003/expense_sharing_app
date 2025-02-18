class ExpenseSharing:
    def __init__(self):
        self.expenses = {}

    def add_participant(self, name):
        if name not in self.expenses:
            self.expenses[name] = 0.0
            print(f"{name} added to the group.")
        else:
            print(f"{name} is already in the group.")

    def record_expense(self, name, amount):
        if name in self.expenses:
            self.expenses[name] += amount
            print(f"Added ₹{amount:.2f} expense for {name}.")
        else:
            print(f"{name} is not in the group. Add them first.")

    def show_balances(self):
        if not self.expenses:
            print("No participants in the group.")
            return

        total_spent = sum(self.expenses.values())
        per_person = total_spent / len(self.expenses)
        balances = {name: spent - per_person for name, spent in self.expenses.items()}

        print("\n--- Balance Summary ---")
        for name, balance in balances.items():
            if balance > 0:
                print(f"{name} should receive ₹{balance:.2f}")
            elif balance < 0:
                print(f"{name} should pay ₹{-balance:.2f}")
            else:
                print(f"{name} is settled.")
        print("-----------------------")

    def start(self):
        while True:
            print("\n1. Add Participant  2. Record Expense  3. Show Balances  4. Exit")
            choice = input("Choose an option: ")

            if choice == "1":
                self.add_participant(input("Enter name: "))

            elif choice == "2":
                name = input("Enter name: ")
                try:
                    amount = float(input("Enter amount: "))
                    self.record_expense(name, amount)
                except ValueError:
                    print("Invalid amount. Please enter a number.")

            elif choice == "3":
                self.show_balances()

            elif choice == "4":
                print("Exiting... Goodbye!")
                break

            else:
                print("Invalid option, try again.")


if __name__ == "__main__":
    ExpenseSharing().start()
