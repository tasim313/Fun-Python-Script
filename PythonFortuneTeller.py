import random
import time
import datetime
from colorama import Fore, Style, init

# Initialize colorama
init(autoreset=True)

# Python-themed fortunes
fortunes = [
    "Your code will compile on the first try!",
    "You will find a bug and squash it with elegance!",
    "A rare 'import' statement will bring unexpected opportunities.",
    "Your next project will be a beautiful and efficient algorithm!",
    "You will refactor your code and achieve peak performance!",
    "The Pythonic gods smile upon your indentation.",
    "Your list comprehension will be the envy of all.",
    "A mysterious 'SyntaxError' will lead you to greatness.",
    "You will discover a new library that changes everything.",
    "Your debugging skills will reach legendary status.",
    "A 'None' value will reveal its true purpose.",
    "Your code will run faster than C (in your dreams).",
    "You will write a function so elegant, it brings tears to your eyes.",
    "A 'KeyError' will guide you to a hidden treasure.",
    "Your next commit will be a masterpiece."
]

# Time-based fortunes
def time_based_fortune():
    hour = datetime.datetime.now().hour
    if 6 <= hour < 12:
        return "The morning sun brings clarity to your code."
    elif 12 <= hour < 18:
        return "The afternoon breeze whispers secrets of optimization."
    else:
        return "The night holds the key to your debugging success."

# Generate a fortune
def generate_fortune():
    # Combine time-based fortune with a random fortune
    return f"{time_based_fortune()} Also, {random.choice(fortunes)}"

# Generate a luck number based on Python's hash() function
def generate_luck_number():
    return abs(hash(str(datetime.datetime.now())) % 100)

# Custom console animation
def animate_fortune():
    print(Fore.YELLOW + "\nThe Pythonic Oracle is thinking..." + Style.RESET_ALL)
    for _ in range(3):
        time.sleep(0.5)
        print(Fore.YELLOW + "..." + Style.RESET_ALL)
    time.sleep(0.5)

# Save fortune to a file
def save_fortune(fortune, luck_number):
    with open("fortunes.txt", "a") as file:
        file.write(f"{datetime.datetime.now()}: {fortune} (Luck Number: {luck_number})\n")

# Main function
def main():
    print(Fore.CYAN + "Welcome to the Personalized Fortune Teller (with Python Twists)!" + Style.RESET_ALL)
    name = input(Fore.GREEN + "Enter your name: " + Style.RESET_ALL).strip()
    print(Fore.CYAN + f"\nHello, {name}! The Pythonic Oracle is ready to reveal your fortune." + Style.RESET_ALL)

    while True:
        input(Fore.YELLOW + "\nPress Enter to receive your fortune..." + Style.RESET_ALL)
        animate_fortune()
        fortune = generate_fortune()
        luck_number = generate_luck_number()
        print(Fore.GREEN + f"\nThe Pythonic Oracle speaks:\n\"{name}, {fortune}\"" + Style.RESET_ALL)
        print(Fore.BLUE + f"Your Luck Number: {luck_number}" + Style.RESET_ALL)
        save_fortune(fortune, luck_number)
        print(Fore.CYAN + "\nYour fortune has been saved to 'fortunes.txt'." + Style.RESET_ALL)
        another = input(Fore.YELLOW + "Would you like another fortune? (yes/no): " + Style.RESET_ALL).strip().lower()
        if another != "yes":
            print(Fore.CYAN + "Thank you for consulting the Pythonic Oracle. Goodbye!" + Style.RESET_ALL)
            break

if __name__ == "__main__":
    main()