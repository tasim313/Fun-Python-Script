import json
import random
import tkinter as tk
from tkinter import messagebox, scrolledtext

# Default facts database
facts_database = {
    "Animals": [
        "A group of flamingos is called a 'flamboyance'.",
        "Octopuses have three hearts.",
        "Honey never spoils.",
        "A shrimp's heart is in its head."
    ],
    "Space": [
        "There are more stars in the universe than grains of sand on Earth.",
        "One million Earths could fit inside the sun.",
        "Neutron stars can spin 600 times per second.",
        "A day on Venus is longer than a year on Venus."
    ],
    "History": [
        "Cleopatra lived closer to the invention of the iPhone than to the construction of the Great Pyramid.",
        "Oxford University is older than the Aztec Empire.",
        "Woolly Mammoths were still alive when the Great Pyramid was being built.",
        "The first computer was invented in the 1940s."
    ]
}

# Save facts to a JSON file
def save_facts():
    with open("facts.json", "w") as file:
        json.dump(facts_database, file)

# Load facts from a JSON file
def load_facts():
    try:
        with open("facts.json", "r") as file:
            return json.load(file)
    except FileNotFoundError:
        return facts_database  # Return default facts if file doesn't exist

# CLI Functions
def display_categories():
    print("\nChoose a category:")
    for index, category in enumerate(facts_database.keys(), start=1):
        print(f"{index}. {category}")

def get_user_choice():
    while True:
        choice = input("Enter your choice (1/2/3): ")
        if choice.isdigit() and 1 <= int(choice) <= len(facts_database):
            return int(choice) - 1
        else:
            print("Invalid choice. Please enter a number corresponding to the categories listed.")

def explore_facts(category):
    fact = random.choice(facts_database[category])
    print(f"\nFun Fact: {fact}")

def search_facts(keyword):
    found_facts = []
    for category, facts in facts_database.items():
        for fact in facts:
            if keyword.lower() in fact.lower():
                found_facts.append(f"{category}: {fact}")
    return found_facts

def get_random_fact():
    category = random.choice(list(facts_database.keys()))
    fact = random.choice(facts_database[category])
    return f"{category}: {fact}"

# CLI Main Function
def cli_main():
    while True:
        print("\n1. Explore a category")
        print("2. Search for a fact by keyword")
        print("3. Get a random fact")
        print("4. Exit")
        choice = input("Enter your choice (1/2/3/4): ").strip()

        if choice == "1":
            display_categories()
            category_index = get_user_choice()
            category = list(facts_database.keys())[category_index]
            explore_facts(category)
        elif choice == "2":
            keyword = input("Enter a keyword to search for facts: ").strip()
            found_facts = search_facts(keyword)
            if found_facts:
                print("\nFound the following facts:")
                for fact in found_facts:
                    print(f"- {fact}")
            else:
                print("No facts found for that keyword.")
        elif choice == "3":
            print("\nRandom Fact:")
            print(get_random_fact())
        elif choice == "4":
            print("Thank you for exploring! Goodbye!")
            break
        else:
            print("Invalid choice. Please try again.")

# GUI Class
class FactExplorerApp:
    def __init__(self, master):
        self.master = master
        master.title("Interactive Fact Explorer")

        # Category selection
        self.label = tk.Label(master, text="Choose a category:")
        self.label.pack()

        self.category_var = tk.StringVar(value="Animals")  # Default category
        self.category_menu = tk.OptionMenu(master, self.category_var, *facts_database.keys())
        self.category_menu.pack()

        # Explore button
        self.explore_button = tk.Button(master, text="Explore", command=self.explore_facts)
        self.explore_button.pack()

        # Search feature
        self.search_label = tk.Label(master, text="Search for a fact by keyword:")
        self.search_label.pack()

        self.search_entry = tk.Entry(master)
        self.search_entry.pack()

        self.search_button = tk.Button(master, text="Search", command=self.search_facts)
        self.search_button.pack()

        # Display area for search results
        self.results_text = scrolledtext.ScrolledText(master, width=50, height=10, wrap=tk.WORD)
        self.results_text.pack()

        # Random fact button
        self.random_button = tk.Button(master, text="Get Random Fact", command=self.show_random_fact)
        self.random_button.pack()

        # Quit button
        self.quit_button = tk.Button(master, text="Quit", command=master.quit)
        self.quit_button.pack()

    def explore_facts(self):
        category = self.category_var.get()
        fact = random.choice(facts_database[category])
        messagebox.showinfo("Fun Fact", fact)

    def search_facts(self):
        keyword = self.search_entry.get().strip()
        found_facts = []
        for category, facts in facts_database.items():
            for fact in facts:
                if keyword.lower() in fact.lower():
                    found_facts.append(f"{category}: {fact}")
        
        self.results_text.delete(1.0, tk.END)  # Clear previous results
        if found_facts:
            self.results_text.insert(tk.END, "\n".join(found_facts))
        else:
            self.results_text.insert(tk.END, "No facts found for that keyword.")

    def show_random_fact(self):
        messagebox.showinfo("Random Fact", get_random_fact())

# Main Function
def main():
    global facts_database
    facts_database = load_facts()  # Load facts from JSON file

    print("Welcome to the Interactive Fact Explorer!")
    print("Choose an option:")
    print("1. Use the Command Line Interface (CLI)")
    print("2. Use the Graphical User Interface (GUI)")
    choice = input("Enter your choice (1/2): ").strip()

    if choice == "1":
        cli_main()
    elif choice == "2":
        root = tk.Tk()
        app = FactExplorerApp(root)
        root.mainloop()
    else:
        print("Invalid choice. Exiting.")

    save_facts()  # Save facts to JSON file before exiting

if __name__ == "__main__":
    main()