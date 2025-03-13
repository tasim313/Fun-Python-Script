import random
import time
import pyttsx3
from plyer import notification

# Data storage
quotes = {
    "high": [
        "The best way to predict the future is to create it. - Abraham Lincoln",
        "You are never too old to set another goal or to dream a new dream. - C.S. Lewis",
        "Success is not the key to happiness. Happiness is the key to success. - Albert Schweitzer"
    ],
    "medium": [
        "Believe you can and you're halfway there. - Theodore Roosevelt",
        "Act as if what you do makes a difference. It does. - William James",
        "The only limit to our realization of tomorrow is our doubts of today. - Franklin D. Roosevelt"
    ],
    "low": [
        "Keep your face always toward the sunshine—and shadows will fall behind you. - Walt Whitman",
        "The future belongs to those who believe in the beauty of their dreams. - Eleanor Roosevelt"
    ]
}

fun_facts = [
    "Did you know that honey never spoils? Archaeologists have found edible honey in ancient Egyptian tombs!",
    "Bananas are berries, but strawberries are not!",
    "A group of flamingos is called a 'flamboyance'!",
    "Octopuses have three hearts!"
]

jokes = [
    "Why don't scientists trust atoms? Because they make up everything!",
    "Why did the scarecrow win an award? Because he was outstanding in his field!",
    "I told my wife she was drawing her eyebrows too high. She looked surprised!",
    "Why don’t skeletons fight each other? They don’t have the guts!"
]

def get_random_quote(motivation_level):
    return random.choice(quotes[motivation_level])

def get_random_fact():
    return random.choice(fun_facts)

def get_random_joke():
    return random.choice(jokes)

def text_to_speech(message):
    engine = pyttsx3.init()
    engine.say(message)
    engine.runAndWait()

def send_notification(quote, fact, joke):
    notification.notify(
        title="Your Daily Dose of Positivity & Trivia",
        message=f"Quote: {quote}\nFun Fact: {fact}\nJoke: {joke}",
        timeout=10
    )

def main():
    motivation_level = input("Enter your motivation level (high, medium, low): ").strip().lower()
    
    if motivation_level not in quotes:
        print("Invalid motivation level! Please enter 'high', 'medium', or 'low'.")
        return
    
    quote = get_random_quote(motivation_level)
    fact = get_random_fact()
    joke = get_random_joke()
    
    output_message = f"Quote: {quote}\nFun Fact: {fact}\nJoke: {joke}"
    print(output_message)
    
    # Text-to-speech
    text_to_speech(output_message)
    
    # Desktop notification
    send_notification(quote, fact, joke)

if __name__ == "__main__":
    main()